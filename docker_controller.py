## Copyright (C) 2024, Nicholas Carlini <nicholas@carlini.com>.
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import pickle
import sys
import time
import tarfile
import io
import threading
import signal
import subprocess
import pty
import os
import select
import re
import termios
import struct
import fcntl
import random
import json
import re


# DO NOT SET THIS FLAG TO TRUE UNLESS YOU ARE SURE YOU UNDERSTAND THE CONSEQUENCES
# IT IS VERY DANGEROUS. YOU WILL BE DIRECTLY EVALUATING WHATEVER COMES OUT OF
# A LANGUAGE MODEL DIRECTLY ON YOUR COMPUTER WITH NO SAFETY CHECKS.
I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE_OR_MAKING_THEM_HALT_AND_CATCH_FIRE = True

BACKEND = json.load(open("config.json"))['container']

def make_tar(files):
    file_like_object = io.BytesIO()
    tar = tarfile.TarFile(fileobj=file_like_object, mode='w')
    
    for file_name, file_content in files.items():
        tarinfo = tarfile.TarInfo(name=file_name)
        tarinfo.size = len(file_content)
        tarinfo.mtime = time.time()
        tar.addfile(tarinfo, io.BytesIO(file_content))

    tar.close()

    file_like_object.seek(0)

    return file_like_object
    

if BACKEND == "docker":
    import docker
    def setup_docker(env):
        env.docker = docker.from_env()
        env.container = env.docker.containers.run("llm-benchmark-image", detach=True, tty=True)    
    
    def stop_and_remove_container(client, container_id):
        # Stopping the container
        client.containers.get(container_id).stop()
    
        # Removing the container
        client.containers.get(container_id).remove()
    
    def async_kill_container(client, container):
        thread = threading.Thread(target=stop_and_remove_container, args=(client, container.id))
        thread.daemon = True
        thread.start()
        
    
    def safe_run(client, container, files, run_cmd):
        tarfile = make_tar(files)
    
        path = "/usr/src/app"
        container.put_archive(path, tarfile)
    
        exit_code, output = container.exec_run(run_cmd)
        
        return output
elif BACKEND == "podman":
    def setup_docker(env):
        # Starting a container with Podman
        result = subprocess.run(["podman", "run", "-d", "-t", "llm-benchmark-image"], capture_output=True, text=True, check=True)
        env.container = result.stdout.strip()
        env.docker = "I AM USING PODMAN THIS IS NOT NEEDED"
    
    def stop_and_remove_podman_container(container_id):
        # Stopping the container
        subprocess.run(["podman", "container", "stop", container_id], check=True)
    
        # Removing the container
        subprocess.run(["podman", "container", "rm", container_id], check=True)
    
    def async_kill_container(client, container_id):
        thread = threading.Thread(target=stop_and_remove_podman_container, args=(container_id,))
        thread.daemon = True
        thread.start()
    
    def safe_run(client, container_id, files, run_cmd):
        tarfile = make_tar(files)

        # Create a temporary directory in the container to store files
        subprocess.run(["podman", "exec", container_id, "mkdir", "-p", "/usr/src/app"], check=True)
    
        # Copying files to the container
        r = random.randint(0, 1000000)
        with open('/tmp/archive%d.tar'%r, 'wb') as out_f:
            out_f.write(tarfile.getbuffer())
        time.sleep(.1)
        subprocess.run(["podman", "cp", "/tmp/archive%d.tar"%r, f"{container_id}:/usr/src/app"], check=True)
        time.sleep(.1)

        result = subprocess.run(["podman", "exec", container_id, "tar", "-xf", "archive%d.tar"%r], capture_output=True, check=True)

        time.sleep(.3)
        
        # Executing command in the container
        result = subprocess.run(["podman", "exec", container_id, *run_cmd], capture_output=True)
    
        return result.stdout + result.stderr
else:
    raise ValueError("Invalid backend")

import fcntl

def is_fd_closed(fd):
    try:
        fcntl.fcntl(fd, fcntl.F_GETFD)
        return False
    except OSError:
        return True


class DockerJob:
    def __init__(self, container_id, eos_string):
        self.eos_string = eos_string

        if BACKEND == "docker":
            cmd = f"docker exec -it {container_id} /bin/bash"
            print("Running", cmd)
        else:
            cmd = f"podman exec -it {container_id} /bin/bash"
        
        self.process = subprocess.Popen(cmd,
                                        shell=True,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)
        
        self.master_fd = self.process.stdout.fileno()  # If you need a file descriptor for reading output
        
    @staticmethod
    def remove_ansi(text):
        ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', text)

    def __call__(self, cmd):
        # Send the command through the PTY
        print("GO", self.process.stdin)
        try:
            self.process.stdin.write((cmd + "\n"))
            self.process.stdin.flush()
        except:
            print("Process was terminated")
            return "Process was terminated"

        # Read the output until the EOS string is encountered
        output = []
        while True:
            ready, _, _ = select.select([self.master_fd], [], [], 2)  # 2-second timeout
            if ready:
                line = os.read(self.master_fd, 128).decode()
                output.append(line)
                if self.eos_string in line:
                    break
                if line == '':
                    break
            else:
                # Timeout occurred
                print("Timeout - no output received in 2 seconds")
                break


        output = ''.join(output)
        output = self.remove_ansi(output)
        print("Output:", repr(output))
        return output


def invoke_docker(env, files, run_cmd, out_bytes=False):
    if env.docker is None:
        setup_docker(env)

    def raise_timeout(signum, frame):
        raise TimeoutError
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(20)
    
    try:
        # Function call that might take too long
        out = safe_run(env.docker, env.container, files, run_cmd)
    except TimeoutError:
        out = b"Timeout: function took too long to complete"

    signal.alarm(0) 

    if out_bytes:
        return out
    else:
        return out.decode("utf-8")


if I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE_OR_MAKING_THEM_HALT_AND_CATCH_FIRE:

    class DockerJob:
        def __init__(self, container_id, eos_string):
            raise NotImplementedError("This test is not implemented in unsafe mode yet")
        
    def setup_docker(env):
        import random
        env.fake_docker_id = random.randint(0, 10000000000)
        os.mkdir("/tmp/fakedocker_%d"%env.fake_docker_id)
        

    def invoke_docker(env, files, run_cmd, out_bytes=False):
        if env.docker is None:
            setup_docker(env)
    
        def raise_timeout(signum, frame):
            raise TimeoutError
        signal.signal(signal.SIGALRM, raise_timeout)
        signal.alarm(20)
        
        try:
            # Function call that might take too long
            for file_name, file_content in files.items():
                with open("/tmp/fakedocker_%d/%s"%(env.fake_docker_id, file_name), "wb") as f:
                    f.write(file_content)
            proc = subprocess.run(run_cmd, cwd="/tmp/fakedocker_%d"%env.fake_docker_id, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except TimeoutError:
            if out_bytes:
                return b"Timeout: function took too long to complete"
            else:
                return "Timeout: function took too long to complete"

        signal.alarm(0) 
    

        if out_bytes:
            return proc.stdout + proc.stderr
        else:
            stdout = proc.stdout.decode("utf-8")
            stderr = proc.stderr.decode("utf-8")
            
            # Replace /fakedocker_[0-9]*/ with /fakedocker/
            stdout = re.sub(r'/fakedocker_[0-9]*/', '/fakedocker/', stdout)
            stderr = re.sub(r'/fakedocker_[0-9]*/', '/fakedocker/', stderr)
        
            return stdout + stderr

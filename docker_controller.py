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


# DO NOT SET THIS FLAG TO TRUE UNLESS YOU ARE SURE YOU UNDERSTAND THE CONSEQUENCES
# IT IS VERY DANGEROUS. YOU WILL BE DIRECTLY EVALUATING WHATEVER COMES OUT OF
# A LANGUAGE MODEL DIRECTLY ON YOUR COMPUTER WITH NO SAFETY CHECKS.
I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE = False

if not I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE:
    import docker


def setup_docker(env):
    env.docker = docker.from_env()
    env.container = env.docker.containers.run("llm-benchmark-image", detach=True, tty=True)


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


class DockerJob:
    def __init__(self, container_id, eos_string):
        self.eos_string = eos_string
        # Create a pseudo-terminal
        master, slave = pty.openpty()

        
        # Set the window size
        winsize = struct.pack("HHHH", 100, 160, 0, 0)
        fcntl.ioctl(slave, termios.TIOCSWINSZ, winsize)


        # Start the Docker subprocess with the pseudo-terminal
        self.process = subprocess.Popen(f"docker exec -it {container_id} /bin/bash",
                                        shell=True,
                                        stdin=slave,
                                        stdout=slave,
                                        stderr=subprocess.PIPE,
                                        text=True)

        # Close the slave FD as it is no longer needed
        os.close(slave)
        self.master_fd = master
        
    @staticmethod
    def remove_ansi(text):
        ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        return ansi_escape.sub('', text)

    def __call__(self, cmd):
        # Send the command through the PTY
        os.write(self.master_fd, (cmd + "\n").encode())

        # Read the output until the EOS string is encountered
        output = []
        while True:
            ready, _, _ = select.select([self.master_fd], [], [], 2)  # 2-second timeout
            if ready:
                line = os.read(self.master_fd, 1024).decode()
                output.append(line)
                if self.eos_string in line:
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


if I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE:

    class DockerJob:
        def __init__(self, container_id, eos_string):
            raise NotImplementedError("Thsi test is not implemented in unsafe mode yet")
        
    def setup_docker(env):
        import random
        env.fake_docker_id = random.randint(0, 1000000)
        os.mkdir("/tmp/fakedocker_%d"%env.fake_docker_id)
        
    def invoke_docker(env, files, run_cmd, out_bytes=False):
        if env.fake_docker_id is None:
            setup_docker(env)

        for file_name, file_content in files.items():
            with open("/tmp/fakedocker_%d/%s"%(env.fake_docker_id, file_name), "wb") as f:
                f.write(file_content)
        proc = subprocess.run(run_cmd, cwd="/tmp/fakedocker_%d"%env.fake_docker_id, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if out_bytes:
            return proc.stdout + proc.stderr
        else:
            return proc.stdout.decode("utf-8") + proc.stderr.decode("utf-8")

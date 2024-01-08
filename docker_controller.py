import asyncio
import pickle
import sys
import time
import tarfile
import io
import threading
import signal


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
    def setup_docker():
        global fake_docker_id
        fake_docker_id = random.randint(0, 1000000)
        os.mkdir("/tmp/fakedocker_%d"%n)
    
    def invoke_docker(env, files, run_cmd, out_bytes=False):
        # TODO: test this
        for file_name, file_content in files.items():
            with open("/tmp/fakedocker_%d/%s"%(fake_docker_id, file_name), "wb") as f:
                f.write(file_content)
        proc = subprocess.run(run_cmd, cwd="/tmp/fakedocker_%d"%fake_docker_id, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if out_bytes:
            return proc.stdout + proc.stderr
        else:
            return proc.stdout.decode("utf-8") + proc.stderr.decode("utf-8")

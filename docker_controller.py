import docker
import asyncio
import pickle
import sys
import time
import tarfile
import io
import threading

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

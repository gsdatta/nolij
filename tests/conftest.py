import tempfile
import pytest



import os
import socket
import subprocess
from shutil import rmtree,copy
from time import clock
import py






def _unused_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    _, port = sock.getsockname()
    sock.close()
    return port





@pytest.fixture(scope='session')
def sessiondir(request):
    tmp_dir = py.path.local(tempfile.mkdtemp())
    request.addfinalizer(lambda: tmp_dir.remove(rec=1))
    return tmp_dir







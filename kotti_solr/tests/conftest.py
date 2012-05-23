from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
from subprocess import Popen
from time import sleep


def waitfor(*ports, **kw):
    timeout = kw.get('timeout', 30)
    host = kw.get('host', 'localhost')
    ip = gethostbyname(host)
    ports = set(ports)
    while ports and timeout > 0:
        for port in list(ports):
            s = socket(AF_INET, SOCK_STREAM)
            if s.connect_ex((ip, port)) == 0:
                ports.remove(port)
            s.close()
        if ports:
            sleep(1)
            timeout -= 1
    return not bool(ports)


def pytest_funcarg__solr(request):
    def setup():
        proc = Popen(['bin/solr-instance', 'fg'])
        waitfor(8983)       # wait for Solr to start up
        request.addfinalizer(proc.terminate)
    return request.cached_setup(setup=setup, scope='session')

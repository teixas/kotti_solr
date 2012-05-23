from mr.laforge import up, waitforports, shutdown


def pytest_funcarg__solr(request):
    def setup():
        up('solr')
        waitforports(8983)      # wait for Solr to start up
        request.addfinalizer(shutdown)
    return request.cached_setup(setup=setup, scope='session')

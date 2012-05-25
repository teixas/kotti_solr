from mr.laforge import up, waitforports, shutdown
from pyramid.testing import setUp, tearDown, DummyRequest
from kotti.resources import default_get_root
from kotti.security import principals_factory
from kotti import testing


settings = {
    'kotti.site_title': 'My Kotti Solr-ized site',
    'kotti.secret': 'qwerty',
    'kotti.root_factory': [default_get_root],
    'kotti.use_tables': '',
    'kotti.populators': [testing._populator],
    'kotti.principals_factory': [principals_factory],
    'pyramid.includes': 'kotti.events kotti_solr',
    'kotti_solr.solr_url': 'http://localhost:8983/solr',
}


def pytest_funcarg__db_session(request):
    request.getfuncargvalue('config')
    from kotti.testing import _initTestingDB
    return _initTestingDB()


def pytest_funcarg__config(request):
    def setup():
        config = setUp(settings=settings)
        for include in settings['pyramid.includes'].split():
            config.include(include)
        return config
    return request.cached_setup(
        setup=setup, teardown=tearDown, scope='session')


def pytest_funcarg__request(request):
    config = request.getfuncargvalue('config')
    config.manager.get()['request'] = request = DummyRequest()
    return request


def pytest_funcarg__solr_server(request):
    def setup():
        up('solr')
        waitforports(8983)      # wait for Solr to start up
    return request.cached_setup(setup=setup,
        teardown=lambda solr: shutdown(), scope='session')


def pytest_funcarg__solr(request):
    request.getfuncargvalue('solr_server')
    from kotti_solr import get_solr
    solr = get_solr(settings['kotti_solr.solr_url'])
    solr.delete_all()
    solr.commit()
    return solr

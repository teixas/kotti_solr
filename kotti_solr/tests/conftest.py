from mr.laforge import up, waitforports, shutdown
from sunburnt import SolrInterface
from pyramid.testing import setUp, tearDown


settings = {
    'kotti.site_title': 'My Kotti Solr-ized site',
    'kotti.secret': 'qwerty',
    'kotti.use_tables': '',
    'kotti.populators': [],
    'pyramid.includes': 'kotti_solr',
    'sqlalchemy.url': 'sqlite:///%(here)s/Kotti.db',
    'kotti_solr.solr_url': 'http://localhost:8983/solr',
}


def pytest_funcarg__db_session(request):
    request.getfuncargvalue('config')
    from kotti.testing import _initTestingDB
    return _initTestingDB()


def pytest_funcarg__config(request):
    return request.cached_setup(
        setup=lambda: setUp(settings=settings),
        teardown=tearDown, scope='function')


def pytest_funcarg__solr(request):
    def setup():
        up('solr')
        waitforports(8983)      # wait for Solr to start up
        return SolrInterface(settings['kotti_solr.solr_url'])
    return request.cached_setup(setup=setup,
        teardown=lambda solr: shutdown(), scope='session')

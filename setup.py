import os
import subprocess
import sys

from setuptools import find_packages, setup, Command


here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

install_requires = [
    'httplib2',
    'Kotti',
    'lxml',
    'sunburnt',
    ]

test_requires = [
    'pytest',
    'pytest-cov'
]


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        script = os.path.join(os.path.dirname(sys.executable), 'py.test')
        errno = subprocess.call([sys.executable, script])
        raise SystemExit(errno)

setup(name='kotti_solr',
      version='0.1',
      description="Solr integration for Kotti",
      long_description='\n\n'.join([README, CHANGES]),
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: Repoze Public License",
        ],
      keywords='solr kotti cms pylons pyramid',
      author='Kotti developers',
      author_email='kotti@googlegroups.com',
      url='http://pypi.python.org/pypi/kotti_solr',
      license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires + test_requires,
      cmdclass={'test': PyTest},
      )

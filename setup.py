# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from setuptools.command.test import test
import media_include
from runtests import runtests

class TestRunner(test):
    def run(self, *args, **kwargs):
        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)
        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)
        runtests()

setup(
    name='django-media-include',
    version=media_include.__version__,
    description='Media management application for Django.',
    author='Michał Lula',
    author_email='lulamichal@gmail.com',
    long_description=open('README.rst', 'r').read(),
    url='http://michallula.pl/projects/media-include/',
    packages = find_packages(),
    test_suite='tests',
    cmdclass={"test": TestRunner},
    install_requires = [
        'django >= 1.3',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)

# -*- coding: utf-8 -*-

import codecs
import os
import sys
from shutil import rmtree

from setuptools import setup, Command


pwd = os.path.abspath(os.path.dirname(__file__))


with codecs.open(os.path.join(pwd, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PublishCommand(Command):
    """Support setup.py publish.

    https://github.com/kennethreitz/setup.py/blob/master/setup.py
    """

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.sep.join(('.', 'dist')))
        except OSError:
            pass

        self.status('Building Source and Wheel distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='beancount-commerzbank',
    version='0.1.1',
    description='Beancount Importer for Commerzbank CSV exports',
    long_description=long_description,
    author='Siddhant Goel',
    author_email='me@sgoel.org',
    license='MIT',
    url='https://github.com/siddhantgoel/beancount-commerzbank',
    packages=['beancount_commerzbank'],
    keywords=['beancount', 'cli-accounting', 'finance'],
    install_requires=('beancount',),
    python_requires='>=3.5.0',
    cmdclass={
        'publish': PublishCommand
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ]
)

from setuptools import setup

license = open('LICENSE.txt').read()

setup(
    name='iloveck101',
    version='0.5.2',
    author='tzangms',
    author_email='tzangms@gmail.com',
    packages=['iloveck101'],
    url='https://github.com/tzangms/iloveck101',
    license=license,
    description='Download images from ck101 thread',
    test_suite='tests',
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'iloveck101 = iloveck101.iloveck101:main',
        ]
    },
    install_requires = [
        "lxml==4.6.2",
        "requests==2.0.1",
        "gevent==1.0",
        "more-itertools==2.2",
    ],
)

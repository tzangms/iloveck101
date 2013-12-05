from setuptools import setup

setup(
    name='iloveck101',
    version='0.5.1',
    author='tzangms',
    author_email='tzangms@gmail.com',
    packages=['iloveck101'],
    url='https://github.com/tzangms/iloveck101',
    license='LICENSE.txt',
    description='Download images from ck101 thread',
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': [
            'iloveck101 = iloveck101.iloveck101:main',
        ]
    },
    install_requires = [
        "lxml==3.2.4",
        "requests==2.0.1",
        "gevent==1.0",
    ],
)

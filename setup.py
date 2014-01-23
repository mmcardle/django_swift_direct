import os
from setuptools import setup, find_packages

__author__ = 'mm'

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='django_swift_direct',
    version='0.0.1',
    description='Direct Uploads to OpenStack Swift using CORS.',
    long_description=readme,
    author="Mark McArdle",
    author_email='m.mc4rdle@gmail.com',
    url='https://github.com/mmcardle/django_swift_direct',
    license='MIT licence, see LICENCE',
    packages=find_packages(),
    install_requires=['setuptools'],
    zip_safe=False,
)

import sys

from setuptools import setup
from setuptools import find_packages


version = '0.0.1.dev0'

install_requires = [
    # For pkg_resources. >=1.0 so pip resolves it to a version cryptography
    # will tolerate; see #2599:
    'setuptools>=1.0',
]

setup(
    name='starttls_policy',
    version=version,
    description="Policy API for STARTTLS Preload",
    url='https://github.com/EFForg/starttls-everywhere',
    author="Sydney Li",
    author_email='sydney@eff.org',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Communications :: Email :: Mail Transport Agents',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)


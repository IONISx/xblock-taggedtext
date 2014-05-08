"""Setup for taggedtext XBlock."""

import os
from setuptools import setup


def package_data(pkg, root):
    """Generic function to find package_data for `pkg` under `root`."""
    data = []
    for dirname, _, files in os.walk(os.path.join(pkg, root)):
        for fname in files:
            data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='taggedtext-xblock',
    version='0.0.1',
    description='Tagged Text XBlock',
    author='IONISx',
    packages=['taggedtext'],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'taggedtext = taggedtext.taggedtextblock:TaggedTextXBlock',
        ]
    },
    package_data=package_data("taggedtext", "static"),
)

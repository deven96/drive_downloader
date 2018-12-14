import os
import sys
import setuptools

CURRENT_DIR = os.getcwd()
REQUIREMENTS = 'requirements.txt'
requires = [line.strip('\n') for line in open(REQUIREMENTS).readlines()]
setuptools.setup(
    name="GDownloader",
    version="1.0.1",
    author='Domnan Diretnan, Mmadu Manasseh',
    description="easy wrapper for downloading google drive files using only shareable link",
    packages=setuptools.find_packages(),
    zip_safe=False,
    install_requires=requires,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    package_data={
        '': ['*.*'],
    },
    include_package_data=True
)
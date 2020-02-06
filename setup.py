# pylint: disable=invalid-name

"""
Main setup file for qiskit-aer
"""

import os
import warnings
import subprocess
import sys
import inspect

try:
    from skbuild import setup
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'scikit-build'])
    from skbuild import setup
try:
    import pybind11
except ImportError:
    subprocess.call([sys.executable, '-m', 'pip', 'install', 'pybind11>=2.4'])

import setuptools

requirements = [
    'numpy>=1.13',
    'scipy>=1.0',
    'cython>=0.27.1',
    'pybind11>=2.4'  # This isn't really an install requirement,
                     # Pybind11 is required to be pre-installed for
                     # CMake to successfully find header files.
                     # This should be fixed in the CMake build files.
]

setup_requirements = requirements + [
    'scikit-build',
    'cmake'
]

if not hasattr(setuptools,
               'find_namespace_packages') or not inspect.ismethod(
                    setuptools.find_namespace_packages):
    print("Your setuptools version:'{}' does not support PEP 420 "
          "(find_namespace_packages). Upgrade it to version >='40.1.0' and "
          "repeat install.".format(setuptools.__version__))
    sys.exit(1)

VERSION_PATH = os.path.join(os.path.dirname(__file__),
                            "qiskit", "providers", "aer", "VERSION.txt")
with open(VERSION_PATH, "r") as version_file:
    VERSION = version_file.read().strip()

# check if wanting to use NumPy BLAS
if "--with-numpy-blas" in sys.argv:
    sys.argv.remove("--with-numpy-blas")
    try:
        import numpy as np
    except:
        raise ImportError('NumPy must be pre-installed.')
    else:
        config = np.__config__
        blas_info = config.blas_opt_info
        has_lib_key = 'libraries' in blas_info.keys()
        if has_lib_key:
            sys.argv.append('--')
            sys.argv.append('-DBLAS_LIB_PATH='+blas_info['library_dirs'][0])
        else:
            warnings.warn('Could not find NumPy blas library.  Continuing without...')

setup(
    name='qiskit-aer',
    version=VERSION,
    packages=setuptools.find_namespace_packages(include=['qiskit.*']),
    cmake_source_dir='.',
    description="Qiskit Aer - High performance simulators for Qiskit",
    url="https://github.com/Qiskit/qiskit-aer",
    author="AER Development Team",
    author_email="qiskit@us.ibm.com",
    license="Apache 2.0",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
    ],
    install_requires=requirements,
    setup_requires=setup_requirements,
    include_package_data=True,
    cmake_args=["-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9"],
    keywords="qiskit aer simulator quantum addon backend",
    zip_safe=False
)

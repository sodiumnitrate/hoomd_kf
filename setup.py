import sys
import os
from setuptools import setup, find_packages
import hoomd_kf

setup(
        name='hoomd_kf',
        version=hoomd_kf.__version__,
        description='tools to run hoomd MC simulations with the Kern-Frenkel model',
        url='https://github.com/sodiumnitrate/hoomd_kf.git',
        author='Irem Altan',
        author_email='irem.altan@yale.edu',
        license='',
        packages=find_packages(),
        #install_requires=['hoomd','gsd','numpy'],
        install_requires=['gsd','numpy'],
        python_requires='>=3.6'
        )

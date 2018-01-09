from os import path

from setuptools import setup, find_packages

from wrfconf import __version__

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as f:
    long_description = f.read()

setup(name='wrfconf',
      version=__version__,
      description='Configuration generator for WRF',
      long_description=long_description,
      author='Jared Lewis',
      author_email='jared@bodekerscientific.com',
      license='MIT',
      keywords='wrf config generate generator science forecast',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2'
          'Programming Language :: Python :: 3'
      ],
      install_requires=[
          'pyyaml'
      ],
      packages=find_packages(exclude='tests'),
      entry_points={
          'console_scripts':
              ['wrfconf = wrfconf.cli:main']
      },
      zip_safe=False)

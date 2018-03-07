from os import path

from setuptools import setup, find_packages

version = None
exec(open('wrfconf/version.py').read())

with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

setup(name='wrfconf',
      version=version,
      description='Configuration generator for WRF namelists',
      long_description=long_description,
      author='Jared Lewis',
      author_email='jared@bodekerscientific.com',
      license='MIT',
      keywords='wrf config generate generator science forecast',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Atmospheric Science'
      ],
      install_requires=[
          'pyyaml',
          'six',
          'marshmallow'
      ],
      packages=find_packages(exclude='tests'),
      entry_points={
          'console_scripts':
              ['wrfconf = wrfconf.cli:main']
      },
      zip_safe=False)

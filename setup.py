from setuptools import setup

setup(name='fatool',
      version='0.3.1',
      description='tools for handling fasta files',
      #url='http://github.com/storborg/funniest',
      author='Blazej Marciniak',
      author_email='blazejmarciniak@gmail.com',
      license='Apache 2.0',
      packages=['fatool'],
      install_requires=[
      ],
      scripts=['bin/cmdfatool.py'],
      zip_safe=False)
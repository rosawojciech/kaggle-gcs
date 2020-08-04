from setuptools import setup
from kagglegcs import __version__
setup(name='kagglegcs',
      version=__version__,
      description='Unofficial Kaggle support for get_gcs_paths()',
      url='http://github.com/rosawojciech/kaggle-gcs',
      author='Wojciech Rosa',
      author_email='roswoj@gmail.com',
      license='Apache 2.0',
      packages=['kagglegcs'],
      zip_safe=False,
      package_data={'kagglegcs': ['data/*.csv']})

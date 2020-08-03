from setuptools import setup

setup(name='kagglegcs',
      version='0.0.1',
      description='Unofficial kaggle support for get_gcs_paths()',
      url='http://github.com/rosawojciech/kaggle-gcs',
      author='Wojciech Rosa',
      author_email='roswoj@gmail.com',
      license='Apache 2.0',
      packages=['kagglegcs'],
      zip_safe=False,
      package_data={'kagglegcs': ['data/*.csv']})

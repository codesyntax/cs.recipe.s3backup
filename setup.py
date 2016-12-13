from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='cs.recipe.s3backup',
      version=version,
      description="Buildout recipe to copy given files/directories to Amazon S3",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Mikel Larreategi',
      author_email='mlarreategi@codesyntax.com',
      url='https://github.com/codesyntax/cs.recipe.s3backup',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['cs', 'cs.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'zc.recipe.egg',
          'zc.buildout',
          'setuptools',
          'boto3',
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'zc.buildout': ["default = cs.recipe.s3backup:Recipe"]
      },
      )

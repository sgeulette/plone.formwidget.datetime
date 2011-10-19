from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='plone.formwidget.datetime',
      version=version,
      description="Datetime widgets for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone date time datetime event widget archetypes z3c.form',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.formwidget'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.app.jquerytools',
          'zope.i18nmessageid',
      ],
      extras_require=dict(
          z3cform=[
              'zope.i18n',
              'z3c.form',
          ],
          archetypes=[
              'Products.Archetypes',
              'Products.CMFCore',
              'Zope2',
          ],
          test=[
              'plone.app.testing',
              'Products.Archetypes',
              'Products.CMFCore',
              'Products.GenericSetup',
              'z3c.form[test]',
              'zope.testing',
              'zc.buildout',
              'Zope2',]),
    )

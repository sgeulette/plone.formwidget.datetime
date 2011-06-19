from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# setup test content types
from Products.GenericSetup import EXTENSION, profile_registry


profile_registry.registerProfile('DatetimeWidget_examples',
    'DatetimeWidget Example Content Types',
    'Extension profile including Archetypes example content types',
    'profiles/examples',
    'plone.formwidget.datetime.at.tests.examples',
    EXTENSION)
ptc.setupPloneSite(
    extension_profiles=['plone.formwidget.datetime.at.tests.examples:DatetimeWidget_examples',])


import plone.formwidget.datetime.at


class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ptc.installPackage('plone.formwidget.datetime', quiet=0)
            zcml.load_config('configure.zcml',
                             plone.formwidget.datetime)
            zcml.load_config('configure.zcml',
                             plone.formwidget.datetime.at)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

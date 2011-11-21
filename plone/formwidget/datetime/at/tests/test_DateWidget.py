import mock
import unittest2 as unittest


class TestDateWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.at.widget import DateWidget
        return DateWidget()

    def test_subclass(self):
        from plone.formwidget.datetime.at.widget import DateWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        from Products.Archetypes.Widget import TypesWidget
        self.assertTrue(DateWidget, (AbstractDateWidget, TypesWidget))
    
    def test__properties(self):
        instance = self.createInstance()
        self.assertEqual(
            instance._properties,
            {
                'show_calendar': True,
                'helper_css': (),
                'with_time': False,
                'description': '',
                'populate': True,
                'show_day': True,
                'macro': 'date_input',
                'postback': True,
                'label': '',
                'visible': {'edit': 'visible', 'view': 'visible'},
                'blurrable': False,
                'modes': ('view', 'edit'),
                'show_content_type': False,
                'condition': '', 
                'helper_js': ()
            }
        )

    # def test__call_(self):
    #     instance = self.createInstance()
    #     mode = mock.Mock()
    #     ins = mock.Mock()
    #     request = mock.Mock()
    #     ins.REQUEST = request
    #     instance(mode, ins)
    #     self.assertTrue(DateWidget.called)

    
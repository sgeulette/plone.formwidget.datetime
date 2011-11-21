import mock
import unittest2 as unittest


class TestDatetimeWidget(unittest.TestCase):

    def createInstance(self):
        from plone.formwidget.datetime.z3cform.widget import DatetimeWidget
        instance = DatetimeWidget(mock.Mock())
        instance.name = 'field'
        return instance

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.widget import DatetimeWidget
        from plone.formwidget.datetime.base import AbstractDatetimeWidget
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        self.assertTrue(
            issubclass(
                DatetimeWidget,
                (
                    AbstractDatetimeWidget,
                    DateWidget,
                )
            )
        )

    def test_instance_provides(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.interfaces import IDatetimeWidget
        self.assertTrue(IDatetimeWidget.providedBy(instance))


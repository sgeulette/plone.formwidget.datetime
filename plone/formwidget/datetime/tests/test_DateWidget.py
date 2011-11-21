import mock
import unittest2 as unittest


class TestDateWidget(unittest.TestCase):


    def createInstance(self):
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        return DateWidget(mock.Mock())

    def test_subclass(self):
        from plone.formwidget.datetime.z3cform.widget import DateWidget
        from plone.formwidget.datetime.base import AbstractDateWidget
        from z3c.form.browser.widget import HTMLTextInputWidget
        from z3c.form.widget import Widget
        self.assertTrue(
            DateWidget,
            (
               AbstractDateWidget,
               HTMLTextInputWidget,
               Widget,
            )
        )

    def test_instance_provides(self):
        instance = self.createInstance()
        from plone.formwidget.datetime.z3cform.interfaces import IDateWidget
        self.assertTrue(IDateWidget.providedBy(instance))

    ## Testing update call from the super class is missing.
    @mock.patch('plone.formwidget.datetime.z3cform.widget.z3c.form.browser.widget.addFieldClass')
    def test_update(self, addFieldClass):
        instance = self.createInstance()
        instance.name = 'name'
        instance.update()
        self.assertTrue(addFieldClass.called)
        
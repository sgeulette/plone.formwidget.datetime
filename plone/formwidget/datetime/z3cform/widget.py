from interfaces import IDateWidget
from interfaces import IDatetimeWidget
from interfaces import IMonthYearWidget
from plone.formwidget.datetime import base

from z3c.form.browser.widget import addFieldClass, FieldWidget
from z3c.form.interfaces import NOVALUE, IFormLayer, IFieldWidget
from z3c.form.browser.widget import HTMLTextInputWidget
from z3c.form.widget import Widget
from zope.component import adapter
from zope.i18n.format import DateTimeParseError
from zope.interface import implementer, implementsOnly
from zope.schema.interfaces import IField

class AbstractDXDateWidget(HTMLTextInputWidget, Widget):
    pass

class DateWidget(base.AbstractDateWidget, AbstractDXDateWidget):
    """ Date widget.

    Please note: zope.schema date/datetime field values are python datetime
    instances.

    """
    implementsOnly(IDateWidget)

    def update(self):
        super(DateWidget, self).update()
        addFieldClass(self)

    def extract(self, default=NOVALUE):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)

        if not default in (year, month, day):
            return (year, month, day)

        # get a hidden value
        formatter = self._dtformatter
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day))
        except DateTimeParseError:
            pass

        return default

    @property
    def js_value(self):
        value_date = self.value[:3]
        if '' not in value_date:
            return 'new Date(%s, %s, %s)' % (value_date)
        else:
            return ''


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def DateFieldWidget(field, request):
    """IFieldWidget factory for DateWidget."""
    return FieldWidget(field, DateWidget(request))


class DatetimeWidget(base.AbstractDatetimeWidget, AbstractDXDateWidget):
    """ DateTime widget """
    implementsOnly(IDatetimeWidget)

    def update(self):
        super(DatetimeWidget, self).update()
        addFieldClass(self)

    def extract(self, default=NOVALUE):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)
        hour = self.request.get(self.name + '-hour', default)
        minute = self.request.get(self.name + '-min', default)
        timezone = self.request.get(self.name + '-timezone', default)

        if (self.ampm is True and
            hour is not default and
            minute is not default and
            int(hour)!=12):
            ampm = self.request.get(self.name + '-ampm', default)
            if ampm == 'PM':
                hour = str(12+int(hour))
            # something strange happened since we either
            # should have 'PM' or 'AM', return default
            elif ampm != 'AM':
                return default

        if default not in (year, month, day, hour, minute, timezone):
            return (year, month, day, hour, minute, timezone)

        # get a hidden value
        formatter = self._dtformatter
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day),
                    str(dateobj.hour),
                    str(dateobj.minute),
                    str(getattr(dateobj, 'tzinfo', '')))
        except DateTimeParseError:
            pass

        return default

    @property
    def js_value(self):
        value_date = self.value[:3]
        if '' not in value_date:
            return 'new Date(%s, %s, %s)' % (value_date)
        else:
            return ''


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def DatetimeFieldWidget(field, request):
    """IFieldWidget factory for DatetimeWidget."""
    return FieldWidget(field, DatetimeWidget(request))


class MonthYearWidget(base.AbstractMonthYearWidget, AbstractDXDateWidget):
    """ Month and year widget """
    implementsOnly(IMonthYearWidget)

    def update(self):
        super(DateWidget, self).update()
        addFieldClass(self)

    def extract(self, default=NOVALUE):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)

        if not default in (year, month, day):
            return (year, month, day)

        # get a hidden value
        formatter = self._dtformatter
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day))
        except DateTimeParseError:
            pass

        return default

    @property
    def js_value(self):
        value_date = self.value[:3]
        if '' not in value_date:
            return 'new Date(%s, %s, %s)' % (value_date)
        else:
            return ''



@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def MonthYearFieldWidget(field, request):
    """IFieldWidget factory for MonthYearWidget."""
    return FieldWidget(field, MonthYearWidget(request))

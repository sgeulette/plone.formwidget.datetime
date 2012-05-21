from datetime import date, datetime, timedelta
from DateTime import DateTime
import pytz

from zope.i18n import translate
from plone.formwidget.datetime import MessageFactory as _
from collections import deque


def rotated(sequence, steps):
    """Returns a (shallow) copy of the ``sequence`` rotated ``steps``
    times to the right.
    """
    dq = deque(sequence)
    dq.rotate(steps)
    return list(dq)


class AbstractDateWidget(object):

    calendar_type = 'gregorian'
    klass = u'date-widget'
    empty_value = ('', '', '')
    years_range = (-10, 10)
    pattern = None # zope.i18n format (default: u'M/d/yyyy')
    value = empty_value

    #
    # pure javascript no dependencies
    show_today_link = False

    # Requires: jquery.tools.datewidget.js, jquery.js
    # Read more: http://flowplayer.org/tools/dateinput/index.html
    show_jquerytools_dateinput = True

    base_jquerytools_dateinput_config = 'selectors: true, ' \
            'trigger: true, ' \
            'yearRange: [%s, %s]'

    @property
    def jquerytools_dateinput_config(self):
        config = self.base_jquerytools_dateinput_config
        if 'yearRange' in config:
            config = config % self.years_range
        return config
    # TODO: yearRange shoud respect site_properties values for
    #       calendar_starting_year and valendar_future_years_avaliable

    #
    # TODO: implement same thing for JQuery.UI
    popup_calendar_icon = '.css(%s)' % str({
                                'background': 'url(popup_calendar.gif)',
                                'height': '16px',
                                'width': '16px',
                                'display': 'inline-block',
                                'vertical-align': 'middle'})
    @property
    def years(self):
        """years."""
        # 0: year
        value = self.value[0]
        if not value:
            value = datetime.now().year
        now = int(value)
        before = now + self.years_range[0]
        after  = now + self.years_range[1]
        year_range = range(*(before, after))
        return [{'value': x, 'name': x} for x in year_range]

    def get_formatted_value(self, dt_value):
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        # but some persons have already a patched version
        # of python working for older years.
        if not dt_value:
            return ''
        if isinstance(dt_value, DateTime):
            dt_value =  dt_value.asdatetime()
        if not dt_value.year < 100:
            try:
                formater = self._dtformatter
                if self.pattern is not None:
                    formater.setPattern(self.pattern)
                return formater.format(dt_value)
            except ValueError, e:
                if dt_value.year <= 1900:
                    pass
        date_fmt = '%Y/%m/%d %H:%M'
        if (not isinstance(dt_value, datetime)
            and isinstance(dt_value, date)):
            date_fmt = '%Y/%m/%d'
        try:
            # try to format with bare python (no i18n)
            return dt_value.strftime(date_fmt)
        except Exception, e:
            # last resort is ctime
            return dt_value.ctime()

    def dtformatter_to_full_year(self, dt_type):
        formater = None
        try:
            formater = self.request.locale.dates.getFormatter(
                dt_type, "short")
            pattern = formater._pattern
            if (isinstance(pattern, basestring)
                and  ('yy' in pattern)
                and (not 'yyyy' in pattern)):
                formater._pattern = pattern.replace('yy', 'yyyy')
                bin_pattern = formater._bin_pattern[:]
                for i, info in enumerate(bin_pattern):
                    if 'y' == info[0]:
                        formater._bin_pattern[i] = (info[0],  4)
        except AttributeError, e:
            """Tests case, no request"""
            pass
        return formater

    @property
    def _dtformatter(self):
        return self.dtformatter_to_full_year("date")

    @property
    def formatted_value(self):
        if self.value in (self.empty_value, None):
            return ''
        dt_value = self._dtvalue(self.value)
        return self.get_formatted_value(dt_value)

    @property
    def months(self):
        try:
            selected = int(self.month)
        except:
            selected = -1

        calendar = self.request.locale.dates.calendars[self.calendar_type]
        month_names = calendar.getMonthNames()

        for i, month in enumerate(month_names):
            yield dict(
                name=month,
                value=i+1,
                selected=i+1 == selected)

    @property
    def days(self):
        day_range = range(1, 32)
        return [{'value': x, 'name': self._padded_value(x)} for x in day_range]

    @property
    def year(self):
        year = self.request.get(self.name+'-year', None)
        if year is not None:
            return year
        if self.value[0] != self.empty_value[0]:
            return self.value[0]
        return None

    @property
    def month(self):
        month = self.request.get(self.name+'-month', None)
        if month:
            return month
        if self.value[1] != self.empty_value[1]:
            return self.value[1]
        return None

    @property
    def day(self):
        day = self.request.get(self.name+'-day', None)
        if day is not None:
            return day
        if self.value[2] == 1:
            return 1
        if self.value[2] != self.empty_value[2]:
            return self.value[2]
        return None

    def _padded_value(self, value):
        return str(value).zfill(2)

    def show_today_link_js(self, fieldname=None):
        id = fieldname and fieldname or self.id
        now = datetime.today()
        show_link_func = id+'-show-today-link'
        for i in ['-', '_']:
            show_link_func = show_link_func.replace(i, '')
        return '<a href="#" onclick="' \
            'document.getElementById(\'%(id)s-day\').value = %(day)s;' \
            'document.getElementById(\'%(id)s-month\').value = %(month)s;' \
            'document.getElementById(\'%(id)s-year\').value = %(year)s;' \
            'return false;">%(today)s</a>' % dict(
                id=id,
                day=now.day,
                month=now.month,
                year=now.year,
                today=translate(_(u"Today"), context=self.request)
            )

    @property
    def js_value(self):
        year = self.year
        month = None
        month = self.month and int(self.month) - 1 or None

        day = self.day
        if year and month and day:
            return 'new Date(%s, %s, %s)' % (
                year, month, day)
        else:
            return ''

    def _base_dtvalue(self, func, value):
        if value:
            # either no noaive datetime or date
            if (len(value) in [4, 6]) and value[-1]:
                timezone = pytz.timezone(value[-1])
                return func(*map(int, value[:-1]), tzinfo=timezone)
            else:
                if (len(value) in [4, 6]) and not value[-1]:
                    # tz is empty
                    value = value[:-1]
                return func(*map(int, value))

    def _dtvalue(self, value):
        return self._base_dtvalue(date, value)

    def get_js(self, fieldname=None):
        # TODO:
        #     * check if self.name must always be self.name or fieldname if
        #       given (search for other self.name appearances)
        #     * has value be passed here from at-template?
        # archetypes based widget have to pass id and name from the template
        id = fieldname and fieldname or self.id
        name = fieldname and fieldname or self.name

        language = self.request.get('LANGUAGE', 'en')
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        firstday = calendar.week.get('firstDay', 0)
        localize = 'jQuery.tools.dateinput.localize("' + language + '", {'
        localize += 'months: "%s",' % ','.join(calendar.getMonthNames())
        localize += 'shortMonths: "%s",' % ','.join(
            calendar.getMonthAbbreviations()
        )
        # jQuery Tools datepicker wants the days to always start with Sunday and
        # uses the 'firstDay' option to reorder them if required. The .getDayNames()
        # and .getDayAbbreviations() return the days ordered by the current locale
        # and unless the week starts on Sunday we need to rotate them.
        localize += 'days: "%s",' % ','.join(rotated(calendar.getDayNames(), firstday))
        localize += 'shortDays: "%s",' % ','.join(rotated(calendar.getDayAbbreviations(), firstday))
        localize += '});'

        config = 'lang: "%s", ' % language
        if self.js_value:
            config += 'value: %s, ' % self.js_value
        config += 'firstDay: %s, ' % firstday

        config += ('change: function() {\n'
                   '  var value = this.getValue("yyyy-m-d").split("-");\n'
                   '  jQuery("#%(id)s-year").val(value[0]); \n' \
                   '  jQuery("#%(id)s-month").val(value[1]); \n' \
                   '  jQuery("#%(id)s-day").val(value[2]); \n' \
                   '}, ') % dict(id=id)
        config += self.jquerytools_dateinput_config

        return '''
            <input type="hidden"
                id="%(id)s-calendar"
                name="%(name)s-calendar"
                class="%(name)s-calendar" />
            <script type="text/javascript">
                if (jQuery().dateinput) {
                    %(localize)s
                    jQuery("#%(id)s-calendar").dateinput({%(config)s}).unbind('change')
                        .bind('onShow', function (event) {
                            var trigger_offset = jQuery(this).next().offset();
                            jQuery(this).data('dateinput').getCalendar().offset(
                                {top: trigger_offset.top+20, left: trigger_offset.left}
                            );
                        });
                    jQuery("#%(id)s-calendar").next()%(popup_calendar_icon)s;
                }
                function updateCalendar(widgetId) {
                    var y = jQuery(widgetId + '-year').val();
                    var m = jQuery(widgetId + '-month').val();
                    var d = jQuery(widgetId + '-day').val();
                    if (!y || !m || !d) {
                        return;
                    }
                    var newDate = new Date(m + '/' + d + '/' + y);
                    if (newDate.getYear()) { // return NaN (which is false) if the date is invalid
                        jQuery(widgetId + '-calendar').val(m + '/' + d + '/' + y);
                        jQuery(widgetId + '-calendar').data()['dateinput'].setValue(newDate);
                    }
                }
            </script>''' % dict(
                id=id, name=name,
                config=config, localize=localize,
                popup_calendar_icon=self.popup_calendar_icon,
            )

    def onchange(self, fieldname=None):
        if not self.show_jquerytools_dateinput:
            return ''

        id = fieldname and fieldname or self.id
        return "updateCalendar('#%(id)s');" % dict(id=id)


class AbstractDatetimeWidget(AbstractDateWidget):

    empty_value = ('', '', '', '00', '00', '')
    value = empty_value
    klass = u'datetime-widget'
    ampm = False
    pattern = None # (default: u'M/d/yyyy h:mm a'')

    @property
    def _dtformatter(self):
        return self.dtformatter_to_full_year("dateTime")

    def _dtvalue(self, value):
        return self._base_dtvalue(datetime, value)

    @property
    def hour(self):
        hour = self.request.get(self.name+'-hour', None)
        if hour is not None:
            return hour
        if self.value[3] != self.empty_value[3]:
            return self.value[3]
        return None

    @property
    def minute(self):
        min = self.request.get(self.name+'-min', None)
        if min is not None:
            return min
        if self.value[4] != self.empty_value[4]:
            return self.value[4]
        return None

    def is_pm(self):
        if int(self.hour) >= 12:
            return True
        return False

    @property
    def timezone(self):
        timezone = self.request.get(self.name+'-timezone', None)
        if timezone:
            return timezone
        if self.value[5] != self.empty_value[5]:
            return self.value[5]
        return None

    @property
    def minutes(self):
        return [{'value': x, 'name': self.padded_minute(x)} for x in range(60)]

    @property
    def hours(self):
        return [{'value': x, 'name': self.padded_hour(x)} for x in range(24)]

    def padded_hour(self, hour=None):
        hour = hour is not None and hour or self.hour
        if hour is not None:
            if self.ampm is True and self.is_pm() and int(hour)!=12:
                hour = str(int(hour)-12)
            return self._padded_value(hour)
        else:
            return None

    def padded_minute(self, minute=None):
        minute = minute is not None and minute or self.minute
        if minute is not None:
            return self._padded_value(minute)
        else:
            return None

    @property
    def js_value(self):
        year = self.year
        month = self.month and int(self.month) - 1 or None
        day = self.day
        hour = self.hour
        min = self.minute
        if year and month and day and hour and min:
            return 'new Date(%s, %s, %s, %s, %s)' % (
                year, month, day, hour, min)
        elif year and month and day:
            return 'new Date(%s, %s, %s)' % (
                year, month, day)
        else:
            return None

class AbstractMonthYearWidget(AbstractDateWidget):

    klass = u'monthyear-widget'
    empty_value = ('', '', 1)
    value = empty_value


class AbstractYearWidget(AbstractDateWidget):

    klass = u'year-widget'
    empty_value = ('', 1, 1)
    value = empty_value
    pattern = 'yyyy'

from datetime import datetime
from datetime import date
import zope.i18n
from plone.formwidget.dateinput import MessageFactory as _

class AbstractDateWidget(object):

    calendar_type = 'gregorian'
    klass = u'date-widget'
    empty_value = ('', '', '')
    value = empty_value

    #
    # pure javascript no dependencies
    show_today_link = False

    #
    # Requires: jquery.tools.datewidget.js, jquery.js
    # Read more: http://flowplayer.org/tools/dateinput/index.html
    show_jquerytools_dateinput = False
    jquerytools_dateinput_config = 'selectors: true, ' \
                                   'trigger: true, ' \
                                   'yearRange: [-10, 10]'
    # TODO: yearRange shoud respect site_properties values for
    #       calendar_starting_year and valendar_future_years_avaliable


    #
    # TODO: implement same thing for JQuery.UI

    popup_calendar_icon = '.css(%s)' % str({
                                'background':'url(popup_calendar.gif)',
                                'height':'16px',
                                'width':'16px',
                                'display':'inline-block',
                                'vertical-align':'middle'})

    @property
    def _dtformatter(self):
        return self.request.locale.dates.getFormatter("date", "short")

    def _dtvalue(self, value):
        return date(*map(int, value))

    @property
    def formatted_value(self):
        if self.value in (self.empty_value, None):
            return ''
        dt_value = self._dtvalue(self.value)
        if dt_value.year > 1900:
            return self._dtformatter.format(dt_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return dt_value.ctime()

    @property
    def years(self):
        year_range = range(2000,2020)
        return [{'value': x, 'name': x} for x in year_range]

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
                name     = month,
                value    = i+1,
                selected = i+1 == selected)

    @property
    def days(self):
        day_range = range(1,32)
        return [{'value': x, 'name': self._padded_value(x)} for x in day_range]


    @property
    def year(self):
        year = self.request.get(self.name+'-year', None)
        if year is not None:
            return year
        return self.value[0]

    @property
    def month(self):
        month = self.request.get(self.name+'-month', None)
        if month:
            return month
        return self.value[1]

    @property
    def day(self):
        day = self.request.get(self.name+'-day', None)
        if day is not None:
            return day
        return self.value[2]

    def _padded_value(self, value):
        return str(value).zfill(2)

    def show_today_link_js(self):
        now = datetime.today()
        show_link_func = self.id+'-show-today-link'
        for i in ['-', '_']:
            show_link_func = show_link_func.replace(i, '')
        return '<a href="#" onclick="' \
            'document.getElementById(\'%(id)s-day\').value = %(day)s;' \
            'document.getElementById(\'%(id)s-month\').value = %(month)s;' \
            'document.getElementById(\'%(id)s-year\').value = %(year)s;' \
            'return false;">%(today)s</a>' % dict(
                id = self.id,
                day = now.day,
                month = now.month,
                year = now.year,
                today = zope.i18n.translate(_(u"Today"), context=self.request)
            )

    @property
    def js_value(self):
        year = self.year
        month = int(self.month) - 1
        day = self.day
        return 'new Date(%s, %s, %s), ' % (year, month, day)

    def get_js(self):
        language = self.request.get('LANGUAGE', 'en')
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        localize =  'jQuery.tools.dateinput.localize("' + language + '", {'
        localize += 'months: "%s",' % ','.join(calendar.getMonthNames())
        localize += 'shortMonths: "%s",' % ','.join(calendar.getMonthAbbreviations())
        localize += 'days: "%s",' % ','.join(calendar.getDayNames())
        localize += 'shortDays: "%s",' % ','.join(calendar.getDayAbbreviations())
        localize += '});'

        config = 'lang: "%s", ' % language
        config += 'value: %s' % self.js_value

        config += ('change: function() {\n'
                   '  var value = this.getValue("yyyy-mm-dd").split("-");\n'
                   '  jQuery("#%(id)s-year").val(self.year); \n' \
                   '  jQuery("#%(id)s-month").val(self.month); \n' \
                   '  jQuery("#%(id)s-day").val(self.day); \n' \
                   '}, ') % dict(id = self.id)
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
            </script>''' % dict(
                id=self.id, name=self.name,
                config=config, localize=localize,
                popup_calendar_icon=self.popup_calendar_icon,
            )


class AbstractDatetimeWidget(AbstractDateWidget):

    empty_value = ('', '', '', '00', '00')
    value = empty_value
    klass = u'datetime-widget'
    ampm  = False

    @property
    def _dtformatter(self):
        return self.request.locale.dates.getFormatter("dateTime", "short")

    def _dtvalue(self, value):
        return datetime(*map(int, value))

    @property
    def hour(self):
        hour = self.request.get(self.name+'-hour', None)
        if hour:
            return hour
        return self.value[3]

    @property
    def minute(self):
        min = self.request.get(self.name+'-min', None)
        if min:
            return min
        return self.value[4]

    def is_pm(self):
        if int(self.hour) >= 12:
            return True
        return False

    @property
    def minutes(self):
        return [{'value': x, 'name': self.padded_minute(x)} for x in range(60)]

    @property
    def hours(self):
        return [{'value': x, 'name': self.padded_hour(x)} for x in range(24)]

    def padded_hour(self):
        hour = self.hour
        if self.ampm is True and self.is_pm() and int(hour)!=12:
            hour = str(int(hour)-12)
        return self._padded_value(hour)

    def padded_minute(self):
        return self._padded_value(self.minute)

    @property
    def js_value(self):
        year = self.year
        month = int(self.month) - 1
        day = self.day
        hour = self.hour
        min = self.minute
        return 'new Date(%s, %s, %s, %s, %s), ' % (
            year, month, day, hour, min)


class AbstractMonthYearWidget(AbstractDateWidget):

    klass = u'monthyear-widget'
    empty_value = ('', '', 1)
    value = empty_value

Changelog
=========


1.0a3 (unreleased)
---------------------

- Archetypes widget now reliably returns DateTime instances instead datetime.
  [thet]

- AM/PM 12-hour time fixes: 12 a.m. == u'00' hour internally, displayed
  consistently; normalization of times gracefully handles missing hour
  values; deal gracefully with 12 p.m. and 12 a.m. hours.
  [seanupton]

- Fixed a bug with the datepicker configuration when the week starts on
  a different day than Sunday.
  [dokai]

- Added a wrapper element around the time components in the z3c.form datetime widget markup
  to faciliate Javascript (and CSS) control.
  [dokai]

- Fixed a bug where the minutes were ignored and set unconditionally
  to zero when the field values were extracted.
  [dokai]

- Fixed a problem with zero valued time components being ignored.
  [dokai]

- fix all tests [kiorky]
- dynamic years range support [kiorky]
- support for very old years  ( <1800 ) [kiorky]
- support for custom date patterns in view mode [kiorky]
- support for only year widget [kiorky]
- Fix support for older years inside AT widgets [kiorky]


1.0a2 (2012-03-12)
------------------

- Include z3c.form's meta.zcml, so widgetsTemplate directive is registered.
  [thet]

- For conditional zcml incudes, use zcml:condition instead of zcml:provides.
  [thet]

- Code cleanup.
  [thet]

1.0a1 (2012-02-24)
------------------

- Initial alpha (!) release from the Plone Konferenz 2012 in Munich.
  [thet]

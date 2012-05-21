import unittest2 as unittest
import doctest
import os.path
#from interlude import interact

OPTIONFLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
DOCFILES = [
]
DOCMODS = [
    'plone.formwidget.datetime.base',
]

def assertEqualDatetime(self, date1, date2, msg=None):
    """ Compare two datetime instances to a resolution of minutes.
    """
    compare_str = '%Y-%m-%d %H:%M %Z'
    self.assertTrue(date1.strftime(compare_str) ==\
                    date2.strftime(compare_str), msg)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        doctest.DocFileSuite(
            os.path.join(os.path.dirname(__file__), docfile),
            module_relative=False,
            optionflags=OPTIONFLAGS,
            globs={#'interact': interact,
                   'assertEqualDatetime': assertEqualDatetime}
        ) for docfile in DOCFILES
    ])
    suite.addTests([
        doctest.DocTestSuite(
            docmod,
            optionflags=OPTIONFLAGS,
            globs={#'interact': interact,
                   'assertEqualDatetime': assertEqualDatetime}
        ) for docmod in DOCMODS
    ])
    return suite

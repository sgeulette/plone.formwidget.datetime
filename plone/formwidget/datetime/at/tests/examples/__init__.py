from plone.formwidget.datetime import PROJECTNAME

from Products.CMFCore.utils import ContentInit
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.permissions import AddPortalContent


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from archetypes.datetimewidget.examples import DatetimeWidgetType
    DatetimeWidgetType  # pyflakes
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = AddPortalContent,
        extra_constructors = constructors,
        ).initialize(context)

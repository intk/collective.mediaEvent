from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from collective.mediaEvent import MessageFactory as _

import datetime

# Interface class; used to define content-type schema.

class ImediaEvent(form.Schema, IImageScaleTraversable):
    """
    Folderish Event
    """

    title = schema.TextLine(
        title=_(u"Event name"),
    )

    description = schema.Text(
        title=_(u"Event summary"),
    )

    start = schema.Datetime(
        title=_(u"Event starts"),
        required=False,
    )

    end = schema.Datetime(
        title=_(u"Event ends"),
        required=False,
    )

    body = RichText(
        title=_(u"Body Text"),
        required=False
    )

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_(
                    u"The event's start date must be before the end date."))


@form.default_value(field=ImediaEvent['start'])
def startDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(7)


@form.default_value(field=ImediaEvent['end'])
def endDefaultValue(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today() + datetime.timedelta(10)


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class mediaEvent(dexterity.Container):
    grok.implements(ImediaEvent)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# mediaevent_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class View(grok.View):
    grok.context(ImediaEvent)
    grok.require('zope2.View')

    # grok.name('view')
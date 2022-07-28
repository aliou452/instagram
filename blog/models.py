# Create your models here.
from __future__ import unicode_literals

from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager





class BlogLikers(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.
    """

    page = ParentalKey(
        'BlogPage', related_name='blog_likers_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'home.People', related_name='likers_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        FieldPanel('people')
    ]


class BlogPageTag(TaggedItemBase):
        """
        This model allows us to create a many-to-many relationship between
        the BlogPage object and tags.
        """
        content_object = ParentalKey('BlogPage', related_name='tagged_items', on_delete=models.CASCADE)


class BlogPage(Page):
    """
    A Blog Page

    We access the People object with an inline panel that references the
    ParentalKey's related_name in BlogPeopleRelationship.
    """
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)



    content_panels = Page.content_panels + [
        FieldPanel('image'),
        InlinePanel(
            'blog_likers_relationship', label="Author(s)",
            panels=None, min_num=1),
        FieldPanel('tags')
    ]


    


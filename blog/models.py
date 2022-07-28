# Create your models here.
from __future__ import unicode_literals

from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Page
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import RichTextField





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

class BlogComment(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.
    """

    page = ParentalKey(
        'BlogPage', related_name='blog_commenters_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        'home.People', related_name='commenters_blog_relationship', on_delete=models.CASCADE
    )

    comment = RichTextField()

    panels = [
        FieldPanel('people'),
        FieldPanel('comment')

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

    creator = models.ForeignKey(
            "home.People",
            null=False,
            blank=False,
            on_delete=models.CASCADE,
            related_name='+',
            help_text='The photo creator.'    
            )



    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('creator'),
        InlinePanel(
            'blog_likers_relationship', label="Liker(s)",
            panels=None),
        InlinePanel(
            'blog_commenters_relationship', label="Commenter(s)",
            panels=None),
        FieldPanel('tags')
    ]

    def likes(self):
        return len(
            [
                n.people for n in self.blog_likers_relationship.all()
            ]
        )


    def authors(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        authors_comments = [
            (n.people, n.comment) for n in self.blog_commenters_relationship.all()
        ]

        for author_comment in authors_comments:
            print(author_comment)

        return authors_comments

    @property
    def get_tags(self):
        """
        Similar to the authors function above we're returning all the tags that
        are related to the blog post into a list we can access on the template.
        We're additionally adding a URL to access BlogPage objects with that tag
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags


    


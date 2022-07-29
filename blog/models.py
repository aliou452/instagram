# Create your models here.
from __future__ import unicode_literals
import imp
from pyexpat import model
from turtle import heading

from django.db import models

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.models import Orderable
from modelcluster.fields import ParentalKey
from taggit.models import Tag, TaggedItemBase
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.fields import RichTextField

from django.shortcuts import redirect, render
from django.contrib import messages
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.contrib.auth.models import User




class BlogLikers(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.
    """

    page = ParentalKey(
        'BlogPage', related_name='blog_likers_relationship', on_delete=models.CASCADE
    )
    people = models.ForeignKey(
        User, related_name='likers_blog_relationship', on_delete=models.CASCADE
    )
    panels = [
        FieldPanel('people')
    ]

class AlbumPhotos(Orderable):
    """Between 1 and 10 photos for album"""
    page = ParentalKey(
        "AlbumPage", related_name="album_photo", on_delete=models.CASCADE
    )

    album_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    panels = [
        FieldPanel('album_image')
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
        User, related_name='commenters_blog_relationship', on_delete=models.CASCADE
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
            User,
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
        Returns the BlogPage's related People.
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
        """
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'tags',
                tag.slug
            ])
        return tags

    parent_page_types = ['BlogIndexPage']



class AlbumPage(BlogPage):
    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('creator'),
        InlinePanel(
            'blog_likers_relationship', label="Liker(s)",
            panels=None),
        InlinePanel(
            'blog_commenters_relationship', label="Commenter(s)",
            panels=None),
        FieldPanel('tags'),
        MultiFieldPanel([
            InlinePanel('album_photo', label='photo', max_num=10, min_num=1)
        ], heading="Album photos"),
        
    ]



class BlogIndexPage(RoutablePageMixin, Page):
    """
    Index page for blogs.
    We need to alter the page model's context to return the child page objects,
    the BlogPage objects, so that it works as an index page.
    """
   
    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
    ]

    subpage_types = ['BlogPage', 'AlbumPage']


    def children(self):
        return self.get_children().specific().live()


    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live()
        return context


    @route(r'^tags/$', name='tag_archive')
    @route(r'^tags/([\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):

        try:
            tag = Tag.objects.get(slug=tag)
        except Tag.DoesNotExist:
            if tag:
                msg = 'There are no blog posts tagged with "{}"'.format(tag)
                messages.add_message(request, messages.INFO, msg)
            return redirect(self.url)

        posts = self.get_posts(tag=tag)
        context = {
            'tag': tag,
            'posts': posts
        }
        return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        return self.serve(request)


    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    def get_child_tags(self):
        tags = []
        for post in self.get_posts():
            tags += post.get_tags
        tags = sorted(set(tags))
        return tags


    


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



class UserProfile(models.Model):
    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            primary_key=True,
        )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    avatar = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )







class ProfilePage(Page, User):
    pass
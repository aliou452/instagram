from django import template

from wagtail.models import Site


register = template.Library()
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context['request']).root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    for menuitem in menuitems_children:
        menuitem.has_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url_path.startswith(menuitem.url_path)
                           if calling_page else False)
        menuitem.children = menuitem.get_children().live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }



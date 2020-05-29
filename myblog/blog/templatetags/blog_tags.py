from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

from ..models import Post


register = template.Library()

# Total posts at site
@register.simple_tag(name='total_post_tag')
# Create template tag
# The name it isn't necessary argument
# if not name in decorator then call name func {% total_post %}
# after add tag reboot server and {% load %} in templates
def total_post():
    return Post.objects.count()


# Most commented posts
@register.simple_tag
def get_post_most_comments(count=5):
    """
    add all comment for post and sort and slicing
    """
    return Post.objects.annotate(total_comments=Count('comments'))\
                                .order_by('-total_comments')[:count]

# Last articles at site
@register.inclusion_tag('blog/tags/latest_post.html')
# Create template tag inclusion
# The argument template name
# context goes in 'blog/tags/latest_post.html'
def show_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts': latest_posts, }


@register.filter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
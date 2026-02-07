from django.template import Library
from ..models import *
from django.db.models import Count

register = Library()


@register.simple_tag
def total_posts():
    return Post.published.all().count()


@register.simple_tag
def total_comments():
    return Comment.objects.filter(active=True).count()


@register.simple_tag(name='lpd')
def last_post_date():
    return Post.published.last().publish


@register.inclusion_tag('partials/latest_post.html')
def latest_posts(count=1):
    lposts = Post.published.order_by('-publish')[:count]
    return {'lposts': lposts}


@register.simple_tag(name='mpp')
def most_popular_posts(count=1):
    return Post.published.annotate(comment_counts=Count('comments')).order_by('-comment_counts')[:count]

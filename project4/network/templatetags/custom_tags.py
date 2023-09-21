from django import template
from network.models import Post,User
from django import template
from django.templatetags.static import static
from django.utils.html import mark_safe
from network.models import User, Post  # Importe os modelos necessários

register = template.Library()


@register.simple_tag
def numberLike(id_post):
    # Sua lógica personalizada aqui
    post = Post.objects.get(id=id_post)
    numberLike = len(post.liked_by.all())
    return numberLike

@register.filter
def like(liker_id,post_id):
    liker = User.objects.get(id=liker_id)
    post = Post.objects.get(id=post_id)
    if liker in post.liked_by.all():
        return True
    else:
        return False
        

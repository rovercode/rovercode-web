"""Blog views."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from datetime import datetime
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from .forms import PostForm


def post_list(request, drafts=False):
    """Test view."""
    published = not drafts
    post_list = Post.objects.filter(published=published)
    return render(request, 'blog_post_list.html', {'post_list': post_list})


@staff_member_required
def post_edit(request, slug=None):
    """Post edit view for a specific blog post."""
    if slug is not None:
        post = get_object_or_404(Post, slug=slug)
    else:
        # Create a new post
        post = Post()
        post.author = request.user
        post.published_date = datetime.now()
    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(
                reverse('blog:post_detail',
                        kwargs={'slug': post.slug})
            )

        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog_post_edit.html', {
        'title': post.title,
        'form': form
    })


def post_detail(request, slug):
    """Post details view for a specific blog post."""
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog_post_detail.html', {'post': post})


class PostViewSet(viewsets.ModelViewSet):
    """API endpoint that allows posts to be viewed or edited."""

    serializer_class = PostSerializer
    queryset = Post.objects.all()

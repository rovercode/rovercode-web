"""Blog views."""
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django_filters.rest_framework import DjangoFilterBackend
from django.core.urlresolvers import reverse
from datetime import datetime
from rest_framework import viewsets, serializers
from rest_framework.renderers import JSONRenderer
from .models import Post
from .serializers import PostSerializer
from .forms import PostForm

def post_list(request, drafts=False):
    """Test view."""
    published = not drafts
    post_list = Post.objects.filter(published=published)
    return render(request, 'blog_post_list.html', {'post_list': post_list})

@staff_member_required
def post_edit(request, pk=None):
    """Post edit view for a specific blog post."""
    if pk is not None:
        post = get_object_or_404(Post, pk=pk)
    else:
        # Create a new post
        post = Post()
        post.author = request.user
        post.published_date = datetime.now()
    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('blog:post_list'))

        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog_post_edit.html', {
        'title': post.title,
        'form': form
    })

def post_detail(request, pk):
    """Post details view for a specific blog post."""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_post_detail.html', {'post': post})

class PostViewSet(viewsets.ModelViewSet):
    """API endpoint that allows posts to be viewed or edited."""

    serializer_class = PostSerializer
    queryset = Post.objects.all()

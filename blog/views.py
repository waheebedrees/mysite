
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.urls import reverse
from .models import Post, Category, Tag
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from blog.templatetags.markdownify import extract_toc, parse_markdown
from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.views.generic import ListView, DetailView


def index(request):
    post_list = Post.objects.all().order_by('-created_on')
    paginator = Paginator(post_list, 6)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    categories = Category.objects.annotate(post_count=Count('posts'))
    tags = Tag.objects.annotate(post_count=Count('posts'))
  
    return render(request, 'index.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    })


def about(request):
    return render(request, 'about.html')

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category).order_by("-created_on")
    return render(request, 'blog_category.html', {'category': category, 'posts': posts})


def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    post_list = Post.objects.filter(tags=tag).order_by('-created_on')
    paginator = Paginator(post_list, 6)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/tag_posts.html', {
        'posts': posts,
        'selected_tag': tag,
    })


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.objects.filter(
        categories=category).order_by('-created_on')
    paginator = Paginator(post_list, 6)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/category_posts.html', {
        'posts': posts,
        'selected_category': category,
    })


def post_list(request):
    post_list = Post.objects.all().order_by('-created_on')
    paginator = Paginator(post_list, 6)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    categories = Category.objects.annotate(post_count=Count('posts'))
    tags = Tag.objects.annotate(post_count=Count('posts'))
  
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags,
    })


def post_details(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        created_on__year=year,
        created_on__month=month,
        created_on__day=day
    )
    toc, body = parse_markdown(post.body)
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'toc': toc,
        'body': body
    })



class AboutView(TemplateView):
    template_name = 'about.html'


def handler404(request, exception):
    return render(request, '404.html', status=404)



def blog_list(request):
    return render(request, 'blog_list.html')



class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Post.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts'))
        context['tags'] = Tag.objects.annotate(post_count=Count('posts'))
        return context
    

class TagPostsView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['slug'])
        return Post.published.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_tag'] = self.tag
        return context


class CategoryPostsView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Post.published.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = self.category
        return context

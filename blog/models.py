from django.utils import timezone
from django.urls import reverse
from django.conf import settings
import itertools
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=40, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)




class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    categories = models.ManyToManyField(Category, related_name='posts')
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    cover_image = models.ImageField(
        upload_to='blog/covers/',
        blank=True,
        null=True
    )
    references = models.TextField(
        blank=True,
        null=True,
        help_text="Format references using Markdown"
    )
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    # Custom manager for published posts
    objects = models.Manager()

    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    published = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            for i in itertools.count(1):
                if not Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[
            self.created_on.year,
            self.created_on.month,
            self.created_on.day,
            self.slug
        ])

    @property
    def read_time(self):
        word_count = len(self.body.split())
        return max(1, round(word_count / 200))


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"


    def __str__(self):
        author_name = getattr(self.author, 'username', str(self.author))
        return f"Comment by {author_name} on {self.post.title}"
    class Meta:
        ordering = ['-created_on']

from django.contrib import admin
from .models import Post, Category, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'last_modified', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')
    list_filter = ('created_on', 'categories')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    filter_horizontal = ('categories',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'body', 'cover_image', 'status')
        }),
        ('Metadata', {
            'fields': ('categories', 'tags'),
            'classes': ('collapse',)
        }),
        ('References', {
            'fields': ('references',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_on', 'approved')
    search_fields = ('author', 'body')
    list_filter = ('approved', 'created_on')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

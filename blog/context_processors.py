def navigation_context(request):
    return {
        'blog_url_names': [
            'post_list',
            'post_detail',
            'tag_posts',
            'category_posts',
            'blog_list'
        ]
    }

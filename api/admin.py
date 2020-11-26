from django.contrib import admin

from .models import User, Comment, Review, Title, Genre, Category


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-empty-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'author', 'text', 'pub_date',)
    search_fields = ('text', 'author',)
    list_filter = ('pub_date',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title_id', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text', 'author')
    list_filter = ('pub_date',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'category')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('year', 'genre', 'category')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)



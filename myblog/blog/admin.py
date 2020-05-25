from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """list_display - отображение желаемых полей
       list_filter - фильтрация по выбранным полям
       search_fields - поиск по полям
       prepopulated_fields - генерация slug из title
       date_hierarchy - отображении навиации дат по ссылкам
       ordering - сортировка по умолчанию
       raw_id_fields - поиск автора а не выплывающий список
       авторов постребуется если много авторов
    """
    list_display = ('title', 'slug', 'author', 'publish', 'status', 'id',)
    list_filter = ('status', 'created', 'publish', 'author',)
    search_fields = ('title', 'body',)
    prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created', 'active', 'id')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('author', 'body')
    # raw_id_fields = ('post',)
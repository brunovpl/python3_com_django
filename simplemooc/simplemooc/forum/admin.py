from django.contrib import admin

from .models import Thread, Reply


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'updated_at']
    search_fields = ['title', 'author__email', 'body']


class ReplyAdmin(admin.ModelAdmin):
    list_display = ['thread', 'author', 'created_at', 'updated_at']
    search_fields = ['thread__tilte', 'author__email', 'reply']


admin.site.register(model_or_iterable=Thread, admin_class=ThreadAdmin)
admin.site.register(model_or_iterable=Reply, admin_class=ReplyAdmin)

from django.contrib import admin

# Register your models here.

from snippets.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    fields = ('title', 'code', 'description',
              'created_by', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Snippet, SnippetAdmin)

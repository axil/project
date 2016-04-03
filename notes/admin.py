from django.contrib import admin
from notes.models import Notes


class Notes_Admin(admin.ModelAdmin):
    fields = ['title', 'text', 'author', 'date', 'favorites']
    list_display = ['title', 'date']
    list_filter = ['title']
    search_fields = ['title']


admin.site.register(Notes, Notes_Admin)
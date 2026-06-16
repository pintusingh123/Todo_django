from django.contrib import admin
from .models import Todo
# Register your models here.


@admin.register(Todo)
class Admintodo(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at')
    list_filter = ('completed', 'created_at')
    search_fields = ('title', 'completed', 'description')
    ordering = ('created_at',)

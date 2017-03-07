from django.contrib import admin
from .models import addcourse, comment
# Register your models here.

class CommentInline(admin.TabularInline):
    model = comment
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['subject']}),
        (None, {'fields': ['courseid']}),
        (None, {'fields': ['prof']}),
        (None, {'fields': ['grade']}),

    ]
    inlines = [CommentInline]
    list_display = ('courseid', 'subject')
    list_filter = ['courseid']
    ordering = ('courseid',)
    search_fields = ['courseid']


admin.site.register(addcourse, CourseAdmin)

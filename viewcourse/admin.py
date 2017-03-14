from django.contrib import admin
from .models import addcourse, comment, professor
# Register your models here.

class CommentInline(admin.TabularInline):
    model = comment
    extra = 1

class ProfessorInline(admin.TabularInline):
    model = professor
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['subject']}),
        (None, {'fields': ['courseid']}),
        (None, {'fields': ['grade']}),

    ]
    inlines = [CommentInline, ProfessorInline]
    list_display = ('courseid', 'subject')
    list_filter = ['courseid']
    ordering = ('courseid',)
    search_fields = ['courseid']


admin.site.register(addcourse, CourseAdmin)

from django.contrib import admin
from .models import course, comment, professor, account
# Register your models here.

class CommentInline(admin.TabularInline):
    model = comment
    extra = 1

class ProfessorInline(admin.TabularInline):
    model = professor
    extra = 1

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['university']}),
        (None, {'fields': ['subject']}),
        (None, {'fields': ['courseid']}),
        (None, {'fields': ['grade']}),

    ]
    inlines = [ProfessorInline, CommentInline]
    list_display = ('courseid', 'subject')
    list_filter = ['courseid']
    ordering = ('courseid',)
    search_fields = ['courseid']

class AccountAdmin(admin.ModelAdmin):
    ordering = ('username',)
    search_fields = ['username']

admin.site.register(course, CourseAdmin)
admin.site.register(account, AccountAdmin)

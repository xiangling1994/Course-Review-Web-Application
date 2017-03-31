from django.contrib import admin
from .models import course, comment, professor, account, vote, judge
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


class VoteInline(admin.TabularInline):
    model = vote
    extra = 1

class JudgeInline(admin.TabularInline):
    model = judge
    extra = 1

class AccountAdmin(admin.ModelAdmin):
    inlines = [VoteInline, JudgeInline]
    ordering = ('username',)
    search_fields = ['username']

admin.site.register(course, CourseAdmin)
admin.site.register(account, AccountAdmin)

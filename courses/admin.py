from django.contrib import admin
from .models import *

admin.site.index_template = 'memcache_status/admin_index.html'
admin.site.register(Instructor)
admin.site.register(Enrollment)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title','slug']
    prepopulated_fields = {
    'slug':('title',)
    }
class ModuleInline(admin.StackedInline):
    model = Module
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title','subject','created']
    list_filter = ['created','subject']
    search_fields = ['title','overview']
    prepopulated_fields = {
    'slug':('title',)
    }
    inline = [ModuleInline]

admin.site.register(Content)
admin.site.register(Module)

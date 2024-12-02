from django.contrib import admin
from .models import Course, Category

# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'date_created'
    )

admin.site.register(Course, CourseAdmin)
admin.site.register(Category)
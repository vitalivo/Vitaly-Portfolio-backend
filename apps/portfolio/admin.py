from django.contrib import admin
from .models import Category, Technology, Project, Skill

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'position', 'is_active']
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'position', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title_en', 'status', 'is_featured', 'published_at']
    prepopulated_fields = {'slug': ('title_en',)}
    filter_horizontal = ['categories', 'technologies']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'category', 'level', 'position', 'is_active']
    prepopulated_fields = {'slug': ('name_en',)}
# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import DictionaryCategories, DictionarySubcategories, Company
# Register your models here.

@admin.register(DictionaryCategories)
class DictionaryCategoriesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code']
    list_editable = ['name', 'code']

@admin.register(DictionarySubcategories)
class DictionarySubcategoriesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_categories_name']
    list_editable = ['name']

    @admin.display(description='Category')
    def get_categories_name(self, obj):
        return obj.dictionary_category.name

@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'street', 'city', 'province', 'zip', 'get_user_name']
    # list_editable = ['name']

    @admin.display(description='User')
    def get_user_name(self, obj):
        return obj.user.username

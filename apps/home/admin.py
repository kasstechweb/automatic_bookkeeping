# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import DictionaryCategories, DictionarySubcategories, Company, DictionarySubcategoriesNotApproved
from django.shortcuts import redirect
from .functions import update_subcategories
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

@admin.register(DictionarySubcategoriesNotApproved)
class DictionarySubcategoriesNotApprovedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_categories_name', 'approved']
    list_editable = ['name', 'approved']
    # list_filter = ('approved',)

    @admin.display(description='Category')
    def get_categories_name(self, obj):
        return obj.dictionary_category.name

    def changelist_view(self, request, extra_context=None):
        referrer = request.META.get('HTTP_REFERER', '')
        get_param = "approved__exact=0"
        if len(request.GET) == 0 and '?' not in referrer:
            return redirect("{url}?{get_parms}".format(url=request.path, get_parms=get_param))
        return super(DictionarySubcategoriesNotApprovedModelAdmin,self).changelist_view(request, extra_context=extra_context)

    # def Approved(self, obj):
    #     return obj.approved > 0

    # Approved.boolean = True
    def save_model(self, request, obj, form, change):
        print(obj.approved)
        if obj.approved == 1:
            update_subcategories(obj)
        # print(obj.id)
        super().save_model(request, obj, form, change)
        # print('ggggggggggggg')

@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'street', 'city', 'province', 'zip', 'get_user_name']
    # list_editable = ['name']

    @admin.display(description='User')
    def get_user_name(self, obj):
        return obj.user.username

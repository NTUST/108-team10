from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Beverage)
admin.site.register(BeverageCapacity)
admin.site.register(TeamMember)


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('name')
    search_hields = ('name')
    ordering = ('name')


class ShopAdmin(admin.ModelAdmin):
    list_filter = ('name')
    search_hields = ('name')
    ordering = ('name')


class BeverageAdmin(admin.ModelAdmin):
    list_filter = ('Shop', 'name',
                   'Category', 'hasCold', 'hasHot')
    search_hields = ('Shop', 'name',
                     'Category', 'hasCold', 'hasHot')
    ordering = ('Shop', 'name', 'Category')


class BeverageCapacityAdmin(admin.ModelAdmin):

    list_filter = ('capacity', 'price',
                   'calories')
    search_hields = ('capacity')
    ordering = ('capacity', 'price', 'calories')


class TeamMemberAdmin(admin.ModelAdmin):
    search_hields = ('StudentId', 'name')
    ordering = ('StudentId')
# Register your models here.

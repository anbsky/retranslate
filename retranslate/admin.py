# encoding=utf-8

from __future__ import print_function

from django.contrib import admin

from models import String


class StringAdmin(admin.ModelAdmin):
    list_display = ('original', 'translated', 'file', 'location_row',
                    'location_col', 'translator')
    list_filter = ('translator', 'language',)
    search_fields = ('original', 'translated', 'file')

    def save_model(self, request, obj, form, change):
        obj.set_translator(request)
        return super(StringAdmin, self).save_model(request, obj, form, change)

admin.site.register(String, StringAdmin)
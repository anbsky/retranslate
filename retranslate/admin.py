# encoding=utf-8

from __future__ import print_function

from django.contrib import admin
from django import forms

from models import String


class StringAdminForm(forms.ModelForm):
    class Meta:
        model = String
        widgets = {
            'original': forms.Textarea(attrs={'cols': 100}),
            'translated': forms.Textarea(attrs={'cols': 100}),
        }


class StringAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_ignored', 'original', 'translation', 'file',
                    'location_row', 'location_col', 'translator')
    list_editable = ('is_ignored',)
    list_filter = ('language', 'is_translated', 'is_ignored')
    search_fields = ('original', 'translated', 'file')
    readonly_fields = ('context', 'translator',)
    form = StringAdminForm

    def save_model(self, request, obj, form, change):
        obj.set_translator(request)
        return super(StringAdmin, self).save_model(request, obj, form, change)

admin.site.register(String, StringAdmin)
#encoding=utf-8

from __future__ import print_function

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class String(models.Model):
    LANGUAGES = (
        ('RU', _('Russian')),
        ('EN', _('English')),
    )

    original = models.TextField(_('original string'), db_index=True)
    translated = models.TextField(_('translated string'), db_index=True)
    file = models.CharField(_('occurs in file'), max_length=255, blank=True, db_index=True)
    location = models.CharField(_('file location'), max_length=10, blank=True)
    language = models.CharField(_('language'), max_length=2, blank=True, choices=LANGUAGES)
    translator = models.ForeignKey(User, verbose_name=_('translator'), blank=True, null=True)

    def __unicode__(self):
        return u'{}...'.format(self.original[:25])

    def set_translator(self, request):
        self.translator = request.user

    def location_row(self):
        try:
            if self.location:
                return int(self.location.split(':')[0])
        except (ValueError, IndexError):
            return None

    def location_col(self):
        try:
            if self.location:
                return int(self.location.split(':')[1])
        except (ValueError, IndexError):
            return None

    class Meta:
        verbose_name = _('string')
        verbose_name_plural = _('strings')
        ordering = ('file', 'location')

from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Player, Event, Match

admin.site.site_title = _('Ranker Content Management')
admin.site.site_header = _('Ranker Content Management')
admin.site.index_title = _('Content Management')

admin.site.unregister(Group)
admin.site.register([Player, Event, Match])

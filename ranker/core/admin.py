from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import Player, Event, Match

admin.site.site_title = _('Ranker Content Management')
admin.site.site_header = _('Ranker Content Management')
admin.site.index_title = _('Content Management')

admin.site.unregister(Group)
admin.site.register([Player, Event])


class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = "__all__"


class MatchAdmin(admin.ModelAdmin):
    form = MatchForm
    readonly_fields = [
        'winner_rating',
        'loser_rating',
        'delta',
    ]


admin.site.register(Match, MatchAdmin)
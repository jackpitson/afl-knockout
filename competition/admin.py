from django.contrib import admin
from .models import Player, Team, Round, Match, Tip


class TipInline(admin.TabularInline):
    model = Tip
    extra = 0
    readonly_fields = ["player", "team"]


class RoundAdmin(admin.ModelAdmin):
    inlines = [TipInline]

class TipAdmin(admin.ModelAdmin):
    list_display = ["player", "round", "team"]
    list_filter = ["round"]

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Tip, TipAdmin)
admin.site.register(Round, RoundAdmin)
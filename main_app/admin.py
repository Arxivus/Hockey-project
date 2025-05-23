from django.contrib import admin
from .models import Profile, Competitor, Micromatch, Announsment, Tournament, TournamentGroup

class TournamentAdmin(admin.ModelAdmin):
    fields = ('tour_id', 'date', 'played_with_matrix')
    readonly_fields = ('tour_id', 'date')  

admin.site.register(Profile)
admin.site.register(Competitor)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Micromatch)
admin.site.register(Announsment)
admin.site.register(TournamentGroup)



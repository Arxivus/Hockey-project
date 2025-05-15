from django.contrib import admin
from .models import Profile, Competitor, Micromatch, Announsment, Tournament

class TournamentAdmin(admin.ModelAdmin):
    fields = ('tour_id', 'date', 'goal_matrix')
    readonly_fields = ('tour_id', 'date')  

admin.site.register(Profile)
admin.site.register(Competitor)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Micromatch)
admin.site.register(Announsment)



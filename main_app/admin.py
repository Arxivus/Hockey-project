from django.contrib import admin
from .models import Profile, Competitor, Micromatch, Announsment, Tournament, TournamentGroup

class TournamentAdmin(admin.ModelAdmin):
    fields = (
        'tour_id', 
        'date', 
        'played_with_matrix', 
        'playing_groups_ids', 
        'time_started', 
        'minutes_btwn_groups',
        'minutes_btwn_matches',
        'isEnded'
    )
    readonly_fields = ('tour_id', 'date')  
    search_fields = ('tour_id',)

class CompetitorAdmin(admin.ModelAdmin):
    search_fields = ('player_id', 'name')
    list_filter = ('group_id', 'gender', 'role')

class MicromatchAdmin(admin.ModelAdmin):
    search_fields = ('start_time',)
    list_filter = ('tournament__tour_id', )
    ordering = ('start_time',)
    
class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('fullname',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Micromatch, MicromatchAdmin)
admin.site.register(Announsment)
admin.site.register(TournamentGroup)



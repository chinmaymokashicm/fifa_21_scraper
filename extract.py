from modules.team import Team
from modules.player import Player

team_obj = Team()
player_obj = Player()

team_obj.get_team_urls()
player_obj.fetch_player_urls(team_obj.list_team_urls)
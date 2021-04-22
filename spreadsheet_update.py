import gspread
from oauth2client.service_account import ServiceAccountCredentials
import retrieve
     

               
def find_to_update(teams,players):
    list_to_update=list()
    for player in players:
        for team in teams:
            if team['team']==player['team']:
                player_team_id=team['team_id']
                if tuple((player['name'], player_team_id)) not in list_to_update:
                    list_to_update.append(tuple((player['name'], player_team_id)))
    return list_to_update
                
def next_available_row(sheet):
    str_list=list(filter(None, sheet.col_values(1)))
    return int(len(str_list)+1)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet_players = client.open("tracking_app").worksheet("players")
sheet_teams=client.open("tracking_app").worksheet("team_ids")

list_of_teams=sheet_teams.get_all_records()
list_of_players=sheet_players.get_all_records()



found_to_update=find_to_update(list_of_teams, list_of_players)
print(found_to_update)
retrieved_data=retrieve.retrieve_stats(found_to_update) #retrieve stats of the required player for the last game 
print(retrieved_data)


for item in retrieved_data:

    #deriving stat parameters
    stat_params=dict()
        
    min_played=item[2][0]['games']['minutes']
    
    offsides=item[2][0]['offsides']
    stat_params['offsides']=offsides
        
    shots_total=item[2][0]['shots']['total']
    stat_params['total shots']=shots_total
        
    shots_target=item[2][0]['shots']['on']
    stat_params['shots on target']=shots_target
        
    goals_scored=item[2][0]['goals']['total']
    stat_params['scored']=goals_scored
        
    goals_conceded=item[2][0]['goals']['conceded']
    stat_params['conceded']=goals_conceded
        
    assists=item[2][0]['goals']['assists']
    stat_params['assists']=assists
        
    saves=item[2][0]['goals']['saves']
    stat_params['saves']=saves
        
    passes_total=item[2][0]['passes']['total']
    stat_params['passes']=passes_total
        
    passes_key=item[2][0]['passes']['key']
    stat_params['key passes']=passes_key
        
    passes_accurate=item[2][0]['passes']['accuracy']
    stat_params['accurate passes']=int(passes_accurate)
        
    blocks=item[2][0]['tackles']['blocks']
    stat_params['shot blocks']=blocks
        
    interceptions=item[2][0]['tackles']['interceptions']
    stat_params['interceptions']=interceptions
        
    duels_total=item[2][0]['duels']['total']
    stat_params['duels']=duels_total
        
    duels_won=item[2][0]['duels']['won']
    stat_params['duels won']=duels_won
        
    dribbles_total=item[2][0]['dribbles']['attempts']
    stat_params['dribbles']=dribbles_total
        
    dribbles_succ=item[2][0]['dribbles']['success']
    stat_params['successful dribbles']=dribbles_succ
        
    dribbles_past=item[2][0]['dribbles']['past']
    stat_params['outplayed']=dribbles_past
        
    fouls_drawn=item[2][0]['fouls']['drawn']
    stat_params['fouls drawn']=fouls_drawn
        
    fouls_committed=item[2][0]['fouls']['committed']
    stat_params['fouls committed']=fouls_committed
        
    penalties_won=item[2][0]['penalty']['won']
    stat_params['penalties won']=penalties_won
        
    penalties_committed=item[2][0]['penalty']['commited']
    stat_params['penalties committed']=penalties_committed
        
    penalties_scored=item[2][0]['penalty']['scored']
    stat_params['penalties scored']=penalties_scored
        
    penalties_missed=item[2][0]['penalty']['missed']
    stat_params['penalties missed']=penalties_missed
        
    penalties_saved=item[2][0]['penalty']['saved']
    stat_params['penalties saved']=penalties_saved
        
        
    #change None to 0 to then do the accuracy calcs and input 0 rather than empty strings in the spreadsheet
    for param,value in stat_params.items():
        if value is None:
            value=0
            stat_params[param]=value
            
            
    try: shots_accuracy=stat_params['shots on target'] / stat_params['total shots'] * 100
    except: shots_accuracy='didn\'t shoot'
    stat_params['shot accuracy']=shots_accuracy
        
    try: tackles=retrieved_data[1][0]['tackles']['total'] - blocks - interceptions
    except: tackles=0
    stat_params['tackles']=tackles
        
    try: duels_winrate=stat_params['duels won'] / stat_params['duels'] * 100
    except: duels_winrate='no duels made'
    stat_params['duels won %']=duels_winrate
        
    try: dribbles_succrate=stat_params['successful dribbles'] / stat_params['dribbles'] * 100 
    except: dribbles_succrate='no dribbles made'
    stat_params['successful dribbles %']=dribbles_succrate
    
    try: passes_accuracy=stat_params['accurate passes'] / stat_params['passes'] * 100
    except: passes_accuracy='did\'t make passes'
    stat_params['passing accuracy']=passes_accuracy
    
    print(stat_params)
    
    #updating all stats in the spreadsheet for the given player if necessary
    for param, value in stat_params.items():
        for player in list_of_players:
            for team in list_of_teams:
                if player['team']==team['team']:
                    player_team_id=team['team_id']
                    
                    #by this pint I have a list of players checked against the list of teams, and if the match is found, I create a variable for the team_id
                    #making sure I won't put the stats of Fred from Man Utd to Fred from Shakhtar
                    if player['name']==item[1] and player_team_id==item[0] and player['parameter']==param and player['value']!=value:   
                        cell_name=sheet_players.find(player['row_id']) #row_id as a unique identifier of a given player instance
                        sheet_players.update_cell(cell_name.row, cell_name.col-1, value) #updating the value cell
                        
                  
    


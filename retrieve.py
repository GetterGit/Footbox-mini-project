import http.client
import ssl
import json

def retrieve_stats(list_of_players):

    #avoiding the ssl check for now
    ssl._create_default_https_context = ssl._create_unverified_context

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "5c0baf453979bd8fb3a08f1c8786328d"
        }


    last_fixture_retrieved=list()
    
    for player_to_retrieve in list_of_players:

        conn.request("GET", f"/fixtures?season=2020&last=1&team={player_to_retrieve[1]}", headers=headers) #no need to use encode() to encode integer; f turns the url into an ACSII value
        last_fixture_response = conn.getresponse()
        last_fixture=json.load(last_fixture_response)
        last_fixture_id=last_fixture['response'][0]['fixture']['id']
    
        conn.request("GET", f"/fixtures/players?fixture={last_fixture_id}", headers=headers)
        last_fixture_players_response = conn.getresponse()
        last_fixture_players=json.load(last_fixture_players_response)
    
        for item in last_fixture_players['response']:
            for player in item['players']:
                if  player_to_retrieve[0] in player['player']['name']:
                    last_fixture_retrieved.append(tuple((item['team']['id'], player['player']['name'], player['statistics'])))
                    print(last_fixture_retrieved)
                    
    return last_fixture_retrieved #returns the list of tuples above

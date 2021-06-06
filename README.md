# Sota

### Footbox is a branch project to create an app for football scouts/analysts to track the last performance of players in their longlist and prioritise who to re-watch first. 

The frontend is made using Glide https://footbox.glideapp.io/ and the backend is Google Spreadsheet + python

The following top-level commands are written in python: 

1) Get recently added players and fetch their stats from https://www.api-football.com/ 
2) If a player instance already exists in the db added by another user - copy the stats to the new player instance
3) Update the last performance stats of players in the db when they finish their game 

retrieve.py - connects to the api and retrieves raw stats of required players
spreadsheet_parse.py - turns the raw data into structured stats and puts them into the database
spreadsheet_update.py - updates the database records at request

#!/usr/bin/env python
import argparse
import sys
import collections
import mysql.connector

def Initialize_Player(q3db, player):
    cursor = q3db.cursor()
    insert = "INSERT IGNORE INTO players (playername, kills, deaths, suicides, hand, machinegun, shotgun, grenade, rocket, railgun, lightning, plasma, bfg, matches) VALUES (\'"
    values = player + "\', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)"
    query = insert + values
    try:
        cursor.execute(query)
    except:
        print "Error adding ", player, " into DB"
    q3db.commit()

def Update_Player(q3db, player, field, value):
    cursor = q3db.cursor()
    query = "UPDATE players SET " + field + " = " + field + " + " + value + " WHERE playername = \'" + player + "\';" 
    print query
    cursor.execute(query)
    q3db.commit()

def main():
    
    # Parse commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='audit log to read from', required=True)

    args = parser.parse_args()

    # Try to open the file for reading first
    try:
        infile = open(args.file)
    except IOError:
        print "Error reading log file"

    # Output data file
    statsfile = "q3stats.dat"

    # MOD (Method of Death) dictionary
    MOD = {
        'MOD_BFG' : 'bfg',
        'MOD_BFG_SPLASH' : 'bfg',
        'MOD_CRUSH' : 'suicides',
        'MOD_FALLING' : 'suicides',
        'MOD_GRENADE' : 'grenade',
        'MOD_GRENADE_SPLASH' : 'grenade',
        'MOD_LAVA' : 'suicides',
        'MOD_LIGHTNING' : 'lightning',
        'MOD_MACHINEGUN' : 'machinegun',
        'MOD_PLASMA' : 'plasma',
        'MOD_PLASMA_SPLASH' : 'plasma',
        'MOD_RAILGUN' : 'railgun',
        'MOD_ROCKET' : 'rocket',
        'MOD_ROCKET_SPLASH' : 'rocket',
        'MOD_SHOTGUN' : 'shotgun',
        'MOD_TRIGGER_HURT' : 'suicides'
    }

    #
    # Database Connection Info
    # NOTE: table name has to be "players".  Use create_table.sql to create the table.
    #
    q3db = mysql.connector.connect(
    host="hostname",
    user="dbuser",
    passwd="dbpassword",
    database="dbname"
    )

    print(q3db)

    # Get list of existing players in DB
    existing_players = []
    cursor = q3db.cursor()
    query = "SELECT playername FROM players"
    cursor.execute(query)
    pldata = cursor.fetchall() 
    for index in range(len(pldata)):
        existing_players.append(pldata[index][0])
    print existing_players

    # Start parsing and counting
    playerlist = []

    for line in infile:
        fields = line.split()
        action = fields[1]
        if action.startswith('--'):
            value = ""
            info = ""
        elif action.startswith('Shutdown'):
            for player in playerlist:
                Update_Player(q3db, player, 'matches', '1')
            playerlist[:] = []
        elif action.startswith('InitGame'):
            initline = line.split('\\')
            mapname = initline[38]
            print "Processing map : ", mapname
        elif action.startswith('ClientUserinfoChanged'):
            playerid = int(fields[2])
            playerline = line.split('\\')
            playername = playerline[1]
            playerlist.insert(playerid,playername)
            if playername not in existing_players:
                print "Adding player ", playername
                Initialize_Player(q3db, playername)
            else:
                print "Existing player ", playername
        elif action.startswith('Kill'):
            killer = fields[5]
            victim = fields[7]
            method = MOD[fields[9]]
            if victim == killer:
                Update_Player(q3db, killer, method, '1')
                Update_Player(q3db, victim, 'suicides', '1')
            elif killer == '<world>':
                Update_Player(q3db, victim, 'suicides', '1')
            else:
                Update_Player(q3db, killer, 'kills', '1')
                Update_Player(q3db, killer, method, '1')
                Update_Player(q3db, victim, 'deaths', '1')
        else:
            value = fields[2:]
        
    print action, value, info
    
if __name__ == '__main__':
    sys.exit(main())

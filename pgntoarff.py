#Sam Duthie
#June 2017
#
#script that takes pgn file and
#outputs file suitable for data mining
#in either .arff or .csv format
#

import re

filename = "Hastings1972.pgn"
pgn = open("Hastings1972.pgn", "r")
tags=0
games=0
movelist = ""


for line in pgn:

    if ("[Event" in line):
        event = re.findall(r'"([^"]*)"', line)


    elif ("[Site" in line):
        site = re.findall(r'"([^"]*)"', line)

    elif ("[Date" in line):
        date = re.findall(r'"([^"]*)"', line)


    elif ("[Round" in line):
        round = re.findall(r'"([^"]*)"', line)


    elif ("[White " in line):
        w_player = re.findall(r'"([^"]*)"', line)


    elif ("[Black " in line):
        b_player = re.findall(r'"([^"]*)"', line)


    elif ("[Result" in line):
        result = re.findall(r'"([^"]*)"', line)


    elif ("[WhiteElo" in line):
        whiteelo = re.findall(r'"([^"]*)"', line)


    elif ("[BlackElo" in line):
        blackelo = re.findall(r'"([^"]*)"', line)


    elif ("[ECO" in line):
        eco = re.findall(r'"([^"]*)"', line)

    elif (line in ['\n', '\r\n']):
        if (tags==0):
            print(event, site, date, round, w_player, b_player, result, whiteelo, blackelo, eco)

            games = games + 1
       #     print("\n")
            tags = 1

        else: #end of single chess game
            tags = tags-1 #reset game
            print(movelist) #print off chess moves
            movelist = "" #reset chessmoves

    else:
        movelist = movelist + line


pgn.close()

print("no of games", games)



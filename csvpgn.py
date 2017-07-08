#csvpgn.py
#takes in pgn file from command line
#outputs csv file with:
#tagged [] metadata
#positional data from game
#UCI engine score data
#
#Sam Duthie 2017

'''
takes in pgn game.


FENstrings
runs pgn-extract for each fenstring and creates new pgn file for each structure
extracts each game from database an
'''

import re, sys
import pandas as pd
import numpy as np
import hashlib
from fnmatch import fnmatch, fnmatchcase

class Game():

    idno = 0
    event = ""
    site = ""
    date = ""
    roundno = ""
    whitePlayer = ""
    blackPlayer = ""
    result = ""
    whiteElo = ""
    blackElo = ""
    eco = ""
    movelist = ""
    totalMoves = 0
    fens = []
    fencheck = ""

       

fenlist = {

           }


try:
    filename = str(sys.argv[1])
    pgn = open(filename, "r")
except:
    print ("Either no file or incorrect file name")
    print ("python pgntoarff.py [filename]")
    sys.exit()
    

tags=0
games=0
gamelist = []
attributelist = [
                'idno',
                'Event', 
                'Site', 
                'Date', 
                'Round', 
                'WhitePlayer', 
                'BlackPlayer', 
                'Result', 
                'WhiteELO', 
                'BlackELO', 
                'ECO' 
                 ]


startNewGame = 0
game = Game()
resultFlag = False
fenFlag = False
tagFlag = False

for line in pgn:

    #check if start of game
    #check if end of game
    #check where to send data
    #send data to game object.

    #check tags to know where we are
    #if line starts with [ then set [ tag to 1
    #if line starts with newline then set newline tag to 1
    #if line starts with move then set movelist tag to 1
    #if line contains result then set result tag to 1
    if ("[" in line):
        tagFlag = True
    elif (line in ['\n', '\r\n']):
        newlineFlag = True
    if (" 1-0" in line) or  (" 0-1" in line) or (" 1/2-1/2" in line):
        resultFlag = True
    if ("{" in line) or ("}" in line):
        fenFlag = True
        

    if (tagFlag):
        if ("[Event" in line):
            game.event = re.findall(r'"([^"]*)"', line)
        if ("[Site" in line):
            game.site = re.findall(r'"([^"]*)"', line)
        if ("[Date" in line):
            game.date = re.findall(r'"([^"]*)"', line)
        if ("[Round" in line):
            game.roundno = re.findall(r'"([^"]*)"', line)
        if ("[White " in line):
            game.whitePlayer = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Black " in line):
            game.blackPlayer = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Result" in line):
            tmp = re.findall(r'"([^"]*)"', line)
            if ("1-0" in tmp): game.result = 1
            elif ("0-1" in tmp): game.result = -1
            else: game.result = 0
        if ("[WhiteElo" in line):
            game.whiteElo = ''.join(re.findall(r'"([^"]*)"', line))
        if ("[BlackElo" in line):
             game.blackElo = ''.join(re.findall(r'"([^"]*)"', line))
        if ("[ECO" in line):
            game.eco = re.findall(r'"([^"]*)"', line)
        tagFlag = False
    else:
        game.movelist+=str(line)
        
    if(fenFlag): #add all fen positions to game
        game.fens.append(re.findall(r"\{([^}]+)\}", line))
                

    if (resultFlag is True):   #add game to list and reset

        #check for missing data first
        if (game.event == "") | (game.event == " " ): game.event="?"
        if (game.site == "") | (game.site == " "): game.site="?"
        if (game.date == ""): game.date=="?"
        if (game.roundno == ""): game.roundno="?"
        if (game.whitePlayer == ""): game.whitePlayer="?"
        if (game.blackPlayer == ""): game.blackPlayer="?"
        if (game.result == ""): game.result="?"
        if (game.whiteElo == "") | (game.whiteElo == " "): game.whiteElo="?"
        if (game.blackElo == "") | (game.blackElo == " "): game.blackElo="?"
        if (game.eco == ""): game.eco="?"
        if (game.totalMoves == ""): game.totalMoves="?"
        
        s = game.event[0], game.site[0], game.date[0], game.roundno[0], game.whitePlayer, game.blackPlayer, str(game.result),  game.whiteElo, game.blackElo, game.eco[0], game.fencheck, #game.movelist
        game.idno = abs(hash(s)) % (10 ** 8)
            
        gamelist.append(game)
        game = Game()
       # sys.stdout.write("Parsing games: " + str(len(gamelist)) + "\r" )
       # sys.stdout.flush()

                
        resultFlag = False
    
    #readnextline

#///pgn file finished///
for game in gamelist:   #check required fen positions against game movelists
    for fen in fenlist:
        print (fen)
        if fnmatch(game.movelist, fen):
            game.fencheck+="1,"
        else:
            game.fencheck+="0,"


#//output//
#print ("%dataset compiled by pgntoarff.py")
#print ("%", len(gamelist), "games in dataset")
#print ("\n")
#print ("@relation", filename)
#print ("\n")
attributes = ""
for attribute in attributelist:
    attributes += attribute + ", "
print (attributes)

for game in gamelist:
    str_list = str(game.idno), game.event[0], game.site[0], game.date[0], game.roundno[0], game.whitePlayer, game.blackPlayer, str(game.result),  game.whiteElo, game.blackElo, game.eco[0], game.fencheck, #game.movelist
    print (', '.join(str_list))
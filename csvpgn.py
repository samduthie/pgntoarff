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

to add:
- castling positions
- UCI scores
'''

import re, sys
#import pandas as pd
#import numpy as np
import hashlib
import subprocess
#from fnmatch import fnmatch, fnmatchcase

class Game():

    idno = 0
    event = "?"
    site = "?"
    date = "?"
    roundno = "?"
    whitePlayer = "?"
    blackPlayer = "?"
    result = "?"
    whiteElo = "?"
    blackElo = "?"
    eco = "?"
    movelist = "?"
    totalMoves = 0
    fens = []
    fencheck = ""
    fenbinary = ""

'''
? - match any square. The square may be occupied or unoccupied.
! - match any occupied square. The square may be occupied by a piece of any type and colour.
A - match a single White piece.
a - match a single Black piece.
* - match zero or more squares, occupied or unoccupied.
[xyz] - match any of xyz, where xyz represents any of the English piece-letter names (KQRNBPkqrnbp) and is case-sensitive. In addition, 'A' and 'a' (as defined above) are available. For instance: [Qq] matches either a White or Black queen; [BbNn] matches any White or Black bishop or knight; [Ar] matches any White piece or a Black rook.
[^xyz] If the first character inside the square brackets is '^' then the match is inverted; i.e., match any piece that is not listed. For instance, [^BbNn] matches any piece that is not a White or Black bishop or knight.

'''
       

fenlist = {
          # 'FENPattern "*/*/*/*/*/*/*/*/*"',
            'FENPattern "*/*/*/*/*/*/*r*r*/*"', #white rooks on the 7th
            'FENPattern "*/*R*R*/*/*/*/*/*/*"', #black rooks on the 7th
            
            'FENPattern "*/*/*/??pnp???/*/??N???P?/*/*"', #Caro
            'FENPattern "*/pp???ppp/????p???/???p????/*/??P?P???/PP???PPP/*"', #Slav
           }



  
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
                'ECO', 
                
                'WhiteRooks7th',
                'BlackRooks7th',
                'Caro',
                'Slav',
                 ]


try:
    filename = str(sys.argv[1])
except:
    print ("Either no file or incorrect file name")
    print ("python pgntoarff.py [filename]")
    sys.exit()


def getGames(file):
    tags=0
    games=0
    gamelist = []
    try:
        pgn = open(file, "r", encoding='latin-1')
    except:
        print ("Either no file or incorrect file name")
        print ("python pgntoarff.py [filename]")
        sys.exit()
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
        if ("1-0" in line) or  ("0-1" in line) or ("1/2-1/2" in line):
            resultFlag = True #resets late if it is the result metadata.
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
                resultFlag = False
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
            #sys.stdout.write("Parsing games: " + str(len(gamelist)) + "\r" )
            #sys.stdout.flush()

                    
            resultFlag = False
           
                
        #readnextline
   
    return gamelist
    
main_database = getGames(filename)



#///pgn file finished///
#fen checker
#first we create a file with one fen in for pgn-extract
path = 'tmpfenfile.txt'
TMPDB = 'tmppgnfile.pgn'
while len(fenlist) > 0:
    fen = fenlist.pop()
    writeFile = open(path,'a')
    writeFile.write(fen)
    writeFile.close()
    
    
    
    
    subprocess.call(['pgn-extract', filename, '-t' + path, "-o", TMPDB, '--quiet'])
    
    fen_database = getGames(TMPDB)
   
    
    for game in main_database:
            if len(fen_database) > 0:
                if game.idno == fen_database[0].idno:

                    game.fenbinary+='1, '
                    fen_database.pop(0)
                else:
                    game.fenbinary+='0, '
            else:
                game.fenbinary+='0, '
    
    #remove temporary files
    subprocess.call(['rm', path])
    subprocess.call(['rm', TMPDB])



#//output//
#csv file commenting ?
#print ("%dataset compiled by pgntoarff.py")
#print ("%", len(gamelist), "games in dataset")
#print ("\n")
#print ("@relation", filename)
#print ("\n")

print(', '.join(attributelist))
#print(len(gamelist), "games processed")

for game in main_database:
    str_list = str(game.idno), game.event[0], game.site[0], game.date[0], game.roundno[0], game.whitePlayer, game.blackPlayer, str(game.result),  game.whiteElo, game.blackElo, game.eco[0], game.fenbinary, #game.movelist
    print (', '.join(str_list))

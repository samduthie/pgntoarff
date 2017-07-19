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
    
    black_kingside_castle = 0
    white_kingside_castle = 0
    black_queenside_castle = 0
    white_queenside_castle = 0

'''
? - match any square. The square may be occupied or unoccupied.
! - match any occupied square. The square may be occupied by a piece of any type and colour.
A - match a single White piece.
a - match a single Black piece.
* - match zero or more squares, occupied or unoccupied.
[xyz] - match any of xyz, where xyz represents any of the English piece-letter names (KQRNBPkqrnbp) and is case-sensitive. In addition, 'A' and 'a' (as defined above) are available. For instance: [Qq] matches either a White or Black queen; [BbNn] matches any White or Black bishop or knight; [Ar] matches any White piece or a Black rook.
[^xyz] If the first character inside the square brackets is '^' then the match is inverted; i.e., match any piece that is not listed. For instance, [^BbNn] matches any piece that is not a White or Black bishop or knight.

'''
       

fenlist = [
            'FENPattern "*/*R*R*/*/*/*/*/*/*"', #white rooks on the 7th
            'FENPattern "*/*/*/*/*/*/*r*r*/*"', #black rooks on the 7th
            
            'FENPattern "*/ppp2ppp/*/3p4/*/2P1P3/*/*"', #Caro
            'FENPattern "*/*/*/??pnp???/*/??N???P?/*/*"', #Maroczy Bind
            'FENPattern "*/pp???ppp/????p???/???p????/*/??P?P???/PP???PPP/*"', #Slav
           ]



  
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
                
                'White_Kingside_Castled',
                'Black_Kingside_Castled',
                'White_Queenside_Castled',
                'Black_Queenside_Castled',
                
                
                'WhiteRooks7th',
                'BlackRooks7th',
                'Caro',
                'Maroczy',
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
    gameno=0
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
    newlineflag = False
    finished = False
    newline = 0
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
        if ("1-0" in line) or  ("0-1" in line) or ("1/2-1/2" in line):
            resultFlag = True #resets late if it is the result metadata.
        if ("{" in line) or ("}" in line):
            fenFlag = True
        if (newlineflag):
             if (line.strip() == ''):
                finished = True
                newline+=1
                newlineflag = False
        elif (line.strip() == ''):
            newlineflag = True
            
            
        if ("[Event " in line):
            game.event = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Site " in line):
            game.site = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Date " in line):
            game.date = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Round " in line):
            game.roundno = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[White " in line):
            game.whitePlayer = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Black " in line):
            game.blackPlayer = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[Result " in line):
            resultFlag = False
            tmp = re.findall(r'"([^"]*)"', line)
            if ("1-0" in tmp): game.result = 1
            elif ("0-1" in tmp): game.result = -1
            else: game.result = 0
        if ("[WhiteElo " in line):
            game.whiteElo = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[BlackElo " in line):
            game.blackElo = ''.join(re.findall(r'"([^"]*)"', line)).replace(",", "")
        if ("[ECO " in line):
            game.eco = re.findall(r'"([^"]*)"', line)
        
        
        if (" O-O-O " in line):
            game.black_queenside_castle = "1"
        if (".O-O-O " in line):
             game.white_queenside_castle = "1"
        if (" O-O " in line):
            game.black_kingside_castle = "1"
        if (".O-O" in line):
            game.white_kingside_castle = "1"
           
            
      #  if(fenFlag): #add all fen positions to game
      #      game.fens.append(re.findall(r"\{([^}]+)\}", line))
                    
    
        if (finished is True):   #add game to list and reset
            '''
            There is a bug here. If a game does not have a result tag it will not process properly. Which means that the number of games will not be correct. Which means that the results will not format properly. The data will come out and look fine but will be wrong.
            '''
    
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
            
            
            s = game.date, game.roundno, game.whitePlayer, game.blackPlayer, str(game.result),  game.whiteElo, game.blackElo, game.eco[0], game.fenbinary
            game.idno = abs(hash(s)) % (10 ** 8)
            
            
            gameno+=1
                
            gamelist.append(game)
            game = Game()
            #sys.stdout.write("Parsing games: " + str(len(gamelist)) + "\r" )
            #sys.stdout.flush()

                    
            finished = False
            
           
                
        #readnextline
  
    return gamelist
    
    
main_database = getGames(filename)




#///pgn file finished///
#fen checker
#first we create a file with one fen in for pgn-extract
path = 'tmpfenfile.txt'
TMPDB = 'tmppgnfile.pgn'
while len(fenlist) > 0:
    fen = fenlist.pop(0)
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
    
 #   remove temporary files
    subprocess.call(['rm', path])
    subprocess.call(['rm', TMPDB])


#//output//
#csv file commenting ?
#print ("%dataset compiled by csv.py")
#print ("%", len(gamelist), "games in dataset")
#print ("\n")
#print ("@relation", filename)
#print ("\n")

print(','.join(attributelist))
#print(len(gamelist), "games processed")

for game in main_database:
    str_list = str(game.idno), game.event, game.site, game.date, game.roundno, game.whitePlayer, game.blackPlayer, str(game.result), game.whiteElo, game.blackElo, game.eco[0], str(game.white_kingside_castle), str(game.white_queenside_castle), str(game.black_kingside_castle), str(game.black_queenside_castle), game.fenbinary, #game.movelist
    print (','.join(str_list))

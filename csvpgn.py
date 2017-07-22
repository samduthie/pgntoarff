'''
csvpgn.py
Sam Duthie 2017

takes in pgn file from command line
example:

$ python csvpgn.py sample.pgn

outputs csv file with:
tagged metadata and positional data from game

takes in pgn game.


FENstrings
runs pgn-extract for each fenstring and creates new pgn file for each structure
extracts each game from database an

to add:
- castling positions
- UCI scores
'''

import re, sys
import hashlib
import subprocess

'''
Game class is a container for each chess game. Each game in a pgn file will be appended to a list - the gamelist
Most variables inside the game are tagged metadata.
fenbinary is a string of binary values from the #FEN data.
'''
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
List of fens that are used by pgn-extract to match against each game.
If a fen pattern is inserted into here it must also be added to the attributelist

Positions taken from https://en.wikipedia.org/wiki/Pawn_structure
'''
fenlist = [
            'FENPattern "*/*R*R*/*/*/*/*/*/*"', #white rooks on the 7th
            'FENPattern "*/*/*/*/*/*/*r*r*/*"', #black rooks on the 7th
            
            'FENPattern "*/pp???ppp/??p?p???/*/???P????/*/PPP??PPP/*"', #Caro
            'FENPattern "*/pp??pppp/???p????/*/??P?P???/*/PP???PPP/*"', #Maroczy Bind
            'FENPattern "*/pp???ppp/??p?p???/*/???P????/????P???/PP???PPP/*"', #Slav
            'FENPattern "*/pp2pp1p/3p2p1/*/5P3/*/PPP2PPP/*"', #EmptyDragon
            
            'FENPattern "*/pp??pp?p/???p??p?/*/????P???/*/PPP??PPP/*"', #dragon
            'FENPattern "*/pp???ppp/???pp???/*/????P???/*/PPP??PPP/*"', #Scheveningen
            'FENPattern "*/?????PPP/PP?PP???/*/??p?p???/*/pp???ppp/*"', #hedgehog
            'FENPattern "*/pp???ppp/???p????/????p???/????P???/*/PPP??PPP/*"', #Sicilian – Boleslavsky hole
            'FENPattern "*/ppp??ppp/???p????/???Pp???/????P???/*/PPP??PP/*"', #d5 chain
            'FENPattern "*/ppp??ppp/????p???/???pP???/???P????/*/PPP??PPP/*"', #e5 chain
            'FENPattern "*/pp???ppp/??p?????/?????p???/??P?P???/*/PP???PPP/* "', #Rauzer formation
            'FENPattern "*/pp???ppp/??pp????/*/??P?P???/*/pp???ppp/*"', #Boleslavsky Wall
            'FENPattern "*/pp???ppp/????pppp/*/???P????/*/PP???PPP/*"', #Queen's Gambit – Isolani
            'FENPattern "*/pp???ppp/??p?????/???p????/???P????/?????p???/pp???ppp/*"', #Queen's Gambit – Orthodox exhchange
            'FENPattern "*/pp???ppp/????p???/*/??PP????/*/P????PPP/*"', #Queen's Gambit –  hanging pawns
            'FENPattern "*/ppp???pp/????p???/???p?p??/???P?P??/????P???/PPP???PP/*"', #Stonewall formation
            'FENPattern "*/pp??pppp/???p????/??p?????/????P???/???P????/PPP??PPP/*"', #Closed Sicilian formation
            
           
       
           
           
            
           ]

'''
List of attributes that are output at the top of the CSV file.
If attributes are changed they must also be changed in final print logic block.
'''
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
                'empty_Dragon',
                'Dragon',
                'Scheveningen',
                'hedgehog',
                'Sicilian_Boleslavsky_hole',
                'd5_chain',
                'e5_chain',
                'Rauzer_formation',
                'Boleslavsky_Wall',
                'Queens_Gambit_Isolani',
                'Queens_Gambit_Orthodox_exhchange',
                'Panov_formation',
                'Queens_Gambit_Hanging_Pawns',
                'Stonewall',
                'closed_sicilian',
                
                 ]


def getGames(file):
    '''
    takes in a pgn file name, opens that file and reads it into memory. 
    returns a list of game objects.
    
    file - a full pgn file (e.g. sample.ogn)
    
    '''
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
    '''
    Follow logic block searches each line in a pgn file to find desired tagged metadata, fen matches and other data such as castling rights
    Will fill in missing data with '?'
    '''
    for line in pgn:
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
        if (". O-O-O " in line):
             game.white_queenside_castle = "1"
        if (" O-O " in line):
            game.black_kingside_castle = "1"
        if (". O-O " in line):
            game.white_kingside_castle = "1"
           
    
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
              
            
            '''
            hashed string for idno, this is used to match games in smaller databases for fen matching purposes
            '''
            s = game.date, game.roundno, game.whitePlayer, game.blackPlayer, str(game.result),  game.whiteElo, game.blackElo, game.eco[0], game.fenbinary
            game.idno = abs(hash(s)) % (10 ** 8)
            
            '''
            gameno is increased and game is appended into the gamelist.
            Upon the last game the whole list will be returned
            '''
            gameno+=1
            gamelist.append(game)
            game = Game()
            finished = False
            
           
  
    return gamelist

'''
open the file in the command line argument
'''
try:
    filename = str(sys.argv[1])
except:
    print ("Either no file or incorrect file name")
    print ("python pgntoarff.py [filename]")
    sys.exit()
    
main_database = getGames(filename)

'''
pgn file finished parsing.

fen checker
first we create a file with one fen in it for pgn-extract to parse through
pgn-extract will create a smaller pgn database for that fen.
we then call getGames on the new database and load it into memory
finally, every game in the new database will be matched against the main database, 
games that included matched fens will have their fenbinary string appended to reflect this
'''

path = 'tmpfenfile.txt'
TMPDB = 'tmppgnfile.pgn'
while len(fenlist) > 0:
    fen = fenlist.pop(0)
    writeFile = open(path,'a')
    writeFile.write(fen)
    writeFile.close()

    subprocess.call(['pgn-extract', filename, '-t' + path, "-o", TMPDB, '--fixresulttags', '--quiet', '--nobadresults'])
    
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

'''
output all data in csv format onto command line.
'''
print(','.join(attributelist))
for game in main_database:
    str_list = str(game.idno), game.event, game.site, game.date, game.roundno, game.whitePlayer, game.blackPlayer, str(game.result), game.whiteElo, game.blackElo, game.eco[0], str(game.white_kingside_castle), str(game.black_kingside_castle), str(game.white_queenside_castle), str(game.black_queenside_castle), game.fenbinary, #game.movelist
    print (','.join(str_list))

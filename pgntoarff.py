#Sam Duthie
#June 2017
#
#script that takes pgn file and
#outputs file suitable for data mining
#in either .arff or .csv format
#
#TODO:
#
#FEN strings need to be more malleable
#Use dictionary
#load fenlist from file?
#error handling and better arguments
#

import re, sys
class Game():

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
    'rnbqkbnr/*/*/*/*/*/*/RNBQKBNR' : 'starting position',
    'r1bq1rk1/ppp1pp1p/2n2bp1/8/Q1pP4/2N1P3/PP3PPP/R3KBNR' : 'test',
    'r1bq1rk1/ppp1pp1p/2n2bp1/8/Q1pP4/2N1P3/PP3PPP/R3KBNR' : 'rook on 7th',
    'r1bq1rk1/ppp1pp1p/2n2bp1/8/Q1pP4/2N1P3/PP3PPP/R3KBNR' : 'maroczy bind'
           }


try:
    filename = str(sys.argv[1])
    pgn = open(filename, "r")
except:
    print "Either no file or incorrect file name"
    print "python pgntoarff.py [filename]"
    sys.exit()
    

tags=0
games=0
gamelist = []
attributelist = ['Event string', 'Site string', 'Date string', 'Round numeric', 'WhitePlayer string', 'BlackPlayer string', 'Result {1, 0, -1}', 'WhiteELO numeric', 'BlackELO numeric', 'Date string', 'ECO string']

#attributeTable = {'Event': 'string', 'Site': 'string', 'Date': 'string', 'Round': 'numeric', 'WhitePlayer': 'string', 'BlackPlayer': 'string', 'Result': 'numeric', 'WhiteELO': 'numeric', 'BlackELO': 'numeric', 'Date': 'string', 'ECO': 'string' }
        #Would like to use a dictionary here but I need it to return in correct order.

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
            game.whitePlayer = re.findall(r'"([^"]*)"', line)
        if ("[Black " in line):
            game.blackPlayer = re.findall(r'"([^"]*)"', line)
        if ("[Result" in line):
            tmp = re.findall(r'"([^"]*)"', line)
            if ("1-0" in tmp): game.result = 1
            elif ("0-1" in tmp): game.result = -1
            else: game.result = 0
        if ("[WhiteElo" in line):
            game.whiteElo = re.findall(r'"([^"]*)"', line)
        if ("[BlackElo" in line):
            game.blackElo = re.findall(r'"([^"]*)"', line)
        if ("[ECO" in line):
            game.eco = re.findall(r'"([^"]*)"', line)
        tagFlag = False
    else:
        game.movelist+=str(line)
        
    if(fenFlag): #add all fen positions to game
        game.fens.append(re.findall(r"\{([^}]+)\}", line))
                

    if (resultFlag is True):   #add game to list and reset

        #check for missing data first
        if (game.event == ""): game.event="?"
        if (game.site == ""): game.site="?"
        if (game.date == ""): game.date="?"
        if (game.roundno == ""): game.roundno="?"
        if (game.whitePlayer == ""): game.whitePlayer="?"
        if (game.blackPlayer == ""): game.blackPlayer="?"
        if (game.result == ""): game.result="?"
        if (game.whiteElo == ""): game.whiteElo="?"
        if (game.blackElo == ""): game.blackElo="?"
        if (game.eco == ""): game.eco="?"
        if (game.totalMoves == ""): game.totalMoves="?"
     
            
        gamelist.append(game)
        game = Game()
       # sys.stdout.write("Parsing games: " + str(len(gamelist)) + "\r" )
       # sys.stdout.flush()

                
        resultFlag = False
    
    #readnextline

#///pgn file finished///
for game in gamelist:   #check required fen positions against game movelists
    for fen in fenlist:
        if (fen in game.movelist):
            game.fencheck+="1,"
        else:
            game.fencheck+="0,"


#//output//
print "%dataset compiled by pgntoarff.py"
print "%", len(gamelist), "games in dataset"
print ("\n")
print "@relation", filename
print ("\n")

for attribute in attributelist:
    print "@attribute", attribute

print ("\n")
print ("@data")
for game in gamelist:
    str_list = game.event[0], game.site[0], str(game.result), game.date[0], game.roundno[0], game.whitePlayer[0], game.blackPlayer[0], game.whiteElo[0], game.blackElo[0], game.eco[0], game.fencheck
    print ', '.join(str_list)



    


pgn.close()



    


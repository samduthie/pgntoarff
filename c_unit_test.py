    #castle finder unit test
    #castle finder unit test
   
        print ("starting....")
        file = "tmppgn.pgn"
        try:
            pgn = open(file, "r", encoding='latin-1')
        except:
            print ("Either no file or incorrect file name")
            print ("python pgntoarff.py [filename]")
            sys.exit()
     
        finished = False
        newlineflag = False
        newline = 0
        b = 0
        w = 0
        bk=0
        bq=0
        tbq=0
        tbk=0
        twk=0
        twq=0
        error=0
    
        ngame=0
       
        for line in pgn:
            if (newlineflag):
                 if (line.strip() == ''):
                    finished = True
                    newline+=1
                    newlineflag = False
            elif (line.strip() == ''):
                newlineflag = True
            
            
            
    
            if(re.findall(r'O-O-O\s[0-9]', line)): #black queenside
                 b=b+1; bq=bq+1
                 tbq = tbq+1
            if(re.findall(r'[0-9].\sO-O-O', line)): #white queenside
                 w=w+1
                 twq = twq+1
            if(re.findall(r'\sO-O\s[0-9]', line)): #black kingside
                 b=b+1; bk=bk+1
                 tbk = tbk+1
            if(re.findall(r'[0-9].\sO-O\s', line)): #white kingside
                 twk = twk+1
                 w=w+1
                
          
               
        
            if (finished is True):   #add game to list and reset
                
                if (b>1):
                    print ("black castled twice", ngame, bq, bk)
                    error = error+1
                if (w>1):
                    print ("white castled twice", ngame, bq, bk)
                    error = error+1
                
                finished = False
                b=0
                w=0
                bq=0
                bk=0
            
                ngame = ngame + 1
        print ("all done", ngame, error)
        print ("%s")
        print ("white q:", 100/ngame*twq)
        print ("white k:", 100/ngame*twk, twk)
        print ("white didnt castle", 100/ngame*(ngame-twq-twk))
        print ("black q:", 100/ngame*tbq)
        print ("black k:", 100/ngame*tbk)
        print ("black didnt castle", 100/ngame*(ngame-tbq-tbk))
               
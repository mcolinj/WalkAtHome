# importing csv module
import numpy as np
import csv 
import statistics

def sanitize(element):
    pad_to = '00000'
    if element.strip() == '':
        return pad_to
    else:
        return element.zfill(len(pad_to))
    
class Steps:
    
    def __init__(self, samples=40, filename = "RPD-WalkAtHome-20200507.csv", sanitize_fn=sanitize):
        
        self.data = {}
        self.geo = {}
  
        # initializing the titles and rows list 
        self.fields = [] 
        self.rows = []
  
        # reading csv file 
        with open(filename, 'r') as csvfile: 
            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 

            # extracting each data row one by one 
            rownum = 0
            for row in csvreader: 
                if rownum == 0:
                    self.headings = row
                else:
                    key = row[1].strip().split(' ')[0]
                    self.geo[key] = row[0]
                    self.data[key] = [sanitize_fn(r) for r in row[2:samples+1]]
                rownum+=1    
    
    def __getattr__(self, attr):
        data = [int(s) for s in self.dat(attr)]    
        accum = [sum(data[0:i]) for i,_ in enumerate(data)]
        print("{}: Grand total = {}".format(attr, accum[-1]))
        return accum

    def parts(self):
        return [name[0:2] for name in self.data.keys()]

    def dat(self, tln):
        matches = [name for name in self.data.keys() if name[0:2] == tln]
        if len(matches) == 0:
            print("{} not found".format(tln), file=stderr)
        elif len(matches) != 1:
            print("{} is ambiguous, could be any of: {}".format(tln, matches), file=stderr)
            return None
        else:
            return self.data[matches[0]]
        
    def bingo(self, tln):
        ordinal = [ "th", "st", "nd", "rd", "th" ]
        sdat = self.dat(tln)
        calls = []
        if sdat is None:
            print("Please try again", file=stderr)
        else:
            # all have been padded the same way, so the first element tells length
            for idx in range(len(sdat[0])):
                calls.append([dsteps[idx] for dsteps in sdat])
            
            # now we have len() sets of calls.   We can evaluate each set of calls
            for idx,call in enumerate(calls):
                # fill out a card
                card = {}
                for ch in call:
                    card[ch]=1
                    
                # Now check for a full card
                markcount = len(card.keys())
                if markcount == 10 and idx == 1:
                    print("{} has a {}{} order BINGO!".format(tln, idx, ordinal[idx]))
                    #print("Card is: {}".format(card))
                    #call.sort()
                    #print("Calls for card {}: {}".format(idx,call))
                elif markcount > 7:
                    print("{} has only {} completed entries in card {}".format(tln, markcount, idx))
            
            
            

                
              
                                  
                                
       
    

        
                
# importing csv module
import numpy as np
import csv 
import six

def sanitize(element):
   pad_to = '00000'
   if element.strip() == '':
       return pad_to
   else:
       return element.zfill(len(pad_to))

class Steps:

   def __init__(self, samples=19, filename = "RPD-WalkAtHome-20200415.csv", sanitize_fn=sanitize):

       self.data = {}

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
                   self.data[row[0].strip().split(' ')[0]] = [sanitize_fn(r) for r in row[1:samples+2]]
               rownum+=1    

   def __getattr__(self, attr):
       data = [int(s) for s in self.dat(attr)]    
       accum = [sum(data[0:i]) for i,_ in enumerate(data)]
       six.print_("{}: Grand total = {}".format(attr, accum[-1]))
       return accum

   def parts(self):
       return [name[0:2] for name in self.data.keys()]

   def dat(self, tln):
       matches = [name for name in self.data.keys() if name[0:2] == tln]
       if len(matches) == 0:
           six.print_("{} not found".format(tln), file=stderr)
       elif len(matches) != 1:
           six.print_("{} is ambiguous, could be any of: {}".format(tln, matches), file=stderr)
           return None
       else:
           return self.data[matches[0]]

   def bingo(self, tln):
       ordinal = [ "th", "st", "nd", "rd", "th" ]
       sdat = self.dat(tln)
       calls = []
       if sdat is None:
           six.print_("Please try again", file=stderr)
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
               if markcount == 10:
                   six.print_("{} has a {}{} order BINGO!".format(tln, idx, ordinal[idx]))
                   #print("Card is: {}".format(card))
                   #call.sort()
                   six.print_("Calls for card {}: {}".format(idx,call))
               elif markcount > 7:
                   six.print_("{} has only {} completed entries in card {}".format(tln, markcount, idx))



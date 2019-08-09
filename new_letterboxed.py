import os
import itertools


about = """

             LETTER BOXED SOLVER
         by Anthony Curtis Adler 2019

    
     
     LETTER BOXED SOLVER FINDS A TWO-WORD SOLUTION
          TO THE 'LETTER BOXED'
     PUZZLE in THE NEW YORK TIMES.

          I'VE INCLUDED words.txt from:
      https://github.com/dwyl/english-words.

     THIS, HOWEVER, INCLUDES MANY
     WORDS THAT WILL NOT BE ACCEPTED
     BY THE NEW TIMES PUZZLE ENGINE.
     
     OTHER WORDS CAN BE USED. \n\n\n"""

print(about)

def all_subsets (enter_set):
     # returns all the subsets of a given set 

     return_set = set()
     for a in range(1,len(enter_set)+1):
          return_set.update(itertools.combinations(enter_set,a))
     return return_set

def strings_from_set (enter_set):
     # returns a set of strings for a given set 
     return {''.join(sorted(x)) for x in enter_set}

def string (word):
     # returns the letters, sorted and without repetition, for a given word 
     return ''.join(sorted(set(word)))



class WordEvaluator:

     def __init__ (self):

          # initiates the evaluator by inputing a description of the puzzle 

          self.sides = {}

          while True:
               try:
                    self.number_of_sides = int(input('HOW MANY SIDES DOES THE LETTER BOXED HAVE?'))
                    print()
                    break
               except:
                    print('VALUES MUST BE INTEGERS!')

          self.all_letters = ''
          for side in range(0,self.number_of_sides):
               x = input('WHAT ARE THE LETTERS FOR SIDE '+str(side+1)+'?')
               self.sides[side] = x
               self.all_letters += x
          print('THE TOTAL NUMBER OF LETTERS ARE '+str(len(self.all_letters)))
          print('LETTERS: '+self.all_letters)


     def is_valid(self,word):
          # tests whether a word is a valid for the given puzzle 

          if not word.isalpha():
               return False

          if set(word) - set(self.all_letters):
               # return false is there are letters not included in the puzzle 
               return False 

          for side in range(0,self.number_of_sides):
               #replaces the letters with numbers corresponding to the four sides 
               for x in self.sides[side]:
                    word=word.replace(x,str(side))
          # test if the word has two adjacent letters belonging to the same side 
          for side in range(0,self.number_of_sides):
               if str(side)*2 in word:
                    return False
          return True

     
     


filename = 'scrabblewords.txt'
# GET TEXT FILE 
while True:
     print('GETTING TEXT FILE!')
     try:
          textfile = open(filename,'r', encoding='utf-8')
          textfile=textfile.read()
          print(filename+' OPENED! \n')
          break
     except:
          print(textfile+' NOT FOUND\n')
          print('ENTER NEW WORD FILE!')
          filename= input('textfile')


# FIND THE CHARACTER DIVIDING THE WORDS
for x in textfile:
     if x not in 'abcdefghijklomnopqrstuvwxyz0123456789':
          split = x
          break

words = textfile.split(x)
print('NUMBER OF WORDS: '+str(len(words)))

starts_with = {} # keeps track of the substrings for a given wordstring
word_dict = {} # keeps track of the word that corresponds to the longest wordstring that it contains 
fragments = {} # allows retrieval of the longest wordstring corresponding to a given fragment
all_words = [] # 
print()



evaluator = WordEvaluator()


for letter in evaluator.all_letters:
     # create sub-dictionaries for each letter in the puzzle 
     starts_with[letter] = {} 
     word_dict[letter] = {}
     fragments[letter] = {}

# find all the valid words 

words = reversed(sorted(words,key=lambda x:len(x)))
     # order the wordlist so that the longest words come first 

for word in words:

     if evaluator.is_valid(word):

          strings = strings_from_set(set(word)) # all the substrings 
          word_string = string(word) # find the string representation,
                                     

          if word_string not in starts_with[word[0]]:
               # exclude words that are already subsumed in words that have already been found
               
               all_words.append((word,word_string))
               word_dict[word[0]][word_string] = word
               for ws_temp in strings_from_set(all_subsets(set(word_string))):
                    starts_with[word[0]][word_string] = ws_temp
                    fragments[word[0]][ws_temp] = word_string

               
all_words = sorted(all_words, key=lambda x: len(evaluator.all_letters)-len(x[1]))
     # sort all the words that have been found by decreasing length 

for word in all_words:
     # go through the list of words, and stop at the first for which there exists a two-word solution 

     first_word = word[0]
     remainder = ''.join(sorted(set(evaluator.all_letters) - set(first_word)))

     if remainder in fragments[first_word[-1]]:
          second_word = word_dict[first_word[-1]][fragments[first_word[-1]][remainder]]
          break

print(first_word+'/'+second_word)
input('?')

               



import random
import string
import subprocess

class Scrabble:

    LOWER = 1
    UPPER = 2
    TILES = "AAAAAAAAABBCCDDDDEEEEEEEEEEEEFFGGGHHIIIIIIIIIJKLLLLMMNNNNNNOOOOOOOOPPQRRRRRRSSSSTTTTTTUUUUVVWWXYYZ.."
    TILE_VALUES = { "a" : 1,   "b" :  3,   "c" :  3,   "d" : 2,   "e" :  1,   "f" : 4,   "g" : 2,
                    "h" : 4,   "i" :  1,   "j" :  8,   "k" : 5,   "l" :  1,   "m" : 3,   "n" : 1,
                    "o" : 1,   "p" :  3,   "q" : 10,   "r" : 1,   "s" :  1,   "t" : 1,   "u" : 1,
                    "v" : 4,   "w" :  4,   "x" :  8,   "y" : 4,   "z" : 10,   "." : 0 }
    
    def __init__(self, seed, dictionary_file = "/usr/share/dict/words", letter_case = LOWER):
        """
        Create a scrambled deck of scrabble tiles using the specified
        random seed and case (default is LOWER)
        """
        self.dictionary_file = dictionary_file
        self.letter_case = letter_case
        
        rnd = random.Random(seed)
        if letter_case == self.LOWER:
            self.tiles = rnd.sample(self.TILES.lower(),len(self.TILES))
        else:
            self.tiles = rnd.sample(self.TILES,len(self.TILES))

    def isaword(self, word):
        cmd = """egrep "^{}$" {}""".format(word, self.dictionary_file)
        try:
            found_word = subprocess.check_output(cmd, shell=True)
            return found_word.decode("utf-8")
        except:
            return None
        
    def tile_by_index(self, index):
        """
        Return the INDEXth tile from the scrambled tile collection
        in this game.
        """
        return self.tiles[index]
        
    def score(self, word):
        """
        This assumes that the argument is a word and returns the score using
        the standard values for tiles (wildcard tile is 0).
        Assumes the word is lowercase (so requires no conversion to
        compute the score.)
        """
        return sum(self.TILE_VALUES[letter] for letter in word)

if __name__ == "__main__":
    """
    Unit test.
    """
    game = Scrabble(10)

    assert(game.isaword("was"))
    assert(game.score("was") == 6)
    assert(game.isaword("wa."))
    assert(game.score("wa.") == 5)
    
    print("Test passed!")

    

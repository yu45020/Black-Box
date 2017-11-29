"""
Simulate Aigis draw 
--- written for another interesting thing
"""
import numpy as np
from time import time
from functools import wraps
from operator import itemgetter
from collections import Counter, OrderedDict
import multiprocessing as mp
import pandas as pd

def timeit(f):
    """ profiler
    print function runtime
    """
    @wraps(f)
    def wrap(*args,**kwargs):
        tstart = time()
        result = f(*args,**kwargs)
        tend = time()
        print('%s run time: %2.4f seconds' % (f.__name__, tend-tstart))
        return result
    return wrap

class DrawSys(object):
    """
    Compare three methods:
        1) Exp(black) = 3%, fixed
        2) built on 1), but the 33th draw is black only if previous draws are not black
        3) built on 1), butt he 33th draw is black, regardless on previous draws
    """

    __slots__ = ["_rare_prob", '_black_threshold','_platinum_threshold'] #reduce memory usage
    
    #rare_prob_dict = {'silver': 0.37, 'gold': 0.5, 'platinum': 0.1, 'black': 0.03,}
    def __init__(self, rare_prob=[0.37, 0.5, 0.1, 0.03], black_threshold=32, platinum_threshold=9):
        self._rare_prob = rare_prob
        self._black_threshold = black_threshold
        self._platinum_threshold = platinum_threshold

    #@timeit
    def draw_start(self,num):
        """
        Main function
        return a list of cards (silver=0, gold=1, platinum=2, black=3)
        """
        result = np.random.choice([0,1,2,3], size=num, replace=True, p=self._rare_prob)
        black_counter = 0
        platinum_counter = 0

        for i in range(num):
            if (black_counter == self._black_threshold or result[i]==3 ):
                result[i] = 3
                black_counter = 0
                platinum_counter += 1 
                
            elif (platinum_counter == self._platinum_threshold or result[i]==2):
                result[i] = 2
                platinum_counter = 0
                black_counter += 1
            else:
                black_counter += 1
                platinum_counter += 1      

        return result

    def count_card_type(self, cards):
        """
        count each type of cards
        """
        cards_type_count = Counter(cards)
        numbers = len(cards)
        cards_type_count["silver"] = cards_type_count.pop(0)/numbers
        cards_type_count["gold"] = cards_type_count.pop(1)/numbers
        cards_type_count["platinum"] = cards_type_count.pop(2)/numbers
        cards_type_count["black"] = cards_type_count.pop(3)/numbers

        return OrderedDict(sorted(cards_type_count.items(), key=itemgetter(1)))

    def _test(self, x):
        cards = self.draw_start(10**4)
        counts = self.count_card_type(cards)
        return counts

    def f1(self, numbers):
        cards = self.draw_start(numbers)
        counts = self.count_card_type(cards)
        return counts
if __name__ == '__main__':
    test = DrawSys()
    trials = 10 ** 7
    print('Number of Draws: %1.0e' % trials)
    print("===============================")
    print("Results:")
    go_pool = mp.Pool()
    s_time = time()
    result = go_pool.map(test._test, range(10**3)) # each test draw 10^4
    e_time = time()
    result = pd.DataFrame(result)
    means = result.mean(axis=0)
    print(means)
    print("===============================")
    print("Run time: %s s" % (e_time-s_time))

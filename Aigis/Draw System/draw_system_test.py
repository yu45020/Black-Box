"""
Version 3.1415
This script explores probability in Aigis' draw system through simulation
Known problem: need to store all draws in memory. Avoid draws > 10**9
"""
import numpy as np
import pandas as pd
from time import time
from functools import wraps
import multiprocessing as mp

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

    __slots__ = ["_name", "_draw_threshold", "_black_prob", "_num_black"] #reduce memory usage

    def __init__(self,challenger_name="slime", draw_threshold=32, black_prob=0.03):
        self._name = challenger_name
        self._draw_threshold = draw_threshold+1
        self._black_prob = black_prob
        self._num_black = {"black": 0}

    def draw(self, num=1):
        """
        draw a card; only care black nor not
        :return: (0, 1) = (none black, black)
        """
        return np.random.choice(2, size=num, p=(1 - self._black_prob, self._black_prob))


    def method_old(self, draws):
        """
        old style: Exp(black) == 0.03
        :return: number of black cards
        """
        cards = self.draw(num=draws)
        self._num_black["black"] += sum(cards)
        return self._num_black


    def method_reset(self, draws):
        """
        Draw x non black cards, (x+1) will be black. Threshold will be reset when black cards are drawed
        :return: number of black cards
        """
        cards = self.draw(num=draws)  # (0,1) = (notblack, black)
        self._num_black["black"] += sum(cards)
        # 1) find all 1s position
        # 2) compute their difference, if the diff > threshold, add blacks
        black_positions = np.nonzero(cards) # potential error when draws are small --> All 0s
        num_noneblack = np.diff(black_positions)
        num_noneblack = np.insert(num_noneblack,0,black_positions[0][0])
        update_cards = num_noneblack[num_noneblack>(self._draw_threshold)]
        self._num_black["black"] += sum(update_cards//(self._draw_threshold))

        return self._num_black


    def method_fix(self,draws):
        """
         Draw x times, x+1 draw will be black regardless previous results
        :return: number of black cards
        """
        cards = self.draw(num=draws)  # (0,1) = (notblack, black)
        self._num_black["black"] += sum(cards)
        non_black = draws - self._num_black["black"]
        self._num_black["black"] += non_black // self._draw_threshold

        return self._num_black

    def test_method(self, draws=33, method="reset"):
        """
        test methods
        :param draws: number of draws
        :param method: old, reset, fixed
        :return: {exp,sd}
        """
        self._num_black["black"] = 0 # reset
        if method == "old":
            self.method_old(draws=draws)
        elif method == 'reset':
            self.method_reset(draws=draws)
        elif method == 'fix':
            self.method_fix(draws=draws)
        else:
            print('choose either one method: old, reset, fix')

        exp = self._num_black["black"]/draws
        pools = np.repeat([0, 1], [draws - self._num_black["black"], self._num_black["black"]])
        sd = np.std(pools)
        return {'Expectation': exp, "SD": sd}

def test_result():
    test = DrawSys()
    trials = 10**6
    #print('number of draws: %1.0e' % trials)
    #method_old = test.test_method(draws=trials, method='old')
    method_reset = test.test_method(draws=trials, method='reset')
    #method_fixed = test.test_method(draws=trials, method='fix')
    #result = pd.DataFrame([method_old, method_reset, method_fixed], index=['old', 'reset', 'fixed'])
    #print(result)
    return method_reset['Expectation']
if __name__ == '__main__':
    go_pool = mp.Pool(4)
    tstart = time()
    results = [go_pool.apply(test_result) for x in range(100)]
    print("Run time: %f s" % (time()-tstart))
    print("========================")
    print(np.mean(results))


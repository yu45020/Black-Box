"""
Decorator for logging function calls and their total run times.
Example:
Time_log = TimeitDecorator()
@Time_log.timeit()
def testfn():
    print("test fn")

@Time_log.timeit()
def testfn2():
    print('test fn 2')

@Time_log.timeit()
def testfn3():
    testfn2()
    testfn()
    print("test fn 3")

testfn3()
Time_log.print_log()
Time_log.log_doc
Time_log.write_log(file_name, model) # default is append "./time_log.txt"

"""

import time
import sys
import wrapt
from collections import OrderedDict
import datetime


class TimeitDecorator(object):
    log_doc = OrderedDict()

    def __init__(self):
        pass

    @classmethod
    def timeit(cls):
        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            _t = time.time()
            result = wrapped(*args, **kwargs)
            runtime = time.time() - _t

            cls._record_log(runtime, wrapped)
            return result

        return wrapper

    @classmethod
    def _record_log(cls, runtim, func):
        try:
            cls.log_doc[func.__name__]["Run Time"] += runtim
            cls.log_doc[func.__name__]["Func Call"] += 1
        except:
            cls.log_doc[func.__name__] = {
                "Run Time": runtim,
                "Func Call": 1,
            }

    def log_print(self):
        print("")
        print("{:^60}".format("Time Log"))
        print("=" * 60)
        print("{:<20}{:<20}{:<20}".format("Function", "Function Calls", "Total Run Time"))
        print("-" * 60)
        for key in self.log_doc.keys():
            print("{:<20}{:<20}{:<20.5f}".format(key, self.log_doc[key]["Func Call"], self.log_doc[key]["Run Time"]))
        print("-" * 60)
        print("{:<60}".format(str(datetime.datetime.now())))
        print("=" * 60)
        print("")

    def log_write(self, file_name='./time_log.txt', model='a'):
        """
        Redirect the print result into a file.
        """
        with open(file_name, model) as f:
            sys.stdout = f
            self.log_print()
            sys.stdout = sys.__stdout__

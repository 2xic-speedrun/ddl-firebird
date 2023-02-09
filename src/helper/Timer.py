import time
from collections import defaultdict

class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance

class Timer(SingletonClass):
    times = defaultdict(int)

    def set(self, func_name, time):
       self.times[func_name] += time

def timer(func):
    def wrapper(*args):
        start = time.time()
        results = func(*args)
        Timer().set(func.__name__, time.time() - start)
        return results
    return wrapper

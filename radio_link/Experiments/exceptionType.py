import sys, os

def foo():
    while True:
        pass

try:
    foo()
except Exception as e:
    print 'exception: '.join(type(e).__name__)


'''
Parse words, comma delimited vars, and parenthesis coupled arguments from
raw string
'''

import re, string

while True:
    cmd = raw_input('lay it down:')

    t = [word.strip(string.punctuation) for word in cmd.split()]

    # parses floating point numbers (even with multiple decimal pts and chars in
    # between
    s = re.findall(r'[+-]?\d*\.*\d+', cmd)

    print s
    print t

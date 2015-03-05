# File : main.py
# Author: Andrew Woods

def matrix(n, s, separator=','):
    l = s.split(separator)
    return [l[a:a+n] for a in range(0, len(l), n)]

def to_string(m):
    s = ''
    for row in m:
        for col in row:
            s += col + ','
    return s[:-1]


if __name__ == '__main__':
    n = input()             # for instance enter 3
    s = raw_input()         # for instance enter "a,b,c,d,e,f,g,h,i"
                            # (without quotes)
    separator = raw_input() # (for instance enter "," (without quotes)
                            # or enter "" (without quotes) for default case
    if separator == '':    
        print matrix(n=n, s=s)  
    else:
        print matrix(n=n, s=s, separator=separator)

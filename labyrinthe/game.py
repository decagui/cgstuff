import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # r: number of rows.
 # c: number of columns.
 # a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in raw_input().split()]

# game loop
while 1:
     # kr: row where Kirk is located.
     # kc: column where Kirk is located.
    kr, kc = [int(i) for i in raw_input().split()]
    themap=[]
    for i in xrange(r):
        row = raw_input() # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        themap.append( list( row ))
    

    
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # Kirk's next move (UP DOWN LEFT or RIGHT).
    print "RIGHT"
    sys.stdout.flush()


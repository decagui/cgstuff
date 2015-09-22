import sys
import math

#open file
themap=''
try:
    _, filename, botY, botX, alarm = sys.argv
    botX=int(botX)
    botY=int(botY)
except:
    print >> sys.stderr, "Usage:",sys.argv[0],"<map file>, start pos X, Y, alarmtime"
    sys.exit(3)
with open(filename, 'r') as F:
    themap=F.read().strip()

themap = [ list(row) for row in themap.split('\n') ]

if len(set([ len(row) for row in themap ]))>1:
    print >> sys.stderr, "map not rectangular"
    sys.exit(4)

maplenX = len(themap[0])
maplenY = len(themap)

discovered_map= [ [ '?' ] * len(row) for row in themap ]

print len(themap), len(themap[0]), alarm

while True:
    print botX, botY
    for col in xrange( max( 0, botX-2 ), min( maplenX, botX+3 ) ):
        for row in xrange( max( 0, botY-2 ), min( maplenY, botY+3) ):
            discovered_map[row][col]=themap[row][col]
    print '\n'.join( [ ''.join(row) for row in discovered_map ] )

    instr=raw_input()
    if instr=="RIGHT":
        botX+=1
    elif instr=="LEFT":
        botX-=1
    elif instr=="UP":
        botY-=1
    elif instr=="DOWN":
        botY+=1




 


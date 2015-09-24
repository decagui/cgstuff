import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # r: number of rows.
 # c: number of columns.
 # a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
maxY, maxX, alarmtime = [int(i) for i in raw_input().split()]

# init game state
foundCmd=False
cmd = None
startX, startY = -1, -1
reachables_fromstart = {}
def get_num_of( char, themap, org, dst ):

    submap = [ themap[y][x] 
                for y in xrange( min(max(0,org[0]),maxY), min(max(0,dst[0])+1,maxY) )
                for x in xrange( min(max(0,org[1]),maxX), min(max(0,dst[1])+1,maxX) )
                if themap[y][x] == char ]
    return len(submap)


def expand_reach_fromstart( reachables, themap, target=None ):
    while True:
        newpoints = {}
        for point in reachables:
            y,x = point
            curlen=reachables[point][0]+1
            if x!=0 and themap[y][x-1] not in ( '#', '?' ) and ( (y,x-1) not in reachables or reachables[(y,x-1)][0] > curlen):
                newpoints[ (y, x-1) ] = ( curlen, reachables[point][1]+['LEFT'] )
            if x!=maxX and themap[y][x+1] not in ( '#', '?' ) and ( (y,x+1) not in reachables or reachables[(y,x+1)][0] > curlen):
                newpoints[ (y, x+1) ] = ( curlen, reachables[point][1]+['RIGHT'] )
            if y!=0 and themap[y-1][x] not in ( '#', '?' ) and ( (y-1,x) not in reachables or reachables[(y-1,x)][0] > curlen):
                newpoints[ (y-1, x) ] = ( curlen, reachables[point][1]+['UP'] )
            if y!=maxY and themap[y+1][x] not in ( '#', '?' ) and ((y+1,x) not in reachables or reachables[(y+1,x)][0] > curlen):
                newpoints[ (y+1, x) ] = ( curlen, reachables[point][1]+['DOWN'] )
        reachables.update(newpoints)
        if not newpoints:
            break
        if target is not None and target in reachables:
            break



def expand_reach_explore( reachables, themap ):
    newpoints = {}
    for point in reachables:
        y,x = point
        if x!=0 and themap[y][x-1] not in ( '#', '?', 'C' ) and (y,x-1) not in reachables:
            newpoints[ (y, x-1) ] = ( get_num_of( '?', themap, (y-2,x-3),(y+2,x-3) ), reachables[point][1]+['LEFT'] )
        if x!=maxX and themap[y][x+1] not in ( '#', '?', 'C' ) and (y,x+1) not in reachables:
            newpoints[ (y, x+1) ] = ( get_num_of( '?', themap, (y-2,x+3),(y+2,x+3) ), reachables[point][1]+['RIGHT'] )
        if y!=0 and themap[y-1][x] not in ( '#', '?', 'C' ) and (y-1,x) not in reachables:
            newpoints[ (y-1, x) ] = ( get_num_of( '?', themap, (y-3,x-2),(y-3,x+2) ), reachables[point][1]+['UP'] )
        if y!=maxY and themap[y+1][x] not in ( '#', '?', 'C' ) and (y+1,x) not in reachables:
            newpoints[ (y+1, x) ] = ( get_num_of( '?', themap, (y+3,x-2),(y+3,x+2) ), reachables[point][1]+['DOWN'] )
    reachables.update(newpoints)
    return newpoints

def explore( reachables, themap ):
    maxscore = (0, [])
    newpoints = expand_reach_explore( reachables, themap )
    if not newpoints:
        raise "map explored totally, no solution found"
    print >> sys.stderr, "new points reachables"
    for point in newpoints:
        print >> sys.stderr, point, newpoints[point]
        if newpoints[point][0] > maxscore[0]:
            maxscore=newpoints[point]
    return maxscore


def read_input():
    themap = []
    global foundCmd, startX, startY, cmd, reachables_fromstart
    botY, botX = [int(i) for i in raw_input().split()]
    if startX == -1:
        startX, startY= botX, botY
        reachables_fromstart = { (startY, startX) : ( 0, [] ) }
    for i in xrange(maxY):
        row = raw_input() # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        if 'C' in row and not cmd:
            cmd = (i, row.index('C'))
        themap.append( row )
    expand_reach_fromstart( reachables_fromstart, themap )
    return botY, botX, themap

def inverse_path(path):
    inv = {
        "UP": "DOWN",
        "DOWN": "UP",
        "LEFT":"RIGHT",
        "RIGHT": "LEFT"}
    return [ inv[step] for step in path ]

while True:
    botY, botX, themap = read_input()
    
    max_score=0
    reachables = { (botY, botX): ( 0, [] ) }
    path = []

    if not cmd or cmd not in reachables_fromstart or reachables_fromstart[cmd][0] > alarmtime:
        while max_score==0:
            print >> sys.stderr, "expanding reach"
            max_score, path = explore( reachables, themap )
        print >> sys.stderr, "Selected path", path
        path.reverse() # because pop
  
    elif (botY,botX)!=cmd: # we still need to activate the target
        print >> sys.stderr, "trying to reach the target!"
        expand_reach_fromstart( reachables, themap, target=cmd)
        path = reachables[cmd][1]
        path.reverse()
    else: # go home Kirk, you're drunk
        print >> sys.stderr, "go back home"
        path = inverse_path(reachables_fromstart[cmd][1])
        # no need to reverse since we actually are in cmd and go back to start
        print >> sys.stderr, "path to follow", path

    while path:
        toplay=path.pop()
        print >> sys.stderr, "playing", toplay
        sys.stderr.flush()
        print toplay
        sys.stdout.flush()
        if path:
            read_input() # dont give a shit lol


print >> sys.stderr, "found cmd !"

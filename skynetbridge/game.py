import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

m = int(raw_input()) # the amount of motorbikes to control
v = int(raw_input()) # the minimum amount of motorbikes that must survive

road=[ raw_input(),raw_input(),raw_input(),raw_input() ]
roadlen = len(road[0])

def collision ( moto_x, moto_y, speedx, speedy, jumping):
    if moto_x+speedx < roadlen and road[ moto_y+speedy ][ moto_x+speedx ] == '0':
        return True
    if jumping:
        return False
    for lane in (road[moto_y], road[moto_y+speedy]):
        if '0' in lane[moto_x+1:moto_x+speedx]:
            return True
    return False

def motos_ys_to_tuple(motos_ys):
    return (0 in motos_ys, 1 in motos_ys, 2 in motos_ys, 3 in motos_ys)
def tuple_to_motos_ys( tup ):
    return [ i for i in xrange(4) if tup[i] ]

def simule_move( motos_x, motos_ys, speedx, speedy, jumping ):
    
    new_motos_ys = [moto_y + speedy for moto_y in motos_ys ]
    if speedy < 0 and 0 in motos_ys:
        return None
    if speedy > 0 and 3 in motos_ys:
        return None
    if speedx < 0:
        return None
    for moto_y in motos_ys:
        if collision( motos_x, moto_y, speedx, speedy, jumping):
            new_motos_ys.remove( moto_y+speedy )
            if len(new_motos_ys) < v: 
                return None
    return motos_x+speedx, new_motos_ys, speedx
            
simule_moves = {
    "UP":   lambda motos_x, motos_ys, speedx: simule_move( motos_x, motos_ys, speedx,-1, False ),
    "DOWN": lambda motos_x, motos_ys, speedx: simule_move( motos_x, motos_ys, speedx, 1, False ),
    "SPEED":lambda motos_x, motos_ys, speedx: simule_move( motos_x, motos_ys, speedx+1, 0, False ),
    "SLOW": lambda motos_x, motos_ys, speedx: simule_move( motos_x, motos_ys, speedx-1, 0, False ),
    "JUMP": lambda motos_x, motos_ys, speedx: simule_move( motos_x, motos_ys, speedx, 0, True ),
}
def expand_possible_moves( moves ):
    to_expand = moves.copy()
    expanded = {}
    cur_solution = (0,[])
    reexpand=True

    while reexpand:
        reexpand = False
        for move in to_expand:
            motos_x, tup, speed = move
            if sum(tup)>cur_solution[0]:
                for action in simule_moves:
                    #print >> sys.stderr, moves[move], move, "testing", action
                    new_pos = simule_moves[action]( motos_x, tuple_to_motos_ys(tup), speed )
                    if new_pos is not None:
                        new_x, new_motos_ys, new_speed = new_pos
                        new_pos = new_x, motos_ys_to_tuple( new_motos_ys ), new_speed
                        #print >> sys.stderr, new_pos
                        if new_pos not in moves:
                            expanded[ new_pos ]=to_expand[move]+[action]
                            if new_x >= roadlen:
                                if len( new_motos_ys)==m:
                                    print >> sys.stderr, "Solution optimale !", m, expanded[new_pos]
                                    return m,expanded[new_pos]
                                elif len(new_motos_ys) > cur_solution[0]:
                                    print >> sys.stderr, "Solution found !", len(new_motos_ys), expanded[new_pos]
                                    cur_solution=len(new_motos_ys),expanded[new_pos]
                            else:
                                if len(new_motos_ys) > cur_solution[0]:
                                    print >> sys.stderr, "still path to explore", new_pos, expanded[ new_pos ]
                                    reexpand=True
        if reexpand:
            #print >> sys.stderr, "reexpanding"
            moves.update(expanded)
            to_expand=expanded
            expanded={}
    if cur_solution[0]==0:
        raise "Pas de solution?!?"
    return cur_solution
        
# game loop
speedx = int(raw_input())
motos_ys = [ int(raw_input().split()[1]) for i in xrange(m) ]
motos_x = 0
moves = { (motos_x, motos_ys_to_tuple(motos_ys) , speedx): [] }

motos_remaining,expanded=expand_possible_moves( moves )
for action in expanded:
    print action
while True:
    s = int(raw_input()) # the motorbikes' speed
    for i in xrange(m):
         # x: x coordinate of the motorbike
         # y: y coordinate of the motorbike
         # a: indicates whether the motorbike is activated "1" or detroyed "0"
        x, y, a = [int(j) for j in raw_input().split()]
    print "WAIT"
    # Write an action using print
    # To debug: print >> sys.stderr, "Debug messages..."

    # A single line containing one of 6 keywords: SPEED, SLOW, JUMP, WAIT, UP, DOWN.


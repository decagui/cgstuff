import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

 # n: the total number of nodes in the level, including the gateways
 # l: the number of links
 # e: the number of exit gateways
n, l, e = [int(i) for i in raw_input().split()]
print >> sys.stderr, n, l, e
dij = [ [ 9999 for i in xrange(n) ] for j in xrange(n) ] # create dijkstra matrix
links = {}
for i in xrange(n):
    dij[i][i]=0

for i in xrange(l):
     # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in raw_input().split()]
    print >> sys.stderr, n1, n2
    links.setdefault(n1, set()).add(n2)
    links.setdefault(n2, set()).add(n1)

gates = set([ int(raw_input()) for i in xrange(e)])
print >> sys.stderr, gates

#ensemble des noeuds ou on a le choix de ce qu'on fait
initiative=dict([ ( n, (0 if links[n].intersection(gates) else 1) ) for n in links ])
for n1 in links:
    for n2 in links[n1]:
        dij[n1][n2]=initiative[n1]

doublegates = set([ node for node in links if len( links[node].intersection( gates) ) > 1 ])


def opt_dij(dij):
    dij_copy= [ list(dij[i]) for i in xrange(n+1) ]
    for a in xrange(n):
        for b in xrange(n):
            for c in xrange(n):
                hypothenuse=dij_copy[a][b]+dij_copy[b][c]
                if hypothenuse<dij_copy[a][c]:
                    dij_copy[a][c] = hypothenuse
                hypothenuse=dij_copy[c][b]+dij_copy[b][a]
                if hypothenuse<dij_copy[c][a]:
                    dij_copy[c][a] = hypothenuse
    return dij_copy

def kill_link(orig, dest):
    links[orig].remove(dest)
    links[dest].remove(orig)
    dij[orig][dest]=9999
    dij[dest][orig]=9999
    print orig,dest

# game loop
while 1:
    si = int(raw_input()) # The index of the node on which the Skynet agent is positioned this turn
    print >> sys.stderr, si


    # case 1 : no choice

    easycase=None
    print >> sys.stderr, gates
    for g in gates:
        if g in links[si]:
            print >> sys.stderr, "easy case"
            easycase=g
            break
    if easycase is not None:
        kill_link(easycase, si)
        continue

    print >> sys.stderr, "non easy case"

    dij_copy=opt_dij(dij)
    min_len=9999
    gatetokill=None
    for dg in doublegates:
        print >> sys.stderr, "checking double gate", dg
        print >> sys.stderr, dij_copy
        print >> sys.stderr, "distance to double gate", dg, dij_copy[si][dg]
        if dij_copy[si][dg] < min_len:
            gatetokill=dg
            min_len=dij_copy[si][dg]

    if gatetokill is None:
        for g in gates:
            if links[g]:
                print >> sys.stderr, "no more double, defaulting to", g
                kill_link(g, list(links[g])[0])
                break
    else:
        print >> sys.stderr, "gate to kill", gatetokill
        #trouver le noeud qui nous connecte a gatetokill en min_len
        link_to_kill=None
        for g in links[gatetokill]:
            if g in gates:
                # kill it with fire
                kill_link(gatetokill,g)
                if len( links[gatetokill].intersection( gates ) ) <= 1:
                    print >> sys.stderr, "removing", gatetokill, "from double gates"
                    doublegates.remove( gatetokill )
                break


# -*- coding: utf-8 -*-
r"""
Creation of random balanced teams

EXAMPLES::

    sage: from slabbe.random_team_creation import print_teams
    sage: A = list(range(10))
    sage: B = list(range(10))
    sage: print_teams(A,B,4)       # random
    Équipe  0
    3
    5
    9
    3
    7
    Équipe  1
    2
    6
    8
    2
    6
    8
    Équipe  2
    0
    4
    1
    4
    9
    Équipe  3
    1
    7
    0
    5

"""
#*****************************************************************************
#       Copyright (C) 2024 Sebastien Labbe <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from collections import defaultdict

try:
    from itertools import batched
except ImportError:
    #https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
    def batched(iterable, n=1):
        r"""
        EXAMPLES::

            sage: from slabbe.random_team_creation import batched
            sage: data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            sage: for x in batched(data, 3): print(x)
            [0, 1, 2]
            [3, 4, 5]
            [6, 7, 8]
            [9, 10]

        """
        l = len(iterable)
        for ndx in range(0, l, n):
            yield iterable[ndx:min(ndx + n, l)]

def create_teams(boys, girls, nteams):
    r"""
    EXAMPLES::

        sage: from slabbe.random_team_creation import create_teams
        sage: A = list(range(10))
        sage: B = list(range(10))
        sage: d = create_teams(A,B,4)
    """
    from sage.misc.prandom import shuffle
    d = defaultdict(list)
    L = list(range(nteams))
    for batch in batched(boys, nteams):
        shuffle(L)
        for i,player in zip(L,batch):
            d[i].append(player)
    for batch in batched(girls, nteams):
        shuffle(L)
        for i,player in zip(L,batch):
            d[i].append(player)
    return dict(d)

def print_teams(boys, girls, nteams):
    r"""
    EXAMPLES::

        sage: from slabbe.random_team_creation import print_teams
        sage: A = list(range(10))
        sage: B = list(range(10))
        sage: print_teams(A,B,4)        # random
        Équipe  0
        1
        4
        1
        6
        Équipe  1
        0
        5
        9
        2
        7
        Équipe  2
        2
        7
        8
        3
        5
        8
        Équipe  3
        3
        6
        0
        4
        9

    """
    d = create_teams(boys, girls, nteams)
    for i in range(nteams):
        team = d[i]
        print("Équipe ", i)
        for player in team:
            print(player)



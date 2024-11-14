# -*- coding: utf-8 -*-
r"""
Creation of random balanced teams

EXAMPLES::

    sage: from slabbe.random_team_creation import print_teams, create_teams
    sage: A = list(range(10))
    sage: B = list(range(10))
    sage: d = create_teams(A, B, 4)
    sage: print_teams(d)       # random
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
    # itertools.batched is a new addition in Python 3.12
    # https://docs.python.org/3.12/whatsnew/3.12.html
    from itertools import batched
except ImportError:
    #https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
    def batched(iterable, n=1):
        r"""
        EXAMPLES::

            sage: from slabbe.random_team_creation import batched
            sage: data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            sage: for x in batched(data, 3): print(x)
            (0, 1, 2)
            (3, 4, 5)
            (6, 7, 8)
            (9, 10)

        """
        l = len(iterable)
        for ndx in range(0, l, n):
            yield tuple(iterable[ndx:min(ndx + n, l)])

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

def print_teams(d):
    r"""
    EXAMPLES::

        sage: from slabbe.random_team_creation import create_teams
        sage: from slabbe.random_team_creation import print_teams
        sage: A = list(range(10))
        sage: B = list(range(10))
        sage: d = create_teams(A,B,4)
        sage: print_teams(d)          # random
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
    for i in range(len(d)):
        team = d[i]
        print("Équipe ", i)
        for player in team:
            print(player)
        print("")


def print_teams_as_table(d):
    r"""
    EXAMPLES::

        sage: from slabbe.random_team_creation import create_teams
        sage: from slabbe.random_team_creation import print_teams_as_table
        sage: A = list(range(10))
        sage: B = list(range(10))
        sage: d = create_teams(A,B,4)
        sage: print_teams_as_table(d)      # random
          0      1      2   3
        ├──────┼──────┼───┼──────┤
          1      0      2   3
          5      4      7   6
          2      0      8   9
          5      4      3   1
          9      None   7   6
          None   None   8   None

    """
    from itertools import zip_longest
    from sage.misc.table import table

    rows = [row for row in zip_longest(*[d[i] for i in range(len(d))])]
    header_row = list(range(len(d)))
    return table(rows, header_row=header_row)



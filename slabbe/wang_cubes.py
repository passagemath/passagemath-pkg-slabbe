# -*- coding: utf-8 -*-
r"""
Wang cubes tiling solver

We solve the problem of tiling a rectangular box by Wang cubes by reducing it to
other well-known problems like linear problem, exact cover problem and SAT.

"""
#*****************************************************************************
#       Copyright (C) 2024 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

class WangCubeSet(object):
    r"""
    Construct a set of Wang cubes.

    INPUT:

    - ``cubes`` -- list or dict of cubes, a Wang cube is a 6-tuple
      identifying a label to each square face orthogonal to the vectors
      in the following order: `(e_1,e_2,e_3,-e_1,-e_2,-e_3)`

    EXAMPLES::

        sage: from slabbe import WangCubeSet
        sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
        sage: T = WangCubeSet(cubes)

    Input can be a dictionnary::

        sage: cubes = {'a':(0,0,0,0,0,0), 'b':(1,1,1,1,1,1), 'c':(2,2,2,2,2,2)}
        sage: T = WangCubeSet(cubes)

    """
    def __init__(self, cubes):
        r"""
        See documentation of the class.

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
        """
        if isinstance(cubes, list):
            self._cubes = {i:cube for (i,cube) in enumerate(cubes)}
        elif isinstance(cubes, dict):
            self._cubes = {i:cube for (i,cube) in cubes.items()}
        else:
            raise TypeError("cubes input type (={}) must be a list or a dict".format(type(cubes)))


    def __iter__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: next(iter(T))
            (0, 0, 0, 0, 0, 0)
        """
        return iter(self._cubes.values())

    def __len__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: len(T)
            3
        """
        return len(self._cubes)

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T
            Set of Wang cubes of cardinality 3
        """
        return r"Set of Wang cubes of cardinality {}".format(len(self))

    def __getitem__(self, i):
        r"""
        INPUT:

        - ``i`` -- integer or cube label, index

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T[1]
            (1, 1, 1, 1, 1, 1)
        """
        return self._cubes[i]


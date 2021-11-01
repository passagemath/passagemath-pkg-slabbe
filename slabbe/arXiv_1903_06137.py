# -*- coding: utf-8 -*-
r"""
The code to construct the partitions in [Lab2021b]_.

REFERENCES:

.. [Lab2021b] S. Labbé.  Markov partitions for toral
   `\mathbb{Z}^2`-rotations featuring Jeandel-Rao Wang shift and model
   sets, *Annales Henri Lebesgue* 4 (2021) 283-324. 
   https://doi.org/10.5802/ahl.73
   https://arxiv.org/abs/1903.06137

.. [Lab2018] S. Labbé. A self-similar aperiodic set of 19 Wang
   tiles. Geom. Dedicata, 201 (2019) 81-109 
   https://doi.org/10.1007/s10711-018-0384-8.
   http://arxiv.org/abs/1802.03265

EXAMPLES:

The partition associated to Jeandel-Rao Wang shift::

    sage: from slabbe.arXiv_1903_06137 import jeandel_rao_wang_shift_partition
    sage: P0 = jeandel_rao_wang_shift_partition()
    sage: P0
    Polyhedron partition of 24 atoms with 11 letters

The partition associated to the self-similar Wang shift `\Omega_{\mathcal{U}}`::

    sage: from slabbe.arXiv_1903_06137 import self_similar_19_atoms_partition
    sage: PU = self_similar_19_atoms_partition()
    sage: PU
    Polyhedron partition of 19 atoms with 19 letters

A 5x5 valid pattern::

    sage: from slabbe.wang_tiles import WangTiling
    sage: from slabbe.arXiv_1903_06137 import jeandel_rao_tiles
    sage: T0 = jeandel_rao_tiles()
    sage: table = [[6, 1, 7, 2, 5],
    ....:          [6, 1, 3, 8, 7],
    ....:          [7, 0, 9, 7, 5],
    ....:          [4, 0, 9, 3, 7],
    ....:          [5, 0, 9, 10, 4]]
    sage: t = WangTiling(table, tiles=T0)
    sage: t._color = None

Image dans l'introduction de l'article::

    sage: from slabbe.arXiv_1903_06137 import geometric_edges_shapes
    sage: draw_H, draw_V = geometric_edges_shapes()
    sage: tikz = t.tikz(color=None, draw_H=draw_H, draw_V=draw_V, 
    ....:              font=r'\bfseries', id=True, label=False, 
    ....:              id_color=r'black',scale="1,very thick")
    sage: tikz._standalone_options = ["border=2mm"]
    sage: _ = tikz.pdf(view=False)

Image dans l'appendice de l'article::

    sage: extra = r'\node[yshift=2.5mm] at (1,5) {\Huge\ScissorRightBrokenBottom};'
    sage: tikz = t.tikz(color=None, draw_H=draw_H, draw_V=draw_V,
    ....:         font=r'\bfseries\LARGE', id=True, label=False,
    ....:         id_color=r'black', scale="3,ultra thick", extra_after=extra)
    sage: tikz._usepackage = ['amsmath', 'bbding']
    sage: tikz._standalone_options = ["border=2mm"]
    sage: _ = tikz.pdf(view=False)

Random generation of Jeandel-Rao tilings::

    sage: from slabbe import random_jeandel_rao_rectangular_pattern
    sage: tiling = random_jeandel_rao_rectangular_pattern(4, 4)
    sage: tiling
    A wang tiling of a 4 x 4 rectangle
    sage: tiling.table()   # random
    [[1, 10, 4, 5], [1, 3, 3, 7], [0, 9, 10, 4], [0, 9, 3, 3]]

"""
#*****************************************************************************
#       Copyright (C) 2019-2021 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from __future__ import absolute_import, print_function
from collections import defaultdict

from sage.rings.polynomial.polynomial_ring import polygen
from sage.rings.rational_field import QQ
from sage.rings.number_field.number_field import NumberField
from sage.geometry.polyhedron.constructor import Polyhedron

from slabbe import PolyhedronPartition

########################################
# Creating the Partitions
########################################
def jeandel_rao_wang_shift_partition(backend=None):
    r"""
    This construct the polygon partition associated to Jeandel-Rao
    tilings introduced in [Lab2021b]_.

    INPUT:

    - ``backend`` -- string, polyhedron backend

    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import jeandel_rao_wang_shift_partition
        sage: P0 = jeandel_rao_wang_shift_partition()
        sage: P0.is_pairwise_disjoint()
        True
        sage: P0.volume()
        4*phi + 1

    The volume is consistent with::

        sage: z = polygen(QQ, 'z')
        sage: K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
        sage: phi = K.gen()
        sage: phi * (phi + 3)
        4*phi + 1

    """
    # the golden mean
    z = polygen(QQ, 'z')
    K = NumberField(z**2-z-1, 'phi', embedding=QQ(1.6))
    phi = K.gen()

    # x and y coordinates
    xcoords = [0, phi**-2, phi**-1, 1, phi]
    ycoords = [0, 1, 2, phi+1, phi+2, phi+3]

    # the vertices
    A = [(x,0) for x in xcoords]
    B = [(x,1) for x in xcoords]
    C = [(x,2) for x in xcoords]
    D = [(x,phi+1) for x in xcoords]
    E = [(x,phi+2) for x in xcoords]
    F = [(x,phi+3) for x in xcoords]

    # atoms corresponding to Jeandel-Rao tile numbers
    L = [
        (0, (A[0], A[2], B[2])), 
        (0, (A[2], A[3], B[3])),
        (0, (A[3], A[4], B[4])),
        (1, (A[0], B[0], B[2])),
        (1, (A[2], B[2], B[3])),
        (1, (A[3], B[3], B[4])),
        (2, (C[0], D[0], E[2])),
        (3, (B[3], C[3], E[4], C[4])),
        (4, (C[0], E[2], E[3])),
        (4, (E[2], E[3], F[3])),
        (5, (D[0], E[0], E[2])),
        (5, (E[0], E[1], F[1])),
        (5, (E[1], E[2], F[3])),
        (6, (E[0], F[0], F[1])),
        (6, (E[1], F[1], F[3])),
        (6, (E[3], F[3], F[4])),
        (7, (D[3], E[3], E[4])),
        (7, (E[3], E[4], F[4])),
        (7, (B[0], C[0], E[3])),
        (8, (B[2], C[2], E[4])),
        (9, (B[0], B[2], C[2])),
        (9, (B[2], B[3], C[3])),
        (9, (B[3], B[4], C[4])),
        (10, (B[0], D[3], E[3])),
        ]
    L = [(key, Polyhedron(vertices, base_ring=K, backend=backend)) 
         for (key,vertices) in L]
    return PolyhedronPartition(L)

def self_similar_19_atoms_partition(backend=None):
    r"""
    This construct the polygon partition introduced in [Lab2021b]_
    associated to the self-similar 19 Wang tiles [Lab2018]_.

    INPUT:

    - ``backend`` -- string, polyhedron backend

    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import self_similar_19_atoms_partition
        sage: PU = self_similar_19_atoms_partition()
        sage: PU.is_pairwise_disjoint()
        True
        sage: PU.volume()
        1

    """
    # the golden mean
    z = polygen(QQ, 'z')
    K = NumberField(z**2-z-1, 'phi', embedding=QQ(1.6))
    phi = K.gen()

    # the partition vertices
    L = [
        (0, [(phi - 1, -2*phi + 4), (phi - 1, phi - 1), (-2*phi + 4, phi - 1)]),
        (1,
        [(phi - 1, -2*phi + 4),
        (phi - 1, 1),
        (1, 1),
        (-2*phi + 4, phi - 1),
        (1, phi - 1)]),
        (2, [(0, 1), (-phi + 2, phi - 1), (2*phi - 3, phi - 1)]),
        (3, [(0, 1), (0, phi - 1), (2*phi - 3, phi - 1)]),
        (4, [(phi - 1, phi - 1), (-phi + 2, 1), (phi - 1, -2*phi + 4)]),
        (5, [(phi - 1, 1), (-phi + 2, 1), (phi - 1, -2*phi + 4)]),
        (6, [(0, 1), (-phi + 2, 1), (-phi + 2, phi - 1)]),
        (7, [(-phi + 2, 1), (-phi + 2, phi - 1), (phi - 1, phi - 1)]),
        (8, [(1, 0), (phi - 1, 0), (phi - 1, -phi + 2)]),
        (9, [(-2*phi + 4, phi - 1), (phi - 1, phi - 1), (1, -phi + 2), (1, 0)]),
        (10, [(1, -phi + 2), (-2*phi + 4, phi - 1), (1, phi - 1)]),
        (11, [(1, 0), (phi - 1, -phi + 2), (phi - 1, phi - 1)]),
        (12, [(-phi + 2, -phi + 2), (-phi + 2, phi - 1), (2*phi - 3, phi - 1)]),
        (13,
        [(-phi + 2, phi - 1),
        (phi - 1, -phi + 2),
        (-phi + 2, -phi + 2),
        (phi - 1, 0)]),
        (14,
        [(2*phi - 3, phi - 1), (0, phi - 1), (-phi + 2, -phi + 2), (-phi + 2, 0)]),
        (15, [(phi - 1, 0), (-phi + 2, 0), (-phi + 2, -phi + 2)]),
        (16, [(0, 0), (-phi + 2, 0), (0, -phi + 2)]),
        (17, [(0, -phi + 2), (-phi + 2, 0), (0, phi - 1)]),
        (18, [(phi - 1, -phi + 2), (-phi + 2, phi - 1), (phi - 1, phi - 1)])
        ]

    L = [(key, Polyhedron(vertices, base_ring=K, backend=backend)) 
         for (key,vertices) in L]
    return PolyhedronPartition(L)
########################################
# Creating the tikz image in the article
########################################
def geometric_edges_shapes():
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import geometric_edges_shapes
        sage: draw_H, draw_V = geometric_edges_shapes()
    """
    draw_H = defaultdict(lambda: r'\draw {} -- ++ (1,0);')
    draw_V = defaultdict(lambda: r'\draw {} -- ++ (0,1);')

    draw_H['0'] = r'\draw[blue] {} -- ++ (1,0);'
    draw_H['1'] = (r'\draw[blue] {} -- ++ (.35,0) '
                                r'-- ++ (.15,.20) -- ++ (.15,-.20) '
                                r'-- ++ (.35,0);')
    draw_H['2'] = (r'\draw[blue] {} -- ++ (.3,0) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.3,0);')
    draw_H['3'] = (r'\draw[blue] {} -- ++ (.2,0) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.2,0);')
    draw_H['4'] = (r'\draw[blue] {} -- ++ (.1,0) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,.15) -- ++ (.1,-.15) '
                                r'-- ++ (.1,0);')
    draw_V['0'] = r'\draw[blue] {} -- ++ (0,1);'
    draw_V['1'] = (r'\draw[blue] {} -- ++ (0,.35) '
                                r'arc (-90:90:.15) '
                                r'-- ++ (0,.35);')
    draw_V['2'] = (r'\draw[blue] {} -- ++ (0,.25) '
                                r'arc (-90:90:.1) '
                                r'-- ++ (0,.1) '
                                r'arc (-90:90:.1) '
                                r'-- ++ (0,.25);')
    draw_V['3'] = (r'\draw[blue] {} -- ++ (0,.15) '
                                r'arc (-90:90:.1) '
                                r'-- ++ (0,.05) '
                                r'arc (-90:90:.1) '
                                r'-- ++ (0,.05) '
                                r'arc (-90:90:.1) '
                                r'-- ++ (0,.15);')
    return draw_H, draw_V

def jeandel_rao_tiles():
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import jeandel_rao_tiles
        sage: jeandel_rao_tiles()
        Wang tile set of cardinality 11

    """
    from slabbe.wang_tiles import WangTileSet
    tiles = [(2,4,2,1), (2,2,2,0), (1,1,3,1), (1,2,3,2), (3,1,3,3), (0,1,3,1), 
            (0,0,0,1), (3,1,0,2), (0,2,1,2), (1,2,1,4), (3,3,1,2)]
    tiles = [[str(a) for a in t] for t in tiles]
    T0 = WangTileSet(tiles)
    return T0

def T0_shapes():
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import T0_shapes
        sage: T0_shapes()
        \documentclass[tikz]{standalone}
        \standaloneconfig{border=2mm}
        \usepackage{amsmath}
        \begin{document}
        \begin{tikzpicture}
        [scale=1,very thick]
        \tikzstyle{every node}=[font=\bfseries]
        % tile at position (x,y)=(0.0, 0.0)
        \node[black] at (0.5, 0.5) {0};
        ...
        ... 60 lines not printed (5279 characters in total) ...
        ...
        \draw[blue] (15.0, 0.0) -- ++ (0,.15) arc (-90:90:.1) -- ++ (0,.05) arc (-90:90:.1) -- ++ (0,.05) arc (-90:90:.1) -- ++ (0,.15);
        \draw[blue] (14.0, 1.0) -- ++ (.2,0) -- ++ (.1,.15) -- ++ (.1,-.15) -- ++ (.1,.15) -- ++ (.1,-.15) -- ++ (.1,.15) -- ++ (.1,-.15) -- ++ (.2,0);
        \draw[blue] (14.0, 0.0) -- ++ (0,.35) arc (-90:90:.15) -- ++ (0,.35);
        \draw[blue] (14.0, 0.0) -- ++ (.3,0) -- ++ (.1,.15) -- ++ (.1,-.15) -- ++ (.1,.15) -- ++ (.1,-.15) -- ++ (.3,0);
        \end{tikzpicture}
        \end{document}

    """
    draw_H, draw_V = geometric_edges_shapes()
    T0 = jeandel_rao_tiles()
    tikz = T0.tikz(color=None, draw_H=draw_H, draw_V=draw_V, id=True,
            font=r'\bfseries', 
            label=False, id_color=r'black',scale="1,very thick",ncolumns=11,space=.4)
    tikz._standalone_options = ["border=2mm"]
    return tikz

def T0_tiles():
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import T0_tiles
        sage: T0_tiles()
        \documentclass[tikz]{standalone}
        \standaloneconfig{border=2mm}
        \usepackage{amsmath}
        \begin{document}
        \begin{tikzpicture}
        [scale=1]
        \tikzstyle{every node}=[font=\normalsize]
        % tile at position (x,y)=(0.0, 0.0)
        \fill[cyan] (1.0, 0.0) -- (0.5, 0.5) -- (1.0, 1.0);
        ...
        ... 137 lines not printed (6927 characters in total) ...
        ...
        \node[rotate=0,black] at (14.8, 0.5) {3};
        \node[rotate=0,black] at (14.5, 0.8) {3};
        \node[rotate=0,black] at (14.2, 0.5) {1};
        \node[rotate=0,black] at (14.5, 0.2) {2};
        \end{tikzpicture}
        \end{document}

    """
    T0 = jeandel_rao_tiles()
    color = defaultdict(lambda : 'white')
    color.update({0:'white', 1:'red', 2:'cyan', 3:'green', 4:'lightgray'})
    color.update({str(k):v for k,v in color.items()})

    tikz = T0.tikz(color=color, id=None, label=True,scale=1,ncolumns=11,space=.4)
    tikz._standalone_options = ["border=2mm"]
    return tikz

##########################################
# Random generation of Jeandel-Rao pattern
##########################################
def plane_to_torus(m,n):
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import plane_to_torus
        sage: plane_to_torus(0, 0)                       # abs tol 1e-10
        (0.000000000000000, 0.0)
        sage: plane_to_torus(0.324, .324)                # abs tol 1e-10
        (0.324000000000000, 0.324)
        sage: plane_to_torus(12.324, 12.324)             # abs tol 1e-10
        (0.615796067500630, 3.08793202250021)
        sage: plane_to_torus(100, 100)                   # abs tol 1e-10
        (1.3343685400050447, 3.021286236252207)

    """
    import math
    phi = .5 + .5 * math.sqrt(5)
    m = float(m)
    n = float(n)
    h = n // float(phi + 3)
    return (m - h) % float(phi), n % float(phi+3)

def torus_to_code(x,y):
    r"""
    Return in which atom of the partition associated to Jeandel-Rao tilings
    the point (x,y) falls in according to [Lab2021b]_.

    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import torus_to_code
        sage: torus_to_code(0,0)
        0
        sage: torus_to_code(0.23,3.5)
        5
        sage: torus_to_code(1.23,2.243)
        3

    ::

        sage: from slabbe.arXiv_1903_06137 import plane_to_torus, random_torus_point
        sage: torus_to_code(*plane_to_torus(14.4141, 89.14))
        9
        sage: torus_to_code(*random_torus_point())                  # random
        3

    """
    import math
    phi = .5 + .5 * math.sqrt(5)
    assert x >= 0, "x(={}) must be nonnegative".format(x)
    assert y >= 0, "y(={}) must be nonnegative".format(y)
    assert x < phi, "x(={}) must be less then phi".format(x)
    assert y < phi+3, "y(={}) must be less then phi+3".format(y)
    # test
    if y < 1:
        if x < (1./phi):
            if y <= phi*x:
                return 0
            else:
                return 1
        elif x < 1:
            if y <= (phi**2)*x -phi:
                return 0
            else:
                return 1
        else:
            if y <= phi*x - phi:
                return 0
            else:
                return 1
    if y <= phi*x + 1:
        if x <= 1./phi:
            return 9
        else:
            if y <= (phi**2)*x + 1 - phi:
                if x >= (1./phi) and x < 1:
                    return 9
                elif x >= 1:
                    if y <= phi*x + 1 - phi:
                        return 9
                    else:
                        return 3
            else:
                return 8
    if y > (phi*x + 1) and y <= phi*x + 2:
        if x <= 1:
            if y <= (phi**2)*x + 1:
                return 10
            else:
                return 7
        else:
            return 7
    if y > phi*x +2:
        if x <= 1:
            if y <= (phi**2)*x + 2:
                return 4
            if y <= (phi*x + phi +1) and y > (phi**2)*x + 2:
                return 2
            else:
                if y > (phi**2)*x + phi + 2:
                    return 6
                if y > (phi*x + 3) and x > (1./(phi**2)):
                    return 6
                else:
                    return 5
        else:
            return 6

def random_torus_point():
    r"""
    Return a random point in the rectangle `[0,\phi[\times[0,\phi+3[`.

    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import random_torus_point
        sage: random_torus_point()                  # random
        (0.947478386174632, 2.62013791669977)
        sage: random_torus_point()                  # random
        (0.568010404619112, 0.933319012345482)
        sage: random_torus_point()                  # random
        (1.06782191679796, 4.58930423801758)

    ::

        sage: from slabbe.arXiv_1903_06137 import torus_to_code
        sage: torus_to_code(*random_torus_point())                  # random
        3
        sage: torus_to_code(*random_torus_point())                  # random
        7

    """
    import math
    from random import random
    phi = .5 + .5 * math.sqrt(5)
    return random() * phi, random() * (phi+3)

def random_jeandel_rao_rectangular_pattern(width, height, start=None):
    r"""
    Returns a jeandel rao rectangular pattern associated to a given
    (random) starting position on the torus.

    INPUT:

    - ``width`` -- integer
    - ``height`` -- integer
    - ``start`` -- pair of real numbers (default:``None``), if ``None``
      a random start point is chosen

    OUTPUT:

    list of lists

    EXAMPLES::

        sage: from slabbe.arXiv_1903_06137 import random_jeandel_rao_rectangular_pattern
        sage: tiling = random_jeandel_rao_rectangular_pattern(4,4)
        sage: tiling
        A wang tiling of a 4 x 4 rectangle
        sage: tiling.table()   # random
        [[1, 10, 4, 5], [1, 3, 3, 7], [0, 9, 10, 4], [0, 9, 3, 3]]

    """
    if start is None:
        x0,y0 = random_torus_point()
    else: 
        x0,y0 = start
        x0,y0 = plane_to_torus(x0, y0)
    tiling = [[torus_to_code(*plane_to_torus(x0+a,y0+b)) 
                  for b in range(height)]
                  for a in range(width)]
    tiles = [(2,4,2,1), (2,2,2,0), (1,1,3,1), (1,2,3,2), (3,1,3,3), (0,1,3,1), 
             (0,0,0,1), (3,1,0,2), (0,2,1,2), (1,2,1,4), (3,3,1,2)]
    tiles = [tuple(str(a) for a in t) for t in tiles]
    from collections import defaultdict
    color = defaultdict(lambda : 'white')
    color.update({0:'white', 1:'red', 2:'cyan', 3:'green', 4:'lightgray'})
    color.update({str(k):v for k,v in color.items()})
    from slabbe.wang_tiles import WangTiling
    return WangTiling(tiling, tiles=tiles, color=color)


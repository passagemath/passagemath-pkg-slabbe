# -*- coding: utf-8 -*-
r"""
The hat: an aperiodic monotile 

This module contains code to construct tilings of rectangles by the
`aperiodic monotile`__ discovered by David Smith, Joseph Samuel Myers,
Craig S. Kaplan, and Chaim Goodman-Strauss `in March 2023`__.

It makes a reduction to an instance of the Universal Cover problem,
which can be solved in SageMath using Donald Knuth's dancing links
algorithm, SAT solvers or Mixed-Integer Linear programs (MILP).

The code uses the coordinate system defined in the file validate/kitegrid.pdf
found in the `source code`__ associated to the article.

__ https://cs.uwaterloo.ca/~csk/hat/
__ https://arxiv.org/abs/2303.10798
__ https://cs.uwaterloo.ca/~csk/hat/validate.tar.gz

EXAMPLES::

    sage: from slabbe.aperiodic_monotile import MonotileSolver
    sage: s = MonotileSolver(20,20)
    sage: s.the_dlx_solver()                               # long time (1s)
    Dancing links solver for 4800 columns and 10320 rows
    sage: s.one_solution(solver='glucose') is not None     # long time (3s)  # optional glucose
    True
    sage: G = s.draw_one_solution(solver='glucose')        # long time (12s) # optional glucose
    sage: G                                                # long time (3s)  # optional glucose
    Graphics object consisting of 4465 graphics primitives
    sage: G.save('solution_20x20.png', figsize=20)         # not tested

"""
#*****************************************************************************
#       Copyright (C) 2023 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
import itertools
from sage.misc.cachefunc import cached_function,cached_method

from sage.matrix.constructor import matrix
from sage.modules.free_module_element import vector
from sage.combinat.tiling import Polyomino

def polyomino_reversal(p):
    r"""
    EXAMPLES::

        sage: from slabbe.aperiodic_monotile import polyomino_reversal
        sage: V = [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)]
        sage: from sage.combinat.tiling import Polyomino
        sage: hexagon = Polyomino(V)
        sage: image = polyomino_reversal(hexagon)
        sage: image == hexagon
        True
        sage: image
        Polyomino: [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)],
        Color: gray

    """
    return Polyomino([-v for v in p])

def polyomino_mirror(p):
    r"""
    EXAMPLES::

        sage: from slabbe.aperiodic_monotile import polyomino_mirror
        sage: V = [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)]
        sage: from sage.combinat.tiling import Polyomino
        sage: hexagon = Polyomino(V)
        sage: image = polyomino_mirror(hexagon)
        sage: image == hexagon
        True
        sage: image
        Polyomino: [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)],
        Color: gray

    """
    return Polyomino([(y,x) for (x,y) in p])

def the_rotated_reflected_monotiles():
    r"""
    EXAMPLES::

        sage: from slabbe.aperiodic_monotile import the_rotated_reflected_monotiles
        sage: L = the_rotated_reflected_monotiles()
        sage: len(L)
        12

    TESTS::

        sage: monotiles = the_rotated_reflected_monotiles()
        sage: box = monotiles[0]
        sage: from sage.combinat.tiling import TilingSolver
        sage: solver = TilingSolver(monotiles, box, rotation=False,
        ....:         reflection=False, reusable=True, outside=False)
        sage: it = solver.solve()
        sage: next(it)
        [Polyomino: [(-1, 1), (-1, 3), (-1, 4), (0, 1), (1, 2), (1, 3), (2,
        1), (3, 1)], Color: gray]

    """
    triangleR = [(-1,3),(1,2),(0,1)]
    p0 = triangleR + [(-1,1), (-1,4), (1,3), (2,1), (3,1)]
    p1 = triangleR + [(-1,4), (2,1), (1,0), (-1,1), (-1,0)]
    p2 = triangleR + [(2,1), (-1,1), (-2,3), (-1,4), (-2,5)]
    triangleL = [(-3,2),(-2,3),(-1,1)]
    p3 = triangleL + [(-1,0), (-4,3), (-3,4), (-1,3), (-1,4)]
    p4 = triangleL + [(-1,3), (-1,0), (-3,1), (-4,3), (-5,3)]
    p5 = triangleL + [(-4,3), (-1,3), (0,1), (-1,0), (0,-1)]
    P = [Polyomino(p) for p in [p0,p1,p2,p3,p4,p5]]
    Pr = [polyomino_mirror(p) for p in P]
    return P+Pr

@cached_function
def the_canonical_12_monotiles():
    r"""
    EXAMPLES::

        sage: from slabbe.aperiodic_monotile import the_canonical_12_monotiles
        sage: the_canonical_12_monotiles()
        {Polyomino: [(0, 0), (0, 2), (0, 3), (1, 0), (2, 1), (2, 2), (3, 0), (4, 0)], Color: gray: 0,
         Polyomino: [(0, 0), (0, 1), (0, 3), (0, 4), (1, 1), (2, 0), (2, 2), (3, 1)], Color: gray: 1,
         Polyomino: [(0, 2), (0, 4), (1, 0), (1, 2), (1, 3), (2, 0), (3, 1), (4, 0)], Color: gray: 2,
         Polyomino: [(0, 3), (1, 2), (1, 4), (2, 3), (3, 0), (3, 1), (3, 3), (3, 4)], Color: gray: 3,
         Polyomino: [(0, 3), (1, 3), (2, 1), (2, 2), (3, 3), (4, 0), (4, 1), (4, 3)], Color: gray: 4,
         Polyomino: [(0, 4), (1, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 0), (4, 2)], Color: gray: 5,
         Polyomino: [(0, 0), (0, 1), (0, 3), (0, 4), (1, 2), (2, 0), (2, 2), (3, 0)], Color: gray: 6,
         Polyomino: [(0, 0), (0, 2), (1, 0), (1, 1), (1, 3), (2, 2), (3, 0), (4, 0)], Color: gray: 7,
         Polyomino: [(0, 1), (0, 2), (0, 4), (1, 3), (2, 0), (2, 1), (3, 1), (4, 0)], Color: gray: 8,
         Polyomino: [(0, 3), (1, 3), (2, 1), (3, 0), (3, 2), (3, 3), (4, 1), (4, 3)], Color: gray: 9,
         Polyomino: [(0, 4), (1, 2), (1, 4), (2, 2), (3, 0), (3, 1), (3, 3), (3, 4)], Color: gray: 10,
         Polyomino: [(0, 4), (1, 3), (2, 3), (2, 4), (3, 1), (4, 0), (4, 2), (4, 3)], Color: gray: 11}

    """
    monotiles = the_rotated_reflected_monotiles()
    return {p.canonical():i for i,p in enumerate(monotiles)}

class MonotileSolver():
    def __init__(self, width=10, heigth=10):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver()

        """
        self._width = width
        self._height = heigth

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: MonotileSolver(10, 10)
            Monotolie solver W=10, H=10

        """
        return ("Monotolie solver W={}, H={}".format(self._width, self._height))

    def the_box(self):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: MonotileSolver(1,1).the_box()
            Polyomino: [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1,
            2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)], Color: gray
            sage: len(MonotileSolver(1,1).the_box())
            12
            sage: len(MonotileSolver(1,2).the_box())
            24
            sage: len(MonotileSolver(2,1).the_box())
            24
            sage: len(MonotileSolver(2,2).the_box())
            48

        """
        from sage.modules.free_module_element import vector

        hexagon_vertices = [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)]
        hexagon = Polyomino(hexagon_vertices)
        hexagon2 = hexagon + (2,2)
        double_hexagon = Polyomino(list(hexagon) + list(hexagon2))
        #m = matrix.column([(-2,4), (2,2)])
        m = matrix.column([(6,0), (-2,4)])
        L = []
        for i in range(self._width):
            for j in range(self._height):
                v = vector((i,j))
                L.extend(double_hexagon + m*v)
        return Polyomino(L)

    def the_monotiles_in_a_box(self, extra=0, verbose=False):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(1,1)
            sage: len(s.the_monotiles_in_a_box(extra=0))
            24
            sage: len(s.the_monotiles_in_a_box(extra=1))
            216
            sage: len(s.the_monotiles_in_a_box(extra=2))
            600

        """
        from sage.modules.free_module_element import vector
        from sage.matrix.constructor import matrix

        monotiles = the_rotated_reflected_monotiles()
        monotiles2 = [monotile + (2,2) for monotile in monotiles]
        double_canonical_monotiles = monotiles + monotiles2
        m = matrix.column([(6,0), (-2,4)])
        L = []
        start_of_each_tile = []
        for monotile in double_canonical_monotiles:
            start_of_each_tile.append(len(L))
            for i in range(-extra,self._width+extra):
                for j in range(-extra,self._height+extra):
                    v = vector((i,j))
                    L.append(monotile + m*v)
        if verbose:
            print(start_of_each_tile)
        return L

    def row_number_to_coord(self):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(10, 10)
            sage: len(s.row_number_to_coord())
            1200
        """
        box = self.the_box()
        bijection_int_to_coord = dict(enumerate(sorted(box)))
        return bijection_int_to_coord

    @cached_method
    def rows(self, extra=4):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: len(s.rows())
            168

        """
        bijection_int_to_coord = self.row_number_to_coord()
        bijection_coord_to_int = {c:i for (i,c) in bijection_int_to_coord.items()}

        pieces = self.the_monotiles_in_a_box(extra=extra)

        rows = []
        for piece in pieces:
            row = []
            for p in piece:
                i = bijection_coord_to_int.get(p, None)
                if not i is None:
                    row.append(i)
            if row:
                row.sort()
                rows.append(row)
        return rows

    def columns(self, extra=4):
        r"""

        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(1,1)
            sage: s.columns()
            {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
        """
        bijection_int_to_coord = self.row_number_to_coord()
        rows = self.rows(extra=extra)
        s = set()
        for row in rows:
            s.update(row)
        assert s == set(bijection_int_to_coord)
        return s

    def the_dlx_solver(self, extra=4):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(1,1)
            sage: d = s.the_dlx_solver(); d
            Dancing links solver for 12 columns and 60 rows
            sage: d.one_solution()                 # random
            [0, 12, 30]

        Extra = 4 seems sufficeent::

            sage: s = MonotileSolver(2,4)
            sage: s.the_dlx_solver(extra=1)
            Dancing links solver for 96 columns and 288 rows
            sage: s.the_dlx_solver(extra=2)
            Dancing links solver for 96 columns and 288 rows
            sage: s.the_dlx_solver(extra=3)
            Dancing links solver for 96 columns and 288 rows
            sage: s.the_dlx_solver(extra=4)
            Dancing links solver for 96 columns and 288 rows

        No solution?::

            sage: s = MonotileSolver(5,5)
            sage: s.the_dlx_solver(extra=0)
            Dancing links solver for 300 columns and 600 rows
            sage: s.the_dlx_solver(extra=1)
            Dancing links solver for 300 columns and 780 rows
            sage: s.the_dlx_solver(extra=2)
            Dancing links solver for 300 columns and 780 rows
            sage: d = s.the_dlx_solver(extra=2)
            sage: L = d.one_solution()
            sage: type(L)
            <class 'list'>

        """
        rows = self.rows(extra=extra)
        from sage.combinat.matrices.dancing_links import dlx_solver
        return dlx_solver(rows)

    @cached_method
    def one_solution(self, extra=4, solver=None):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.one_solution()           # random
            [5, 4, 89, 108, 79, 62, 24, 86, 21, 25]

        ::

            sage: s = MonotileSolver(8,8)
            sage: s.one_solution(solver='glucose') is not None   # optional glucose
            True

        """
        dlx = self.the_dlx_solver(extra=extra)
        if solver is None:
            return dlx.one_solution()
        else:
            return dlx.one_solution_using_sat_solver(solver=solver)

    def hexagonal_projection(self):
        r"""

        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(20,20)
            sage: s.hexagonal_projection()
            [        1       1/2]
            [        0 1/2*sqrt3]

        """
        from sage.rings.rational_field import QQ
        from sage.rings.polynomial.polynomial_ring import polygen
        x = polygen(QQ, 'x')
        from sage.rings.number_field.number_field import NumberField
        K = NumberField(x**2-3, 'sqrt3', embedding=QQ(1.7))
        sqrt3 = K.gen()
        return matrix.column(K,[(1,0), (.5,sqrt3/2)])

    def plot_domain(self):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.plot_domain()
            Graphics object consisting of 1 graphics primitive
        """
        from sage.plot.point import points
        box = self.the_box()
        M = self.hexagonal_projection()
        return points([M*v for v in box], color='green', size=20)

    def canonical_vertex(self, v):
        r"""
        Return the vertex in the fundamental domain
        [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)]
        which is in the same orbit under
        the translations by matrix.column([(-2,4), (2,2)])

        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: H = [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)]
            sage: s = MonotileSolver(2,2)
            sage: [s.canonical_vertex(h) for h in H]
            [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]

        ::

            sage: set(s.canonical_vertex(v) for v in s.the_box())
            {(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)}

        """
        i,j = v
        # we subtract the base vector (-4,2)
        q = j // 2
        j = j % 2
        i = i - (-4)*q
        # we subtract the base vector (6,0)
        i = i % 6
        # we move closer to the origin
        if i+j>1:
            i -= 2
            j -= 2
        #if i+j<-1:
        #    i += 2
        #    j += 2
        if i > 1:
            i -= 4
            j += 2
        return (i,j)

    def canonical_kite(self, v):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.canonical_kite((2,3))
            [(0, 0), (1, 1), (0, 2), (-1, 2)]

        """
        i,j = self.canonical_vertex(v)
        if (i,j) == (0,1):
            return [(0,0), (1,1), (0,2), (-1,2)]
        elif (i,j) == (-1,1):
            return [(0,0), (-1,2), (-2,2), (-2,1)]
        elif (i,j) == (-1,0):
            return [(0,0), (-2,1), (-2,0), (-1,-1)]
        elif (i,j) == (0,-1):
            return [(0,0), (-1,-1), (0,-2), (1,-2)]
        elif (i,j) == (1,-1):
            return [(0,0), (1,-2), (2,-2), (2,-1)]
        elif (i,j) == (1,0):
            return [(0,0), (2,-1), (2,0), (1,1)]
        else:
            raise ValueError("i={},j={} not canonical vertex".format(i,j))

    def plot_kite(self, v, color, **kwds):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: G = s.plot_domain() + s.plot_kite((2,3), color='red')

        """
        from sage.plot.polygon import polygon
        vc = vector(self.canonical_vertex(v))
        kite = [vector(p) for p in self.canonical_kite(v)]
        v = vector(v)
        M = self.hexagonal_projection()
        vertices = [M*(v-vc+p) for p in kite]
        return polygon(vertices, color=color, **kwds)

    def kite_edges(self, v):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.kite_edges((2,3))
            [((3, sqrt3), (9/2, 3/2*sqrt3)),
             ((9/2, 3/2*sqrt3), (4, 2*sqrt3)),
             ((4, 2*sqrt3), (3, 2*sqrt3)),
             ((3, 2*sqrt3), (3, sqrt3))]

        """
        vc = vector(self.canonical_vertex(v))
        kite = [vector(p) for p in self.canonical_kite(v)]
        v = vector(v)
        M = self.hexagonal_projection()
        vertices = [M*(v-vc+p) for p in kite]
        for v in vertices:
            v.set_immutable()
        len_v = len(vertices)
        edges = [(vertices[i],vertices[(i+1)%len_v]) for i in range(len_v)]
        return edges

    def draw_the_12_shapes(self):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.draw_one_solution()
            Graphics object consisting of 17 graphics primitives

        """
        from sage.plot.graphics import Graphics
        from sage.misc.prandom import choice
        from sage.plot.point import points
        from sage.plot.colors import colors

        monotiles = the_rotated_reflected_monotiles()

        # Graphics
        G = Graphics()
        M = self.hexagonal_projection()

        # draw the domain
        G += self.plot_domain()

        # draw
        list_of_colors = list(colors)
        for i,monotile in enumerate(monotiles):
            vertices = list(monotile + (6*i,0))
            color = choice(list_of_colors)
            V = [M*v for v in vertices]
            G += points(V, color=color, size=50)
            for v in vertices:
                G += self.plot_kite(v, color=color)

        return G

    def draw_one_solution(self, ignore_incomplete=True, extra=4,
            solver=None, color_by_id=False, illustrate_3_mod_6=False):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.draw_one_solution()
            Graphics object consisting of ... graphics primitives

        """
        from sage.plot.graphics import Graphics
        from sage.misc.prandom import choice
        from sage.plot.point import points
        from sage.plot.colors import rainbow
        from sage.plot.colors import colors

        # dlx data
        rows = self.rows(extra=extra)
        bijection_int_to_coord = self.row_number_to_coord()

        # Graphics
        G = Graphics()
        M = self.hexagonal_projection()

        # draw the domain
        G += self.plot_domain()

        # find a solution
        solution = self.one_solution(extra=extra, solver=solver)
        #d = self.tile_positions_in_solution(solution, extra=extra)

        D = the_canonical_12_monotiles()
        rainbow12 = rainbow(12)

        # draw a solution
        list_of_colors = list(colors)
        for n_row in solution:
            vertices = [bijection_int_to_coord[i] for i in rows[n_row]]
            if ignore_incomplete and len(vertices) < 8:
                continue
            if color_by_id and len(vertices) == 8:
                P = Polyomino(vertices)
                P_canonical = P.canonical()
                id = D[P_canonical]
                color = rainbow12[id]
                (x,y) = next(iter(P)) - next(iter(P_canonical))
                if illustrate_3_mod_6 and (x-y)%6 == 3:
                    kwds = dict(edgecolor='red', thickness=1, alpha=0.5)
                else:
                    kwds = {}
            else:
                color = choice(list_of_colors)
                kwds = {}
            for v in vertices:
                G += self.plot_kite(v, color=color, **kwds)

        return G

    def one_solution_list_of_edges(self, ignore_incomplete=True, extra=4, solver=None):
        r"""
        Return the list of edges of a solution.

        Each edge appears only once in the output. This allows to avoid the
        laser cut machine to pass twice at the same place.

        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: L = s.one_solution_list_of_edges()
            sage: sorted(L)                                # random
            [frozenset({(3, 0), (4, 0)}),
             frozenset({(3, 2*sqrt3), (4, 2*sqrt3)}),
             frozenset({(-3/2, 1/2*sqrt3), (-1, sqrt3)}),
             frozenset({(0, sqrt3), (0, 2*sqrt3)}),
             frozenset({(3, sqrt3), (3, 2*sqrt3)}),
             frozenset({(9/2, -1/2*sqrt3), (6, 0)}),
             frozenset({(9/2, 5/2*sqrt3), (6, 2*sqrt3)}),
             frozenset({(6, 0), (6, sqrt3)}),
             frozenset({(0, 0), (3/2, 1/2*sqrt3)}),
             frozenset({(-1, sqrt3), (0, sqrt3)}),
             frozenset({(0, 2*sqrt3), (3/2, 5/2*sqrt3)}),
             frozenset({(6, sqrt3), (7, sqrt3)}),
             frozenset({(15/2, 3/2*sqrt3), (8, 2*sqrt3)}),
             frozenset({(6, 2*sqrt3), (15/2, 5/2*sqrt3)}),
             frozenset({(4, 0), (9/2, 1/2*sqrt3)}),
             frozenset({(3/2, 1/2*sqrt3), (2, 0)}),
             frozenset({(4, 2*sqrt3), (9/2, 5/2*sqrt3)}),
             frozenset({(-3/2, 1/2*sqrt3), (0, 0)}),
             frozenset({(7, sqrt3), (15/2, 3/2*sqrt3)}),
             frozenset({(3/2, 5/2*sqrt3), (2, 2*sqrt3)}),
             frozenset({(4, 0), (9/2, -1/2*sqrt3)}),
             frozenset({(2, 2*sqrt3), (3, 2*sqrt3)}),
             frozenset({(2, 0), (3, 0)}),
             frozenset({(3, sqrt3), (9/2, 1/2*sqrt3)}),
             frozenset({(15/2, 5/2*sqrt3), (8, 2*sqrt3)})]
            sage: sum(line(edge) for edge in L)
            Graphics object consisting of ... graphics primitives

        """
        from collections import Counter

        # dlx data
        rows = self.rows(extra=extra)
        bijection_int_to_coord = self.row_number_to_coord()
        solution = self.one_solution(extra=extra, solver=solver)

        # gather the boundary edges of the pieces of a solution
        edges = set()
        for n_row in solution:
            vertices = [bijection_int_to_coord[i] for i in rows[n_row]]
            if ignore_incomplete and len(vertices) < 8:
                continue

            c = Counter()
            for v in vertices:
                for edge in self.kite_edges(v):
                    edge = frozenset(edge)
                    c[edge] += 1
            assert set(c.values()) <= set([1,2])
            boundary_edges = [edge for edge in c if c[edge] == 1]

            edges.update(boundary_edges)

        return edges

    def one_solution_tikz(self, ignore_incomplete=True, extra=4, solver=None):
        r"""
        Return the list of edges of a solution.

        Each edge appears only once in the output. This allows to avoid the
        laser cut machine to pass twice at the same place.

        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s.one_solution_tikz()
            \documentclass[tikz]{standalone}
            \begin{document}
            \begin{tikzpicture}
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            ...
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            \draw[red] (..., ...) -- (..., ...);
            \end{tikzpicture}
            \end{document}

        """
        edges = self.one_solution_list_of_edges(ignore_incomplete=ignore_incomplete,
                                                extra=extra, 
                                                solver=solver)
        edges = sorted(edges)

        lines = []
        lines.append(r"\begin{tikzpicture}")
        for edge in edges:
            x,y = edge
            lines.append(r"\draw[red] {} -- {};".format(x.n(),y.n()))
        lines.append(r"\end{tikzpicture}")
        from sage.misc.latex_standalone import TikzPicture
        return TikzPicture('\n'.join(lines))


    def tile_positions_in_solution(self, solution, extra=4):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(4,4)
            sage: solution = s.one_solution()
            sage: s.tile_positions_in_solution(solution)    # random
            {0: [(3, 5), (-5, 9), (5, 1), (9, 5)],
             1: [(3, 10)],
             2: [(0, 3)],
             3: [(8, 0), (12, 4), (16, 2)],
             4: [(13, 0), (5, 10), (11, 10)],
             5: [(-2, 7)],
             7: [(10, 9)],
             9: [(4, 6)],
             11: [(-5, 4)]}

        """
        # dlx data
        rows = self.rows(extra=extra)
        bijection_int_to_coord = self.row_number_to_coord()

        M = self.hexagonal_projection()

        D = the_canonical_12_monotiles()

        from collections import defaultdict
        positions = defaultdict(list)

        for n_row in solution:
            vertices = [bijection_int_to_coord[i] for i in rows[n_row]]
            if len(vertices) < 8:
                continue
            assert len(vertices) == 8

            P = Polyomino(vertices)
            P_canonical = P.canonical()
            id = D[P_canonical]
            
            position = next(iter(P)) - next(iter(P_canonical))

            positions[id].append(position)

        return dict(positions)

    def _draw_all(self, ignore_incomplete=True, extra=4):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s._draw_all()                       # long time (1s)
            Graphics object consisting of 325 graphics primitives

        """
        from sage.plot.graphics import Graphics
        from sage.misc.prandom import choice
        from sage.plot.point import points
        from sage.plot.colors import colors

        # dlx data
        rows = self.rows(extra=extra)
        bijection_int_to_coord = self.row_number_to_coord()

        # Graphics
        G = Graphics()
        M = self.hexagonal_projection()

        # draw the domain
        G += self.plot_domain()

        # find a solution
        #solution = self.one_solution(extra=extra)
        #L = [Polyomino for n_row in solution]

        # draw a solution
        list_of_colors = list(colors)
        #s_rows = sorted(list(enumerate(rows)), key=lambda t:len(t[1]))
        #for n_row,_ in s_rows:
        for n_row in range(len(rows)):
            vertices = [bijection_int_to_coord[i] for i in rows[n_row]]
            if ignore_incomplete and len(vertices) < 8:
                continue
            color = choice(list_of_colors)
            V = [M*v for v in vertices]
            G += points(V, color=color, size=50)
            for v in vertices:
                G += self.plot_kite(v, color=color)

        return G



    def _draw_row(self, n_row, extra=4):
        r"""
        EXAMPLES::

            sage: from slabbe.aperiodic_monotile import MonotileSolver
            sage: s = MonotileSolver(2,2)
            sage: s._draw_row(0)
            Graphics object consisting of 4 graphics primitives

        """
        from sage.plot.graphics import Graphics
        from sage.misc.prandom import choice
        from sage.plot.point import points
        from sage.plot.colors import colors

        # dlx data
        rows = self.rows(extra=extra)
        bijection_int_to_coord = self.row_number_to_coord()

        # Graphics
        G = Graphics()
        M = self.hexagonal_projection()

        # draw the domain
        G += self.plot_domain()

        # find a solution
        #solution = self.one_solution(extra=extra)
        #L = [Polyomino for n_row in solution]

        list_of_colors = list(colors)

        vertices = [bijection_int_to_coord[i] for i in rows[n_row]]
        color = choice(list_of_colors)
        V = [M*v for v in vertices]
        G += points(V, color=color, size=50)
        for v in vertices:
            G += self.plot_kite(v, color=color)

        return G



# -*- coding: utf-8 -*-
r"""
Tiling of the plane by isometric copies of a polygon

EXAMPLES::

    sage: F = AffineGroup(2, AA)
    sage: F([1,2,3,4],[5,6])
          [1 2]     [5]
    x |-> [3 4] x + [6]

AUTHORS:

 - Fait avec Lucas <lfx337@gmail.com>, le 28 novembre 2024.

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
from sage.groups.affine_gps.affine_group import AffineGroup

class PolygonTiling:
    r"""
    A periodic tiling by one polygon
    """
    def __init__(self, polygon, patch_symmetries=None, translations=None, ring=None):
        r"""
        INPUT:

        - ``polygon`` -- list of vertices
        - ``patch_symmetries`` -- list of transformations (affine maps)
        - ``translations`` -- list of vectors
        - ``ring`` -- ring (default:``None``), if ``None``, then is uses ``AA``

        EXAMPLES::

            sage: from slabbe.polygon_tiling import PolygonTiling
            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: J = PolygonTiling(jennifer)
            sage: J
            Tiling by the polygon [(0, 0), (1, 0), (2.732050807568878?,
            1), (1.866025403784439?, 3/2), (0, 1)]

        """
        if ring is None:
            from sage.rings.qqbar import AA
            ring = AA

        from sage.modules.free_module_element import vector
        self._polygon = [vector(ring, p) for p in polygon]

        if patch_symmetries is None:
            F = AffineGroup(2, ring)
            self._patch_symmetries = [F.one()]
        else:
            self._patch_symmetries = patch_symmetries

        if translations is None:
            F = AffineGroup(2, ring)
            self._translations = [F.one()]
        else:
            self._translations = translations

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe.polygon_tiling import PolygonTiling
            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: J = PolygonTiling(jennifer)
            sage: J
            Tiling by the polygon [(0, 0), (1, 0), (2.732050807568878?,
            1), (1.866025403784439?, 3/2), (0, 1)]

        """
        return "Tiling by the polygon {}".format(self._polygon)

    def vertex_distances(self):
        r"""
        EXAMPLES::

            sage: from slabbe.polygon_tiling import PolygonTiling
            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: J = PolygonTiling(jennifer)
            sage: J.vertex_distances()
            [1, 2.000000000000000?, 1.000000000000000?, 1.931851652578137?, 1]

        """
        N = len(self._polygon)
        distances = []
        for i in range(N):
            p = self._polygon[i]
            q = self._polygon[(i+1)%N]
            v = q - p
            distances.append(v.norm())
        return distances

    def patch(self):
        r"""

        EXAMPLES::

            sage: from slabbe.polygon_tiling import PolygonTiling
            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: J = PolygonTiling(jennifer)
            sage: J.patch()
            [[(0, 0),
              (1, 0),
              (2.732050807568878?, 1),
              (1.866025403784439?, 1.5000000000000000?),
              (0, 1)]]

        """
        return [[s*v for v in self._polygon] for s in self._patch_symmetries]

    def polygons(self):
        pass

    def plot(self):
        r"""
        EXAMPLES::

            sage: from slabbe.polygon_tiling import PolygonTiling
            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: J = PolygonTiling(jennifer)
            sage: J.plot()
            Graphics object consisting of 1 graphics primitive


        ::

            sage: jennifer = [(0,0), (1,0), (1+sqrt(3),1), (1+sqrt(3)/2,3/2), (0,1)]
            sage: F = AffineGroup(2, AA)
            sage: patch_symmetries = [F.one(), F.translation((2,2))]
            sage: J = PolygonTiling(jennifer, patch_symmetries)
            sage: J.plot()
            Graphics object consisting of 2 graphics primitives

        """
        from sage.plot.graphics import Graphics
        from sage.plot.polygon import polygon2d
        G = Graphics()
        for p in self.patch():
            G += polygon2d(p, fill=False, thickness=4, color='orange')
        return G

def symmetrie(p1, p2):
    r"""
    Return la transformation lineraire qui fait la symmetrie dans la droite
    passant par p1 et p2.
    
    EXAMPLES::

        sage: from slabbe.polygon_tiling import symmetrie
        sage: p1 = (12,166)
        sage: p2 = (45,227)
        sage: T = symmetrie(p1, p2)
        sage: T
              [-1316/2405  2013/2405]     [-289506/2405]
        x |-> [ 2013/2405  1316/2405] x + [ 156618/2405]
        sage: T(p1)
        (12, 166)
        sage: T(p2)
        (45, 227)

    """
    from sage.matrix.constructor import matrix
    from sage.rings.qqbar import AA
    F = AffineGroup(2, AA)
    F_p1 = F.translation(p1)
    (x2,y2) = F_p1.inverse()(p2)
    F_rotate_p2 = F(matrix.column([(x2,y2),(-y2,x2)]))
    F_symmetry = F(matrix.column([(1,0),(0,-1)]))
    T = (F_p1 * F_rotate_p2 * F_symmetry * F_rotate_p2.inverse() * F_p1.inverse())
    assert tuple(p1) == tuple(T(p1)), "{} == {}".format(p1, T(p1))
    assert tuple(p2) == tuple(T(p2)), "{} == {}".format(p2, T(p2))
    return T

def symmetrie_mediatrice(p1, p2):
    r"""
    Return la transformation lineraire qui fait la symmetrie dans la
    mediatrice du segment passant par p1 et p2.
    
    EXAMPLES::

        sage: from slabbe.polygon_tiling import symmetrie_mediatrice
        sage: p1 = (12,166)
        sage: p2 = (45,227)
        sage: T = symmetrie_mediatrice(p1, p2)
        sage: T
              [ 1316/2405 -2013/2405]     [426591/2405]
        x |-> [-2013/2405 -1316/2405] x + [788547/2405]
        sage: T(p1)
        (45, 227)
        sage: T(p2)
        (12, 166)

    """
    from sage.matrix.constructor import matrix
    from sage.rings.qqbar import AA
    F = AffineGroup(2, AA)
    F_p1 = F.translation(p1)
    (x2,y2) = F_p1.inverse()(p2)
    F_rotate_p2 = F(matrix.column([(x2,y2),(-y2,x2)]))
    F_symmetry = F(matrix.column([(-1,0),(0,1)]),(1,0))
    T = (F_p1 * F_rotate_p2 * F_symmetry * F_rotate_p2.inverse() * F_p1.inverse())
    assert tuple(p2) == tuple(T(p1)), "{} == {}".format(p2, T(p1))
    assert tuple(p1) == tuple(T(p2)), "{} == {}".format(p1, T(p2))
    return T

def Jennifer():
    r"""
    EXAMPLES::

        sage: from slabbe.polygon_tiling import Jennifer
        sage: Jennifer()
        Tiling by the polygon [(0, 0), (1, 0), (1.866025403784439?, 1/2),
        (2.732050807568878?, 1), (1.866025403784439?, 3/2), (0, 1)]

    """
    from sage.misc.functional import sqrt
    from sage.rings.rational_field import QQ
    from sage.rings.qqbar import AA
    A = (0,0) 
    B1 = (1,0)
    B2 = (1+sqrt(3)/2,QQ(1/2))
    C = (1+sqrt(3),1)
    D = (1+sqrt(3)/2,QQ(3/2))
    E = (0,1)
    jennifer = [A, B1, B2, C, D, E]

    # transformations
    F = AffineGroup(2, AA)
    rotate30 = F([sqrt(3)/2,QQ(1/2),-QQ(1/2),sqrt(3)/2])
    exchange_xy = F([0,1,1,0])

    patch3 = [F.one(), 
              #rotate30,
              F.translation(D)*rotate30*exchange_xy,
              symmetrie(D, E),
              ]

    g = F.translation((-QQ(1/2), sqrt(3)/2 + 1))
    patch6 = [t for t in patch3]
    patch6.extend(g*rotate30.inverse()*exchange_xy*t for t in patch3)

    #h1 = (sqrt(3)*3/2 + QQ(3/2), sqrt(3)/2 + QQ(5/2))
    #h2 = (sqrt(3)*3/2 + QQ(3/2), sqrt(3)/2 + QQ(3/2))
    #h1 = (sqrt(3)/2 - QQ(1/2), sqrt(3)*3/2 + QQ(7/2))
    h1 = (-QQ(1/2), sqrt(3)*3/2 + 4)
    h2 = (sqrt(3)/2 - QQ(1/2), sqrt(3)*3/2 + QQ(9/2))
    h  = symmetrie(h1, h2)
    hm = symmetrie_mediatrice(h1, h2)
    patch12 = [t for t in patch6]
    patch12.extend(hm*h*t for t in patch6)

    J = PolygonTiling(jennifer, patch12)
    return J

#J = Jennifer()



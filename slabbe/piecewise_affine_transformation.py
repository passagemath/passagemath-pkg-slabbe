# -*- coding: utf-8 -*-
r"""
Piecewise affine transformations and induced transformations

EXAMPLES:

Recall how to create affine maps::

    sage: F = AffineGroup(3, QQ); F
    Affine Group of degree 3 over Rational Field
    sage: M = matrix(QQ,[[1,2,3],[4,5,6],[7,8,0]])
    sage: v = vector(QQ,[10,11,12])
    sage: F(M, v)
          [1 2 3]     [10]
    x |-> [4 5 6] x + [11]
          [7 8 0]     [12]
    sage: F.linear(M)
          [1 2 3]     [0]
    x |-> [4 5 6] x + [0]
          [7 8 0]     [0]
    sage: F.translation(v)
          [1 0 0]     [10]
    x |-> [0 1 0] x + [11]
          [0 0 1]     [12]

A polyhedron partition::

    sage: from slabbe import PolyhedronPartition
    sage: h = 1/3
    sage: p = Polyhedron([(0,h),(0,1),(h,1)])
    sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
    sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
    sage: s = Polyhedron([(h,0), (1,0), (1,h)])
    sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s})

Inducing a piecewise affine transformation on a sub-domain::

    sage: from slabbe import PolyhedronPartition
    sage: from slabbe import PiecewiseAffineTransformation
    sage: h = 1/3
    sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
    sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
    sage: P = PolyhedronPartition({0:p, 1:q})
    sage: F = AffineGroup(2, QQ)
    sage: M = matrix(2, [0,1,1,0])
    sage: f0 = F(M, (0, 2/3))
    sage: f1 = F(M, (0, -1/3))
    sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
    sage: ieq = [1/2, -1, 0]   # x0 <= 1/2
    sage: T_induced,sub = T.induced_transformation(ieq)
    sage: T_induced.pp()
    Piecewise Affine Transformation given by a
    Polyhedron partition of 6 atoms with 6 letters
    defined by 6 affine maps:
    Affine map 0:
          [0 1]     [  0]
    x |-> [1 0] x + [2/3]
    Affine map 1:
          [0 1]     [   0]
    x |-> [1 0] x + [-1/3]
    Affine map 2:
          [1 0]     [-1/3]
    x |-> [0 1] x + [-1/3]
    Affine map 3:
          [0 1]     [-1/3]
    x |-> [1 0] x + [ 1/3]
    Affine map 4:
          [1 0]     [ 1/3]
    x |-> [0 1] x + [-2/3]
    Affine map 5:
          [0 1]     [-2/3]
    x |-> [1 0] x + [   0]
    sage: sub
    {0: [0], 1: [1], 2: [1, 1], 3: [0, 1, 1], 4: [0, 1, 1, 1], 5: [0, 1, 1, 1, 1]}

AUTHORS:

- Sébastien Labbé, January 2019, added a class for polyhedron exchange transformations
- Sébastien Labbé, September 15, 2023, translated PET into piecewise affine transformations
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
from sage.geometry.polyhedron.constructor import Polyhedron
from slabbe import PolyhedronPartition

class PiecewiseAffineTransformation(object):
    r"""
    Piecewise Affine Transformation (PAT).

    INPUT:

    - ``partition`` -- a polyhedron partition (with associated indices)
    - ``affine_maps`` -- list or dict, associating each index with an affine map
    - ``affine_group`` -- affine group (default:``None``), the affine group
      in which the affine maps live. If ``None``, it takes the parent of
      the first affine map as default value.

    EXAMPLES:

    Create Polyhedron partition::

        sage: from slabbe import PolyhedronPartition
        sage: h = 1/3
        sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
        sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
        sage: P = PolyhedronPartition({0:p, 1:q})

    Create affine maps::

        sage: F = AffineGroup(2, QQ)
        sage: M = matrix(2, [0,1,1,0])
        sage: f0 = F(M, (0, 2/3))
        sage: f1 = F(M, (0, -1/3))

    Create a piecewise affine transformation::

        sage: from slabbe import PiecewiseAffineTransformation
        sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})

    TESTS:

    Works with general indices::

        sage: P = PolyhedronPartition({'a':p, 'b':q})
        sage: T = PiecewiseAffineTransformation(P, {'a':f0, 'b':f1})

    """
    def __init__(self, partition, affine_maps, affine_group=None):
        r"""
        See :class:`PiecewiseAffineTransformation` for documentation.

        EXAMPLES::

            sage: from slabbe import PiecewiseAffineTransformation

        """
        if isinstance(partition, PolyhedronPartition):
            self._partition = partition
        else:
            raise TypeError('partition(={}) must be a '
                            'PolyhedronPartition'.format(partition))
        self._ambient_space = self._partition.ambient_space()

        if affine_group is None:
            if affine_maps:
                if isinstance(affine_maps, list):
                    some_map = affine_maps[0]
                elif isinstance(affine_maps, dict):
                    some_map = next(iter(affine_maps.values()))
                self._affine_group = some_map.parent()
            else:
                raise ValueError("can't guess the affine group from an"
                        " empty list of affine maps")
        else:
            self._affine_group = affine_group

        if isinstance(affine_maps, list):
            self._affine_maps = {a:self._affine_group(f) for (a,f) in enumerate(affine_maps)}
        elif isinstance(affine_maps, dict):
            self._affine_maps = {a:self._affine_group(f) for (a,f) in affine_maps.items()}
        else:
            raise TypeError('affine_maps(={}) must be a '
                            'list or dict'.format(affine_maps))

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T
            Piecewise Affine Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps

        """
        return ('Piecewise Affine Transformation of\n{}\ndefined by '
               '{} affine maps').format(self._partition,
                       len(self._affine_maps))

    def pp(self):
        r"""
        Pretty print

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.pp()
            Piecewise Affine Transformation given by a
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps:
            Affine map 0:
                  [0 1]     [  0]
            x |-> [1 0] x + [2/3]
            Affine map 1:
                  [0 1]     [   0]
            x |-> [1 0] x + [-1/3]

        """
        print(('Piecewise Affine Transformation given by a\n{}\ndefined by '
            '{} affine maps:').format(self._partition,
                       len(self._affine_maps)))

        for (a,f) in self._affine_maps.items():
            print("Affine map {}:".format(a))
            print(f)

    def partition(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.partition()
            Polyhedron partition of 2 atoms with 2 letters

        This code also handle PETs::

            sage: from slabbe import PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: d = {0:(1-h,0), 1:(-h,0)}
            sage: T = PolyhedronExchangeTransformation(P, d)
            sage: T.partition()
            Polyhedron partition of 2 atoms with 2 letters

        """
        return self._partition

    def affine_maps(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: d = T.affine_maps()
            sage: type(d)
            <class 'dict'>

        """
        return self._affine_maps

    def ambient_space(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.ambient_space()
            Vector space of dimension 2 over Rational Field

        This code also handle PETs::

            sage: from slabbe import PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F.ambient_space()
            Vector space of dimension 2 over Rational Field

        """
        return self._ambient_space

    def affine_group(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.affine_group()
            Affine Group of degree 2 over Rational Field

        """
        return self._affine_group

    def image_partition(self):
        r"""
        Return the partition of the image.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.image_partition()
            Polyhedron partition of 2 atoms with 2 letters

        It works also for PETs::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F.image_partition()
            Polyhedron partition of 2 atoms with 2 letters

        ::

            sage: h = 1/3
            sage: p = Polyhedron([(0,h),(0,1),(h,1)])
            sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
            sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
            sage: s = Polyhedron([(h,0), (1,0), (1,h)])
            sage: P = PolyhedronPartition([(0,p), (0,q), (1,r), (1,s)])
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F.image_partition()
            Polyhedron partition of 4 atoms with 2 letters

        """
        return PolyhedronPartition([(a,self._affine_maps[a](p))
                                    for (a,p) in self._partition])

    def domain(self):
        r"""
        Return the domain of the transformation.

        OUTPUT:

            a polyhedron

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.domain()
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices
            sage: T.domain().vertices()
            (A vertex at (0, 0),
             A vertex at (0, 1),
             A vertex at (1, 0),
             A vertex at (1, 1))

        This code also handle PETs::

            sage: from slabbe import PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F.domain()
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices
            sage: F.domain().vertices()
            (A vertex at (0, 0),
             A vertex at (0, 1),
             A vertex at (1, 0),
             A vertex at (1, 1))
        """
        return self.partition().domain()

    def plot(self):
        r"""
        Return a image representating the domain and image partition
        side-to-side.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.plot()
            Graphics Array of size 1 x 2

        Title is still placed correctly if size of domain changes::

            sage: (5*T).plot()
            Graphics Array of size 1 x 2

        This code also works for PETs::

            sage: from slabbe import PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: d = {0:(1-h,0), 1:(-h,0)}
            sage: T = PolyhedronExchangeTransformation(P, d)
            sage: T.plot()
            Graphics Array of size 1 x 2

        """
        from sage.plot.text import text
        from sage.plot.plot import graphics_array

        # computing the range of the domain in each dimension
        V = self.domain().vertices()
        MAX = list(map(max, *V))
        MIN = list(map(min, *V))

        title_position = ((MIN[0]+MAX[0])/2., MAX[1]*1.08)

        P = self.partition().plot()
        Q = self.image_partition().plot()
        tP = text(r"domain partition", title_position, fontsize=10)
        tQ = text(r"image partition", title_position, fontsize=10)
        return graphics_array([P + tP,  Q + tQ])

    def inverse(self):
        r"""
        Return the inverse of self.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: T.pp()
            Piecewise Affine Transformation given by a
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps:
            Affine map 0:
                  [0 1]     [  0]
            x |-> [1 0] x + [2/3]
            Affine map 1:
                  [0 1]     [   0]
            x |-> [1 0] x + [-1/3]
            sage: T.inverse().pp()
            Piecewise Affine Transformation given by a
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps:
            Affine map 0:
                  [0 1]     [-2/3]
            x |-> [1 0] x + [   0]
            Affine map 1:
                  [0 1]     [1/3]
            x |-> [1 0] x + [  0]

        """
        P = self.image_partition()
        T = {a:f.inverse() for (a,f) in self._affine_maps.items()}
        return PiecewiseAffineTransformation(P, T,
                affine_group=self.affine_group())

    def __eq__(self, other):
        r"""
        Return whether two piecewise affine transformations are equal.

        INPUT:

        - ``other`` -- piecewise affine transformation

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: U = PiecewiseAffineTransformation(P, {1:f1, 0:f0})
            sage: T == U
            True

        """
        return (isinstance(other, PiecewiseAffineTransformation)
                and self._partition == other._partition
                and self._affine_maps == other._affine_maps)

    def _affine_maps_immutable(self):
        r"""
        Return the affine maps as a dict of immutable tuple (A,b).

        This is to avoid the issue that `f.set_immutable()` does not exist
        for affine map in Sage.

        .. TODO:: add the method `f.set_immutable()` 

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,1/2), (1,1), (h,1), (h,1/2)])
            sage: r = Polyhedron([(1,0), (1,1/2), (h,1/2), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1, 2:f1})
            sage: _ = T._affine_maps_immutable()

        """
        d = {}
        for (key,f) in self.affine_maps().items():
            A = f.A()
            b = f.b()
            A.set_immutable()
            b.set_immutable()
            Ab_immutable = (A,b)
            d[key] = Ab_immutable
            
            # test that hash works
            hash(Ab_immutable)
        return d

    def merge_atoms_with_same_transformation(self):
        r"""
        Return a new partition into convex polyhedrons where atoms mapped
        by the same transformation are merged if their union is convex.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,1/2), (1,1), (h,1), (h,1/2)])
            sage: r = Polyhedron([(1,0), (1,1/2), (h,1/2), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1, 2:f1})
            sage: T
            Piecewise Affine Transformation of
            Polyhedron partition of 3 atoms with 3 letters
            defined by 3 affine maps
            sage: T.merge_atoms_with_same_transformation()
            Piecewise Affine Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps

        """
        from collections import defaultdict

        # a dictionary affine map -> list of keys
        d = defaultdict(list)
        for (key,Ab_immutable) in self._affine_maps_immutable().items():
            d[Ab_immutable].append(key)

        # a dictionary affine map -> a unique atom key (the minimum)
        d = {Ab:min(d[Ab]) for Ab in d}

        # a dictionary key -> new key
        d = {a:d[Ab_immutable] for a,Ab_immutable in self._affine_maps_immutable().items()}

        # merged partition
        P = self.partition().merge_atoms(d)

        # a dictionary of translations with the new keys
        affine_maps_dict = self.affine_maps()
        affine_maps_dict = {a:affine_maps_dict[a] for a in d.values()}

        return PiecewiseAffineTransformation(P, affine_maps_dict)

    def __mul__(self, other):
        r"""
        Return the product of piecewise affine transformations

        INPUT:

        - ``other`` -- piecewise affine transformation

        OUTPUT:

        - piecewise affine transformation

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: (T*T).pp()
            Piecewise Affine Transformation given by a
            Polyhedron partition of 4 atoms with 4 letters
            defined by 4 affine maps:
            Affine map 0:
                  [1 0]     [2/3]
            x |-> [0 1] x + [2/3]
            Affine map 1:
                  [1 0]     [ 2/3]
            x |-> [0 1] x + [-1/3]
            Affine map 2:
                  [1 0]     [-1/3]
            x |-> [0 1] x + [ 2/3]
            Affine map 3:
                  [1 0]     [-1/3]
            x |-> [0 1] x + [-1/3]

        """
        if not isinstance(other, PiecewiseAffineTransformation):
            return NotImplemented
        R,d = self.image_partition().refinement(other.partition(),
                                                certificate=True)

        atoms_dict = {}
        trans_dict = {}
        for key,atom in R:
            (a,b) = d[key]
            f_a = self._affine_maps[a]
            f_b = other._affine_maps[b]
            atoms_dict[key] = f_a.inverse()(atom)
            trans_dict[key] = f_b * f_a

        P = PolyhedronPartition(atoms_dict)
        return PiecewiseAffineTransformation(P, trans_dict)

    def __rmul__(self, factor):
        r"""
        Returns the PET scaled by some factor.

        INPUT:

        - ``factor`` -- real number or matrix or affine map

        OUTPUT:

        - piecewise affine transformation

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: 2 * T
            Piecewise Affine Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps
            sage: -2 * T
            Piecewise Affine Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps
            sage: M * T
            Piecewise Affine Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            defined by 2 affine maps

        """
        if isinstance(factor, PiecewiseAffineTransformation):
            return NotImplemented
        factor = self.affine_group()(factor)
        P = factor * self.partition()
        trans_dict = {key:factor*f*factor.inverse() for (key,f) in self.affine_maps().items()}
        return PiecewiseAffineTransformation(P, trans_dict)

    def __call__(self, p, niterations=1):
        r"""
        Apply the transformation.

        INPUT:

        - ``p`` -- vector or polyhedron or partition
        - ``niterations`` -- nonnegative integer (default: ``1``)

        OUTPUT:

            vector or polyhedron or partition of polyhedron

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})

        Image of a vector::

            sage: T((1/10, 1/10))
            (1/10, 23/30)

        Image of a polyhedron::

            sage: T(p)
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices

        Image of a partition into polyhedron::

            sage: T(P)
            Polyhedron partition of 2 atoms with 2 letters

        Doing many iterations::

            sage: T((1/10, 1/10), niterations=5)
            (13/30, 1/10)
            sage: T(p, niterations=1)
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices
            sage: T(P, niterations=5)
            Polyhedron partition of 9 atoms with 2 letters
            sage: T((1/10, 1/10), niterations=0)
            (1/10, 1/10)

        This code also works for PETs::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F((1/10, 1/10))
            (23/30, 1/10)
            sage: F(p)
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices
            sage: F(P)
            Polyhedron partition of 2 atoms with 2 letters
            sage: F((1/10, 1/10), niterations=5)
            (13/30, 1/10)
            sage: F(p, niterations=5)
            A 2-dimensional polyhedron in QQ^2 defined as the convex hull of 4 vertices
            sage: F(P, niterations=5)
            Polyhedron partition of 3 atoms with 2 letters

        TESTS::


            sage: from slabbe import PolyhedronPartition
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: u = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: uP = u(P); uP
            Polyhedron partition of 2 atoms with 2 letters
            sage: uP.volume()
            1
            sage: uuP = u(uP); uuP
            Polyhedron partition of 4 atoms with 2 letters
            sage: uuP.volume()
            1

        This code also works for PETs::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: h = 1/3
            sage: p = Polyhedron([(0,h),(0,1),(h,1)])
            sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
            sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
            sage: s = Polyhedron([(h,0), (1,0), (1,h)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s})
            sage: base = identity_matrix(2)
            sage: translation = vector((2/3, 0))
            sage: u = PET.toral_translation(base, translation)
            sage: uP = u(P); uP
            Polyhedron partition of 4 atoms with 4 letters
            sage: uP.volume()
            1
            sage: uuP = u(uP); uuP
            Polyhedron partition of 6 atoms with 4 letters
            sage: uuP.volume()
            1

        """
        from sage.structure.element import Vector
        from sage.geometry.polyhedron.base import Polyhedron_base

        if not niterations >= 0:
            raise NotImplementedError("niterations(={}) supported only"
                    " when >= 0".format(niterations))

        if isinstance(p, (tuple, Vector)):
            p = self.ambient_space()(p)
            for _ in range(niterations):
                a = self._partition.code(Polyhedron([p]))
                t = self._affine_maps[a]
                p = t(p)
            return p

        elif isinstance(p, Polyhedron_base):
            for j in range(niterations):
                S = set(i for i,atom in self._partition if p <= atom)
                if len(S) == 1:
                    a = next(iter(S))
                    t = self._affine_maps[a]
                    p = t(p)
                elif len(S) > 1:
                    raise ValueError('During {}-th iteration, image of {} is not' 
                    ' well-defined as it belongs to many distinct atoms(={})' 
                    ' of the partition'.format(j,p,S))
                else:
                    raise ValueError('During {}-th iteration, image of polyhedron' 
                    ' (={}) is not defined as it overlaps distinct'
                    ' atoms of the partition'.format(j,p))
            return p

        elif isinstance(p, PolyhedronPartition):
            for _ in range(niterations):
                p,d = p.refinement(self._partition, certificate=True)
                L = []
                for key,atom in p:
                    good_key,pet_key = d[key]
                    a = self._partition.code(atom)
                    assert a == pet_key, "I think this is true (to check)"
                    t = self._affine_maps[a]
                    L.append((good_key, t(atom)))
                p = PolyhedronPartition(L)
            return p

        else:
            raise TypeError('call undefined on input p(={})'.format(p))

    def induced_partition(self, ieq, partition=None,
            substitution_type='dict', ignore_volume=0, verbose=False):
        r"""
        Returns the partition of the induced transformation on the domain.

        INPUT:

        - ``ieq`` -- list, an inequality. An entry equal to "[-1,7,3,4]"
          represents the inequality 7x_1+3x_2+4x_3>= 1.
        - ``partition`` -- polyhedron partition (default:``None``), if
          None, it uses the domain partition of the transformation
        - ``substitution_type`` -- string (default:``'dict'``), if
          ``'column'`` or ``'row'``, it returns a substitution2d, otherwise
          it returns a dict.
        - ``ignore_volume`` -- real (optional:``0``), stop the while loop if
          the volume of what's not yet returned is less than the given
          threshold
        - ``verbose`` -- bool (optional:``False``), print verbose
          information

        OUTPUT:

            - a polyhedron partition
            - a substitution2d or a dict

        EXAMPLES::

            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: base = identity_matrix(2)
            sage: translation = vector((1/3, 0))
            sage: u = PET.toral_translation(base, translation)

        We compute the induced partition of a polyhedron exchange
        transformation on a subdomain given by an inequality::

            sage: ieq = [1/3, -1, 0]   # x0 <= 1/3
            sage: u.induced_partition(ieq)
            (Polyhedron partition of 1 atoms with 1 letters,
             {0: [0, 0, 1]})
            sage: ieq = [1/2, -1, 0]   # x0 <= 1/2
            sage: u.induced_partition(ieq)
            (Polyhedron partition of 3 atoms with 3 letters,
             {0: [0], 1: [0, 1], 2: [0, 0, 1]})

        The second output can be turned into a column or a row
        Substitution2d if desired::

            sage: u.induced_partition(ieq, substitution_type='row')
            (Polyhedron partition of 3 atoms with 3 letters,
             Substitution 2d: {0: [[0]], 1: [[0], [1]], 2: [[0], [0], [1]]})

        Now we construct a another coding partition::

            sage: from slabbe import PolyhedronPartition
            sage: h = 1/3
            sage: p = Polyhedron([(0,h),(0,1),(h,1)])
            sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
            sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
            sage: s = Polyhedron([(h,0), (1,0), (1,h)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s})

        We use this other partition to compute the induced partition::

            sage: ieq = [h, -1, 0]   # x0 <= h
            sage: Q,sub = u.induced_partition(ieq, P)
            sage: Q
            Polyhedron partition of 4 atoms with 4 letters
            sage: sub
            {0: [0, 2, 2], 1: [1, 2, 2], 2: [1, 2, 3], 3: [1, 3, 3]}

        ::

            sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s})
            sage: ieq2 = [1/2, -1, 0]   # x0 <= 1/2
            sage: Q,sub = u.induced_partition(ieq2, P)
            sage: Q
            Polyhedron partition of 9 atoms with 9 letters
            sage: sub
            {0: [0],
             1: [1],
             2: [2, 2],
             3: [2, 3],
             4: [3, 3],
             5: [0, 2, 2],
             6: [1, 2, 2],
             7: [1, 2, 3],
             8: [1, 3, 3]}

        Irrationnal rotations::

            sage: z = polygen(QQ, 'z') #z = QQ['z'].0 # same as
            sage: K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
            sage: phi = K.gen()
            sage: h = 1/phi^2
            sage: p = Polyhedron([(0,h),(0,1),(h,1)])
            sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
            sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
            sage: s = Polyhedron([(h,0), (1,0), (1,h)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s}, base_ring=K)
            sage: base = identity_matrix(2)
            sage: translation = vector((1/phi, 0))
            sage: u = PET.toral_translation(base, translation)
            sage: ieq = [h, -1, 0]   # x0 <= h
            sage: P1,sub01 = u.induced_partition(ieq, P)
            sage: P1
            Polyhedron partition of 7 atoms with 7 letters
            sage: sub01
            {0: [0, 2],
             1: [1, 2],
             2: [1, 3],
             3: [0, 2, 2],
             4: [1, 2, 2],
             5: [1, 3, 2],
             6: [1, 3, 3]}

        We do the induction on a smaller domain::

            sage: ieq2 = [1/phi^3, -1, 0]   # x0 <= h
            sage: P2,sub02 = u.induced_partition(ieq2, P)
            sage: P2
            Polyhedron partition of 10 atoms with 10 letters
            sage: sub02
            {0: [0, 2, 2],
             1: [1, 2, 2],
             2: [1, 3, 2],
             3: [1, 3, 3],
             4: [0, 2, 0, 2, 2],
             5: [0, 2, 1, 2, 2],
             6: [1, 2, 1, 2, 2],
             7: [1, 2, 1, 3, 2],
             8: [1, 3, 1, 3, 2],
             9: [1, 3, 1, 3, 3]}

        We check that inductions commute::

            sage: base = diagonal_matrix((phi^-2,1))
            sage: translation = vector((phi^-3, 0))
            sage: u1 = PET.toral_translation(base, translation)
            sage: P2_alt,sub12 = u1.induced_partition(ieq2, P1)
            sage: P2_alt
            Polyhedron partition of 10 atoms with 10 letters
            sage: P2_alt == P2
            True

        Up to a permutation of the alphabet, ``sub02`` and ``sub01*sub12``
        are equal::

            sage: s01 = WordMorphism(sub01)
            sage: s12 = WordMorphism(sub12)
            sage: s02 = WordMorphism(sub02)
            sage: s02
            WordMorphism: 0->022, 1->122, 2->132, 3->133, 4->02022, 5->02122, 6->12122, 7->12132, 8->13132, 9->13133
            sage: s01*s12 == s02
            True

        By chance, the above is true, but in general, we have::

            sage: perm = WordMorphism(P2.keys_permutation(P2_alt))
            sage: perm
            WordMorphism: 0->0, 1->1, 2->2, 3->3, 4->4, 5->5, 6->6, 7->7, 8->8, 9->9
            sage: s01*s12*perm == s02
            True

        """
        # Default partition
        if partition is None:
            partition = self.partition()

        # good side of the hyperplane
        half_polyhedron = Polyhedron(ieqs=[ieq])
        half = PolyhedronPartition([half_polyhedron])

        # the other side of the hyperplane
        other_half_polyhedron = Polyhedron(ieqs=[[-a for a in ieq]])
        other_half = PolyhedronPartition([other_half_polyhedron])

        # the window is the intersection of the domain with the half space
        W = self.domain().intersection(half_polyhedron)
        if W.volume() == 0:
            raise ValueError("Inequality {} does not intersect partition "
                    "(={})".format(half_polyhedron.inequalities()[0], partition))

        # Compute the induced partition and associated return words
        Q = PolyhedronPartition([(tuple(), W)])
        S = []
        self_inv = self.inverse()
        while len(Q) and Q.volume() > ignore_volume:
            if verbose:
                print("Volume not yet returned={}={} ({} atoms).".format(
                    Q.volume(),
                    Q.volume().n(),
                    len(Q)))

            Q = self_inv(Q)
            # Compute the refinement of P and Q (concatenate the labels)
            PQ,d = partition.refinement(Q, certificate=True)
            Q = PolyhedronPartition([((d[i][0],)+d[i][1], q) for (i,q) in PQ])
            # Take what has returned to the window (keep labels from Q only)
            Q_returned,d = Q.refinement(half, certificate=True)
            S.extend((d[i][0], q) for (i,q) in Q_returned)
            # Continue with what is left (keep labels from Q only)
            Q,d = Q.refinement(other_half, certificate=True)
            Q = PolyhedronPartition([(d[i][0], q) for (i,q) in Q])

        if verbose:
            print("Volume not yet returned={}={} ({} atoms).".format(
                Q.volume(),
                Q.volume().n(),
                len(Q)))
            print("Under these conditions, we stop the while loop of the Rauzy induction.")

        # We sort the keys and relabel them with nonnegative integers
        from slabbe.finite_word import sort_word_by_length_lex_key
        return_words = set(w for (w,q) in S)
        sorted_return_words = sorted(return_words, key=sort_word_by_length_lex_key)
        key_to_word = {key:list(w) for (key,w) in enumerate(sorted_return_words)}
        word_to_key = {w:key for (key,w) in enumerate(sorted_return_words)}
        induced_partition = PolyhedronPartition([(word_to_key[w],q) for (w,q) in S])

        # Build a substitution2d if desired
        if substitution_type == 'dict':
            sub = key_to_word
        elif substitution_type == 'column':
            from slabbe import Substitution2d
            sub = Substitution2d.from_1d_column_substitution(key_to_word)
        elif substitution_type == 'row':
            from slabbe import Substitution2d
            sub = Substitution2d.from_1d_row_substitution(key_to_word)
        else:
            raise ValueError('Unknown value for substitution_type'
                    ' (={})'.format(substitution_type))

        return induced_partition, sub

    def induced_transformation(self, ieq, ignore_volume=0, verbose=False):
        r"""
        Return the induced transformation on the domain.

        INPUT:

        - ``ieq`` -- list, an inequality. An entry equal to "[-1,7,3,4]"
          represents the inequality 7x_1+3x_2+4x_3>= 1.
        - ``ignore_volume`` -- real (optional:``0``), stop the while loop if
          the volume of what's not yet returned is less than the given
          threshold
        - ``verbose`` -- bool (optional:``False``), print verbose
          information

        OUTPUT:

            - a polyhedron exchange transformation on the subdomain
            - a substitution (dict)

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: ieq = [1/2, -1, 0]   # x0 <= 1/2
            sage: T_induced,sub = T.induced_transformation(ieq)
            sage: T_induced.pp()
            Piecewise Affine Transformation given by a
            Polyhedron partition of 6 atoms with 6 letters
            defined by 6 affine maps:
            Affine map 0:
                  [0 1]     [  0]
            x |-> [1 0] x + [2/3]
            Affine map 1:
                  [0 1]     [   0]
            x |-> [1 0] x + [-1/3]
            Affine map 2:
                  [1 0]     [-1/3]
            x |-> [0 1] x + [-1/3]
            Affine map 3:
                  [0 1]     [-1/3]
            x |-> [1 0] x + [ 1/3]
            Affine map 4:
                  [1 0]     [ 1/3]
            x |-> [0 1] x + [-2/3]
            Affine map 5:
                  [0 1]     [-2/3]
            x |-> [1 0] x + [   0]
            sage: sub
            {0: [0], 1: [1], 2: [1, 1], 3: [0, 1, 1], 4: [0, 1, 1, 1], 5: [0, 1, 1, 1, 1]}

        """
        from sage.misc.misc_c import prod
        newP, sub = self.induced_partition(ieq, ignore_volume=ignore_volume, verbose=verbose)
        d = self.affine_maps()
        newd = {a:prod(d[b] for b in reversed(sub[a])) for a in sub}
        return PiecewiseAffineTransformation(newP, newd), sub

    def cylinder(self, word, partition=None):
        r"""
        Return the region associated to the coding word.

        INPUT:

        - ``word`` -- list
        - ``partition`` -- polyhedron partition (default:``None``), if
          None, it uses the domain partition of the transformation

        OUTPUT:

            polyhedron partition

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: c = T.cylinder([0,1,1]); c
            Polyhedron partition of 1 atoms with 1 letters
            sage: c.volume()
            2/9
            sage: T.cylinder([0,1,1,1,1,0]).volume()
            1/9
            sage: T.cylinder([0,1,1,1,1,1]).volume()
            0

        Cylinders of words of length 0::

            sage: T.cylinder([], P).volume()
            1

        Cylinders of words of length 1::

            sage: C1 = [T.cylinder([a], P).volume() for a in range(3)]
            sage: C1
            [1/3, 2/3, 0]
            sage: sum(C1)
            1

        Cylinders of words of length 2::

            sage: import itertools
            sage: L2 = itertools.product(range(3),repeat=2)
            sage: C2 = [T.cylinder([a,b], P).volume() for (a,b) in L2]
            sage: C2
            [1/9, 2/9, 0, 2/9, 4/9, 0, 0, 0, 0]
            sage: sum(C2)
            1

        Cylinders of words of length 3::

            sage: L3 = itertools.product(range(3),repeat=3)
            sage: C3 = [T.cylinder([a,b,c], P).volume() for (a,b,c) in L3]
            sage: sum(C3)
            1

        It also works for PETs::

            sage: from slabbe import PolyhedronPartition
            sage: h = 1/2
            sage: p = Polyhedron([(0,h),(0,1),(h,1)])
            sage: q = Polyhedron([(0,0), (0,h), (h,1), (1,1), (1,h), (h,0)])
            sage: r = Polyhedron([(h,0), (1,0), (1,h)])
            sage: P = PolyhedronPartition([p,q,r])

        ::

            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: base = identity_matrix(2)
            sage: translation = vector((1/3, 0))
            sage: u = PET.toral_translation(base, translation)
            sage: c = u.cylinder([2,2], P); c
            Polyhedron partition of 1 atoms with 1 letters
            sage: c.alphabet()
            {0}
            sage: u.cylinder([1,1], P)
            Polyhedron partition of 2 atoms with 2 letters
            sage: u.cylinder([1], P)
            Polyhedron partition of 1 atoms with 1 letters
            sage: u.cylinder([], P).volume()
            1
            sage: C1 = [u.cylinder([a], P).volume() for a in range(3)]
            sage: C1
            [1/8, 3/4, 1/8]
            sage: sum(C1)
            1
            sage: import itertools
            sage: L2 = itertools.product(range(3),repeat=2)
            sage: C2 = [u.cylinder([a,b], P).volume() for (a,b) in L2]
            sage: C2
            [1/72, 1/9, 0, 1/9, 19/36, 1/9, 0, 1/9, 1/72]
            sage: sum(C2)
            1
            sage: L3 = itertools.product(range(3),repeat=3)
            sage: C3 = [u.cylinder([a,b,c], P).volume() for (a,b,c) in L3]
            sage: sum(C3)
            1

        TESTS::

            sage: u.cylinder([0,0,0], P)
            Polyhedron partition of 0 atoms with 0 letters
            sage: u.cylinder([2,3], P)
            Polyhedron partition of 0 atoms with 0 letters
            sage: u.cylinder([2,1], P)
            Polyhedron partition of 1 atoms with 1 letters
            sage: u.cylinder([], P)
            Polyhedron partition of 3 atoms with 3 letters

        """
        # Default partition
        if partition is None:
            partition = self.partition()
        if not word:
            return partition
        trans_inv = self.inverse()
        reversed_word = reversed(word)
        P = partition[next(reversed_word)]
        for a in reversed_word:
            P = trans_inv(P)
            P = partition[a].refinement(P)
        return P

    def cylinders(self, size, partition=None):
        r"""
        Return the cylinders of given size.

        INPUT:

        - ``size`` -- nonnegative integer
        - ``partition`` -- polyhedron partition (default:``None``), if
          None, it uses the domain partition of the transformation

        OUTPUT:

            polyhedron partition

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition
            sage: from slabbe import PiecewiseAffineTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(0,1),(h,1),(h,0)])
            sage: q = Polyhedron([(1,0), (1,1), (h,1), (h,0)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: F = AffineGroup(2, QQ)
            sage: M = matrix(2, [0,1,1,0])
            sage: f0 = F(M, (0, 2/3))
            sage: f1 = F(M, (0, -1/3))
            sage: T = PiecewiseAffineTransformation(P, {0:f0, 1:f1})
            sage: [T.cylinders(i) for i in range(5)]
            [Polyhedron partition of 1 atoms with 1 letters,
             Polyhedron partition of 2 atoms with 2 letters,
             Polyhedron partition of 4 atoms with 4 letters,
             Polyhedron partition of 6 atoms with 6 letters,
             Polyhedron partition of 9 atoms with 9 letters]
            sage: [T.cylinders(i).alphabet() for i in range(5)]
            [{()}, {0, 1}, {0, 1, 2, 3}, {0, 1, 2, 3, 4, 5}, {0, 1, 2, 3, 4, 5, 6, 7, 8}]

        The code works also for PETs::

            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: base = identity_matrix(2)
            sage: translation = vector((1/3, 0))
            sage: u = PET.toral_translation(base, translation)
            sage: [u.cylinders(i) for i in range(5)]
            [Polyhedron partition of 1 atoms with 1 letters,
             Polyhedron partition of 2 atoms with 2 letters,
             Polyhedron partition of 3 atoms with 3 letters,
             Polyhedron partition of 3 atoms with 3 letters,
             Polyhedron partition of 3 atoms with 3 letters]
            sage: [u.cylinders(i).alphabet() for i in range(5)]
            [{()}, {0, 1}, {0, 1, 2}, {0, 1, 2}, {0, 1, 2}]

        """
        # Default partition
        if partition is None:
            partition = self.partition()

        if size == 0:
            return PolyhedronPartition([(tuple(), self.domain())])

        P = partition
        trans_inv = self.inverse()
        for i in range(size-1):
            P = trans_inv(P)
            P = partition.refinement(P)
        return P


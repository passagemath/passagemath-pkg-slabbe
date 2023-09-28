# -*- coding: utf-8 -*-
r"""
Polyhedron exchange transformations and induced transformations

EXAMPLES:

A polyhedron partition::

    sage: from slabbe import PolyhedronPartition
    sage: h = 1/3
    sage: p = Polyhedron([(0,h),(0,1),(h,1)])
    sage: q = Polyhedron([(0,0), (0,h), (h,1), (h,0)])
    sage: r = Polyhedron([(h,1), (1,1), (1,h), (h,0)])
    sage: s = Polyhedron([(h,0), (1,0), (1,h)])
    sage: P = PolyhedronPartition({0:p, 1:q, 2:r, 3:s})

Applying a rationnal rotation::

    sage: from slabbe import PolyhedronExchangeTransformation as PET
    sage: base = identity_matrix(2)
    sage: translation = vector((2/3, 0))
    sage: u = PET.toral_translation(base, translation)
    sage: Q = u(P)
    sage: Q
    Polyhedron partition of 4 atoms with 4 letters

Inducing an irrationnal rotation on a subdomain::

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

AUTHORS:

- Sébastien Labbé, January 2019, added a class for polyhedron exchange transformations
- Sébastien Labbé, Sep 2023, moved many methods up to class PiecewiseAffineTransformation

"""
#*****************************************************************************
#       Copyright (C) 2017-2023 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from __future__ import absolute_import, print_function
import itertools
from copy import copy
from sage.misc.cachefunc import cached_method
from sage.geometry.polyhedron.constructor import Polyhedron
from slabbe import PolyhedronPartition
from slabbe.piecewise_affine_transformation import PiecewiseAffineTransformation

class PolyhedronExchangeTransformation(PiecewiseAffineTransformation):
    r"""
    Polyhedron Exchange Transformation (PET).

    INPUT:

    - ``partition`` -- a polyhedron partition
    - ``translations`` -- list or dict

    EXAMPLES::

        sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
        sage: h = 1/3
        sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
        sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
        sage: P = PolyhedronPartition({0:p, 1:q})
        sage: T = {0:(1-h,0), 1:(-h,0)}
        sage: PolyhedronExchangeTransformation(P, T)
        Polyhedron Exchange Transformation of
        Polyhedron partition of 2 atoms with 2 letters
        with translations {0: (2/3, 0), 1: (-1/3, 0)}

    .. TODO::

        - Code the __pow__ methods.

        - Do we want to merge atoms mapped by the same translation?

    REFERENCES:

    - Schwartz, Richard Evan. The Octagonal PETs. First Edition edition.
      Providence, Rhode Island: American Mathematical Society, 2014.
    """
    def __init__(self, partition, translations):
        r"""

        """
        if not isinstance(partition, PolyhedronPartition):
            raise TypeError('partition(={}) must be a '
                            'PolyhedronPartition'.format(partition))
        ambient_space = partition.ambient_space()

        if isinstance(translations, list):
            self._translations = {a:ambient_space(t) for (a,t) in enumerate(translations)}
        elif isinstance(translations, dict):
            self._translations = {a:ambient_space(t) for (a,t) in translations.items()}
        else:
            raise TypeError('translations(={}) must be a '
                            'list or dict'.format(translations))

        from sage.groups.affine_gps.affine_group import AffineGroup
        affine_group = AffineGroup(ambient_space)
        affine_maps = {a:affine_group.translation(t) for (a,t) in self._translations.items()}

        PiecewiseAffineTransformation.__init__(self, partition,
                affine_maps, affine_group=affine_group)

    @classmethod
    def toral_translation(cls, base, translation, fundamental_domain=None):
        r"""
        Return a polyhedron exchange transformation defined by a translation on
        a d-dimensional torus.

        INPUT:

        - ``base`` -- matrix, the columns are the base of a lattice
        - ``translation`` -- vector, translation vector
        - ``fundamental_domain`` -- polyhedron or ``None`` (default:
          ``None``), if ``None`` the parallelotope defined by ``base`` is
          used.

        OUTPUT:

            a polyhedron exchange transformation on the fundamental domain of
            the lattice

        EXAMPLES::

            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: base = diagonal_matrix((1,1))
            sage: translation = vector((1/5, 1/3))
            sage: T = PET.toral_translation(base, translation)
            sage: T
            Polyhedron Exchange Transformation of
            Polyhedron partition of 4 atoms with 4 letters
            with translations {0: (1/5, 1/3), 1: (1/5, -2/3), 2: (-4/5, 1/3), 3: (-4/5, -2/3)}
            sage: T.partition()
            Polyhedron partition of 4 atoms with 4 letters

        Some preliminary definitions::

            sage: z = polygen(QQ, 'z') #z = QQ['z'].0 # same as
            sage: K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
            sage: phi = K.gen()
            sage: vertices = ((-phi + 2, phi - 1), (-phi + 2, 1), (phi - 1, 1))
            sage: p = Polyhedron(vertices, base_ring=K)

        A translation +1 modulo phi on the x coordinate::

            sage: base = diagonal_matrix((phi,phi))
            sage: translation = vector((1, 0))
            sage: t0 = PET.toral_translation(base, translation)
            sage: t0
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: ..., 1: ...}
            sage: t0(p).vertices()
            (A vertex at (-phi + 3, phi - 1),
             A vertex at (-phi + 3, 1),
             A vertex at (phi, 1))

        The inverse map::

            sage: t0.inverse()
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: ..., 1: ...}
            sage: t0(p) == p
            False
            sage: t0.inverse()(t0(p)) == p
            True

        A rotation modulo 1 on the y coordinate::

            sage: base = diagonal_matrix((phi,phi))
            sage: translation = vector((0, 1))
            sage: t1 = PET.toral_translation(base, translation)
            sage: t1(p).vertices()
            (A vertex at (-phi + 2, 0),
             A vertex at (-phi + 2, -phi + 2),
             A vertex at (phi - 1, -phi + 2))

        It works if the translation is larger than the fundamental domain::

            sage: base = diagonal_matrix((1,1))
            sage: translation = vector((phi, 0))
            sage: t2 = PET.toral_translation(base, translation)
            sage: t2(p).vertices()
            (A vertex at (0, phi - 1), 
             A vertex at (0, 1), 
             A vertex at (2*phi - 3, 1))

        The domain is the fundamental domain of the given lattice::

            sage: base = diagonal_matrix((phi^-2,1))
            sage: translation = vector((phi^-3, 0))
            sage: t3 = PET.toral_translation(base, translation)
            sage: sorted(t3.domain().vertices())
            [A vertex at (0, 0),
             A vertex at (0, 1),
             A vertex at (-phi + 2, 0),
             A vertex at (-phi + 2, 1)]

        The fundamental domain can be given as input. For example, it can
        be a translated copy of the base parallelotope::

            sage: base = diagonal_matrix((1,1))
            sage: translation = vector((1/5, 1/3))
            sage: F = polytopes.parallelotope(base)
            sage: T = PET.toral_translation(base, translation, F-vector((1/10,1/10)))

        But it does not always work well yet, for example for other shape
        of fundamental domains::

            sage: m = matrix(2, (1,1,0,1))
            sage: mF = polytopes.parallelotope(m*base)
            sage: T = PET.toral_translation(base, translation, mF)
            Traceback (most recent call last):
            ...
            NotImplementedError: Volume of the partition is 73/75 but the
            fundamental domain as volume 1. The code does not handle this
            case properly yet.

        .. TODO::

            Fix the above when the fundamental domain is far from the
            lattice base.
        """
        from sage.geometry.polyhedron.library import polytopes
        from sage.modules.free_module_element import vector
        from sage.functions.other import floor

        # Compute the representent of the translation inside the base
        v = base.inverse() * translation
        v_floor = vector(map(floor, v))
        translation -= base * v_floor

        # The fundamental domain
        base_parallelotope = polytopes.parallelotope(base.columns())
        if fundamental_domain is None:
            fundamental_domain = base_parallelotope
        FD = fundamental_domain # shorcut

        # Computing the partitions and translations
        atoms = {}
        trans = {}
        for vertex in base_parallelotope.vertices():
            t = vertex.vector() - translation
            I = FD.intersection(FD.translation(t))
            if I.volume():
                k = len(atoms)
                atoms[k] = I
                trans[k] = -t
        partition = PolyhedronPartition(atoms)

        if partition.volume() != FD.volume():
            raise NotImplementedError('Volume of the partition is {} but'
                    ' the fundamental domain as volume {}. The code does'
                    ' not handle this case properly yet.'.format(partition.volume(), 
                                                             FD.volume()))

        return PolyhedronExchangeTransformation(partition, trans)

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F
            Polyhedron Exchange Transformation of 
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (2/3, 0), 1: (-1/3, 0)}
        """
        return ('Polyhedron Exchange Transformation of\n{}\nwith '
               'translations {}').format(self._partition, self._translations)

    def translations(self):
        r"""
        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F.translations()
            {0: (2/3, 0), 1: (-1/3, 0)}
        """
        return self._translations

    def merge_atoms_with_same_translation(self):
        r"""
        Return a new partition into convex polyhedrons where atoms mapped
        by the same translation are merged if their union is convex.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,h),(0,h)])
            sage: q = Polyhedron([(0,h),(h,h),(h,1),(0,1)])
            sage: r = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q, 2:r})
            sage: d = {0:(1-h,0), 1:(1-h,0), 2:(-h,0)}
            sage: T = PolyhedronExchangeTransformation(P, d)
            sage: T
            Polyhedron Exchange Transformation of
            Polyhedron partition of 3 atoms with 3 letters
            with translations {0: (2/3, 0), 1: (2/3, 0), 2: (-1/3, 0)}
            sage: T.merge_atoms_with_same_translation()
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (2/3, 0), 2: (-1/3, 0)}

        """
        f = self.merge_atoms_with_same_transformation()
        translation_dict = {a:affine_map.b() for (a,affine_map) in f.affine_maps().items()}
        return PolyhedronExchangeTransformation(f.partition(), translation_dict)

    def __eq__(self, other):
        r"""
        Return whether two polyhedron exchange transformations are equal.

        INPUT:

        - ``other`` -- polyhedron exchange transformation

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 4/5
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 3 atoms with 3 letters
            with translations {0: (2/5, 0), 1: (-3/5, 0), 2: (-3/5, 0)}
            sage: F * F * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 4 atoms with 4 letters
            with translations {0: (3/5, 0), 1: (-2/5, 0), 2: (-2/5, 0), 3: (-2/5, 0)}

        """
        return (isinstance(other, PolyhedronExchangeTransformation)
                and self._partition == other._partition
                and self._translations == other._translations)

    def inverse(self):
        r"""
        Return the inverse of self.

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 1/3
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F
            Polyhedron Exchange Transformation of 
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (2/3, 0), 1: (-1/3, 0)}

        ::

            sage: F.inverse()
            Polyhedron Exchange Transformation of 
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (-2/3, 0), 1: (1/3, 0)}

        """
        P = self.image_partition()
        T = {a:-t for (a,t) in self._translations.items()}
        return PolyhedronExchangeTransformation(P, T)

    def __mul__(self, other):
        r"""
        Return the product of polyhedron exchange transformations.

        INPUT:

        - ``other`` -- polyhedron exchange transformation

        OUTPUT:

        - polyhedron exchange transformation with keys being a tuple of
          previous keys

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 4/5
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: F * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 3 atoms with 3 letters
            with translations {0: (2/5, 0), 1: (-3/5, 0), 2: (-3/5, 0)}
            sage: F * F * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 4 atoms with 4 letters
            with translations {0: (3/5, 0), 1: (-2/5, 0), 2: (-2/5, 0), 3: (-2/5, 0)}

        """
        if not isinstance(other, PolyhedronExchangeTransformation):
            return NotImplemented
        R,d = self.image_partition().refinement(other.partition(),
                                                certificate=True)

        atoms_dict = {}
        trans_dict = {}
        for key,atom in R:
            (a,b) = d[key]
            atoms_dict[key] = atom - self._translations[a]
            trans_dict[key] = self._translations[a] + other._translations[b]

        P = PolyhedronPartition(atoms_dict)
        return PolyhedronExchangeTransformation(P, trans_dict)

    def __rmul__(self, factor):
        r"""
        Returns the PET scaled by some factor.

        INPUT:

        - ``factor`` -- real number

        OUTPUT:

        - polyhedron exchange transformation

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 4/5
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: 2 * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (2/5, 0), 1: (-8/5, 0)}
            sage: -2 * F
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (-2/5, 0), 1: (8/5, 0)}

        """
        if isinstance(factor, PolyhedronExchangeTransformation):
            return NotImplemented
        P = factor * self.partition()
        trans_dict = {key:factor*t for (key,t) in self.translations().items()}
        return PolyhedronExchangeTransformation(P, trans_dict)

    def translate_domain(self, displacement):
        """
        Return the PET on a domain translated by some displacement.

        INPUT:

        - ``displacement`` -- a displacement vector or a list/tuple of
          coordinates that determines a displacement vector.

        OUTPUT:

        The translated PET

        EXAMPLES::

            sage: from slabbe import PolyhedronPartition, PolyhedronExchangeTransformation
            sage: h = 4/5
            sage: p = Polyhedron([(0,0),(h,0),(h,1),(0,1)])
            sage: q = Polyhedron([(1,0),(h,0),(h,1),(1,1)])
            sage: P = PolyhedronPartition({0:p, 1:q})
            sage: T = {0:(1-h,0), 1:(-h,0)}
            sage: F = PolyhedronExchangeTransformation(P, T)
            sage: Ft = F.translate_domain((3,1))
            sage: Ft
            Polyhedron Exchange Transformation of
            Polyhedron partition of 2 atoms with 2 letters
            with translations {0: (1/5, 0), 1: (-4/5, 0)}
            sage: Ft.domain().vertices()
            (A vertex at (3, 1),
             A vertex at (3, 2),
             A vertex at (4, 1),
             A vertex at (4, 2))

        """
        P = self.partition().translate(displacement)
        trans_dict = {key:t for (key,t) in self.translations().items()}
        return PolyhedronExchangeTransformation(P, trans_dict)

    def induced_transformation(self, ieq):
        r"""
        Return the induced transformation on the domain.

        INPUT:

        - ``ieq`` -- list, an inequality. An entry equal to "[-1,7,3,4]"
          represents the inequality 7x_1+3x_2+4x_3>= 1.

        OUTPUT:

            - a polyhedron exchange transformation on the subdomain
            - a substitution (dict)

        EXAMPLES::

            sage: from slabbe import PolyhedronExchangeTransformation as PET
            sage: base = identity_matrix(2)
            sage: translation = vector((1/3, 0))
            sage: u = PET.toral_translation(base, translation)

        We compute the induced transformation of a polyhedron exchange
        transformation on a subdomain given by an inequality::

            sage: ieq = [1/2, -1, 0]   # x0 <= 1/2
            sage: T,sub = u.induced_transformation(ieq)
            sage: T
            Polyhedron Exchange Transformation of
            Polyhedron partition of 3 atoms with 3 letters
            with translations {0: (1/3, 0), 1: (-1/3, 0), 2: (0, 0)}
            sage: sub
            {0: [0], 1: [0, 1], 2: [0, 0, 1]}

        """
        newP, sub = self.induced_partition(ieq)
        T = self.translations()
        newT = {a:sum(T[b] for b in sub[a]) for a in sub}
        return PolyhedronExchangeTransformation(newP, newT), sub


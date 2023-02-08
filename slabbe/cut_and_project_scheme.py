# -*- coding: utf-8 -*-
r"""
Cut and project schemes and model sets
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
from sage.structure.sage_object import SageObject

class CutAndProjectScheme(SageObject):
    r"""
    INPUT:

    - ``base_ring`` -- ring
    - ``pi`` -- `n\times d` matrix, projection of the ambiant space to
        the physical space
    - ``pi_int`` -- `n\times (n-d)` matrix, projection of the ambiant space
        to the internal space
    - ``lattice`` -- `n\times n` matrix, the columns form a base of a
        lattice in R^n
    - ``check`` -- boolean (default:``True``), whether to check that
        dimensions of the matrices given as input are consistent

    EXAMPLES::

        sage: from slabbe import CutAndProjectScheme
        sage: z = polygen(QQ, 'z')
        sage: K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
        sage: phi = K.gen()
        sage: pi = matrix([[phi, 1]])
        sage: pi_int = matrix([[-~phi, 1]])
        sage: lattice = identity_matrix(2)
        sage: cap = CutAndProjectScheme(K, pi, pi_int, lattice)

    """
    def __init__(self, base_ring, pi, pi_int, lattice, check=True):
        r"""
        Constructor
        """
        self._base_ring = base_ring
        self._pi = pi
        self._pi_int = pi_int
        self._lattice = lattice

        if check:
            self._check()

    def _check(self):
        r"""
        Perform checks on the dimension of the matrices given as input
        and raise a ``ValueError`` in case of an inconsistency

        """
        if self._pi.ncols() != self._pi_int.ncols():
            raise ValueError("pi and pi_int matrices must have the same number of columns")

        if self._pi.ncols() != self._pi.nrows() +  self._pi_int.nrows():
            raise ValueError("pi and pi_int matrices must have the same number of columns")

    def base_ring(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.base_ring()
            Number Field in phi with defining polynomial z^2 - z - 1 with phi = 1.618033988749895?

        """
        return self._base_ring

    def physical_space_projection(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.physical_space_projection()
            [      1 phi - 1]

        """
        return self._pi

    def internal_space_projection(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.internal_space_projection()
            [-phi + 1        1]

        """
        return self._pi_int

    def lattice(self):
        r"""
        Return the lattice

        OUTPUT:

            a matrix whose columns generate the lattice

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.lattice()
            [1 0]
            [0 1]

        """
        return self._lattice

    def lattice_base(self):
        r"""
        Return the lattice base

        OUTPUT:

            a matrix whose columns generate the lattice

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.lattice_base()
            [(1, 0), (0, 1)]

        """
        return self._lattice.columns()

    def ambiant_space(self):
        r"""
        Return the ambiant space

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.ambiant_space()
            Vector space of dimension 2 over Number Field in phi with
            defining polynomial z^2 - z - 1 with phi = 1.618033988749895?

        """
        return self.physical_space_projection().row_ambient_module()
    def physical_space(self):
        r"""
        Return the physical space

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.physical_space()
            Vector space of dimension 1 over Number Field in phi with
            defining polynomial z^2 - z - 1 with phi = 1.618033988749895?

        """
        return self.physical_space_projection().column_ambient_module()
    def internal_space(self):
        r"""
        Return the internal space

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.internal_space()
            Vector space of dimension 1 over Number Field in phi with
            defining polynomial z^2 - z - 1 with phi = 1.618033988749895?

        """
        return self.internal_space_projection().column_ambient_module()

    def ambiant_space_dimension(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.ambiant_space_dimension()
            2

        """
        return self._pi.ncols()

    def physical_space_dimension(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.physical_space_dimension()
            1

        """
        return self._pi.nrows()

    def internal_space_dimension(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: cap.internal_space_dimension()
            1

        """
        return self._pi_int.nrows()

    def __repr__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cut_and_project_schemes.Fibonacci()
            2-to-1 cut and project scheme

        """
        return "{}-to-{} cut and project scheme".format(
                self.ambiant_space_dimension(),
                self.physical_space_dimension())

    def __str__(self):
        r"""
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: print(cut_and_project_schemes.Fibonacci())
            2-to-1 cut and project scheme over
            Number Field in phi with defining polynomial z^2 - z - 1 with phi = 1.618033988749895?
            Projection to physical space:
            [      1 phi - 1]
            Projection to internal space:
            [-phi + 1        1]
            Lattice generated by the columns of:
            [1 0]
            [0 1]

        """
        s = ("{}-to-{} cut and project scheme over\n{}\n"
             "Projection to physical space:\n{}\n"
             "Projection to internal space:\n{}\n"
             "Lattice generated by the columns of:\n{}")
        return s.format(
                self.ambiant_space_dimension(),
                self.physical_space_dimension(),
                self.base_ring(),
                self.physical_space_projection(), 
                self.internal_space_projection(), 
                self.lattice())

    def star_map(self):
        pass

    def lattice_neighbors(self, v):
        r"""
        Return the neighbors of a point according
        to the base of the lattice

        INPUT:

        - ``v`` -- tuple or vector, in the ambiant space

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: v = vector((10, 10))
            sage: cap.lattice_neighbors(v)
            [(11, 10), (10, 11), (9, 10), (10, 9)]

        """
        L = []
        L.extend(v+p for p in self.lattice_base())
        L.extend(v-p for p in self.lattice_base())
        for u in L:
            u.set_immutable()
        return L

class ModelSet(SageObject):
    r"""
    Regular Euclidean model set

    INPUT:

    - ``cut_and_project_schemes`` -- a cut and project scheme
    - ``window`` -- polyhedron

    EXAMPLES::

        sage: from slabbe import cut_and_project_schemes, ModelSet
        sage: cap = cut_and_project_schemes.Fibonacci()
        sage: phi = cap.base_ring().gen()
        sage: W = Polyhedron([(-1,),(phi-1,)])
        sage: m = ModelSet(cap, W)

    """
    def __init__(self, cut_and_project_scheme, window):
        r"""
        Construct the model set
        """
        self._cut_and_project_scheme = cut_and_project_scheme
        self._window = window

    def cut_and_project_scheme(self):
        return self._cut_and_project_scheme

    def window(self):
        return self._window

    def __repr__(self):
        r"""
        String representation
        
        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes, ModelSet
            sage: cap = cut_and_project_schemes.Fibonacci()
            sage: phi = cap.base_ring().gen()
            sage: W = Polyhedron([(-1,),(phi-1,)])
            sage: ModelSet(cap, W)
            Model Set of a 2-to-1 cut and project scheme

        """
        return "Model Set of a {}".format(repr(self._cut_and_project_scheme))

    def is_Meyer(self):
        raise NotImplementedError
    def is_regular(self):
        raise NotImplementedError
    def is_singular(self):
        raise NotImplementedError
    def is_generic(self):
        raise NotImplementedError
    def is_uniformly_discrete(self):
        raise NotImplementedError
    def is_relatively_dense(self):
        raise NotImplementedError

    def lattice_neighbors_projected_in_window(self, v):
        r"""
        Return the neighbors of a point that are projected in the (internal
        space) window

        INPUT:

        - ``v`` -- tuple or vector, in the ambiant space

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: m = model_sets.Fibonacci()
            sage: v = vector((0,0))
            sage: m.lattice_neighbors_projected_in_window(v)
            [(1, 0), (-1, 0), (0, -1)]

        """
        cap = self.cut_and_project_scheme()
        M = cap.internal_space_projection()
        window = self.window()
        return [p for p in cap.lattice_neighbors(v) if M * p in window]

    def cut(self, physical_window):
        r"""
        Return the lattice points that are projected in the internal space
        window (and that are projected to the provided physical space
        window).

        INPUT:

        - ``physical_window`` -- polyhedron

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: m = model_sets.Fibonacci()
            sage: W = Polyhedron([(0,),(10,)])
            sage: m.cut(W)
            [(0, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (4, 2), (4, 3),
             (5, 3), (6, 3), (6, 4), (7, 4)]

        """
        cap = self.cut_and_project_scheme()
        V = cap.ambiant_space()
        zero = V(0)
        zero.set_immutable()
        seeds = [zero]

        M = cap.physical_space_projection()
        def successors(v): 
            return [p for p in self.lattice_neighbors_projected_in_window(v) 
                      if M * p in physical_window]

        from sage.sets.recursively_enumerated_set import RecursivelyEnumeratedSet
        R = RecursivelyEnumeratedSet(seeds, successors, structure='symmetric')
        return list(R)

    def cut_and_project(self, physical_window):
        r"""
        Return the model set restricted to a window in the physical space

        INPUT:

        - ``physical_window`` -- polyhedron

        OUTPUT:

            list

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: m = model_sets.Fibonacci()
            sage: W = Polyhedron([(0,),(10,)])
            sage: m.cut_and_project(W)
            [(0),
             (1),
             (phi),
             (phi + 1),
             (phi + 2),
             (2*phi + 1),
             (2*phi + 2),
             (3*phi + 1),
             (3*phi + 2),
             (3*phi + 3),
             (4*phi + 2),
             (4*phi + 3)]

        """
        L = self.cut(physical_window)
        cap = self.cut_and_project_scheme()
        M = cap.physical_space_projection()
        return [M*p for p in L]

    def plot_in_ambiant_space(self, physical_window, pointsize=100):
        r"""
        Return a Graphics representing the model set restricted to a window
        in the physical space (seen in the ambiant space)

        INPUT:

        - ``physical_window`` -- polyhedron
        - ``pointsize`` -- integer (default:20)

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: m = model_sets.Fibonacci()
            sage: W = Polyhedron([(-10,),(10,)])
            sage: G = m.plot_in_ambiant_space(W)
            sage: G.show(aspect_ratio=1, figsize=20)

        TODO: The following needs a little fix since the slope is zero
        (some limit case for the region_plot)::

            sage: m = model_sets.Fibonacci_the_Minkowski_way()
            sage: W = Polyhedron([(-10,),(10,)])
            sage: G = m.plot_in_ambiant_space(W)
            sage: G.show(aspect_ratio=1, figsize=20)    # known bug

        TESTS::

            sage: m = model_sets.Fibonacci2D()
            sage: W = polytopes.hypercube(2, intervals=[(-10,10), (-10,10)])
            sage: G = m.plot_in_ambiant_space(W)
            Traceback (most recent call last):
            ...
            NotImplementedError: when physical space dimension is 2 and
            ambiant space dimension is 4

        """
        cap = self.cut_and_project_scheme()
        if (cap.physical_space_dimension() != 1 or cap.ambiant_space_dimension() != 2):
            raise NotImplementedError("when physical space dimension "
                    "is {} and ambiant space dimension is {}".format(
                        cap.physical_space_dimension(),
                        cap.ambiant_space_dimension()))

        from sage.plot.graphics import Graphics
        from sage.plot.point import point
        from sage.plot.arrow import arrow
        from sage.calculus.var import var
        from sage.plot.contour_plot import region_plot
        from sage.modules.free_module_element import vector

        G = Graphics()

        # the strip (alternate way using polyhedron)
        #M_int = cap.internal_space_projection()
        #vertices = [(0,b) for (b,) in self.window().vertices()]
        #lines = M_int.right_kernel().basis()
        #from sage.geometry.polyhedron.constructor import Polyhedron
        #strip = Polyhedron(vertices=vertices, lines=lines)
        #G += strip.plot(fill='lightyellow')

        wp_vertices = sorted(b for (b,) in physical_window.vertices())
        wp_min, wp_max = wp_vertices

        # the strip
        M_int = cap.internal_space_projection()
        [[a,b]] = M_int
        wi_vertices = sorted(b for (b,) in self.window().vertices())
        wi_min, wi_max = wi_vertices
        x,y = var('x,y')
        ineqs = [a*x+b*y<wi_max, a*x+b*y>wi_min]
        if b:
            y_max = ((wi_max-a*wp_max)/b).n()
            y_min = ((wi_min-a*wp_min)/b).n()
        else:
            raise NotImplementedError
        G += region_plot(ineqs, (x,wp_min,wp_max), (y,y_min,y_max),
                incol='lightcoral', 
                bordercol='coral', borderstyle='dotted',
                borderwidth=2, 
                alpha=.1)

        # points in the strip
        L = self.cut(physical_window)
        G += point(L, color='red', size=pointsize)

        # arrows and projected points
        M = cap.physical_space_projection()
        for p in L:
            (a,) = M_p = M*p
            a_0 = vector((a,0))
            edge = (p,a_0)
            if p != a_0:
                # see https://github.com/sagemath/sage/issues/35031
                G += arrow(p, a_0, linestyle='dashed', color='green',
                        arrowshorten=15)
            G += point([a_0], size=pointsize, color='blue')

        return G

    def plot_in_physical_space(self, physical_window, pointsize=100):
        r"""
        Return a Graphics representing the model set restricted to a window
        in the physical space

        INPUT:

        - ``physical_window`` -- polyhedron
        - ``pointsize`` -- integer (default:20)

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: m = model_sets.Fibonacci2D()
            sage: W = polytopes.hypercube(2, intervals=[(-10,10), (-10,10)])
            sage: G = m.plot_in_physical_space(W)
            sage: G.show(aspect_ratio=1, figsize=20)

        TESTS::

            sage: m = model_sets.Fibonacci()
            sage: W = Polyhedron([(-10,),(10,)])
            sage: G = m.plot_in_physical_space(W)
            Traceback (most recent call last):
            ...
            NotImplementedError: when physical space dimension is 1

        """
        from sage.plot.point import point
        cap = self.cut_and_project_scheme()
        if cap.physical_space_dimension() != 2:
            raise NotImplementedError("when physical space dimension "
                    "is {}".format(cap.physical_space_dimension()))

        L = self.cut_and_project(physical_window)
        return point(L, size=pointsize)


class CutAndProjectSchemeGenerator():
    r"""
    Constructor of several famous cut and project schemes

    EXAMPLES::

        sage: from slabbe import cut_and_project_schemes
        sage: cut_and_project_schemes.Fibonacci()
        2-to-1 cut and project scheme
    """
    def Fibonacci(self):
        r"""
        Return the Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cut_and_project_schemes.Fibonacci()
            2-to-1 cut and project scheme

        """
        from sage.rings.rational_field import QQ
        from sage.rings.real_mpfr import RR
        from sage.rings.polynomial.polynomial_ring import polygen
        from sage.rings.number_field.number_field import NumberField
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix

        z = polygen(QQ, 'z')
        K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
        phi = K.gen()
        pi = matrix([[1, ~phi]])
        pi_int = matrix([[-~phi, 1]])
        lattice = identity_matrix(2)
        return CutAndProjectScheme(K, pi, pi_int, lattice)

    def Fibonacci_the_Minkowski_way(self):
        r"""
        Return the Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cut_and_project_schemes.Fibonacci_the_Minkowski_way()
            2-to-1 cut and project scheme
            sage: print(cut_and_project_schemes.Fibonacci_the_Minkowski_way())
            2-to-1 cut and project scheme over
            Number Field in phi with defining polynomial z^2 - z - 1 with
            phi = 1.618033988749895?
            Projection to physical space:
            [1 0]
            Projection to internal space:
            [0 1]
            Lattice generated by the columns of:
            [       1      phi]
            [       1 -phi + 1]


        """
        from sage.rings.rational_field import QQ
        from sage.rings.real_mpfr import RR
        from sage.rings.polynomial.polynomial_ring import polygen
        from sage.rings.number_field.number_field import NumberField
        from sage.matrix.constructor import matrix

        z = polygen(QQ, 'z')
        K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
        phi = K.gen()
        pi = matrix([[1, 0]])
        pi_int = matrix([[0, 1]])
        lattice = matrix.column(2,[(1,1), (phi,-~phi)])
        return CutAndProjectScheme(K, pi, pi_int, lattice)


    def Fibonacci2D(self):
        r"""
        Return the 2D Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import cut_and_project_schemes
            sage: cut_and_project_schemes.Fibonacci2D()
            4-to-2 cut and project scheme

        """
        from sage.rings.rational_field import QQ
        from sage.rings.real_mpfr import RR
        from sage.rings.polynomial.polynomial_ring import polygen
        from sage.rings.number_field.number_field import NumberField
        from sage.matrix.constructor import matrix
        from sage.matrix.special import identity_matrix

        z = polygen(QQ, 'z')
        K = NumberField(z**2-z-1, 'phi', embedding=RR(1.6))
        phi = K.gen()
        pi = matrix([[1, ~phi, 0, 0], [0, 0, 1, ~phi]])
        pi_int = matrix([[-~phi, 1, 0, 0], [0, 0, -~phi, 1]])
        lattice = identity_matrix(4)
        return CutAndProjectScheme(K, pi, pi_int, lattice)

cut_and_project_schemes = CutAndProjectSchemeGenerator()
class ModelSetGenerator():
    r"""
    Constructor of several famous model sets

    EXAMPLES::

        sage: from slabbe import model_sets
        sage: model_sets.Fibonacci()
        Model Set of a 2-to-1 cut and project scheme

    """
    def Fibonacci(self):
        r"""
        Return the Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: model_sets.Fibonacci()
            Model Set of a 2-to-1 cut and project scheme

        """
        from sage.geometry.polyhedron.constructor import Polyhedron
        cap = cut_and_project_schemes.Fibonacci()
        K = cap.base_ring()
        phi = K.gen()
        W = Polyhedron([(-1,),(phi-1,)])
        return ModelSet(cap, W)

    def Fibonacci_the_Minkowski_way(self):
        r"""
        Return the Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: model_sets.Fibonacci_the_Minkowski_way()
            Model Set of a 2-to-1 cut and project scheme

        """
        from sage.geometry.polyhedron.constructor import Polyhedron
        cap = cut_and_project_schemes.Fibonacci_the_Minkowski_way()
        K = cap.base_ring()
        phi = K.gen()
        W = Polyhedron([(-1,),(phi-1,)])
        return ModelSet(cap, W)

    def Fibonacci2D(self):
        r"""
        Return the 2D Fibonacci cut and project scheme

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: model_sets.Fibonacci2D()
            Model Set of a 4-to-2 cut and project scheme

        """
        from sage.geometry.polyhedron.library import polytopes
        cap = cut_and_project_schemes.Fibonacci2D()
        K = cap.base_ring()
        phi = K.gen()
        W = polytopes.hypercube(2, intervals=[(-1,phi-1), (-1,phi-1)])
        return ModelSet(cap, W)



    def Penrose(self):
        r"""
        Return the Penrose cut and project scheme

        EXAMPLES::

            sage: from slabbe import model_sets
            sage: model_sets.Penrose()    # not tested
            Model Set of a 5-to-2 cut and project scheme

        """
        raise NotImplementedError

model_sets = ModelSetGenerator()

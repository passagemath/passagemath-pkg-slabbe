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
import itertools
from sage.misc.cachefunc import cached_method

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

    def indices(self):
        r"""

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: list(T.indices())
            [0, 1, 2]
        """
        return self._cubes.keys()

    def cubes(self):
        r"""

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.cubes()
            {0: (0, 0, 0, 0, 0, 0),
             1: (1, 1, 1, 1, 1, 1),
             2: (2, 2, 2, 2, 2, 2)}
        """
        return self._cubes

    def tikz(self, ncols=3, scale=1, node_scale=1):
        r"""

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(i,i,i,i,i,i) for i in range(7)]
            sage: cubes.append((0,1,2,3,4,5))
            sage: T = WangCubeSet(cubes)
            sage: t = T.tikz()
        """
        from sage.misc.latex_standalone import TikzPicture

        def unwrapped_cube(id, cube):
            lines = []
            lines.append(r"\draw (0,0) rectangle (4,1);")
            lines.append(r"\draw (1,-1) rectangle (2,2);")
            lines.append(r"\draw (3,0) -- (3,1);")
            lines.append(r"\node at (0.5,.5) {{{}}};".format(cube[0]))
            lines.append(r"\node at (1.5,.5) {{{}}};".format(cube[1]))
            lines.append(r"\node at (2.5,.5) {{{}}};".format(cube[3]))
            lines.append(r"\node at (3.5,.5) {{{}}};".format(cube[4]))
            lines.append(r"\node at (1.5,1.5) {{{}}};".format(cube[2]))
            lines.append(r"\node at (1.5,-.5) {{{}}};".format(cube[5]))
            lines.append(r"\node[left] at (1,-.5) {{\bf\#{}}};".format(id))
            return lines

        lines = []
        lines.append(r'\begin{tikzpicture}')
        lines.append(r"[")
        lines.append(r"baseline=-\the\dimexpr\fontdimen22\textfont2\relax,")
        lines.append(r"ampersand replacement=\&,")
        lines.append(r"scale={},".format(scale))
        lines.append(r"every node/.style={{scale={}}}".format(node_scale))
        lines.append(r"]")
        #lines.append(r"  \matrix[matrix of math nodes,nodes={")
        #lines.append(r"       minimum size=1.2ex,text width=1.2ex,")
        #lines.append(r"       text height=1.2ex,inner sep=3pt,draw={gray!20},align=center,")
        #lines.append(r"       anchor=base")
        #lines.append(r"     }, row sep=1pt,column sep=1pt]")
        lines.append(r"  \matrix [column sep=5mm,row sep=7mm]")
        lines.append(r"  (config) {")
        for i,(key,cube) in enumerate(self.cubes().items()):
            lines.extend(unwrapped_cube(key, cube))
            if i % ncols == ncols-1:
                lines.append(r'\\')
            else:
                lines.append(r'\&')
        if len(self) % ncols != 0:
            lines.append(r'\\')
        lines.append(r"};")

        lines.append(r'\end{tikzpicture}')
        usetikzlibrary = "matrix,fit".split(',')
        return TikzPicture('\n'.join(lines), usetikzlibrary=usetikzlibrary)

    @cached_method
    def sat_variable_to_cube_position_bijection(self, box):
        r"""
        Return the dictionary giving the correspondence between variables
        and cube indices i at position (j,k)

        INPUT:

        - ``box`` -- tuple of 3 integers

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: box = (2,2,2)
            sage: d1,d2 = T.sat_variable_to_cube_position_bijection(box)
            sage: d1
            {1: (0, 0, 0, 0),
             2: (0, 0, 0, 1),
             3: (0, 0, 1, 0),
             4: (0, 0, 1, 1),
             5: (0, 1, 0, 0),
             6: (0, 1, 0, 1),
             7: (0, 1, 1, 0),
             8: (0, 1, 1, 1),
             9: (1, 0, 0, 0),
             10: (1, 0, 0, 1),
             11: (1, 0, 1, 0),
             12: (1, 0, 1, 1),
             13: (1, 1, 0, 0),
             14: (1, 1, 0, 1),
             15: (1, 1, 1, 0),
             16: (1, 1, 1, 1),
             17: (2, 0, 0, 0),
             18: (2, 0, 0, 1),
             19: (2, 0, 1, 0),
             20: (2, 0, 1, 1),
             21: (2, 1, 0, 0),
             22: (2, 1, 0, 1),
             23: (2, 1, 1, 0),
             24: (2, 1, 1, 1)}

        """
        (X,Y,Z) = box
        n_cubes = len(self)
        L = list(itertools.product(self.indices(), range(X), range(Y), range(Z)))
        var_to_cube_pos = dict(enumerate(L, start=1))
        cube_pos_to_var = dict((b,a) for (a,b) in enumerate(L, start=1))
        return var_to_cube_pos, cube_pos_to_var

    def sat_solver(self, box, cyclic=False, 
            preassigned_color=None, preassigned_cubes=None, solver=None):
        r"""
        Return the SAT solver.

        INPUT:

        - ``box`` -- tuple of 3 integers
        - ``cyclic`` -- boolean (default: ``False``), whether the
          constraints on opposite boundary must match
        - ``preassigned_color`` -- None or list of 6 dict or the form
          ``[{}, {}, {}, {}, {}, {}]`` right, top, left, bottom colors
          preassigned to some positions (on the border or inside)
        - ``preassigned_cubes`` -- None or dict of cubes preassigned to
          some positions
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: box = (2,2,2)

        ::

            sage: s = T.sat_solver(box)
            sage: s             # random
            PicoSAT solver: 24 variables, 104 clauses.
            sage: list(s())
            [None, ...]

        ::


            sage: s = T.sat_solver(box, cyclic=True)
            sage: s             # random
            PicoSAT solver: 24 variables, 176 clauses.
            sage: list(s())
            [None, ...]

        """
        (X,Y,Z) = box
        cubes = self._cubes
        indices = list(self.indices())

        if preassigned_cubes is None:
            preassigned_cubes = {}
        if preassigned_color is None:
            preassigned_color = [{}, {}, {}, {}, {}, {}]

        from sage.sat.solvers.satsolver import SAT
        s = SAT(solver)

        (var_to_cube_pos, 
         cube_pos_to_var) = self.sat_variable_to_cube_position_bijection(box)

        # at least one tile at each position (j,k,l)
        # (exactly one if one could use a xor clause)
        for (j,k,l) in itertools.product(range(X),range(Y),range(Z)):
            constraint = [cube_pos_to_var[(i,j,k,l)] for i in indices]
            s.add_clause(constraint)

        # no two cubes at the same position (j,k,l)
        for (j,k,l) in itertools.product(range(X),range(Y),range(Z)):
            for i1,i2 in itertools.combinations(indices, 2):
                constraint = [-cube_pos_to_var[(i1,j,k,l)], 
                              -cube_pos_to_var[(i2,j,k,l)]]
                s.add_clause(constraint)

        # preassigned cubes at position (j,k,l)
        for (j,k,l) in preassigned_cubes:
            i = preassigned_cubes[(j,k,l)]
            constraint = [cube_pos_to_var[(i,j,k,l)]]
            s.add_clause(constraint)

        # matching color of cube faces orthogonal to vector e1
        range_X = range(X) if cyclic else range(X-1)
        for (j,k,l) in itertools.product(range_X,range(Y),range(Z)):
            for i1,i2 in itertools.product(indices, repeat=2):
                if cubes[i1][0] != cubes[i2][3]:
                    constraint = [-cube_pos_to_var[(i1,j,k,l)], 
                                  -cube_pos_to_var[(i2,(j+1)%X,k,l)]]
                    s.add_clause(constraint)

        # matching color of cube faces orthogonal to vector e2
        range_Y = range(Y) if cyclic else range(Y-1)
        for (j,k,l) in itertools.product(range(X),range_Y,range(Z)):
            for i1,i2 in itertools.product(indices, repeat=2):
                if cubes[i1][1] != cubes[i2][4]:
                    constraint = [-cube_pos_to_var[(i1,j,k,l)], 
                                  -cube_pos_to_var[(i2,j,(k+1)%Y,l)]]
                    s.add_clause(constraint)

        # matching color of cube faces orthogonal to vector e3
        range_Z = range(Z) if cyclic else range(Z-1)
        for (j,k,l) in itertools.product(range(X),range(Y),range_Z):
            for i1,i2 in itertools.product(indices, repeat=2):
                if cubes[i1][2] != cubes[i2][5]:
                    constraint = [-cube_pos_to_var[(i1,j,k,l)], 
                                  -cube_pos_to_var[(i2,j,k,(l+1)%Z)]]
                    s.add_clause(constraint)

        # matching preassigned color constraints
        #legend = {0:'e1',1:'e2',2:'e3',3:'-e1',4:'-e2',5:'-e3'}
        for angle, D in enumerate(preassigned_color):
            for j,k,l in D:
                for i in indices:
                    if cubes[i][angle] != D[(j,k,l)]:
                        constraint = [-cube_pos_to_var[(i,j,k,l)]]
                        s.add_clause(constraint)

        return s

    def sat_solution_to_tiling(self, box, solution):
        r"""
        Return a configuration of cubes from a SAT solution

        INPUT:

        - ``box`` -- tuple of 3 integers
        - ``solution`` -- tuple of bools

        OUTPUT:

            dict

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: box = (2,2,2)
            sage: solution = (None, False, False, False, False, False,
            ....:   False, False, False, True, True, True, True, True, True, True,
            ....:   True, False, False, False, False, False, False, False, False)
            sage: T.sat_solution_to_tiling(box, solution)
            array([[[1, 1],
                    [1, 1]],
            <BLANKLINE>
                   [[1, 1],
                    [1, 1]]], dtype=int8)

        """
        (var_to_cube_pos,
         cube_pos_to_var) = self.sat_variable_to_cube_position_bijection(box)

        support = [key for (key,val) in enumerate(solution) if val]
        assert len(support) == box[0] * box[1] * box[2], ("len(support)={} "
                "!= volume of the box".format(len(support)))
        X,Y,Z = box
        #configuration = {(j,k,l):None for (j,k,l) in itertools.product(range(X),range(Y),range(Z))}
        import numpy
        configuration = numpy.zeros(box, dtype=numpy.int8)
        for val in support:
            i,j,k,l = var_to_cube_pos[val]
            configuration[(j,k,l)] = i
        return configuration

    def solve_tiling_a_box(self, box, cyclic=False, solver=None,
            solver_parameters=None, ncpus=1):
        r"""
        Return a configuration of cubes in a box matching the constraints

        INPUT:

        - ``box`` -- tuple of 3 integers
        - ``cyclic`` -- boolean (default: ``False``), whether the
          constraints on opposite boundary must match
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath
        - ``solver_parameters`` -- dict (default: ``{}``), parameters given
          to the MILP solver using method ``solver_parameter``. For a list
          of available parameters for example for the Gurobi backend, see
          dictionary ``parameters_type`` in the file
          ``sage/numerical/backends/gurobi_backend.pyx``
        - ``ncpus`` -- integer (default: ``1``), maximal number of
          subprocesses to use at the same time, used only if ``solver`` is
          ``'dancing_links'``.

        OUTPUT:

            dict

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: box = (2,2,2)
            sage: T.solve_tiling_a_box(box, solver='glucose')
            array([[[1, 1],
                    [1, 1]],
            <BLANKLINE>
                   [[1, 1],
                    [1, 1]]], dtype=int8)
            sage: T.solve_tiling_a_box(box, cyclic=True, solver='glucose')
            array([[[1, 1],
                    [1, 1]],
            <BLANKLINE>
                   [[1, 1],
                    [1, 1]]], dtype=int8)

        """
        if solver == 'dancing_links':
            raise NotImplementedError('TODO')

        elif solver in ['Gurobi', 'gurobi', 'GLPK', 'cplex', 'Coin', 'CVXOPT', 'PPL', None]:
            raise NotImplementedError('TODO')

        else: # we assume we use a sat solver
            (var_to_cube_pos,
             cube_pos_to_var) = self.sat_variable_to_cube_position_bijection(box)
            sat_solver = self.sat_solver(box=box, cyclic=cyclic, solver=solver)
            solution = sat_solver()
            del sat_solver
            if not solution:
                raise ValueError('no solution found using SAT solver (={})'.format(solver))
            return self.sat_solution_to_tiling(box, solution)

    def is_periodic_111(self):
        r"""
        Return True is some Wang cube tiles the space trivially.

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,0,1), (2,2,2,0,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic_111()
            True

        ::

            sage: cubes = [(1,0,0,0,0,0), (1,1,1,1,0,1), (2,2,2,0,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic_111()
            False

        """
        return any(all(cube[i]==cube[i+3] for i in range(3))
                   for cube in self.cubes().values())

    def is_periodic(self, stop=None, start=3, solver=None, certificate=False, verbose=False):
        r"""

        INPUT:

        - ``stop`` -- integer
        - ``start`` -- integer (default:``3``), sum of the sizes of the
          rectangular box
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath
        - ``certificate`` -- bool (default:``False``)
        - ``verbose`` -- bool (default:``False``)

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic(5, certificate=True)
            (True, (1, 1, 1))

        ::

            sage: cubes = [(0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 1)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic(5, certificate=True)

        """
        if start == 3:
            if self.is_periodic_111():
                if verbose:
                    print('trivial solution found!')
                if certificate:
                    return True, (1,1,1)
                else:
                    return True
            else:
                start = 4

        from sage.combinat.integer_lists.invlex import IntegerListsLex
        it = itertools.count(start) if stop is None else range(start, stop)
        for n in it:
            if verbose:
                print('Trying n=x+y+z={}'.format(n))
            for X_Y_Z in IntegerListsLex(n=n, length=3, min_part=1):
                if verbose:
                    print('Trying to tile (cyclically) a box of size (x,y,z)={}: '.format(X_Y_Z), end='')
                sat_solver = self.sat_solver(box=X_Y_Z, cyclic=True, solver=solver)
                solution = sat_solver()
                del sat_solver
                if solution:
                    if verbose:
                        print('solution found!')
                    if certificate:
                        return True, tuple(X_Y_Z)
                    else:
                        return True
                else:
                    if verbose:
                        print('no solution')


    def is_periodic_parallel(self, stop=None, solver=None,
            certificate=False, verbose=False, ncpus=8):
        r"""

        INPUT:

        - ``stop`` -- integer
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath
        - ``certificate`` -- bool (default:``False``)
        - ``verbose`` -- bool (default:``False``)
        - ``ncpus`` -- integer (default:``8``)

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic_parallel(5, certificate=True)
            (True, (1, 1, 1))

        """
        from sage.combinat.integer_lists.invlex import IntegerListsLex
        from sage.parallel.decorate import parallel

        @parallel(ncpus=ncpus)
        def find_cyclic_tiling(box):
            sat_solver = self.sat_solver(box=box, cyclic=True, solver=solver)
            solution = sat_solver()
            del sat_solver
            return solution

        it = itertools.count(3) if stop is None else range(3, stop)

        boxes = (box for n in it
                     for box in IntegerListsLex(n=n, length=3, min_part=1))

        for (args,kwds),result in find_cyclic_tiling(boxes):
            (arg,) = args
            if verbose:
                print('Trying to tile (cyclically) a box of size (x,y,z)={}: '.format(arg), end='')

            if result:
                if verbose:
                    print('solution found!')
                if certificate:
                    return True, tuple(arg)
                else:
                    return True
            else:
                if verbose:
                    print('no solution')


    def is_finite(self, stop=None, start=1, solver=None, certificate=False, verbose=False):
        r"""

        INPUT:

        - ``stop`` -- integer
        - ``start`` -- integer (default: ``1``)
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath
        - ``certificate`` -- bool (default:``False``)
        - ``verbose`` -- bool (default:``False``)

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,1,0,1,0), (1,1,3,1,2,1), (2,0,2,0,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_finite(5, certificate=True)
            (True, (2, 2, 2))

        """
        it = itertools.count(start) if stop is None else range(start, stop)
        for n in it:
            X_Y_Z = (n,n,n)
            if verbose:
                print('Trying to tile a box of size (x,y,z)={}: '.format(X_Y_Z), end='')
            sat_solver = self.sat_solver(box=X_Y_Z, cyclic=False, solver=solver)
            solution = sat_solver()
            del sat_solver
            if solution:
                if verbose:
                    print('solution found')
            else:
                if verbose:
                    print('no solution found!')
                if certificate:
                    return True, X_Y_Z
                else:
                    return True

    def is_aperiodic_candidate(self, stop=None, verbose=False, solver=None, certificate=True):
        r"""
        Return False if a periodic configuration is found or if some finite
        3d rectangular box admit no tiling.

        INPUT:

        - ``stop`` -- integer
        - ``solver`` -- string or None (default: ``None``), 
          ``'dancing_links'`` or the name of a MILP solver in Sage like
          ``'GLPK'``, ``'Coin'``, ``'cplex'`` or ``'Gurobi'`` or the name
          of a SAT solver in SageMath
        - ``certificate`` -- bool (default:``False``)
        - ``verbose`` -- bool (default:``False``)

        EXAMPLES::

            sage: from slabbe import WangCubeSet
            sage: cubes = [(0,0,1,0,1,0), (1,1,3,1,2,1), (2,0,2,0,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_aperiodic_candidate(5, certificate=True)
            (False, 'is_finite', (True, (2, 2, 2)))

        ::

            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_aperiodic_candidate(5, certificate=True)
            (False, 'is_periodic', (True, (1, 1, 1)))

        """
        from sage.parallel.decorate import parallel

        @parallel(ncpus=2)
        def call_method(method):
            F = getattr(self, method) 
            return F(stop=stop,verbose=verbose,solver=solver,certificate=certificate)

        methods = ['is_periodic', 'is_finite']
        #methods = ['is_periodic_parallel', 'is_finite']
        for ((args,kwds),result) in call_method(methods):
            (arg,) = args
            if result:
                if certificate:
                    return False, arg, result
                else:
                    return False

        if certificate:
            return True, None, None
        else:
            return True

class WangCubeSets(object):
    r"""
    Construct a set of Wang cubes.

    INPUT:

    - ``n`` -- integer, number of cubes

    EXAMPLES::

        sage: from slabbe.wang_cubes import WangCubeSets
        sage: S = WangCubeSets(3)

    """
    def __init__(self, n):
        r"""
        EXAMPLES::

            sage: from slabbe.wang_cubes import WangCubeSets
            sage: S = WangCubeSets(3)
        """
        self._n = n

    def __iter__(self):
        r"""
        Generates all sets of Wang cubes whose directed multigraph with loops
        in each direction has no sink and nor source.

        EXAMPLES::

            sage: from slabbe.wang_cubes import WangCubeSets
            sage: S = WangCubeSets(1)
            sage: L = list(S)
            sage: len(L)
            1

        ::


            sage: S = WangCubeSets(2)
            sage: L = list(S)
            sage: len(L)
            33

        ::

            sage: S = WangCubeSets(3)
            sage: L = list(S)
            sage: len(L)
            3142

        ::

            sage: S = WangCubeSets(4)
            sage: L = list(S)       # not tested # long (1min 43s)
            sage: len(L)            # not tested
            1545093

        All sets of 2 Wang cubes are periodic::

            sage: from collections import Counter
            sage: S = WangCubeSets(2)
            sage: c = Counter(T.is_aperiodic_candidate(7, solver='kissat') for T in S) # long time # known bug
            sage: dict(c)                                                              # long time # known bug
            {(False, 'is_periodic', (True, (1, 1, 1))): 11,
             (False, 'is_periodic', (True, (1, 1, 2))): 10,
             (False, 'is_periodic', (True, (1, 2, 2))): 8,
             (False, 'is_periodic', (True, (2, 2, 2))): 4}

        """
        from sage.combinat.permutation import Permutations
        P = Permutations(list(range(self._n)))

        from slabbe.graph import digraphs_with_n_edges
        L = digraphs_with_n_edges(self._n)

        for gx,gy,gz in itertools.combinations_with_replacement(L, 3):
            gx_edges = [(u,v) for (u,v,_) in gx.edges()]
            gy_edges = [(u,v) for (u,v,_) in gy.edges()]
            gz_edges = [(u,v) for (u,v,_) in gz.edges()]

            P_gy_edges = set(tuple(gy_edges[p[i]] for i in range(self._n)) for p in P)
            P_gz_edges = set(tuple(gz_edges[p[i]] for i in range(self._n)) for p in P)
            #print(len(L), len(P_gy_edges), len(P_gz_edges))

            for permuted_gy_edges,permuted_gz_edges in itertools.product(P_gy_edges, P_gz_edges):
                cubes = [(a,c,e,b,d,f) for (a,b),(c,d),(e,f) 
                                  in zip(gx_edges, permuted_gy_edges, permuted_gz_edges)]
                T = WangCubeSet(cubes)
                yield T

    def aperiodic_candidates(self, stop, verbose=False, solver='kissat',
            certificate=False, initial_candidates=None, ncpus=4):
        r"""
        EXAMPLES::

            sage: from slabbe.wang_cubes import WangCubeSets
            sage: S = WangCubeSets(2)
            sage: L = list(S.aperiodic_candidates(stop=4))   # long time (5s)    # known bug
            sage: len(L)                                     # long time (fast)  # known bug
            22

        This proves that there are no aperiodic set of 2 Wang cubes::

            sage: L = list(S.aperiodic_candidates(stop=7)) # not tested (3s)
            sage: len(L)                                   # not tested
            0

        Of the 3142 candidates of sets of 3 Wang cubes, their remains 1556
        to check::

            sage: S = WangCubeSets(3)
            sage: L = list(S.aperiodic_candidates(stop=6, verbose=True)) # not tested 4 min
            sage: len(L)                                                 # not tested
            1556
            sage: %time L = list(S.aperiodic_candidates(stop=7, verbose=True)) # not tested 4 min
            sage: len(L)                                                       # not tested
            1509

        ::

            sage: %time L = list(S.aperiodic_candidates(stop=13, verbose=True)) # not tested (6min)
            {(False, 'is_finite', 'NO DATA'): 11,
             (False, 'is_finite', (True, (2, 2, 2))): 792,
             (False, 'is_finite', (True, (3, 3, 3))): 289,
             (False, 'is_periodic', 'NO DATA'): 33,
             (False, 'is_periodic', (True, [1, 1, 2])): 155,
             (False, 'is_periodic', (True, [1, 1, 3])): 145,
             (False, 'is_periodic', (True, [1, 2, 1])): 23,
             (False, 'is_periodic', (True, [1, 2, 2])): 127,
             (False, 'is_periodic', (True, [1, 3, 3])): 220,
             (False, 'is_periodic', (True, [2, 1, 1])): 16,
             (False, 'is_periodic', (True, [2, 1, 2])): 26,
             (False, 'is_periodic', (True, [2, 2, 1])): 4,
             (False, 'is_periodic', (True, [2, 2, 2])): 34,
             (False, 'is_periodic', (True, [3, 1, 3])): 34
             (False, 'is_periodic', (True, [3, 3, 1])): 23, 
             (False, 'is_periodic', (True, [3, 3, 3])): 136, 
             (False, 'is_periodic', (True, [1, 1, 1])): 1074} 

        """
        from sage.parallel.decorate import parallel
        from collections import Counter

        @parallel(ncpus=ncpus)
        def is_it_aperiodic(candidate):
            return candidate.is_aperiodic_candidate(stop=stop,verbose=False,solver=solver,
                                                    certificate=True)

        if initial_candidates:
            L = list(initial_candidates)
        else:
            L = list(self)
            if verbose:
                print('list of {} candidates created'.format(len(L)))

        i = 0
        N = 0
        c = Counter()
        for (args,kwds),result in is_it_aperiodic(L):
            i += 1
            (arg,) = args
            c[result] += 1
            if verbose:
                print(i, arg.cubes(), result, N)
            if result is None:
                N += 1
                yield arg
            elif result[2] == 'NO DATA':
                N += 1
                yield arg
        if verbose:
            print(dict(c))




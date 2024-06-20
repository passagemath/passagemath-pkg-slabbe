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
        L = list(itertools.product(range(n_cubes), range(X), range(Y), range(Z)))
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
            [None, False, ... False, True, ... True]

        ::


            sage: s = T.sat_solver(box, cyclic=True)
            sage: s             # random
            PicoSAT solver: 24 variables, 176 clauses.
            sage: list(s())
            [None, False, ... False, True, ... True]

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
            {(0, 0, 0): 1,
             (0, 0, 1): 1,
             (0, 1, 0): 1,
             (0, 1, 1): 1,
             (1, 0, 0): 1,
             (1, 0, 1): 1,
             (1, 1, 0): 1,
             (1, 1, 1): 1}
            sage: T.solve_tiling_a_box(box, cyclic=True, solver='glucose')
            {(0, 0, 0): 1,
             (0, 0, 1): 1,
             (0, 1, 0): 1,
             (0, 1, 1): 1,
             (1, 0, 0): 1,
             (1, 0, 1): 1,
             (1, 1, 0): 1,
             (1, 1, 1): 1}

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
            if not solution:
                raise ValueError('no solution found using SAT solver (={})'.format(solver))
            support = [key for (key,val) in enumerate(solution) if val]
            assert len(support) == box[0] * box[1] * box[2], ("len(support)={} "
                    "!= volume of the box".format(len(support)))
            X,Y,Z = box
            configuration = {(j,k,l):None for (j,k,l) in itertools.product(range(X),range(Y),range(Z))}
            for val in support:
                i,j,k,l = var_to_cube_pos[val]
                configuration[(j,k,l)] = i
            return configuration

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
            (True, [1, 1, 1])

        """
        if start == 3:
            if self.is_periodic_111():
                if verbose:
                    print('trivial solution found!')
                if certificate:
                    return True, [1,1,1]
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
                if solution:
                    if verbose:
                        print('solution found!')
                    if certificate:
                        return True, X_Y_Z
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
            (True, [1, 1, 1])

        """
        from sage.combinat.integer_lists.invlex import IntegerListsLex
        from sage.parallel.decorate import parallel

        @parallel(ncpus=ncpus)
        def find_cyclic_tiling(box):
            sat_solver = self.sat_solver(box=box, cyclic=True, solver=solver)
            return sat_solver()

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
                    return True, arg
                else:
                    return True
            else:
                if verbose:
                    print('no solution')


    def is_finite(self, stop=None, solver=None, certificate=False, verbose=False):
        r"""

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
            sage: T.is_finite(5, certificate=True)
            (True, (2, 2, 2))

        """
        it = itertools.count(1) if stop is None else range(1, stop)
        for n in it:
            X_Y_Z = (n,n,n)
            if verbose:
                print('Trying to tile a box of size (x,y,z)={}: '.format(X_Y_Z), end='')
            sat_solver = self.sat_solver(box=X_Y_Z, cyclic=False, solver=solver)
            solution = sat_solver()
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
            (False, ('is_finite', True, (2, 2, 2)))

        ::

            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_aperiodic_candidate(5, certificate=True)
            (False, ('is_periodic', True, [1, 1, 1]))

        """
        from sage.parallel.decorate import parallel

        @parallel(ncpus=2)
        def call_method(method):
            F = getattr(self, method) 
            return F(stop=stop,verbose=verbose,solver=solver,certificate=certificate)

        methods = ['is_periodic', 'is_finite']
        #methods = ['is_periodic_parallel', 'is_finite']
        for ((args,kwds),result) in call_method(methods):
            if result:
                if certificate:
                    return False, args, result
                else:
                    return False

        return True

def KariCulik21cubes(version='what_seems_to_work'):
    r"""
    INPUT:

    - ``version`` -- string (optional). Valid options are:

      - ``'what_the_paper_say'``
      - ``'what_it_should_be'``
      - ``'what_seems_to_work'`` (default)

    EXAMPLES::

        sage: from slabbe.wang_cubes import KariCulik21cubes

    **What the paper say**

    The paper has a typo. There is an issue with the tiles in the set C
    because it admits a periodic configuration (a simple domino of tiles of
    indices 18 and 20)::

        sage: W21 = KariCulik21cubes(version='what_the_paper_say')
        sage: W21
        Set of Wang cubes of cardinality 21
        sage: W21.is_periodic(5, certificate=True, solver='kissat') # optional: kissat
        (True, [1, 2, 1])
        sage: W21.solve_tiling_a_box((1,2,1), cyclic=True, solver='kissat') # optional: kissat
        {(0, 0, 0): 18, (0, 1, 0): 20}
        sage: W21[18]
        (1, ('0/2', 1), (0, 1), 1, ('1/2', 1), (0, 1))
        sage: W21[20]
        (1, ('1/2', 1), (0, 1), 1, ('0/2', 1), (0, 1))

    The typo can be found by comparing the set of tiles in the set C with
    the 4 tiles removed from the set T_{13} to define T_9. We observe that
    in one of the tile, the bottom edge labeled 1 needs to be replaced by 0
    (or 0'?). There is an ambiguity here on how to fix the typo, because
    the typo precisely involves the two tiles that are equal except the
    bottom edge labeled 0 or 0' (this is the great contribution made by
    Culik (adding the 0' on some horizontal edges) for creating the 13
    tiles from the 12 naturally obtained from the multiplication by 1/2 and
    by 3). 

    **What it should be**

    Kari (personnal communication, April 2nd, 2024, at CIRM, Marseille)
    believes the typo should be fixed by replacing it by 0'. But this
    does not seem to work, because the 21 cubes that we get do not tile a
    6x6x6 block::
    
        sage: W21 = KariCulik21cubes(version='what_it_should_be')
        sage: W21.is_finite(10, certificate=True, solver='kissat') # optional: kissat # long time (2s)
        (True, (6, 6, 6))
        sage: W21.solve_tiling_a_box((6,6,6), solver='kissat') # optional: kissat
        Traceback (most recent call last):
        ...
        ValueError: no solution found using SAT solver (=kissat)

    **What seems to work**

    What seems to work is to replace the 1 by a 0::

        sage: W21 = KariCulik21cubes(version='what_seems_to_work')
        sage: W21 = KariCulik21cubes()                             # its the default
        sage: W21
        Set of Wang cubes of cardinality 21

    No short periodic configuration is found::

        sage: W21.is_periodic(6, certificate=True, solver='kissat', verbose=True) # optional: kissat # long time (2s)
        Trying n=x+y+z=3
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 1, 1]
        Trying n=x+y+z=4
        Trying to tile (cyclically) a box of size (x,y,z)=[2, 1, 1]
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 2, 1]
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 1, 2]
        Trying n=x+y+z=5
        Trying to tile (cyclically) a box of size (x,y,z)=[3, 1, 1]
        Trying to tile (cyclically) a box of size (x,y,z)=[2, 2, 1]
        Trying to tile (cyclically) a box of size (x,y,z)=[2, 1, 2]
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 3, 1]
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 2, 2]
        Trying to tile (cyclically) a box of size (x,y,z)=[1, 1, 3]

    We check that it can tile larger and larger boxes::

        sage: W21.is_finite(7, certificate=True, verbose=True, solver='kissat') # optional: kissat # long time (2s) 
        Trying to tile a box of size (x,y,z)=(1, 1, 1)
        Trying to tile a box of size (x,y,z)=(2, 2, 2)
        Trying to tile a box of size (x,y,z)=(3, 3, 3)
        Trying to tile a box of size (x,y,z)=(4, 4, 4)
        Trying to tile a box of size (x,y,z)=(5, 5, 5)
        Trying to tile a box of size (x,y,z)=(6, 6, 6)

    Tested up to 26x26x26::

        sage: from slabbe.wang_cubes import KariCulik21cubes
        sage: W21 = KariCulik21cubes(version='what_seems_to_work')
        sage: W21.is_finite(30, certificate=True, solver='kissat', verbose=True) # not tested
        Trying to tile a box of size (x,y,z)=(1, 1, 1)
        Trying to tile a box of size (x,y,z)=(2, 2, 2)
        Trying to tile a box of size (x,y,z)=(3, 3, 3)
        Trying to tile a box of size (x,y,z)=(4, 4, 4)
        Trying to tile a box of size (x,y,z)=(5, 5, 5)
        Trying to tile a box of size (x,y,z)=(6, 6, 6)
        Trying to tile a box of size (x,y,z)=(7, 7, 7)
        Trying to tile a box of size (x,y,z)=(8, 8, 8)
        Trying to tile a box of size (x,y,z)=(9, 9, 9)
        Trying to tile a box of size (x,y,z)=(10, 10, 10)
        Trying to tile a box of size (x,y,z)=(11, 11, 11)
        Trying to tile a box of size (x,y,z)=(12, 12, 12)
        Trying to tile a box of size (x,y,z)=(13, 13, 13)
        Trying to tile a box of size (x,y,z)=(14, 14, 14)
        Trying to tile a box of size (x,y,z)=(15, 15, 15)
        Trying to tile a box of size (x,y,z)=(16, 16, 16)
        Trying to tile a box of size (x,y,z)=(17, 17, 17)
        Trying to tile a box of size (x,y,z)=(18, 18, 18)
        Trying to tile a box of size (x,y,z)=(19, 19, 19)
        Trying to tile a box of size (x,y,z)=(20, 20, 20)
        Trying to tile a box of size (x,y,z)=(21, 21, 21)
        Trying to tile a box of size (x,y,z)=(22, 22, 22)
        Trying to tile a box of size (x,y,z)=(23, 23, 23)
        Trying to tile a box of size (x,y,z)=(24, 24, 24)
        Trying to tile a box of size (x,y,z)=(25, 25, 25)
        Trying to tile a box of size (x,y,z)=(26, 26, 26)
        Traceback (most recent call last):
        ...
        KeyboardInterrupt:

    REFERENCES:

        Culik, Karel, II, et Jarkko Kari. « An aperiodic set of Wang cubes ».
        In STACS 96 (Grenoble, 1996), 1046:137‑46. Lecture Notes in Comput.
        Sci. Springer, Berlin, 1996.
        https://mathscinet.ams.org/mathscinet-getitem?mr=1462092.
    """
    divide_by_2 = [("0/2","0'","0/2",0), ("0/2",2,"0/2",1), ("1/2",1,"0/2",0), ("1/2",1,"0/2","0'"), ("1/2","0'","1/2",0), ("1/2",2,"1/2",1), ("0/2",1,"1/2",1)]
    times_3 = [(-1,1,-2,2), (0,1,-2,1), (0,1,-1,2), (-2,0,-1,1), (-2,0,0,2), (-1,0,0,1)]
    Culik_T13 = divide_by_2 + times_3
    to_remove = [("0/2",2,"0/2",1), ("1/2",1,"0/2",0), ("1/2",2,"1/2",1), ("0/2",1,"1/2",1)]
    T_9 = [t for t in Culik_T13 if t not in to_remove]
    assert len(T_9) == 9, "len(T9)(={}) should be 9".format(len(T_9))

    A = [((s,1),a,b,(t,1), (1,1), (1,1)) for (t,a,s,b) in T_9]
    B = [((s,x),2,1,(s,y), (1,x), (1,(x+y)%2)) for s in ["0/2","1/2"]
                                               for x in [0,1]
                                               for y in [0,1]]
    C = [(("1/2",1),1,1,("0/2",x), (0,1), (0,1)) for x in [0,1]]

    if version == 'what_the_paper_say':
        C += [(("0/2",1),1,1,("1/2",x), (0,1), (0,1)) for x in [0,1]]  
    elif version == 'what_it_should_be':
        # what it should be
        # (Kari, personnal communication, April 2nd, 2024, at CIRM)
        C += [(("0/2",1),1,"0'",("1/2",x), (0,1), (0,1)) for x in [0,1]]
    elif version == 'what_seems_to_work':
        C += [(("0/2",1),1,0,("1/2",x), (0,1), (0,1)) for x in [0,1]]
    else:
        raise ValueError('invalid version (={})'.format(version))

    W_21 = A + B + C

    # NOTE: the first pages of the paper say they use (left, right, front, back, top, bottom)
    # but they really use (left, front, back, right, top, bottom)

    W_21_reordered = [(front, right, top, back, left, bottom)
                      for (left, front, back, right, top, bottom) in W_21]

    return WangCubeSet(W_21_reordered)


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
            sage: len(L)
            1545093

        All sets of 2 Wang cubes are periodic::

            sage: from collections import Counter
            sage: S = WangCubeSets(2)
            sage: c = Counter(T.is_aperiodic_candidate(7, solver='kissat') for T in S)
            sage: dict(c)
            {(False, ('is_periodic',), (True, [1, 1, 1])): 11,
             (False, ('is_periodic',), (True, [1, 1, 2])): 10,
             (False, ('is_periodic',), (True, [1, 2, 2])): 8,
             (False, ('is_periodic',), (True, [2, 2, 2])): 4}

        """
        from sage.combinat.permutation import Permutations
        P = Permutations(list(range(self._n)))

        L = self._graphs_with_n_edges()
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

    @cached_method
    def _graphs_with_n_edges(self):
        r"""
        Return the list of directed multigraphs graphs with loops with n
        edges with no sink nor sources.

        EXAMPLES::

            sage: from slabbe.wang_cubes import WangCubeSets
            sage: S = WangCubeSets(1)
            sage: S._graphs_with_n_edges()
            [Looped multi-digraph on 1 vertex]
            sage: S = WangCubeSets(2)
            sage: S._graphs_with_n_edges()
            [Looped multi-digraph on 1 vertex,
             Looped multi-digraph on 2 vertices,
             Looped multi-digraph on 2 vertices]
            sage: S = WangCubeSets(3)
            sage: S._graphs_with_n_edges()
            [Looped multi-digraph on 1 vertex,
             Looped multi-digraph on 2 vertices,
             Looped multi-digraph on 2 vertices,
             Looped multi-digraph on 2 vertices,
             Looped multi-digraph on 3 vertices,
             Looped multi-digraph on 3 vertices,
             Looped multi-digraph on 2 vertices,
             Looped multi-digraph on 3 vertices]

        ::

            sage: len(list(WangCubeSets(4)._graphs_with_n_edges())) # long (10s)
            29
            sage: len(list(WangCubeSets(5)._graphs_with_n_edges())) # not tested (1h)
            110

        List [1,3,8,29,110] is almost related to https://oeis.org/A350907 ?
        "Number of unlabeled initially connected digraphs with n arcs." 

        """
        from sage.graphs.digraph import DiGraph

        def has_sink(G):
            return any(d== 0 for d in G.out_degree_iterator())
        def has_source(G):
            return any(d== 0 for d in G.in_degree_iterator())

        L = []

        nvertices = 2 * self._n
        V = list(range(nvertices))
        VV = list(itertools.product(V, repeat=2))
        for edges in itertools.combinations_with_replacement(VV, self._n):
            g = DiGraph(edges, format='list_of_edges', loops=True, multiedges=True)
            if has_sink(g) or has_source(g):
                continue
            if any(g.is_isomorphic(h) for h in L):
                continue

            L.append(g)

        return L

    def _graphs_with_n_edges_more_clever(self):
        r"""
        EXAMPLES::

        - allows loops?
        - allows multiedges?

        Idea: use `integer_lists_mod_perm_group` in the Vincent package
        `adm_cycles` which is better than the one in Sage.

        See: https://gitlab.com/modulispaces/admcycles/-/blob/master/admcycles/integer_list.py?ref_type=heads

        ::

            sage: I = IntegerVectorsModPermutationGroup(PermutationGroup([[(1,2,3)]]), sum=6)
            sage: I.cardinality()
            10
            sage: I.list()
            [[6, 0, 0], [5, 1, 0], [5, 0, 1], [4, 2, 0], [4, 1, 1],
             [4, 0, 2], [3, 3, 0], [3, 2, 1], [3, 1, 2], [2, 2, 2]]

        """
        from sage.graphs.digraph_generators import digraphs
        #max_nvertices = 2 * self._n
        max_nvertices = self._n
        for nvertices in range(1, max_nvertices+1):
            for g in digraphs(nvertices, size=self._n, copy=True):
                yield g

    def aperiodic_candidates(self, stop, verbose=False, solver='kissat',
            certificate=False, initial_candidates=None, ncpus=8):
        r"""
        EXAMPLES::

            sage: from slabbe.wang_cubes import WangCubeSets
            sage: S = WangCubeSets(2)
            sage: L = list(S.aperiodic_candidates(stop=4))   # long time (5s)
            sage: len(L)                                     # long time (fast)
            22

        This proves that there are no aperiodic set of 2 Wang cubes::

            sage: L = list(S.aperiodic_candidates(stop=7)) # not tested (3s)
            sage: len(L)
            0

        Of the 3142 candidates of sets of 3 Wang cubes, their remains 1556
        to check::

            sage: S = WangCubeSets(3)
            sage: L = list(S.aperiodic_candidates(stop=6, verbose=True)) # not tested 4 min
            sage: len(L)
            1556
            sage: c = Counter(T.is_aperiodic_candidate(7, solver='kissat') for T in S)
            sage: %time L = list(S.aperiodic_candidates(stop=7, verbose=True)) # not tested 4 min
            sage: len(L)
            1509

        ::

            sage: %time L = list(S.aperiodic_candidates(stop=13, verbose=True)) # not tested (6min)
            {(False, ('is_finite',), 'NO DATA'): 11,
             (False, ('is_finite',), (True, (2, 2, 2))): 792,
             (False, ('is_finite',), (True, (3, 3, 3))): 289,
             (False, ('is_periodic',), 'NO DATA'): 33,
             (False, ('is_periodic',), (True, [1, 1, 2])): 155,
             (False, ('is_periodic',), (True, [1, 1, 3])): 145,
             (False, ('is_periodic',), (True, [1, 2, 1])): 23,
             (False, ('is_periodic',), (True, [1, 2, 2])): 127,
             (False, ('is_periodic',), (True, [1, 3, 3])): 220,
             (False, ('is_periodic',), (True, [2, 1, 1])): 16,
             (False, ('is_periodic',), (True, [2, 1, 2])): 26,
             (False, ('is_periodic',), (True, [2, 2, 1])): 4,
             (False, ('is_periodic',), (True, [2, 2, 2])): 34,
             (False, ('is_periodic',), (True, [3, 1, 3])): 34
             (False, ('is_periodic',), (True, [3, 3, 1])): 23, 
             (False, ('is_periodic',), (True, [3, 3, 3])): 136, 
             (False, ('is_periodic',), (True, [1, 1, 1])): 1074} 

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
            elif result == 'NO DATA':
                N += 1
                yield arg
        if verbose:
            print(dict(c))




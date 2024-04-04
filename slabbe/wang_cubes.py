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

    def is_periodic(self, stop=None, solver=None, certificate=False, verbose=False):
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
            sage: cubes = [(0,0,0,0,0,0), (1,1,1,1,1,1), (2,2,2,2,2,2)]
            sage: T = WangCubeSet(cubes)
            sage: T.is_periodic(5, certificate=True)
            (True, [1, 1, 1])

        """
        from sage.combinat.integer_lists.invlex import IntegerListsLex
        it = itertools.count(3) if stop is None else range(3, stop)
        for n in it:
            if verbose:
                print('Trying n=x+y+z={}'.format(n))
            for X_Y_Z in IntegerListsLex(n=n, length=3, min_part=1):
                if verbose:
                    print('Trying to tile (cyclically) a box of size (x,y,z)={}'.format(X_Y_Z))
                sat_solver = self.sat_solver(box=X_Y_Z, cyclic=True, solver=solver)
                solution = sat_solver()
                if solution:
                    if certificate:
                        return True, X_Y_Z
                    else:
                        return True

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
                print('Trying to tile a box of size (x,y,z)={}'.format(X_Y_Z))
            sat_solver = self.sat_solver(box=X_Y_Z, cyclic=False, solver=solver)
            solution = sat_solver()
            if not solution:
                if certificate:
                    return True, X_Y_Z
                else:
                    return True

    def is_aperiodic(self, verbose=True):
        r"""
        Return False if a periodic configuration is found or if some finite
        3d rectangular box admit to tiling.
        """
        raise NotImplementedError

def KariCulik21cubes():
    r"""
    EXAMPLES::

        sage: W21 = KariCulik21cubes()
        sage: W21
        Set of Wang cubes of cardinality 21

    No short periodic configuration is found::

        sage: W21.is_periodic(9, certificate=True, solver='kissat')   # not tested # long (11 s)

    Problem, it can't not find a tiling of a 2x2x2 box (???)::

        sage: W21.is_finite(9, certificate=True, verbose=True, solver='kissat')
        Trying to tile a box of size (x,y,z)=(1, 1, 1)
        Trying to tile a box of size (x,y,z)=(2, 2, 2)
        (True, (2, 2, 2))

    ::

        sage: W21.solve_tiling_a_box((2,2,2), solver='kissat')
        Traceback (most recent call last):
        ...
        ValueError: no solution found using SAT solver (=kissat)

    Is there a problem in the interpretation of the definition of the set `W_21`?

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
    C = [(("1/2",1),1,1,("0/2",0), (0,1), (0,1)),
         (("1/2",1),1,1,("0/2",1), (0,1), (0,1)),
         (("0/2",1),1,1,("1/2",0), (0,1), (0,1)),
         (("0/2",1),1,1,("1/2",1), (0,1), (0,1))]
    W_21 = A + B + C

    # NOTE: Kari, Culik claim they use (left, right, front, back, top, bottom)
    # but they rather use (left, front, back, right, top, bottom)

    W_21_reordered = [(front, right, top, back, left, bottom)
                      for (left, front, back, right, top, bottom) in W_21]

    return WangCubeSet(W_21_reordered)



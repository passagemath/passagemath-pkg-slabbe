# -*- coding: utf-8 -*-
r"""
The code in Metallic mean Wang tiles II [Lab2024]_.

EXAMPLES:

The set of Wang tiles::

    sage: from slabbe.arXiv_2403_03197 import metallic_mean_wang_tile_set
    sage: metallic_mean_wang_tile_set(1)
    Wang tile set of cardinality 16
    sage: metallic_mean_wang_tile_set(2)
    Wang tile set of cardinality 25

The partition::

    sage: from slabbe.arXiv_2403_03197 import partition
    sage: partition(1)
    Polyhedron partition of 16 atoms with 16 letters
    sage: partition(2)
    Polyhedron partition of 25 atoms with 25 letters
    sage: partition(3)
    Polyhedron partition of 36 atoms with 36 letters

The self-similarity::

    sage: from slabbe.arXiv_2403_03197 import self_similarity
    sage: self_similarity(2)            # long time (3s)
    Substitution 2d: {0: [[3, 15, 18], [6, 21, 22], [12, 23, 24]], 1: [[2,
    14, 17], [6, 21, 22], [12, 23, 24]], 2: [[1, 15, 18], [5, 21, 22], [10, 23,
    24]], 3: [[0, 14, 17], [5, 21, 22], [10, 23, 24]], 4: [[0, 14, 15], [5, 21,
    22], [10, 23, 24]], 5: [[4, 19, 20], [10, 23, 24]], 6: [[3, 17, 20], [10, 21,
    24]], 7: [[0, 14, 17], [5, 21, 22], [6, 23, 24]], 8: [[0, 14, 15], [5, 21, 22],
    [6, 23, 24]], 9: [[4, 19, 20], [6, 23, 24]], 10: [[3, 17, 20], [6, 21, 24]],
    11: [[2, 16, 19], [6, 21, 24]], 12: [[3, 15, 18], [6, 21, 22]], 13: [[2, 14,
    17], [6, 21, 22]], 14: [[7, 17], [11, 22], [13, 24]], 15: [[3, 17], [10, 21],
    [13, 24]], 16: [[7, 15], [11, 22], [13, 24]], 17: [[3, 15], [10, 21], [13,
    24]], 18: [[3, 15], [6, 21], [12, 23]], 19: [[1, 15], [9, 21], [11, 24]], 20:
    [[1, 15], [5, 21], [10, 23]], 21: [[8, 19], [11, 24]], 22: [[4, 19], [10, 23]],
    23: [[7, 17], [11, 22]], 24: [[3, 17], [10, 21]]}

REFERENCES:

.. [Lab2024] S. Labbé. Metallic mean Wang tiles II: the dynamics of an
   aperiodic computer chip, :arXiv:`2403.03197`

"""
#*****************************************************************************
#       Copyright (C) 2024-2025 Sébastien Labbé <slabqc@gmail.com>
#
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)
#
#  The full text of the GPLv2 is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from sage.misc.cachefunc import cached_function

def vector_to_str(v):
    r"""
    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import vector_to_str
        sage: vector_to_str((0,1,4))
        '014'
    """
    return "".join(str(a) for a in v)

@cached_function
def nth_metallic_mean(n):
    r"""
    INPUT:

    - ``n`` -- integer

    EXAMPLES::
    
        sage: from slabbe.arXiv_2403_03197 import nth_metallic_mean    
        sage: nth_metallic_mean(3)
        beta
        sage: nth_metallic_mean(3).n()
        3.30277563773199

    """
    from sage.rings.rational_field import QQ
    from sage.rings.polynomial.polynomial_ring import polygen
    from sage.rings.number_field.number_field import NumberField
    from sage.rings.real_mpfr import RR

    x = polygen(QQ, "x")
    K = NumberField(x**2 - n*x - 1, name='beta', embedding=RR(n))
    beta = K.gen()
    return beta

def Lambda_inv(a,b,c, n):
    r"""
    Return the (a,b,c) atom in the EAST partition.

    INPUT:

    - ``a`` -- integer
    - ``b`` -- integer
    - ``c`` -- integer
    - ``n`` -- integer

    OUTPUT:

    Polyhedron

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import Lambda_inv
        sage: Lambda_inv(0,0,3,5)
        A 2-dimensional polyhedron in (Number Field in beta with defining
        polynomial x^2 - 5*x - 1 with beta = 5.192582403567252?)^2 defined as
        the convex hull of 4 vertices
        sage: Lambda_inv(0,0,3,5).volume()
        -5/2*beta + 13

    TESTS::

        sage: n = 3
        sage: Vn = [(a,b,c) for a in range(2) for b in range(2) for c in range(n+2) if a<=b<=c]

    Sum of the atom is 1::

        sage: sum(Lambda_inv(*v, n=n).volume() for v in Vn)
        1     

    One of the atom has empty interior::

        sage: Lambda_inv(0,0,n+1, n).volume()
        0
    """
    from sage.geometry.polyhedron.constructor import Polyhedron

    beta = nth_metallic_mean(n)

    unit_square_ieqs = [[0, 1, 0], [0, 0, 1], [1, -1, 0], [1, 0, -1]]
    ieqs = list(unit_square_ieqs)
    ieqs.extend([[-1/beta+1-a, 0, 1], [a+1/beta, 0, -1]])
    ieqs.extend([[-1/beta+1-b, 1/beta, 1], [b+1/beta, -1/beta, -1]])
    ieqs.extend([[-1/beta+1-c, beta, 1], [c+1/beta, -beta, -1]])
    return Polyhedron(ieqs=ieqs)

def east_partition(n):
    r"""
    Return the EAST partition

    INPUT:

    - ``n`` -- integer

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import east_partition
        sage: east_partition(3)
        Polyhedron partition of 12 atoms with 12 letters

    """
    from slabbe import PolyhedronPartition
    Vn = [(a,b,c) for a in range(2) for b in range(2) for c in range(n+2) if a<=b<=c]
    atoms = {vector_to_str(v):Lambda_inv(*v, n=n) for v in Vn}
    non_empty_atoms = {key:atom for (key,atom) in atoms.items() if atom.volume() > 0}
    EAST = PolyhedronPartition(non_empty_atoms)
    return EAST

def east_north_west_south_partitions(n):
    r"""
    INPUT:

    - ``n`` -- integer

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import east_north_west_south_partitions
        sage: east_north_west_south_partitions(3)
        (Polyhedron partition of 12 atoms with 12 letters,
         Polyhedron partition of 12 atoms with 12 letters,
         Polyhedron partition of 15 atoms with 12 letters,
         Polyhedron partition of 15 atoms with 12 letters)

    """
    from sage.matrix.constructor import matrix
    from sage.matrix.special import identity_matrix
    from sage.modules.free_module_element import vector

    beta = nth_metallic_mean(n)

    EAST = east_partition(n)
    M = matrix(2, (0,1,1,0))
    NORTH = EAST.apply_linear_map(M)

    lattice_base = identity_matrix(2)
    from slabbe import PolyhedronExchangeTransformation as PET
    Re1 = PET.toral_translation(lattice_base, vector((1/beta,0)))
    Re2 = PET.toral_translation(lattice_base, vector((0,1/beta)))

    WEST = Re1(EAST)
    SOUTH = Re2(NORTH)

    return EAST, NORTH, WEST, SOUTH

def partition(n):
    r"""
    INPUT:

    - ``n`` -- integer

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import partition
        sage: partition(1)
        Polyhedron partition of 16 atoms with 16 letters
        sage: partition(2)
        Polyhedron partition of 25 atoms with 25 letters
        sage: partition(3)
        Polyhedron partition of 36 atoms with 36 letters
        sage: partition(4)
        Polyhedron partition of 49 atoms with 49 letters

    """
    from sage.matrix.constructor import matrix

    EAST = east_partition(n)
    M = matrix(2, (0,1,1,0))
    NORTH = EAST.apply_linear_map(M)
    
    PEN,dEN = EAST.refinement(NORTH, certificate=True)

    return PEN

def metallic_mean_wang_tile_set(n):
    r"""
    Return the n-th metallic mean Wang tile set.

    It contains (n+3)^2 Wang tiles.

    INPUT:

    - ``n`` -- integer

    OUTPUT:

    a set of Wang tiles

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import metallic_mean_wang_tile_set
        sage: metallic_mean_wang_tile_set(1)
        Wang tile set of cardinality 16
        sage: metallic_mean_wang_tile_set(2)
        Wang tile set of cardinality 25
        sage: metallic_mean_wang_tile_set(2).tiles()
        [('000', '000', '002', '002'),
         ('000', '001', '012', '002'),
         ('001', '000', '002', '012'),
         ('001', '001', '012', '012'),
         ('001', '011', '013', '012'),
         ('001', '111', '000', '112'),
         ('002', '111', '001', '112'),
         ('011', '001', '012', '013'),
         ('011', '011', '013', '013'),
         ('011', '111', '000', '113'),
         ('012', '111', '001', '113'),
         ('012', '112', '011', '113'),
         ('013', '111', '002', '113'),
         ('013', '112', '012', '113'),
         ('111', '001', '112', '000'),
         ('111', '002', '112', '001'),
         ('111', '011', '113', '000'),
         ('111', '012', '113', '001'),
         ('111', '013', '113', '002'),
         ('112', '012', '113', '011'),
         ('112', '013', '113', '012'),
         ('112', '112', '111', '111'),
         ('112', '113', '111', '112'),
         ('113', '112', '112', '111'),
         ('113', '113', '112', '112')]

    """

    EAST, NORTH, WEST, SOUTH = east_north_west_south_partitions(n)
    
    PEN,dEN = EAST.refinement(NORTH, certificate=True)
    PWS,dWS = WEST.refinement(SOUTH, certificate=True)
    
    assert PWS.is_equal_up_to_relabeling(PEN)
    P = PEN           # faster than P = PEN.refinement(PWS)
    bijection = P.keys_permutation(PWS)
    
    from slabbe import WangTileSet
    tiles = [dEN[i]+dWS[bijection[i]] for i in sorted(dEN)]
    Tn = WangTileSet(tiles)

    return Tn

def self_similarity(n):
    r"""
    Return the self-similarity of the n-th metallic mean Wang shift.

    INPUT:

    - ``n`` -- integer

    OUTPUT:

    a 2-dimensional substitution

    EXAMPLES::

        sage: from slabbe.arXiv_2403_03197 import self_similarity
        sage: self_similarity(1)            # long time (1s)
        Substitution 2d: {0: [[3, 13], [9, 15]], 1: [[2, 12], [9, 15]], 2: [[1,
        13], [8, 15]], 3: [[0, 12], [8, 15]], 4: [[0, 11], [8, 15]], 5: [[7, 14]], 6:
        [[0, 12], [5, 15]], 7: [[0, 11], [5, 15]], 8: [[4, 14]], 9: [[3, 13]], 10: [[2,
        12]], 11: [[7], [10]], 12: [[6], [10]], 13: [[3], [9]], 14: [[1], [8]], 15:
        [[7]]}

    ::

        sage: self_similarity(2)            # long time (3s)
        Substitution 2d: {0: [[3, 15, 18], [6, 21, 22], [12, 23, 24]], 1: [[2,
        14, 17], [6, 21, 22], [12, 23, 24]], 2: [[1, 15, 18], [5, 21, 22], [10, 23,
        24]], 3: [[0, 14, 17], [5, 21, 22], [10, 23, 24]], 4: [[0, 14, 15], [5, 21,
        22], [10, 23, 24]], 5: [[4, 19, 20], [10, 23, 24]], 6: [[3, 17, 20], [10, 21,
        24]], 7: [[0, 14, 17], [5, 21, 22], [6, 23, 24]], 8: [[0, 14, 15], [5, 21, 22],
        [6, 23, 24]], 9: [[4, 19, 20], [6, 23, 24]], 10: [[3, 17, 20], [6, 21, 24]],
        11: [[2, 16, 19], [6, 21, 24]], 12: [[3, 15, 18], [6, 21, 22]], 13: [[2, 14,
        17], [6, 21, 22]], 14: [[7, 17], [11, 22], [13, 24]], 15: [[3, 17], [10, 21],
        [13, 24]], 16: [[7, 15], [11, 22], [13, 24]], 17: [[3, 15], [10, 21], [13,
        24]], 18: [[3, 15], [6, 21], [12, 23]], 19: [[1, 15], [9, 21], [11, 24]], 20:
        [[1, 15], [5, 21], [10, 23]], 21: [[8, 19], [11, 24]], 22: [[4, 19], [10, 23]],
        23: [[7, 17], [11, 22]], 24: [[3, 17], [10, 21]]}

    ::

        sage: self_similarity(3)            # long time (8s)
        Substitution 2d: {0: [[3, 18, 19, 23], [6, 27, 28, 29], [7, 30, 31,
        32], [15, 33, 34, 35]], 1: [[2, 17, 18, 22], [6, 27, 28, 29], [7, 30, 31, 32],
        [15, 33, 34, 35]], 2: [[1, 18, 19, 23], [5, 27, 28, 29], [6, 30, 31, 32], [13,
        33, 34, 35]], 3: [[0, 17, 18, 22], [5, 27, 28, 29], [6, 30, 31, 32], [13, 33,
        34, 35]], 4: [[0, 17, 18, 19], [5, 27, 28, 29], [6, 30, 31, 32], [13, 33, 34,
        35]], 5: [[4, 24, 25, 26], [6, 30, 31, 32], [13, 33, 34, 35]], 6: [[3, 21, 25,
        26], [6, 27, 31, 32], [13, 30, 34, 35]], 7: [[3, 18, 22, 26], [6, 27, 28, 32],
        [13, 30, 31, 35]], 8: [[0, 17, 18, 22], [5, 27, 28, 29], [6, 30, 31, 32], [7,
        33, 34, 35]], 9: [[0, 17, 18, 19], [5, 27, 28, 29], [6, 30, 31, 32], [7, 33,
        34, 35]], 10: [[4, 24, 25, 26], [6, 30, 31, 32], [7, 33, 34, 35]], 11: [[3, 21,
        25, 26], [6, 27, 31, 32], [7, 30, 34, 35]], 12: [[2, 20, 24, 25], [6, 27, 31,
        32], [7, 30, 34, 35]], 13: [[3, 18, 22, 26], [6, 27, 28, 32], [7, 30, 31, 35]],
        14: [[2, 17, 21, 25], [6, 27, 28, 32], [7, 30, 31, 35]], 15: [[3, 18, 19, 23],
        [6, 27, 28, 29], [7, 30, 31, 32]], 16: [[2, 17, 18, 22], [6, 27, 28, 29], [7,
        30, 31, 32]], 17: [[8, 18, 22], [12, 28, 29], [14, 31, 32], [16, 34, 35]], 18:
        [[3, 18, 22], [11, 27, 28], [14, 31, 32], [16, 34, 35]], 19: [[3, 18, 22], [6,
        27, 28], [13, 30, 31], [16, 34, 35]], 20: [[8, 18, 19], [12, 28, 29], [14, 31,
        32], [16, 34, 35]], 21: [[3, 18, 19], [11, 27, 28], [14, 31, 32], [16, 34,
        35]], 22: [[3, 18, 19], [6, 27, 28], [13, 30, 31], [16, 34, 35]], 23: [[3, 18,
        19], [6, 27, 28], [7, 30, 31], [15, 33, 34]], 24: [[1, 18, 19], [10, 27, 28],
        [12, 31, 32], [14, 34, 35]], 25: [[1, 18, 19], [5, 27, 28], [11, 30, 31], [14,
        34, 35]], 26: [[1, 18, 19], [5, 27, 28], [6, 30, 31], [13, 33, 34]], 27: [[9,
        24, 25], [12, 31, 32], [14, 34, 35]], 28: [[4, 24, 25], [11, 30, 31], [14, 34,
        35]], 29: [[4, 24, 25], [6, 30, 31], [13, 33, 34]], 30: [[8, 21, 25], [12, 28,
        32], [14, 31, 35]], 31: [[3, 21, 25], [11, 27, 31], [14, 31, 35]], 32: [[3, 21,
        25], [6, 27, 31], [13, 30, 34]], 33: [[8, 18, 22], [12, 28, 29], [14, 31, 32]],
        34: [[3, 18, 22], [11, 27, 28], [14, 31, 32]], 35: [[3, 18, 22], [6, 27, 28],
        [13, 30, 31]]}

    """
    from sage.matrix.special import identity_matrix
    from sage.modules.free_module_element import vector

    beta = nth_metallic_mean(n)
    
    lattice_base = identity_matrix(2)
    from slabbe import PolyhedronExchangeTransformation as PET
    Re1 = PET.toral_translation(lattice_base, vector((1/beta,0)))
    Re2 = PET.toral_translation(lattice_base, vector((0,1/beta)))

    P = partition(n)
    
    x_le_beta_inv = [1/beta,-1,0]
    P1,s1 = Re1.induced_partition(x_le_beta_inv, P, substitution_type="row")
    R1e1,_ = Re1.induced_transformation(x_le_beta_inv)
    R1e2,_ = Re2.induced_transformation(x_le_beta_inv)
    
    y_le_beta_inv = [1/beta,0,-1]
    P2,s2 = Re2.induced_partition(y_le_beta_inv, P1, substitution_type="column")
    R2e1,_ = R1e1.induced_transformation(y_le_beta_inv)
    R2e2,_ = R1e2.induced_transformation(y_le_beta_inv)
    
    P2_scaled = (-beta * P2).translate((1,1))
    P3 = Re2(Re1(P2_scaled))
    
    assert P.is_equal_up_to_relabeling(P3)
    assert Re1 == (beta * R2e1).inverse()
    assert Re2 == (beta * R2e2).inverse()
    
    from slabbe import Substitution2d
    s3 = Substitution2d.from_permutation(P.keys_permutation(P3))
    self_similarity = s1*s2*s3

    return self_similarity



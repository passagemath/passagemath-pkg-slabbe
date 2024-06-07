from __future__ import absolute_import, print_function

# Eventually, toward support of Python 3
#from __future__ import division, absolute_import, print_function, unicode_literals

# For sphinx to work, we first need to import the sage library
import sage.all_cmdline

from sage.misc.latex import latex
latex.add_to_preamble('\\usepackage{tikz}')
latex.add_to_preamble('\\usepackage{pgfplots}')
latex.add_to_preamble('\\usetikzlibrary{pgfplots.groupplots}')

from .discrete_subset import DiscreteSubset, DiscreteBox, DiscreteTube, Intersection
from .billiard import BilliardCube
from .discrete_plane import DiscretePlane, DiscreteLine, DiscreteHyperplane
from .christoffel_graph import ChristoffelGraph
from .bispecial_extension_type import ExtensionType, ExtensionType1to1, ExtensionTypeLong
from .double_square_tile import DoubleSquare, christoffel_tile
from .fruit import Fruit, Banana, Strawberry
from .joyal_bijection import Endofunctions, Endofunction, DoubleRootedTree
from .bond_percolation import (BondPercolationSamples, 
                             BondPercolationSample, 
                             PercolationProbability)
from .billiard_nD import HypercubicBilliardSubshift

try:
    from sage.misc.latex_standalone import TikzPicture, Standalone
except ImportError:
    from .tikz_picture import TikzPicture, Standalone

from .sturmian_subshift import SturmianSubshift
from .ddim_sturmian_configuration import dSturmianConfiguration

from .matrices import M3to2, M2to3, M4to2, M4to3

from .substitution_2d import Substitution2d
from .wang_tiles import WangTiling, WangTileSolver, WangTileSet, wang_tiles
from .wang_cubes import WangCubeSet

from .polyhedron_partition import PolyhedronPartition
from .polyhedron_exchange_transformation import PolyhedronExchangeTransformation
from .piecewise_affine_transformation import PiecewiseAffineTransformation
from .coding_of_PETs import PETsCoding

from .partial_injection import (number_of_partial_injection,
                                random_partial_injection,
                                random_cyclically_reduced_stallings_graph)

from .write_to_file import write_str_to_file

from .arXiv_1903_06137 import random_jeandel_rao_rectangular_pattern
from .graph_directed_IFS import GraphDirectedIteratedFunctionSystem

from .beta_numeration_system import BetaTransformation

from .EkEkstar import kFace, kPatch, GeoSub

from .cut_and_project_scheme import (CutAndProjectScheme,
                                     ModelSet,
                                     cut_and_project_schemes,
                                     model_sets)

# BUG (sometimes, cython code does not work properly)
# from .kolakoski_word import KolakoskiWord

# for doctext to work, we import convex_boundary
# from .discrete_subset import convex_boundary

# do not import module names just the above stuff
#__all__ = []


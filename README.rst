===============================
Sébastien Labbé's Research Code
===============================

README
======

This is an optional package for SageMath containing code I wrote for research.
It contains modules on the following topics.

**Discrete dynamical systems**
  diophantine approximation, Markov transformations, Wang tilings, Lyapunov
  exponents, matrix cocycles, multidimensional continued fraction algorithms,
  polyhedron exchange transformations (PETs), GIFS,

**Combinatorics**
  2d substitutions, bispecial factors, bond percolation, Dyck word in 3D,
  words, Joyal bijection, languages, Oldenburger sequence, ostrowski
  numeration, partial injections, d-dimensional Sturmian configurations,
  hypercubic billiard words

**Digital geometry**
  Christoffel graph, discrete subset, discrete plane, double square tiles,
  polyhedron partitions,

**Vizualization**
  tikzpicture

**Miscellaneous**
  analyze Sage build time, fruit Python classes example, ranking scale

Links: 

 - documentation: http://www.slabbe.org/docs/
 - PyPI: http://pypi.python.org/pypi/slabbe
 - gitlab: http://gitlab.com/seblabbe/slabbe
 - www: http://www.slabbe.org/Sage/

Prerequisites - System packages (easy to install)
-------------------------------------------------

Some functionalities of ``slabbe`` package depend on the installation of
packages on the system such as libpari-dev, pdflatex, lualatex (lualatex
compiles large tikzpicture exceeding the memory limits of pdflatex), pdf2svg as
well as softwares including ImageMagick__ (to convert pdf to png so that
tikzpicture appear directly in the Jupyter notebook), Graphviz__ (to draw
graphs). 

__ https://imagemagick.org/
__ https://graphviz.org/

On Debian or Ubuntu, one may do::

    sudo apt update
    sudo apt install libpari-dev -y
    sudo apt install texlive texlive-latex-extra texlive-luatex texlive-fonts-extra -qy
    sudo apt install graphviz imagemagick pdf2svg -y

The installation of imagemagick done above provides the command ``convert`` but
it does not *allow* to convert pdf to png unless you edit the Imagemagick's
``policy.xml`` file which can be done as follows (thanks to `Naveed's comment
on stackoverflow`__)::

    sudo sed -i '/PDF/s/none/read|write/' /etc/ImageMagick-6/policy.xml

__ https://stackoverflow.com/questions/42928765/

On **OSX**, one should first `install Homebrew`__. Then one can install the
above packages similarly as above using ``brew`` instead of ``apt``::

    sudo brew install graphviz imagemagick pdf2svg

__ https://brew.sh/

Prerequisites - SageMath optional packages
------------------------------------------

Installing slabbe requires a working SageMath installation (with Cython and
gcc). Depending on the usage, it might be necessary to install the optional
sagemath packages dot2tex__ (translate dot file to tikz to draw nice graphs),
glucose__ (SAT solver) and latte_int__::

    sage -i dot2tex glucose latte_int

Note that graphviz must be installed *before* dot2tex.

__ https://dot2tex.readthedocs.io/en/latest/
__ https://www.labri.fr/perso/lsimon/glucose/
__ https://www.math.ucdavis.edu/~latte/

Installation
------------

The module is distributed on PyPI and is easily installed through the Python
package manager pip::

    sage -pip install slabbe

To install the module in your user space (which does not require administrator
rights)::

    sage -pip install slabbe --user

To install the most recent development version::

    sage -pip install --upgrade git+https://gitlab.com/seblabbe/slabbe

Usage::

    sage: from slabbe import *

Other Python packages you may want to install
---------------------------------------------

Some functionalities of ``slabbe`` package depend on the installation of few
Python libraries such as pytimeparse__ (time expression parser) and roman__
(integer to Roman numerals converter)::

    sage -pip install pytimeparse roman

__ https://pypi.org/project/pytimeparse/
__ https://pypi.org/project/roman/

Other System packages you may want to install
---------------------------------------------

Some functionalities of ``slabbe`` package depend on the installation of a
linear program solver such as Gurobi__. See the thematic tutorial to setup the
`installation of Gurobi in SageMath``__.

__ http://www.gurobi.com/
__ http://doc.sagemath.org/html/en/thematic_tutorials/linear_programming.html#using-cplex-or-gurobi-through-sage

It builds on SageMath
---------------------

It depends heavily on the SageMath library as it uses the following modules:
combinat, functions, geometry, graphs, matrix, misc, modules, numerical,
parallel, plot, probability, rings, sat, sets, structure, symbolic.

SageMath__ is free open source math software that supports research and
teaching in algebra, geometry, number theory, cryptography, and related areas.  

__ http://www.sagemath.org/

Follows the Best practices for scientific computing
---------------------------------------------------

It follows as much as possible the `SageMath general conventions`__ and the
`Best Practices for Scientific Computing`__. Each module is fully documented
and doctested. Before each new release, we make sure that all examples are
working. As the `ReScience Journal`__ says: "*Reproducible science is good.
Replicated Science is better*".

__ http://doc.sagemath.org/html/en/developer/coding_basics.html
__ https://doi.org/10.1371/journal.pbio.1001745
__ http://rescience.github.io/

Future inclusion into Sage
--------------------------

Some modules may have a wider interest to the SageMath community
(``tikz_picture.py`` for example) and could be included in SageMath at some
point. Please contact the author if you want to act as a reviewer for some
module(s) and I will create a ticket on trac__ for its inclusion into SageMath.

__ https://trac.sagemath.org/

Release history
---------------

*Version 0.7.7 (Nov 14, 2024)*
  New (small) module on q-Markoff numbers.
  New (small) module on Wang cubes.
  Added demo files containing the code used in `arXiv:2312.03652`__ and
  `arXiv:2403.03197`__.
  New module to generate random balanced teams used for managing a weekly
  local Ultimate frisbee league.
  Various small improvements in many modules.
  Updated cython code to work with latest Cython versions.
  Updated doctests to adapt to changes made in SageMath.
  All tests passed on SageMath version 10.4.beta9 (Release Date: 2024-06-09) using Python 3.10.12.
  All tests passed on SageMath version 10.5.beta6 (Release Date: 2024-09-29) using Python 3.12.5.

__ https://arxiv.org/abs/2403.03197
__ https://arxiv.org/abs/2312.03652

*Version 0.7.6 (Dec 6, 2023)*
  New module to deal with piecewise affine transformations, the module
  on polyhedron exchange transformations is now based on it.
  Few improvements and bug fixes on drawing substitution and Wang tilings.
  Many doctests are currently failing with SageMath version 10.2 because Cython
  modules in the slabbe packages are broken by a recent update of Cython in
  SageMath. These are not fixed in this release.

*Version 0.7.5 (Sep 15, 2023)*
  Desactivate Cython modules

*Version 0.7.4 (Sep 13, 2023)*
  No more c files in the distribution tar.gz file.
  Fixing the latex string of 2-dimensional substitutions in the Jupyter notebook.
  In preparation for a conference at CIRM, Marseille, Sep 11-15 2023.
  All tests passed on SageMath version 10.0.beta4 using Python 3.10.12.
  All tests passed on SageMath version 10.2.beta1 using Python 3.11.1 (except two).

*Version 0.7.3 (Sep 7, 2023)*
  Improving the way Polyhedron exchange transformations are plotted 
  in preparation for a conference at CIRM, Marseille, Sep 11-15 2023.
  All tests passed on SageMath version 10.0.beta4 using Python 3.10.12.
  All tests passed on SageMath version 10.2.beta1 using Python 3.11.1 (except two).

*Version 0.7.2 (Sep 6, 2023)*
  Fixing few doctests and failures with module Kolakoski related to Cython and
  Python 3.11.
  All tests passed on SageMath version 10.0.beta4 using Python 3.10.12.
  All tests passed on SageMath version 10.2.beta1 using Python 3.11.1 (except two).

*Version 0.7.1 (June 30, 2023)*
  New module on cut and project scheme (still preliminary).
  New module to draw tilings with the Smith's aperiodic monotile (see this `blog post`__).
  Few other improvements.
  All tests passed on version 10.0 of SageMath.

__ http://www.slabbe.org/blogue/2023/05/decoupe-laser-du-chapeau-tuile-aperiodique-decouverte-recemment/

*Version 0.7 (December 8, 2022)*
  New module on d-dimensional Sturmian configurations, to draw figures from `arXiv:2204.06413`__.
  New module on Hypercubic billiard words (written with Mélodie Andrieu).
  The module ``TikzPicture`` got merged in SageMath 9.6 into
  ``sage.misc.latex_standalone`` through ticket `#20343`__ during which many
  improvements were made. The line ``from slabbe import TikzPicture`` now uses
  the one in SageMath by default. All tests passed on version 9.7 of SageMath.
  Up to recently, all tests passed on versions 9.0, 9.1, 9.2, 9.3 and 9.4 of SageMath;
  can't test those earlier versions of SageMath anymore because gitlab continuous
  integration tests is not free anymore.

__ https://arxiv.org/abs/2204.06413
__ https://trac.sagemath.org/ticket/20343

*Version 0.6.3 (November 1, 2021)*
  New module on Ostrowski numeration system (basic stuff).
  New module on EkEkStar (written with Milton Minvervino).
  New modules containing the updated code published in `arXiv:1808.07768`__,
  `arXiv:1903.06137`__ and `arXiv:1906.01104`__.
  All tests passed on versions 9.0, 9.1, 9.2, 9.3 and 9.4 of SageMath.

__ https://arxiv.org/abs/1808.07768
__ https://arxiv.org/abs/1903.06137
__ https://arxiv.org/abs/1906.01104

*Version 0.6.2 (December 15, 2020)*
  New module on Graph-directed iterated function systems (GIFS).
  Fixed ``TransitiveIdeal`` import error.
  Now using gitlab continuous integration automatic tests:
  installation + ``import slabbe`` tested to work on versions 8.7, 8.8, 9.0, 9.1, 9.2 of SageMath.
  All tests passed on versions 9.0, 9.1, 9.2 of SageMath.

*Version 0.6.1 (May 8, 2020)*
  New modules to deal with the coding of `Z^d`-action by PETs, `d`-dimensional
  sturmian configurations. Improved the computation of induced polyhedron partition
  and induced polyhedron exchange transformation. New modules containing the
  code for the articles `arxiv:1903.06137`__ and `arXiv:1906.01104`__

__ https://arxiv.org/abs/1903.06137
__ https://arxiv.org/abs/1906.01104

*Version 0.6 (November 22, 2019)*
  Make the package work with Python 3. Most of the tests pass with Python 3 now.

*Version 0.5.1 (May 30, 2019)*
  Few fixes for the publication of "Induction of `Z^2`-actions on partitions of
  the 2-torus". Improved html documentation.

*Version 0.5 (April 10, 2019)*
  Few fixes for the version 2 of "Substitutive structure of Jeandel-Rao
  aperiodic tilings". New additions includes solving Wang tilings problem
  using SAT solvers and a class for Polyhedron exchange transformations.

*Version 0.4.4 (September 28, 2018)*
  Make ``import slabbe`` work in Sage with Python 3.

*Version 0.4.3 (August 22, 2018)*
  Few fixes for the publication of "Substitutive structure of Jeandel-Rao
  aperiodic tilings".

*Version 0.4.2 (July 20, 2018)*
  Few fixes for the version 2 of "A self-similar aperiodic set of 19 Wang
  tiles".

*Version 0.4.1 (February 9, 2018)*
  Few fixes for the publication of "A self-similar aperiodic set of 19 Wang
  tiles".  New module to solve the Magic hexagon problem.

*Version 0.4 (January 20, 2018)*
  Version ``0.4`` includes new modules for Wang tilings, 2d substitutions,
  polyhedron partitions, partial injections, ostrowski numeration and many
  improvements to other modules.

*Version 0.3b2 (December 11, 2016)*
  Version ``0.3b2`` includes a new module for diophantine approximations,
  random point generation inside polytopes, analyzing sage building time, and
  many improvements to previous modules.

*Version 0.3b1 (June 12, 2016)*
  Version ``0.3b1`` is now a Python package available in the Python Package
  Index (PyPI). It was migrated from the previous sage optional spkg old-style
  format. It also adds code to deal with bispecial factors, some new methods
  of graphs, substitutions and matrices.

*Version 0.2 (November 25, 2015)*
  slabbe-0.2.spkg__ (documentation__) provides modules on multidimensional
  continued fraction algorithms, matrix cocycles, languages and tikzpictures.  

__ http://www.slabbe.org/Sage/slabbe-0.2.spkg
__ http://www.slabbe.org/Sage/slabbe-0.2.pdf

*Version 0.1.1 (June 3, 2015)*
  slabbe-0.1.1.spkg__ fixes a bug with ``gcd`` import error.

__ http://www.slabbe.org/Sage/slabbe-0.1.1.spkg

*Version 0.1 (August 27, 2014)*
  slabbe-0.1.spkg__ (documentation__) contains modules on digital geometry,
  combinatorics on words and more. 

__ http://www.slabbe.org/Sage/slabbe-0.1.spkg
__ http://www.slabbe.org/Sage/slabbe-0.1.pdf


|PyPIBadge|_ |ActionsBadge|_ |DocsBadge|_ |CoverageBadge|_

Introduction
============

``stethoscope`` is a command line tool to filter and format the events coming
from the MonetDB profiler. The profiler is part of the MonetDB server and works
by emitting two JSON objects: one at the start and one at the end of every MAL
instruction executed. ``stethoscope`` connects to a MonetDB server process,
reads the objects emitted by the profiler and performs various transformations
specified by the user.

Installation
============

Installation is done via pip:

.. code:: shell

   pip install -U monetdb-stethoscope

This project is compatible with Python 3.6 or later and with MonetDB server
version Jun2020 or later.

We recommend the use of virtual environments (see `this
primer <https://realpython.com/python-virtual-environments-a-primer/>`__
if you are unfamiliar) for installing and using
``monetdb-stethoscope``.


Documentation
=============

For more detailed documentation please see the documentation on `readthedocs
<https://monetdb-solutions-monetdb-stethoscope.readthedocs-hosted.com/en/latest/>`__.

Developer notes
---------------

See the `documentation
<https://monetdb-solutions-monetdb-stethoscope.readthedocs-hosted.com/en/latest/>`__
for instructions.

.. |ActionsBadge| image:: https://github.com/MonetDBSolutions/monetdb-stethoscope/workflows/Test%20pystethoscope/badge.svg?branch=master
.. _ActionsBadge: https://github.com/MonetDBSolutions/monetdb-stethoscope/actions
.. |DocsBadge| image:: https://readthedocs.com/projects/monetdb-solutions-monetdb-stethoscope/badge/?version=latest&token=c659c74db0e19ebd763adc2d217404f48588e223dcc84b24583446a1f86fcc83
.. _DocsBadge: https://monetdb-solutions-monetdb-stethoscope.readthedocs-hosted.com/en/latest/?badge=latest
.. |CoverageBadge| image:: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope/branch/master/graph/badge.svg
.. _CoverageBadge: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope
.. |PyPIBadge| image:: https://img.shields.io/pypi/v/monetdb-stethoscope.svg
.. _PyPIBadge: https://pypi.org/project/monetdb-stethoscope/

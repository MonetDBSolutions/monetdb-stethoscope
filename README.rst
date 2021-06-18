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

   pip install -U monetdb-pystethoscope

This project is compatible with Python 3.5 or later and with MonetDB server
version Jun2020 or later.

We recommend the use of virtual environments (see `this
primer <https://realpython.com/python-virtual-environments-a-primer/>`__
if you are unfamiliar) for installing and using
``monetdb-pystethoscope``.


Documentation
=============

For more detailed documentation please see the documentation on `readthedocs
<https://monetdb-pystethoscope.readthedocs.io/en/latest/>`__.

Developer notes
---------------

See the `documentation
<https://monetdb-pystethoscope.readthedocs.io/en/latest/dev_notes.html>`__
for instructions.

.. |ActionsBadge| image:: https://github.com/MonetDBSolutions/monetdb-pystethoscope/workflows/Test%20pystethoscope/badge.svg?branch=master
.. _ActionsBadge: https://github.com/MonetDBSolutions/monetdb-pystethoscope/actions
.. |DocsBadge| image:: https://readthedocs.org/projects/monetdb-pystethoscope/badge/?version=latest
.. _DocsBadge: https://monetdb-pystethoscope.readthedocs.io/en/latest/?badge=latest
.. |CoverageBadge| image:: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope/branch/master/graph/badge.svg
.. _CoverageBadge: https://codecov.io/gh/MonetDBSolutions/monetdb-pystethoscope
.. |PyPIBadge| image:: https://img.shields.io/pypi/v/monetdb-pystethoscope.svg
.. _PyPIBadge: https://pypi.org/project/monetdb-pystethoscope/

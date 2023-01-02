# This Source Code Form is subject to the terms of the Mozilla
# Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at
# https://mozilla.org/MPL/2.0/.
#
# Copyright 1997 - July 2008 CWI, August 2008 - 2023 MonetDB B.V.

import logging

LOGGER = logging.getLogger(__name__)

def identity_function(input_object):
    """Returns the argument as is."""
    return input_object


def check_phase(json_object, phase="mal_engine"):
    """Returns True if the json object has a key "phase" with value equal to the one passed as argument.

If the object does not have a key "phase", print a warning about version incompatibility and return false."""
    ophase = json_object.get('phase', 'NA')
    if ophase == 'NA':
        LOGGER.warning("'phase' key not found in the json object.")
        LOGGER.warning("You should be using version 0.5.0 of stethoscope with MonetDB server version Sep2022 or later.")

    return ophase == phase

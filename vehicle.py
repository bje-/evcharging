# Copyright (C) 2026 Ben Elliston
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

"""Representation of an individual vehicle."""

import random
from math import trunc

EVSE_POWER = 2.3  # kW

START_TIME_MEAN = 90  # minutes
START_TIME_STDDEV = 30  # minutes

DAILY_ENERGY_MEAN = 10 # kWh
DAILY_ENERGY_STDDEV = 2 # kWh


class Vehicle:
    """A vehicle."""

    def __init__(self, ident: int, mean: float = DAILY_ENERGY_MEAN) -> None:
        """Construct a new vehicle."""
        self.charging = False
        self.id = ident
        self.evse_power = EVSE_POWER
        self.arrival_time = trunc(random.gauss(START_TIME_MEAN,
                                               START_TIME_STDDEV))
        self.energy = random.gauss(mean, DAILY_ENERGY_STDDEV)
        self.runtime = 0  # intervals

    def arrived_p(self, time_t: int) -> bool:
        """Return True if this vehicle has arrived."""
        return time_t >= self.arrival_time

    def __str__(self) -> str:
        """Customised string representation of the objedct."""
        return f"vehicle {self.id} arrival {self.arrival_time} kWh "
    "{self.energy:.2f} rt {self.runtime}"

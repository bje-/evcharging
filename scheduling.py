# Copyright (C) 2026 Ben Elliston
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

"""Different scheduling algorithms."""

from vehicle import Vehicle

# 12 intervals per hour = 5 minutes
INTV_PER_HOUR = 12

# ruff: ignore[ARG001]
def uncontrolled(vehicles: list[Vehicle], maxpower: float, time_t: int) -> float:
    """Uncontrolled charging."""
    power = 0
    eligible = [v for v in vehicles if v.arrived_p(time_t)]
    sorted_arrival = sorted(eligible, key=lambda v: v.arrival_time)
    for vehicle in sorted_arrival:
        if vehicle.arrived_p(time_t) and vehicle.energy > 0:
            power += vehicle.evse_power
            vehicle.energy -= vehicle.evse_power / INTV_PER_HOUR
            vehicle.energy = max(0, vehicle.energy)
    return power

def fcfs(vehicles: list[Vehicle], maxpower: float, time_t: int) -> float:
    """First come, first served."""
    power = 0
    eligible = [v for v in vehicles if v.arrived_p(time_t)]
    sorted_arrival = sorted(eligible, key=lambda v: v.arrival_time)
    for vehicle in sorted_arrival:
        if vehicle.arrived_p(time_t) and vehicle.energy > 0:
            if power + vehicle.evse_power > maxpower:
                continue
            power += vehicle.evse_power
            vehicle.energy -= vehicle.evse_power / INTV_PER_HOUR
            vehicle.energy = max(0, vehicle.energy)
    return power

def round_robin(vehicles: list[Vehicle], maxpower: float, time_t: int) -> float:
    """Round robin."""
    # 15 minutes
    rr_interval = 60 / INTV_PER_HOUR * 3

    power = 0
    eligible = [v for v in vehicles if v.arrived_p(time_t)]
    sorted_runtime = sorted(eligible, key=lambda v: v.runtime, reverse=True)
    for vehicle in sorted_runtime:
        if vehicle.energy > 0:
            if power + vehicle.evse_power > maxpower:
                continue
            power += vehicle.evse_power
            vehicle.runtime += 1
            vehicle.energy -= vehicle.evse_power / INTV_PER_HOUR
            vehicle.energy = max(0, vehicle.energy)
            if vehicle.runtime >= rr_interval:
                # go to the back of the queue
                vehicle.runtime = 0
    return power

def shortest_first(vehicles: list[Vehicle], maxpower: float, time_t: int) -> float:
    """Shortest car first."""
    power = 0
    eligible = [v for v in vehicles if v.arrived_p(time_t)]
    sorted_energy = sorted(eligible, key=lambda v: v.energy)
    for vehicle in sorted_energy:
        if vehicle.energy > 0:
            if power + vehicle.evse_power > maxpower:
                continue
            power += vehicle.evse_power
            vehicle.energy -= vehicle.evse_power / INTV_PER_HOUR
            vehicle.energy = max(0, vehicle.energy)
    return power

def longest_first(vehicles: list[Vehicle], maxpower: float, time_t: int) -> float:
    """Longest car first."""
    power = 0
    eligible = [v for v in vehicles if v.arrived_p(time_t)]
    sorted_energy = sorted(eligible, key=lambda v: v.energy, reverse=True)
    for vehicle in sorted_energy:
        if vehicle.energy > 0:
            if power + vehicle.evse_power > maxpower:
                continue
            power += vehicle.evse_power
            vehicle.energy -= vehicle.evse_power / INTV_PER_HOUR
            vehicle.energy = max(0, vehicle.energy)
    return power

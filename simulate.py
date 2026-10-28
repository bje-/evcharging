# Copyright (C) 2026 Ben Elliston
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

"""A simulation of different EVSE charging regimes."""

import csv
import datetime
import random
from zoneinfo import ZoneInfo

import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from matplotlib.widgets import Slider
from scheduling import fcfs, longest_first, round_robin, shortest_first, uncontrolled
from vehicle import DAILY_ENERGY_MEAN, EVSE_POWER, Vehicle

MAX_POWER = 30
NUM_VEHICLES = 40

UTC=ZoneInfo("UTC")
START_TIME_DT = datetime.datetime(2026, 1, 1, 17, 0, 0, tzinfo=UTC)

with open('load_profile.csv', mode='r') as trace:
    reader = csv.DictReader(trace)
    trace_data = [float(row['normalised_to_peak']) for row in reader]

# ruff: ignore[ARG001]
def maxpower(time_t: int) -> float:
    """In the future, this can be a time series."""
    return MAX_POWER

def run(alg: str="fcfs", nvehicles: int = NUM_VEHICLES, mean: float =
        DAILY_ENERGY_MEAN, evsepower: float = EVSE_POWER, maxpower:
        float = MAX_POWER) -> None:
    """Run a specified scheduling algorithm."""
    ### SEED ###
    random.seed(42)

    if alg == "fcfs":
        func = fcfs
    elif alg == "shortest_first":
        func = shortest_first
    elif alg == "longest_first":
        func = longest_first
    elif alg == "uncontrolled":
        func = uncontrolled
    elif alg == "rr":
        func = round_robin
    else:
        raise ValueError

    vehicles = [Vehicle(ident, mean) for ident in range(nvehicles)]
    for vehicle in vehicles:
        vehicle.evse_power = evsepower

    power_series = []
    t = 0
    while sum([v.energy for v in vehicles]) > 0:
        power = func(vehicles, maxpower, t)
        power_series.append(power)
        t += 5
    power_series += [0, 0, 0]

    x_tics = [START_TIME_DT + datetime.timedelta(minutes=5 * i) for i
              in range(len(power_series))]
    label = alg if alg == "uncontrolled" else f"{alg} {maxpower:.1f}kW"
    line, = axes.plot(x_tics, power_series, label=label)
    axes.legend()
    return line

fig, axes = plt.subplots()
plt.subplots_adjust(bottom=0.25)
plt.ylabel("kW")
ax_evse_power = plt.axes([0.3, 0.15, 0.5, 0.05])
ax_max_power = plt.axes([0.3, 0.1, 0.5, 0.05])
ax_num_vehicles = plt.axes([0.3, 0.05, 0.5, 0.05])
ax_mean_kwh = plt.axes([0.3, 0.00, 0.5, 0.05])

slider_evse_power = Slider(ax=ax_evse_power, label="EVSE power (kW)",
                           valstep=0.1, valmin=1.4, valmax=22,
                           valinit=EVSE_POWER)

slider_max_power = Slider(ax=ax_max_power, label="Max. power (kW)",
                          valstep=10, valmin=0, valmax=500,
                          valinit=MAX_POWER)

slider_mean_kwh = Slider(ax=ax_mean_kwh, label="Mean charging (kWh)",
                         valstep=0.1, valmin=0, valmax=30,
                         valinit=12)

slider_num_vehicles = Slider(ax=ax_num_vehicles,
                             label="Number of vehicles",
                             valstep=5, valmin=5,
                             valmax=200, valinit=NUM_VEHICLES)

sliders = [slider_evse_power, slider_max_power, slider_mean_kwh,
           slider_num_vehicles]

date_form = mdates.DateFormatter("%H:%M")
axes.xaxis.set_major_formatter(date_form)
fig.autofmt_xdate()

# ruff: ignore[ARG001]
def update(val: int) -> None:
    """Update the plots as a slider has moved."""
    evsepower = slider_evse_power.val
    maxpower = slider_max_power.val
    nvehicles = slider_num_vehicles.val
    mean = slider_mean_kwh.val
    for line in axes.lines:
        line.remove()
    for alg in ["uncontrolled", "fcfs", "shortest_first", "longest_first", "rr"]:
        run(alg, nvehicles, mean, evsepower, maxpower)
    axes.relim()

for slider in sliders:
    slider.on_changed(update)

for alg in ["uncontrolled", "fcfs", "shortest_first", "longest_first", "rr"]:
    run(alg)
plt.show()

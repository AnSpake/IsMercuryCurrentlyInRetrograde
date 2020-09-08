#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import de421
import sys
import calendar
import skyfield.api
from skyfield import almanac


PLANETS = skyfield.api.load("de421.bsp")
EARTH = PLANETS["earth"]
MERCURY = PLANETS["mercury"]


# Steps:
# Calculate the apparent angular position of Mercury from Earth in ecliptic coordinates
# Finde places where the ecliptic longitude is decreasing

# Subtract the position of Earth from the position of Mercury
# Express resulted vector in spherical coordinates


# Retrograde (from the Earth, inner planet):
# Move from Greatest ESTERN Elongation {through Inferior Conjuction} to Greatest WESTERN Elongation


def get_days_from_leap_year(start_year, end_year):
    """
    Returns how many days we have to count from all the leap years
    """
    leap_year = 0
    for i in range(start_year, end_year + 1):
        if calendar.isleap(i):
            leap_year += 1
    return leap_year


def figure(years, mercury_prograde, mercury_retrograde):
    plt.figure()
    plt.plot(years[:-1], mercury_prograde, '-g', linewidth=1)
    plt.plot(years[:-1], mercury_retrograde, '-r', linewidth=3)
    plt.ylim(0, 360)
    plt.title("Mercury Ecliptic Longitude degrees AD 2018 to 2038")
    plt.show()


def find_mercury_elongation_degrees(time):
    sun = PLANETS["sun"]
    sun_apparent_pos = EARTH.at(time).observe(sun).apparent()
    mercury_apparent_pos = EARTH.at(time).observe(MERCURY).apparent()
    return sun_apparent_pos.separation_from(mercury_apparent_pos).degrees


def find_mercury_max_elongation(time_scale, years):

    year_zero, year_final = years

    # fig1
    time = time_scale.utc(year_zero,
               1,
               range((365 + get_days_from_leap_year(year_zero, year_final)) * (year_final - year_zero)))

    find_mercury_elongation_degrees.rough_period = 1.0
    time_zero = time_scale.utc(year_zero)
    time_final = time_scale.utc(year_final)
    time_maxima, values = skyfield.searchlib.find_maxima(time_zero, time_final, find_mercury_elongation_degrees)
    print(len(time_maxima), "9 maxima should be found")

    # TODO: western or eastern
    for ti, vi in zip(time_maxima, values):
        print(ti.utc_strftime("%Y-%m-%d %H:%M "), "%.2f" % vi, "degrees in elongation")

    # Epita school in paris suburb
    paris_coord = skyfield.api.Topos('48.568380 N', '21.47808 W')
    t1 = time_scale.utc(2024, 12, 24)
    t2 = time_scale.utc(2025, 3, 9)
    time_cp, values_cp = skyfield.searchlib.find_discrete(t1, t2, almanac.sunrise_sunset(PLANETS, paris_coord))

    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(time.J, find_mercury_elongation_degrees(time))
    ax.set(title="Elongation of Mercury in degrees", xlabel="Year")
    ax.grid()
    fig.tight_layout()
    fig.show()


def compute_retrograde():

    year_zero = 2025
    year_final = 2026
    days = np.linspace(1, (year_final - year_zero) * 365, 10000)
    years = year_zero + days / (365 + get_days_from_leap_year(year_zero, year_final))

    time_scale = skyfield.api.load.timescale()
    time = time_scale.utc(year_zero, 1, days)

    find_mercury_max_elongation(time_scale, (year_zero, year_final))

    latitude, longitude, distance = EARTH.at(time).observe(MERCURY).ecliptic_latlon()

    longds = (180.0 / np.pi) * longitude.radians
    londel = longds[1:] - longds[:-1]

    londel[londel < -300] += 360.0
    londel[londel > +300] -= 360.0

    prograde = londel > 0.0
    mercury_prograde = longds.copy()[:-1]
    mercury_retrograde = longds.copy()[:-1]

    mercury_prograde[~prograde] = np.nan
    mercury_retrograde[prograde] = np.nan
    return years, mercury_prograde, mercury_retrograde

def main():
    """
    Main function
    """
    years, mercury_prograde, mercury_retrograde = compute_retrograde()
    figure(years, mercury_prograde, mercury_retrograde)

    return 0


if __name__ == "__main__":
    main()

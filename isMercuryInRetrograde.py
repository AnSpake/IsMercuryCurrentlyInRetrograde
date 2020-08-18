#!/usr/bin/env python3

from jplephem import Ephemeris
import matplotlib.pyplot as plot
import matplotlib.dates
import numpy as np
import de421
import sys
import calendar
import skyfield.api


# Steps:
# Calculate the apparent angular position of Mercury from Earth in ecliptic coordinates
# Finde places where the ecliptic longitude is decreasing

# Subtract the position of Earth from the position of Mercury
# Express resulted vector in spherical coordinates


def get_days_from_leap_year(start_year, end_year):
    """
    Returns how many days we have to count from all the leap years
    """
    leap_year = 0
    for i in range(start_year, end_year + 1):
        if calendar.isleap(i):
            leap_year += 1
    return leap_year


def main():
    """
    Main function
    """

    planets = skyfield.api.load("de421.bsp")
    earth = planets["earth"]
    mercury = planets["mercury"]

    year_zero = 2008
    year_final = 2035
    days = np.linspace(1, (year_final - year_zero) * 365, 10000)
    years = year_zero + days / (365 + get_days_from_leap_year(year_zero, 2035))

    time_scale = skyfield.api.load.timescale()
    time = time_scale.utc(year_zero, 1, days)

    latitude, longitude, distance = earth.at(time).observe(mercury).ecliptic_latlon()

    longds = (180.0 / np.pi) * longitude.radians
    londel = longds[1:] - longds[:1]

    londel[londel < -300] += 360.0
    londel[londel > +300] += 360.0

    prograde = londel > 0.0
    mercury_prograde = longds.copy()[:1]
    mercury_retrograde = longds.copy()[:1]

    plot.figure()
    plot.plot(years[:1], mercury_prograde, '-b', linewidth=1)
    plot.plot(years[:1], mercury_prograde, '-r', linewidth=3)
    plot.ylim(0, 360)
    plot.title("Mercury Ecliptic Longitude degrees AD 2008 to 2035")
    plot.show()

    return 0


if __name__ == "__main__":
    main()

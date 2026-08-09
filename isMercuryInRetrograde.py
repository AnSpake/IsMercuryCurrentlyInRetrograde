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
TIME_SCALE = skyfield.api.load.timescale()


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


def omega(earth_time):
    dt = 1 / 24
    t0 = TIME_SCALE.tt_jd(earth_time)
    t1 = TIME_SCALE.tt_jd(earth_time + dt)

    lat0, long0, dist0 = EARTH.at(t0).observe(MERCURY).ecliptic_latlon()
    lat1, long1, dist1 = EARTH.at(t1).observe(MERCURY).ecliptic_latlon()

    dlon = (long1.degrees - long0.degrees + 180) % 360 - 180
    omega = dlon / dt
    return omega


def find_mercury_elongation_degrees(time):
    sun = PLANETS["sun"]
    sun_apparent_pos = EARTH.at(time).observe(sun).apparent()
    mercury_apparent_pos = EARTH.at(time).observe(MERCURY).apparent()
    return sun_apparent_pos.separation_from(mercury_apparent_pos).degrees

def find_mercury_max_elongation(year_zero, year_final):

    # fig1
    time = TIME_SCALE.utc(year_zero, 1, range((365 + get_days_from_leap_year(year_zero, year_final)) * (year_final - year_zero)))

    find_mercury_elongation_degrees.rough_period = 116.0
    time_zero = TIME_SCALE.utc(year_zero)
    time_final = TIME_SCALE.utc(year_final)
    time_maxima, values = skyfield.searchlib.find_maxima(time_zero, time_final, find_mercury_elongation_degrees)

    # 3~4 retrogrades per year => 2 elongations per retrograde
    # Mandatory to have a pair (East + West)
    if (len(time_maxima) % 2) != 0:
        raise ValueError('Date may be incorrect, could not find a pair of elongations for this retrograde (should have East and West elongations)')


    for ti, vi in zip(time_maxima, values):
        print(ti.utc_strftime("%Y-%m-%d %H:%M "), "%.2f" % vi, "degrees in elongation")

    # TODO: western or eastern
    # Find if planet is visible from the earth
    # Find when the planet is visible from the eart (after sunset = west) (before sunrise/dawn = eastern)
    lat, lon, distance = EARTH.at(time).observe(MERCURY).ecliptic_latlon()

    """
    The moment at which a planet is in opposition/conjunction with the Sun is
    when their ecliptic longitudes are at 0 or 180 degrees difference

    For inner planets like Mercury: they only ever experience conjunctions with
    the Sun from Earth PoV and can never be in oppositions

    conj_y reads as follows
    -> 0 indicates an inferior conjunction
    -> 1 indicates a superior conjunction
    """
    conj_t0 = TIME_SCALE.utc(year_zero, 1, 1)
    conj_t1 = TIME_SCALE.utc(year_final, 1, 1)
    inf_conj = almanac.oppositions_conjunctions(PLANETS, MERCURY)
    conj_t, conj_y = almanac.find_discrete(conj_t0, conj_t1, inf_conj)

    inf_conj_date = [conj_t[i] for i, j in enumerate(conj_y) if j == 0]

    print(conj_t.utc_iso())

    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(time.J, find_mercury_elongation_degrees(time))
    ax.set(title="Elongation of Mercury in degrees", xlabel="Year")
    ax.grid()
    fig.tight_layout()
    fig.show()


def compute_retrograde():

    year_zero = 2018
    year_final = 2038
    days = np.linspace(1, (year_final - year_zero) * 365, 10000)
    years = year_zero + days / (365 + get_days_from_leap_year(year_zero, year_final))

    time = TIME_SCALE.utc(year_zero, 1, days)

    find_mercury_max_elongation(year_zero, year_final)

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

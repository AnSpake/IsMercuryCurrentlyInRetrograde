#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np
import de421
import sys
import calendar
import skyfield.api
from skyfield import almanac
from scipy.optimize import brentq


PLANETS = skyfield.api.load("de421.bsp")
EARTH = PLANETS["earth"]
MERCURY = PLANETS["mercury"]
TIME_SCALE = skyfield.api.load.timescale()


def figure_mercury_elongation_in_degrees(time):
    """
    Graphic showing Mercury elongations in degrees for the given time period.
    """
    fig, ax = plt.subplots(figsize=(5, 2))
    ax.plot(time.J, find_mercury_elongation_degrees(time))
    ax.set(title="Elongation of Mercury in degrees", xlabel="Year")
    ax.grid()
    fig.tight_layout()
    fig.show()


def figure_retrograde(years, longitude, retrogrades):
    """
    Graphic showing Mercury ecliptic longitude on the given time period
    and highlights the found retrogrades period.
    """
    # Prep longitude values so it can be used in the plot
    longitude = np.unwrap(np.radians(longitude.degrees))
    longitude = np.degrees(longitude)

    plt.figure()
    plt.plot(years, longitude, color="green")

    for retro, direct in retrogrades:
        plt.axvspan(retro.utc_datetime().timetuple().tm_yday / 365 + retro.utc_datetime().year, \
                    direct.utc_datetime().timetuple().tm_yday / 365 + direct.utc_datetime().year, color="red", alpha=0.3)
    plt.title("Mercury Retrograde")
    plt.xlabel("Year")
    plt.ylabel("Ecliptic longitude (deg)")
    plt.grid()
    plt.show()


def get_days_from_leap_year(start_year, end_year):
    """
    Returns how many days we have to count from all the leap years.
    """
    leap_year = 0
    for i in range(start_year, end_year + 1):
        if calendar.isleap(i):
            leap_year += 1
    return leap_year


def omega(earth_time):
    """
    Omega function => d0/dt < 0
    The planet is in retrograde motion, exclusively from the Earth perspective,
    when the planets orbit anticlockwise in the coordinate system.
    When omega > 0 => the planet is "going forward" / direct.
    When omega = 0 => the planet is at a stationary point.
    When omega < 0 => the planet is "going backwards" / retrograde.
    """
    dt = 1 / 24
    t0 = TIME_SCALE.tt_jd(earth_time)
    t1 = TIME_SCALE.tt_jd(earth_time + dt)

    lat0, long0, dist0 = EARTH.at(t0).observe(MERCURY).ecliptic_latlon()
    lat1, long1, dist1 = EARTH.at(t1).observe(MERCURY).ecliptic_latlon()

    dlon = (long1.degrees - long0.degrees + 180) % 360 - 180
    omega = dlon / dt
    return omega


def find_mercury_elongation_degrees(time):
    """
    Compute the elongation of Mercury in degrees.
    The elongation is the "apparent" angular separation between the Sun and the relevant Planet,
    as viewed from the Earth.
    This helps because we need to find the maximum elongations (East and West),
    in order to focus our search of the retrogrades.
    """
    sun = PLANETS["sun"]
    sun_apparent_pos = EARTH.at(time).observe(sun).apparent()
    mercury_apparent_pos = EARTH.at(time).observe(MERCURY).apparent()
    return sun_apparent_pos.separation_from(mercury_apparent_pos).degrees


def find_mercury_max_elongation(year_zero, year_final):
    """
    Given the range of mercury elongations, find maximum points.
    The output comes in pair and in order East then West.
    No sanity check if the given time period is less then a year.
    """
    find_mercury_elongation_degrees.rough_period = 116.0
    time_zero = TIME_SCALE.utc(year_zero)
    time_final = TIME_SCALE.utc(year_final)
    time_maxima, values = skyfield.searchlib.find_maxima(time_zero, time_final, find_mercury_elongation_degrees)

    # 3~4 retrogrades per year => 2 elongations per retrograde
    # Mandatory to have a pair (East + West)
    if (len(time_maxima) % 2) != 0:
        raise ValueError('Date may be incorrect, could not find a pair of elongations for this retrograde (should have East and West elongations)')

    return time_maxima

def find_inferior_conjunction(year_zero, year_final):
    """
    The moment at which a planet is in opposition/conjunction with the Sun is
    when their ecliptic longitudes are at 0 or 180 degrees difference.

    For inner planets like Mercury: they only ever experience conjunctions with
    the Sun from Earth PoV and can never be in oppositions.

    conj_y reads as follows:
    -> 0 indicates an inferior conjunction.
    -> 1 indicates a superior conjunction.
    """
    conj_t0 = TIME_SCALE.utc(year_zero, 1, 1)
    conj_t1 = TIME_SCALE.utc(year_final, 1, 1)
    inf_conj = almanac.oppositions_conjunctions(PLANETS, MERCURY)
    conj_t, conj_y = almanac.find_discrete(conj_t0, conj_t1, inf_conj)

    inf_conj_date = [conj_t[i] for i, j in enumerate(conj_y) if j == 0]
    return inf_conj_date


def find_mercury_retrogrades(year_zero, year_final):
    """
    Compute mercury orbit cycles viewed from the Earth.
    Find the retrograde and direct period of Mercury by searching for the
    stationary point (angular speed = 0).
    Retrograde happens between the Maximum East elongation point to the inferior conjunction point.
    Mercury goes Direct again, between the inferior conjunction point to the Maximum West elongation point.
    """
    leap_year = get_days_from_leap_year(year_zero, year_final)
    days = np.array(range((365 + leap_year) * (year_final - year_zero)))
    years = year_zero + days / (365 + get_days_from_leap_year(year_zero, year_final))
    time = TIME_SCALE.utc(year_zero, 1, days)

    mercury_max_elong = find_mercury_max_elongation(year_zero, year_final)
    mercury_east_elong = mercury_max_elong[0::2]
    mercury_west_elong = mercury_max_elong[1::2]

    mercury_inf_conj = find_inferior_conjunction(year_zero, year_final)
    _, lon, _ = EARTH.at(time).observe(MERCURY).ecliptic_latlon()

    mercury_cycles = []
    for east_elong, west_elong, conj_iter in zip(mercury_east_elong, mercury_west_elong, mercury_inf_conj):
        mercury_retrograde = brentq(omega, east_elong.tt, conj_iter.tt)
        mercury_direct = brentq(omega, conj_iter.tt, west_elong.tt)

        mercury_cycles.append((TIME_SCALE.tt_jd(mercury_retrograde), TIME_SCALE.tt_jd(mercury_direct)))

    return years, lon, mercury_cycles


def main():
    """
    Main function
    """
    year_zero = 2025
    year_final = 2026

    years, longitude, retrogrades = find_mercury_retrogrades(year_zero, year_final)

    figure_retrograde(years, longitude, retrogrades)

    return 0


if __name__ == "__main__":
    main()

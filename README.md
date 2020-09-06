# IsMercuryCurrentlyInRetrograde
A quick python script to know if you can use "mercury is in retrograde" as an excuse in your life.

# Install
```bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

# Run
```bash
./isMercuryInRetrograde.py
```

# Spoiler
Brace yourselves.
Something is wrong in 2025 and 2032, fix ongoing
![alt text](https://github.com/AnSpake/IsMercuryCurrentlyInRetrograde/blob/master/mercury_retrograde_result.png)

# Notes
Should base retrograde calculation on this:
https://physics.stackexchange.com/questions/249493/mathematically-calculate-if-a-planet-is-in-retrograde

Master branch use this, its buggy but need it to test if results diverged too much for the fix on 2020-only branch:
https://astronomy.stackexchange.com/questions/18832/mathematically-calculate-if-a-planet-is-in-retrograde?rq=1

2020-only use the following logic:
Retrograde motion appear when inner planet go through an inferior conjunction.
Meaning going from its Maximum Estern Elongation to the Maximum Western Elongation

# Progress (2020-only branch)
| Subject | Progress |
| Elongation | DONE |
| Maximum Elongation | DONE |
| E/W Elongation | ONGOING |
| Retrograde | NOPE |
| Parsable output | NOPE |
| Astro Sign | NOPE |

Next todo:
- Argparse
- Answer the question bro
- Find in which Astro sign, mercury is retrograding to

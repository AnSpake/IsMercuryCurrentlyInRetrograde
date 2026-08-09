# IsMercuryCurrentlyInRetrograde
A quick python script to know if you can use "mercury is in retrograde" in your talk of the day.

Retrograde can only be observed from the Earth.  
This code is only for Mercury but it can easily be adapted to Venus.  
This script is only for inner planets and cannot be adapted to outer planets,  
it's a completely different direction (See given links).

When an inner planet move from their Greatest ESTERN Elongation to their Greatest WESTERN Elongation,  
they go through a stationary point (its angular speed reaches 0).
When its angular speed is negative, we call it a retrograde because viewed from the Earth,  
it "looks like" the inner planet is going backwards.  
When that angular speed is positive again is said to be when the inner planet is going direct again.  
Through all that, Mercury will reach its inferior conjunction point.  
It's said to be the "peak" of the retrograde. In astronomy, this is when Mercury is on a straight line with  
the Sun and the Earth.  
As you guessed it, this is when Mercury is closest to the Earth so take a look outside !

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
![alt text](https://github.com/AnSpake/IsMercuryCurrentlyInRetrograde/blob/master/mercury_retrograde_result.png)

# Notes 
If you want to find the retrograde of an outer planet, you should check the following links:  
https://physics.stackexchange.com/questions/249493/mathematically-calculate-if-a-planet-is-in-retrograde  
https://astronomy.stackexchange.com/questions/18832/mathematically-calculate-if-a-planet-is-in-retrograde?rq=1

#### UPDATE 10/23/20:  
We are not going to use Maximum Elongation anymore since the retrograde doesn't  
start at the East Maximum Elongation, but some days before the Inferior Conjunction.  
The retrograde does occur when the inner planet is going through the East to the  
West max Elongation but we will not get accurate result.  
And I'm a bit stuck on finding if it's a East or West Max elongation in a pretty way.

Next Steps:
- Calculate the apprent angular position of Mercury viewed from the Earth in ecliptic coordinates.  
- Find places where the ecliptic longitude is decreasing until it reaches 0 or change sign  

#### UPDATE 08/07/26:  
It's been a while, forgive todo comments here and there.  
Making old branch functional and merging them before reworking this project.

From memories, precise computation were impossible to run on my personal computer  
and had to try elsewhere + I had an idea for the fix on the current bugs but wrote that  
nowhere and completely forgot it so I hope while working back on this, it (or a new idea)  
will come back !

#### UPDATE 08/09/26:  
I had all the pieces in my previous code and I only needed to put everything together.  
Previously, I found the elongation of mercury + their maximum + the inferior conjunction of mercury.  
Everything I'm writting is specific to inner planets only (Venus/Mercury),  
the outer planet is a bit different since remember it's all as viewed from the  
Earth perspective and retrograde are kind of a optical illusion.

As previously written, the retrograde happens a bit after the Max East elongation  
and the planet goes direct again a bit before the Max West elongation.  
To sums up, we need to track the angular speed of the planet and monitor when  
it's changing sign or is equal to 0 again.  
For testing purposes, I did a classic bisection method but later found brentq  
which is supposed to optimize this type of search.  

# Progress 
| Subject | DONE |  
| Elongation | DONE |  
| Maximum Elongation | DONE |  
| E/W Elongation | DONE |  
| Retrograde | DONE |  
| Parsable output | TODO |  
| Astro Sign | TODO |  

Next todo:
- [ ] Argparse
- [ ] Answer the question bro (almost there)
- [ ] Find in which Astro sign, mercury is retrograding to

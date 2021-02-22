---
title: "Simulating Planetary Motion with Python"
date: 2021-01-10
updated: 2021-01-10
author: "Callum Alkins"
contact: "https://www.linkedin.com/in/callum-alkins-810898203/"
tags:
- simulation
- animation
- visualization
categories:
- [Natural Sciences, Physics]
languages:
- python
description: "Tracking the motion of the planets is a challenge that is proven to be intractable using pure mathematics alone. Can we, however, find a solution using data science?"
cover: /banners/planetary-motion.jpg
---

{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you'll be able to find it linked here.
{% endnote %}
As the 19th Century drew to a close, King Oscar II of Sweden set out a challenge. The problem was to find a general solution to what is known as the $n$-body problem.

This problem was mathematical in nature, asking how a system of planetary bodies would evolve with time according to Newton's laws of gravitation and motion. That is, can you predict where a planet will be in the future with precision using physics alone?

The problem sounds simple enough. With a complete understanding of the laws of motion that planets obey, it was just a matter of extrapolating forwards in time. As such, it wasn't long before a proof, by the esteemed mathematician Henri Poincaré, was published.

Sadly, it wasn't much longer after that before a fatal mistake in his proof was found. And the heartbreak doesn't end there; it was soon discovered that the problem was in fact unsolvable for non-trivial cases. That is, although there were special cases where a solution exists, a general solution was proved non-existent. 
{% note success %}
Although this tale has a rather disappointing conclusion, it is worth noting that this problem was a great inspiration for the invention of the mathemical field of chaos theory, devoted to understanding and analysing _chaotic_ systems such as $n$-body planetary motion.
{% endnote %}
If no closed-form solution exists for these problems, how can we make predictions about planetary motion? How do we know that in a few years' time there won't be an apocalyptic collision between the Earth and another member of the solar system?

The answer is simulation. 

Although the mathematical laws of the universe prevent us from generating an elegant formula for the state of an orbital system in the future, they do not prevent us from simulating such a system to any degree of accuracy we demand (provided we have enough time/computational resources). We can use such simulations to make accurate predictions about the future, letting us sleep easy at night, knowing that, at the very least, planetary collision will not be our downfall any time soon.

In this post, we walk through the physics and the code required to simulate a simple system of planetary motion using Python. Using some basic ideas from high school physics and rudimentary Python, we can create some stunning visual simulations. Before we get there though, we need a recap of the laws of motion.

## The Physics of Planetary Motion

### The Setup

To keep things simple (both in terms of the physics and resulting visualisations), we restrict ourselves to a two-dimensional universe. We will, however, discuss how to generalise the methods demonstrated here to three dimensions at the end of the post.

As with any physics problem, we have to start with some assumptions.

The first of these is assuming that all planetary bodies act as point masses. That is to say, even though the bodies have a non-zero radius and therefore an area, we assume that the entirety of their mass is located at the centre. This makes calculations related to gravitational forces far easier with minimal impact on the resulting values in most circumstances. Secondly, if there are any collisions between the masses, moving forward we shall treat them as a singular body with a mass equal to the sum of the two that collided.

We also assume that the forces acting on our planetary bodies are constant over very short durations. This allows us to use a simple set of equations known as SUVAT (more on this later) instead of relying on complex integral calculus. This assumption is largely reasonable, only failing substantially when we get close to massive bodies (such as a black hole or neutron star), at which point the outcome of motion (collision and merging) is essentially determined already.

We also make some minor assumptions, such as treating all planetary bodies as circular.

Under these assumptions, and given the initial positions, velocities, and masses of our bodies (plus some cosmetic conditions that are not necessary for the physics), our goal is to simulate the resulting planetary motion.

### Deriving Motion

With our assumptions in place, we can begin to calculate the trajectories of our planetary bodies. As discussed in the introduction to this piece, there is no closed form solution for the positions in a system of 3 or more bodies at any given time. That said, we can use our second assumption from above to accurately progress the motion one small timestep at a time.

To do this, we take the positions and masses of the objects at any given timestep, and use these to calculate the instantaneous forces between all bodies in the simulation. From this, we can calculate accelerations, velocities and, finally, the positions of the bodies at the next timestep. At this point the process is repeated, building up a realistic simulation of planetary motion, piece-by-piece.

It follows that the first problem we need to solve is how to calculate the force acting on any particular body at an instant of time. The most straightforward method of doing this is to decompose the overall force into its $x$ and $y$ components using the trigonometric functions sine and cosine. This is because the coordinates used in our code are relative to the $x$ and $y$ axes, and so it is much simpler to update velocities and positions in these components.

To start, consider the initial positions of masses 1 and 2, the $x$ and $y$. It is relatively simple to calculate the displacement between the two bodies.

$$ 
dx = x_2 - x_1 \\
dy = y_2 - y_1
$$

The next step is to calculate the gravitational force between the objects using Newton's law of gravity.

$$ F_{1,2} = \frac{GM_1M_2}{r_{1,2}^2}$$

Here, $G$ is the Gravitational constant ($\approx 6.67\times10^{-11}$), $M_1$ and $M_2$ are the masses of objects 1 and 2 respectively, and,

$$ r_{1,2} = \sqrt{(dx)^2 + (dy)^2}$$

is the distance between the two bodies (using Pythagoras' theorem). 

Again, since we are working in $x$ and $y$ coordinates, it is easier to split this total force into its individual components.

$$ 
F_{1,2}^{(x)} = F_{1,2} \cos(\theta) \\
F_{1,2}^{(y)} = F_{1,2} \sin(\theta)
$$

We use theta to represent the angle between the two bodies and calculate its value using this formula.

$$ \theta = \arctan\left(\frac{dx}{dy}\right)$$

This however only gives us the forces acting between bodies 1 and 2. In the case we have $n$ bodies, we have to add up the force contributions from each of these to see the total impact on the first body. That is,

$$
F_1^{(x)} = F_{1,2}^{(x)} + F_{1,3}^{(x)} + \ldots + F_{1,n}^{(x)}\\
F_1^{(y)} = F_{1,2}^{(y)} + F_{1,3}^{(y)} + \ldots + F_{1,n}^{(y)}
$$

with similar results for all other bodies.

From this, the component acceleration of the object's gravitational attraction with the other bodies is calculated using Newton's second law. We shall continue using only the $x$ component, noting that the same process is used for the $y$ component.

$$ a_1^{(x)} = \frac{F_1^{(x)}}{M_1}$$

As hinted at earlier, because we are assuming forces and therefore acceleration to be constant over short time periods, we can use a set of formulae known as the SUVAT equations. These relate acceleration, current/new velocity, change in position, and time difference, in such a way that knowing any three gives you the others. We know our fixed timestep, the current velocity, and we just calculated the acceleration acting on the body, so we are good to go.

We start by calculating the new velocity ($v_1^{(x)}$). It is given by the following formula, where $u_1^{(x)}$ is the current $x$-component of the first body's velocity and $dt$ is the timestep we have chosen.

$$v_1^{(x)} = u_1^{(x)} + a_1^{(x)}dt$$

The final step it to calculate the change in the position of the body, again using the SUVAT equations.

$$ v_1^{(x)}dt - \frac{1}{2}a_1^{(x)} dt^2$$

With our updated position and velocities in hand, we can now repeat this process to build a simulation of the planetary motion.
{% note info %}
We could also have used the expression

$$ u_1^{(x)}dt + \frac{1}{2}a_1^{(x)} dt^2$$

for the change in $x$-position. Since we update the velocity $u_1^{(1)}$ to become $v_1^{(1)}$ first though, it is simpler (though, admittedly, less numerically stable) to use the expression given above.
{% endnote %}
### Handling Collisions

A special case that must be accounted for is collisions. Although the masses are treated as point sources of gravity, a radius for each mass has been set to allow for collisions. In this model, we assume that when two masses collide they merge and move forward as one mass with the combined momentum of each. First, the momentum of each object is calculated,

$$
p_1 = M_1v_1 \\
p_2 = M_2v_2 
$$

The momentum of the 'new' object is equal to the combined momentum of the two objects that made it,

$$ p_{\text{new}} = p_1 + p_2 $$

In order to calculate the velocity of the new object, we divide its momentum by its mass (which is now the sum of the two original masses).

$$ v_{\text{new}} = \frac{p_{\text{new}}}{M_{\text{new}}} = \frac{M_1v_1 + M_2v_2}{M_1 + M_2}$$

The simulation then carries on as before, just with one object fewer.
{% note info %}
A more intuitive way of viewing the above derivation is that the new velocity is the mass-weighted average of the two original velocities.
{% endnote %}{% note warning %}
Note, that the momentums above are actually two-dimensional vectors with $x$ and $y$ components. In our code we treat these components separately though the maths is exactly the same.
{% endnote %}
## The Code

Now that we understand the physics behind our simulation, we can start coding it up. To keep things simple we will only focus on the aspects of the code relevant to physics (as opposed to the additional code for visualisation and animation). The full code, however, can be found [here](https://colab.research.google.com/drive/1YKjSs8_giaZVrUKDhWLnUAfebuLTC-A5?usp=sharing).

The first step is to set up the initial conditions, in this case, the bodies are set up in a list called `planets`.

```python
planets = [
  {
    'colour': (255, 69, 0),  # orange
    'position': {'x': 0.5, 'y': 0.5},
    'velocity': {'x': 0, 'y': 0},
    'mass': 1.989e30,
    'radius': 3.963e10
  },
  {
    'colour': (159,193,100),  # green
    'position': {'x': 0.8, 'y': 0.5},
    'velocity': {'x': 0, 'y': 2.97e4},
    'mass': 5.972e24,
    'radius': 8.371e9
  },
  {
    'colour': (97, 51, 24),  # brown
    'position': {'x': 0.5, 'y': 0.9},
    'velocity': {'x': 2.42e4, 'y': 0},
    'mass': 3.768e18,
    'radius': 5.416e9
  },
]
```
{% note info %}
Note that all units for the simulation are [SI units](https://en.wikipedia.org/wiki/International_System_of_Units) (meters, seconds, etc.)
{% endnote %}
In addition, we define some constants that shall be used later.

```python
DT = 5e6
G = 6.67408e-11
```

`DT` represents the timestep (in seconds) used in our simulation and 'G' is the gravitational constant used in Newton's law of gravitation. The latter is determined by physics (though you can use different values for simulating different universes) though the former must be chosen.

It is important to use an appropriate timestep. Using large timesteps will produce inaccurate simulations, as we cannot rely on the assumption of constant force/acceleration that the SUVAT equations require. In contrast, a simulation that uses a miniscule timestep will run much slower, as the number of calculations required is greater. At the end of the post we discuss methods for optimising this approach further to allow for a smaller timestep without requiring more computational power.

From here, we follow the same procedure as in the previous section:

1. Calculate the distances between the bodies
2. Calculate the gravitational forces between the bodies
3. Calculate the component forces in the $x$ and $y$ directions
4. Calculate the component accelerations due to this attraction
5. Calculate the change in velocities due to the acceleration
6. Calculate the new positions

The force calculations take place in a nested loop, the outer layer looping through each planet, and the inner looping through all other planets to calculate the force acting between them.

```python
for i, p1 in enumerate(planets):
    for j, p2 in enumerate(planets):
        if i != j:
            # Calculate forces...
```

Inside, there are multiple lines responsible for calculating the total forces acting on each body. The first line extracts the $x$ position of both planets in question and calculates the difference between them (the same is shown for 'y' below). The code then follows the logic as before, calculating the force due to gravity and then the acceleration. Comparing the code below to the equations in the previous section, we see that they are identical.

```python
dx = p2['position']['x'] - p1['position']['x']
dy = p2['position']['y'] - p1['position']['y']

r = math.sqrt(dx**2 + dy**2)

F = G * planets[j]['mass'] * planets[i]['mass'] / r**2
        
theta = math.atan2(dy, dx)
  
Fx += math.cos(theta)*F
Fy += math.sin(theta)*F

ax = Fx / p1['mass']
ay = Fy / p1['mass']
```
{% note info %}
If you haven't seen the notion `x += y` before, it means the same as `x = x + y`. That is, increment the left-hand variable by the value on the right.
{% endnote %}
Theta, as before, has been calculated in order to split the total force into its components in the $x$ and $y$ directions, which are then used to find the component accelerations. The accelerations are used to calculate the updated velocity,

```python
planets[i]['velocity']['x'] += ax * DT
planets[i]['velocity']['y'] += ay * DT
```

A similar process is required for the position of the mass. As before, the SUVAT equation are required to calculate the change in position over the timestep; `sx` and `sy` represent these changes.

```python
sx = p1['velocity']['x'] * DT - 0.5 * ax * DT**2
sy = p1['velocity']['y'] * DT - 0.5 * ay * DT**2
```

All that is needed now, is to update the positions for the next timestep.

```python
planets[i]['position']['x'] += sx
planets[i]['position']['y'] += sy
```

The last piece of physics to be implemented is the collision condition. In order to check for a collision, we compare the distance between two masses and the sum of their radii.

```python
d = (p1['position']['x'] - p2['position']['x']) ** 2 + \
          (p1['position']['y'] - p2['position']['y']) ** 2
r = (p1['radius'] + p2['radius']) ** 2
if d < r:
    # Handle collision...
```
{% note success %}
Note that, we in fact compared the squared distance between the planets with the squared sum of radii. This turns out to be equivalent to comparing the distance and radii sum directly since the function $x^2$ is increasing for $x>0$. By removing the square root (a costly operation), we make our code slightly faster.
{% endnote %}
If the collision condition is met, the two planets are combined by summing their masses and using the momentum equations given in the last section. In addition, the new, combined planet is given a radius equal to the root mean squared average of the two previous planets so that it has an area equal to the sum of the original two areas.

```python
'radius': (p1['radius']**2 + p2['radius']**2)**(1/2)
```

On top of this, a new colour is chosen based on the area-weighted combination of old planets' colours.

The final thing to mention is that a wrap around function (similar to the classic game Asteroids) has been used to keep the planets interacting with each other. This makes sure the animation stays within a certain area (rather than allowing planets to escape each other's gravity and tend to infinity). When a planet reaches the border it is given a new position on the opposite side of the animation.

## An Example Planetary System

Now that we have the physics and code for our simulation sorted, let's see it in action. We simulate two bodies orbiting a third larger body. That said, the code is incredibly flexible so you are encouraged to play with it yourself.




<video src="planetary_motion.mp4" controls  >
      Your browser does not support the <code>video</code> element.
    </video>



## Additional Notes

### Moving to 3D

As mentioned before, this is the most simple version of an $n$-Body simulation and therefore can be expanded in many ways. The first major step would be to generate a simulation in three-dimensions. In order to do this, the force would have to be split into its three component forces in the $x$, $y$ and $z$ directions, thus allowing the calculation of the change in position/velocity in each direction.

Given a vector $(x, y, z)$ we first calculate the polar angle $\theta$ and the azimuthal angle $\phi$ using the following formulae.

$$
\theta = \arccos\left(\frac{z}{\sqrt{x^2 + y^2 + z^2}}\right) \\
\phi = \arctan\left(\frac{y}{x}\right)
$$

Some trigonometry then gives the following results.

$$
F^{(x)} = F \sin(\theta)\cos(\phi) \\
F^{(y)} = F \sin(\theta)\sin(\phi)\\
F^{(z)} = F \cos(\theta)
$$

From here, the mathematics is the same as in the two-dimensional case.

### Turbocharging the Simulation

In the name of simplicity, many opportunities for efficiency have been deliberately missed in writing this code. To wrap-up this post, here is a list of a few ideas (in increasing complexity) that could increase the efficiency of the simulation.

1. Due to Newton's second law, once we know the force acting on body $i$ by body $j$, we know the opposing force to be equal. We can therefore halve the number of force calculations we use.
2. Base Python is notoriously slow, instead switching to NumPy, or better yet, JIT-compilation using Numba would offer a massive speed boost.
3. Due to the nature of the problem, there is a lot of scope for parallelisation. An efficient solution would break up the motion calculations between cores to avoid downtime.
4. For large simulations for $n$ >> 1 bodies, it may be worthwhile chunking the 'universe' up into grids based on the largest mass in the system, so that any planets in different grid cells have negligible impacts on each other and so can be omitted from the resultant force calculations.## Additional Notes

### Moving to 3D

As mentioned before, this is the most simple version of an $n$-Body simulation and therefore can be expanded in many ways. The first major step would be to generate a simulation in three-dimensions. In order to do this, the force would have to be split into its three component forces in the $x$, $y$ and $z$ directions, thus allowing the calculation of the change in position/velocity in each direction.

Given a vector $(x, y, z)$ we first calculate the polar angle $\theta$ and azimuthal angle $\phi$ using the following formulae.

$$
\theta = \arccos\left(\frac{z}{\sqrt{x^2 + y^2 + z^2}}\right) \\
\phi = \arctan\left(\frac{y}{x}\right)
$$

Some trigonometry then gives the following results.

$$
F^{(x)} = F \sin(\theta)\cos(\phi) \\
F^{(y)} = F \sin(\theta)\sin(\phi)\\
F^{(z)} = F \cos(\theta)
$$

From here, the mathematics is the same as in the two-dimensional case.

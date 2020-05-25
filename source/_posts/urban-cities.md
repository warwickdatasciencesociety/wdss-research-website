---
title: "Urban Cities: A History Told By Data"
date: 2020-05-23
updated: 2020-05-23
author: "Ciaran Evans"
contact: "https://www.linkedin.com/in/ciaran-evans-9226b3186/"
tags:
- visualization
- data-analysis
categories:
- [Humanities, Geography]
- [Humanities, History]
languages:
- python
description: "Remnants of history often find themselves scattered in the modern word. With the right tools—in this case, some data-science-savvy—their stories can be brought back to life."
cover: /banners/urban-cities.jpg
---
{% note info %}
**Accessing Post Source**
We are still working on getting this site set up, so source code for this post is not yet available. Check back soon and you’ll be able to find it linked here.
{% endnote %}
## Introduction

![The skyline of Barcelona](/images/urban-cities/barcelona.jpg)

An aerial observer would be forgiven for mistaking Barcelona’s octagonal blocks and diagonal streets as some red-brick reimagining of Legoland. Indeed, Spain’s 2000-year-old capital is a strict grid-like design, engineered to tackle overpopulation while maximizing airflow for its inhabitants. It’s an ancient city with all the efficiency of contemporary urban structures like New York.

Barcelona is a fascinating example, but its grid-like patterns are obvious to the human eye. I wondered about other cities with more complex features. What subtle quirks lie in the road/street structures of Bristol, Newcastle or Coventry?

For that question I wanted a scientific answer, so I set about applying data science to learn more about the intricacies of the UK’s densely populated cities.

### Methodology

This project was made possible by [OpenStreetMap](https://www.openstreetmap.org/) (OSM). OSM is a world-wide database of roads, trails and streets, verified by field maps and aerial imagery and  maintained by an active community of engineers and GIS professionals. Its open API enables raw geodata to be sourced on any city in the world.

OSM describes geodata elements in a number of ways. Linear features, like roads or rivers, are modelled using a “way”: nodes (between 2 and 2000) connected into a simple chain of line segments, a polyline. Most whole cities with solid polygon geometries (Manchester and Birmingham to name a few) are bounded by a single “closed way”, with the same start and end nodes. These are generally those with a well-defined natural border in the real world. Others, that have no obvious boundary, are rather represented as a single point marker, denoting the center of the city. We will be focusing on the former type as the more complex definition of the geometry allows us to draw far more insight.

Of the UK cities with these 'nice' geometries, the twelve with the largest populations were considered and OSM API was used to fetch full network graphs, from which the bearings of streets were determined. A summary of this data is shown below.



<table>
  <thead>
    <tr>
      <th></th>
      <th>geometry</th>
      <th>place_name</th>
      <th>bbox_north</th>
      <th>bbox_south</th>
      <th>bbox_east</th>
      <th>bbox_west</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>POLYGON ((-2.03365 52.40231, -2.03322 52.40217...</td>
      <td>Birmingham, West Midlands Combined Authority, ...</td>
      <td>52.608706</td>
      <td>52.381053</td>
      <td>-1.728858</td>
      <td>-2.033649</td>
    </tr>
    <tr>
      <th>1</th>
      <td>POLYGON ((-1.80042 53.88595, -1.80041 53.88594...</td>
      <td>Leeds, Yorkshire and the Humber, England, Unit...</td>
      <td>53.945872</td>
      <td>53.698968</td>
      <td>-1.290352</td>
      <td>-1.800421</td>
    </tr>
    <tr>
      <th>2</th>
      <td>POLYGON ((-1.80147 53.48098, -1.80049 53.48027...</td>
      <td>Sheffield, Yorkshire and the Humber, England, ...</td>
      <td>53.503104</td>
      <td>53.304512</td>
      <td>-1.324669</td>
      <td>-1.801471</td>
    </tr>
    <tr>
      <th>3</th>
      <td>POLYGON ((-2.06125 53.82562, -2.06017 53.82504...</td>
      <td>Bradford, Yorkshire and the Humber, England, U...</td>
      <td>53.963151</td>
      <td>53.724341</td>
      <td>-1.640330</td>
      <td>-2.061248</td>
    </tr>
    <tr>
      <th>4</th>
      <td>POLYGON ((-2.31992 53.41161, -2.31847 53.40999...</td>
      <td>Manchester, Greater Manchester, North West Eng...</td>
      <td>53.544592</td>
      <td>53.340104</td>
      <td>-2.146829</td>
      <td>-2.319918</td>
    </tr>
    <tr>
      <th>5</th>
      <td>POLYGON ((-3.01917 53.43616, -3.01806 53.43323...</td>
      <td>Liverpool, North West England, England, United...</td>
      <td>53.474967</td>
      <td>53.311543</td>
      <td>-2.818000</td>
      <td>-3.019173</td>
    </tr>
    <tr>
      <th>6</th>
      <td>POLYGON ((-2.71837 51.50617, -2.71837 51.50616...</td>
      <td>Bristol, City of Bristol, South West England, ...</td>
      <td>51.544432</td>
      <td>51.397284</td>
      <td>-2.510419</td>
      <td>-2.718370</td>
    </tr>
    <tr>
      <th>7</th>
      <td>POLYGON ((-1.62490 53.65363, -1.62488 53.65358...</td>
      <td>Wakefield, Yorkshire and the Humber, England, ...</td>
      <td>53.741811</td>
      <td>53.575349</td>
      <td>-1.198814</td>
      <td>-1.624898</td>
    </tr>
    <tr>
      <th>8</th>
      <td>POLYGON ((-1.61446 52.42795, -1.61412 52.42774...</td>
      <td>Coventry, West Midlands Combined Authority, We...</td>
      <td>52.464772</td>
      <td>52.363885</td>
      <td>-1.423957</td>
      <td>-1.614459</td>
    </tr>
    <tr>
      <th>9</th>
      <td>POLYGON ((-1.24696 52.95344, -1.24689 52.95317...</td>
      <td>City of Nottingham, East Midlands, England, Un...</td>
      <td>53.018672</td>
      <td>52.889008</td>
      <td>-1.086119</td>
      <td>-1.246956</td>
    </tr>
    <tr>
      <th>10</th>
      <td>POLYGON ((-1.77567 54.98962, -1.77566 54.98955...</td>
      <td>Newcastle upon Tyne, Tyne and Wear, North East...</td>
      <td>55.079382</td>
      <td>54.959032</td>
      <td>-1.529200</td>
      <td>-1.775672</td>
    </tr>
    <tr>
      <th>11</th>
      <td>POLYGON ((-1.56888 54.92462, -1.56824 54.92409...</td>
      <td>Sunderland, Tyne and Wear, North East England,...</td>
      <td>54.944170</td>
      <td>54.799042</td>
      <td>-1.345665</td>
      <td>-1.568879</td>
    </tr>
  </tbody>
</table>


## Visualizations

For each of these 12 cities, the returned bearings were weighted by street length to produce the following visualisations using simple polar projection plots. It is important to note two key points about this approach:
1. The bearings of streets were derived from only their start and finish nodes, ignoring paths in-between. This was to ensure reasonable computation times as an alternative to using the full polylines.
2. Naturally, bearings are rotationally symmetric as we do not account for the direction of one-way streets. 

### Birmingham


![](/images/urban-cities/urban-cities_10_0.png)


Birmingham’s visualization is unmistakably circular. Many older cities lack a grid structure, with impromptu-built streets going off in many different directions. The place now called “Birmingham” has been around for more than 1,400 years. It was believed to have been established by a Saxon tribe, before expanding over the centuries into the city of 8500 streets we know today.
![William Westley's 1732 Prospect of Birmingham](/images/urban-cities/prospect_of_birmingham.jpg)
### Manchester & Newcastle


![](/images/urban-cities/urban-cities_14_0.png)


Manchester displays quite a clear cross-like visualization. This city has an interesting grid structure with a strong emphasis on moving north-to-south. The east-to-west flow is perhaps due to Manchester sitting almost directly between Liverpool and Sheffield, and the reduced SE/NW activity might result from its position just in the upper left of the Peak District.

Newcastle is similar but for a more obvious reason; its central ring-road system, which is vaguely hexagonal, is presumably responsible for the high degree of symmetry we observe.

### Coventry


![](/images/urban-cities/urban-cities_17_0.png)


Not unlike Manchester, Coventry’s visualization hints at a grid-like design. Famously, this ancient city—once a hotspot of trade for cloth and textiles—was obliterated in 1940 by a series of bombing raids, now called the Coventry Blitz. In the decades following, the city’s remains were rebuilt into a modern grid structure.

### Bristol


![](/images/urban-cities/urban-cities_20_0.png)


For a city founded on the turn of the second-last millennia, we wouldn’t expect to see much beyond a uniformly distributed set of bearings. Yet Bristol’s otherwise almost-circular plot is cut along the NE/SW line. Modern Bristol is dominated by the M5, as well as the River Avon. It’s interesting that a 1960s motorway construction can have such an impact on the bearings of an ancient city.

## Final Thoughts

As well as analyzing the street orientations of individual cities, it is beneficial to to showcase their visualizations side-by-side to draw comparisons and appreciate relative differences. To extend, I have collated the visualizations for the twelve cities I considered into one final image.


![](/images/urban-cities/urban-cities_24_0.png)


### The Importance of Data Science

I think it important to observe how data science, once a niche and theoretical discipline, can offer such rich insights into the history of the UK’s major cities. From Birmingham’s pre-industrial beginnings, to the devastating campaigns of the German Luftwaffe, these simple visualisations tell stories of our past. They compress a millennia-long archive of the achievements and failures that gave rise to modern Britain.

To that extent, if you are a data scientist wondering how you can apply your technical skills to real-world projects, or a student with domain expertise, keen to build up the technical skills to answer the questions you care about, make sure you follow Warwick Data Science Society [on social media](https://www.facebook.com/warwickdatascience) to keep up-to-date with relevant opportunties. These include academic talks, data science news, workshops, and beginners programming courses, so there is certainly something for everyone. Thank you for reading this piece.

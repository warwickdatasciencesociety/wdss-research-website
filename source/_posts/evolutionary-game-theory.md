---
title: "Computational Approach to Evolutionary Game Theory"
date: 2021-04-04
updated: 2021-04-04
authors_plus:
- "Ed Plumb"
- "Jacobus Smit"
contacts_plus:
- "https://www.linkedin.com/in/edward-plumb-469a46173/"
- "https://www.linkedin.com/in/jacobus-smit/"
editor: "Keeley Ruane"
editor_contact: "https://www.linkedin.com/in/keeley-ruane-6aab4219b/"
tags:
- simulation
- agent-based-modelling
- animation
categories:
- [Economics, Game Theory]
languages:
- julia
description: "From abstraction to simulation, we try to solve the same evolutionary problem using both analytical and computational techniques but do we reach the same conclusions?"
cover: /banners/evolutionary-game-theory.jpg
---

## Introduction

Evolutionary game theory (EGT) is a field of game theory that originated from a formalisation of ideas outlined by population geneticist Ronald Fisher in 1930. The theory predicts that the sex ratio of most species is approximately 1:1, meaning the same number of male and female offspring are produced. The reasoning behind this being that if there were an excess of a certain sex, the genes that predispose a member of the species to have more offspring of the other sex would have more surviving offspring, thus shifting the genes towards the 1:1 ratio.

The most important concept in microeconomics is that of equilibrium, and this is no different in game theory. Equilibrium concepts in traditional game theory include Nash equilibria (NE) and dominating strategy, however as games become more complex through the repetition of gameplay, these "one-shot" solutions no longer fully capture or explain the behaviour of the players. For this reason, the 1973 article by John Maynard Smith and George R. Price "Game theory and evolution" which formalised Fisher's ideas into solution concepts is celebrated as the birth of a new type of game theory.

However, EGT is not just for studying populations of living creatures. In the field of Multi-Agent Reinforcement Learning, the theory of EGT contributes insights into learning in multi-agent systems (MAS) and helps researchers develop improved learning algorithms.

MAS is closely related to agent-based modelling (ABM), which looks for emergent behaviours in complex systems through simulating interactions of autonomous individuals. It looks for how micro-scale changes to individuals can have macro-scale effects on the overarching system.

In this article, we will introduce a problem in population dynamics containing three different species of bird each with a unique behaviour. We will study the problem from two different perspectives, EGT and ABM, and aim to answer two questions:

1. For any given setup, is there a species that drives out all the others?

2. Are there any stable points where the ratio of the three species gravitate towards 1:1 from the offspring sex ratio example?

![Equilibrium](/images/evolutionary-game-theory/equilibrium.jpg)
## The Situation

In his 1976 book *The Selfish Gene*, one of the situations Dawkins describes is how certain birds have evolved the strategy of sneaking their eggs into other birds' nests so they don't have to expend the energy in look after the offspring themselves. Cuckoos, sometimes referred to as Brood Parasites, are an example of birds that use this strategy.

One potential problem for our parasitic cuckoos, however, is that certain species of birds have evolved to be able to identify their own eggs. This means that a cuckoo unfortunate enough to lay their egg in one of these nests would not get any benefit from doing so. Guillemots are birds who can identify their own eggs, on the other hand this identification process may take a while and use energy that could otherwise be used on finding food. Finally, some species such as chickens have such a strong ingrained sense of looking after whatever is in their nest that they will sit on anything that falls into it, including fake eggs and even small animals such as kittens. Anything in their nest they treat as their own. In their naturally evolved habitat, there would be no brood parasites, so identifying one's own eggs would not have been a particularly useful trait.

Now in a game theory setting, we assign payoffs to outcomes. We assume that sitting on an egg always causes it to hatch a chick. For every egg that hatches, the bird who laid the egg will get $h$ points. For every egg that the bird has to sit on, the bird will lose $e$ points. If a bird has to take the time to identify its own eggs out of all those in its nest it will lose $i$ points (but if it finds any eggs that are not its own this cost will help to cancel out with the cost of sitting on the now destroyed egg). We assume that cuckoos do not sit on eggs as they do not make nests. We can summarise these payoffs in a list:
* $h$ — the utility that a bird receives by having their own egg hatch.
* $e$ — the cost per egg that a bird incurs by looking after an egg.
* $i$ — the cost of identifying eggs.

We will suppose that all of $h, e, i > 0$ and $h - e - i > 0$, so that the identifiers always get a strictly positive payoff.

## Evolutionary Game Theory (Analytic) Approach

Within the total bird population, there are the constituent populations of each type of bird. For the sake of clarity, the phrase “population state” will be used to refer to the number of each type of bird within the total population.

There are two types of equilibrium that we are interested in.
The first is the Nash equilibrium. In this context, a Nash equilibrium is a certain population state in which no type would want to change the actions that they take. Hence, in order to have a Nash equilibrium, the utility of each type of bird in a population must be equal and, if any types of birds are not in this population, the utility of these types, if they were to be introduced, must not be greater than the utility of the birds that are in the population. The second type of equilibrium is the Evolutionary Stable Strategy (ESS). An ESS is a certain population state in which no type of bird would benefit from a small change in the state.

In order to find these equilibria, there are two viewpoints that need to be considered.
The first is the most intuitive: we consider each member of the population as an individual who will act in a certain way according to their type. 
The second is less intuitive, but often more helpful when it comes to calculations: we consider an ‘average’ member of the population who can take any of the actions available to the population types and will take any particular action with a certain probability. In particular, it will take a certain type’s action with probability equal to the proportion of that type in the population.
These viewpoints are equivalent. Suppose you have a population of three types: $A$, $B$ and $C$. If there are $10$ members of each type, this is equivalent to having an ‘average’ member who takes type A’s action, type B’s action and type C’s action ⅓ of the time. Likewise, if there are 15 members of type A, 10 of type B and 5 of type C, this is equivalent to an ‘average’ player who takes A’s, B’s and C’s actions with probabilities ½, ⅓ and ⅙ respectively. The second viewpoint allows us to formally define a Nash equilibrium and an ESS.
{% note info %}
The derivation of the equilibria will be completed in the appendix.
{% endnote %}
Suppose that we have a total population size of T. Let $p_S, p_I, p_C \in [0, 1]$ be the proportion of ‘Sitters’, ‘Identifiers’ and ‘Cheaters’ in the population. 
Then we can derive the expected payoff from each of these cases:

firstly in the case $p_C < 1$

$$
\begin{aligned}
    \mathbb{E}(S) &=   h - e\left(1 + \frac{p_{C}}{p_{S}+p_{I}}\right)\\
    \mathbb{E}(I) &=  h - e - i\\
    \mathbb{E}(C) &= h \frac{p_{S}}{p_{S}+p_{I}}
\end{aligned}
$$

and then in the case $p_{C} = 1$

$$
\begin{aligned}
    \mathbb{E}(S) &=   h - e(1 + T)\\
    \mathbb{E}(I) &=  h - e - i\\
    \mathbb{E}(C) &= 0
\end{aligned}
$$
   
From these we are able to derive that there is a unique Nash Equilibrium, however it is not an ESS.
The unique Nash Equilibrium is found in the state:

$$p_S = \frac{e(h-e-i)}{h(i+e)}, \; p_I = \frac{e}{h}, \; p_C = \frac{i}{i+e}$$


There is some intuition behind these numbers. 
For $p_C$, this illustrates how, if the cost of identifying decreases, then it will be profitable to identify. Hence, there will be more identifiers and so fewer cheaters. 
Similarly, for $p_S$ and $p_I$, if the cost of an egg increases, then it will be a greater cost to look after extra eggs for the sitters and so, there will be fewer sitters and more identifiers. In this state, each of the types gets a payoff of $h-e-i$. However, this is not an ESS. For those curious as to why this will be demonstrated in the appendix, but we can also gain insight about this by using simulation.

## Agent Based Modelling (Simulated) Approach

As discussed earlier, the aim of ABM is to model the micro to observe the macro. Those from an Economics background may already have alarm bells ringing in their head as microeconomics and macroeconomics are treated fundamentally differently and often do not cross paths. Indeed, much criticism has been raised to agent-based models used in the social sciences due to the complexity of human behaviour and the black-box nature of agent-based methods. In this situation however, our agents are predisposed to act in a certain way due to their genes. Of course, in real life there will be idiosyncrasies in the behaviour of each individual animal, but the goal of this model is to see effects on a species level, rather than an individual level, so each agent is modelled to be identical to others in its species.

Our agent-based model is written using the Julia package, `Agents`, which allows the user to focus on what is important to their own model rather than having to write an entire model from scratch. We provide the package with the types of our agents, their attributes, how they act, what order they act in, how they reproduce, and how they are affected by their environments (if relevant). The full code is available [here](https://github.com/jacobusmmsmit/evolutionary-abm).

As much of the code is repeated, we'll look at the implementation of one of our custom types so you can get a feel for how `Agents` works:

``` julia
mutable struct Cheater <: AbstractAgent
    id::Int
    eggs_laid::Int  # how many eggs the agent lays
    egg_ids::Dict  # how many eggs placed in this nest by each id
    utility::Float64
end
```

A few technical things to note:
 1. A `mutable struct` is what Julia calls a class from Python.
 2. We specify in the definition that `Cheater` is a subtype of `AbstractAgent` which lets `Agents` assume everything applying to an arbitrary agent will also apply to our `Cheater` type.
 3. Our struct must contain an `id`, this is our only way to tell agents of the same type apart.
 
 Now we can define how our agent will behave when it is called upon to move. We want our cheater to
 1. Pick a random nest
 2. Lay an egg in this nest (or multiple eggs if specified)
 
In our implementation each agent has an associated dictionary whose keys are the `id`s of birds who have laid eggs into its nest (including its own id), and the values are how many eggs from each bird.

``` julia
function agent_step!(cheater::Cheater, model)
    # Will return -1 if there are no nests
    if random_agent_type(model, [Sitter, Identifier]) != -1
        for _ in 1:cheater.eggs_laid
            # Choose a random nest
            rand_agent_id = random_agent_type(model, [Sitter, Identifier])
            increment_dict!(model[rand_agent_id].egg_ids, cheater.id)
        end
    end
end
```

After defining how each of our species behave and their attributes, we need to define how the model itself acts after each agent has moved. In our case, this will be to tally up the utility of each type and construct a new population such that the proportion of each type is equal to that type's share of the total utility in the previous step. We also want to define some sort of population mutation which can introduce an element of randomness into the model. This is to see if we can confirm the analytic solution by making the setup as similar as possible.

``` julia
function model_step!(model)
    nonextinct_types = unique(typeof.(allagents(model)))
    
    # Aggregate all egg_ids of non-extinct types into an array of IDs 
    nest_id_array = [
        id for (id, agent) in model.agents
        if typeof(agent) in intersect([Sitter, Identifier],nonextinct_types)
    ]
    hatched_egg_dict = Dict{Int64,Int64}()
    for nest_id in nest_id_array
        for (egg_id, tally) in model.agents[nest_id].egg_ids
            increment_dict!(hatched_egg_dict, egg_id, tally)
        end
    end

    # Calculate utility of each agent and then type
    for (key, agent) in model.agents
        agent.utility = model.hatch_utility * get(hatched_egg_dict, key, 0) +
            Int(!isa(agent, Cheater)) * -model.egg_cost * get(agent.egg_ids, key, 0) +
            Int(isa(agent, Identifier)) * -model.identify_cost
    end
    utilities = map(agent_type -> get_total_utility(model, agent_type),
                    nonextinct_types)
    
    # Resample population weighted by utility
    total_agents = nagents(model)
    # In case we don't want to kill *all* agents
    killed_agents = Int(ceil(total_agents / 1))
    for _ in 1:killed_agents
        kill_agent!(random_agent(model), model)
    end    
    n_offspring = countmap(Distributions.sample(nonextinct_types, 
                                                Weights(utilities),
                                                killed_agents))
    for (agent_type, count) in n_offspring
        for _ in 1:n_offspring[agent_type]
            reproduce!(agent_type, model)
        end
    end
    
    # Mutate population
    if rand() < model.p_mutation
        # Kill a random member in order to keep number of agents the same
        kill_agent!(random_agent(model), model)
        # Sample from all 3 types as NSS can be interior
        reproduce!(rand([Sitter, Identifier, Cheater]), model)
    end
    
    # Tell the model that all types are alive
    for variable in [model.sitters_extinct, 
                     model.identifiers_extinct,
                     model.cheaters_extinct]
        variable = 1
    end
end
```

The rest of the model's code is not included in this post for simplicity can be found in the post source.

We can now run our model and see how the proportion of each type changes over time




![](/images/evolutionary-game-theory/evolutionary-game-theory_11_0.svg)



We can also visualise our model's development in a ternary plot, in which every point inside a triangle represents a different composition of the three constituent populations.
![Animated Model](/images/evolutionary-game-theory/model_animated.gif)
Both graphs show something that we would expect given our analytic solutions, namely that there are no evolutionarily stable states. Our animated example shows that even if we start in the centre we are pushed out to the extrema. We can visualise this movement in a vector field plot, also known as a quiver plot. Here the plot is constructed by initialising the model with a certain number of agents, running it for one step (i.e. letting all agents move once), and then seeing where the model ends up. If we average this out over 100s of runs we can come to a pretty accurate approximation for the true value. Constructing a plot like this could be possible analytically, but requires knowledge of differential equations to get a similar level of accuracy that can be obtained through simulation.




![](/images/evolutionary-game-theory/evolutionary-game-theory_17_0.svg)



Using this quiver plot we can see that our NSS from before is clearly not going to be evolutionarily stable, as there are arrows all around it forcing the population state away from the point.




![](/images/evolutionary-game-theory/evolutionary-game-theory_20_0.svg)



## Discussion

Traditional analytic methods give precise general solutions. These solutions can be particularly useful when you're looking to induce a certain behaviour or state in a given system, as they can tell you what the input parameters should be to ensure you end up at the state you want. However, these methods are limited in scope. An obvious limitation is that there is no concept of the environment in which the agents live, so you can’t model things like distance travelled without making special considerations. You can extend analytic methods by looking at evolutionary graph theory, which considers how topology affects a population, but these extensions themselves can become intractable and may not have closed form solutions.

Agent-based models produce simulations and one can make inferences from their outcomes about the nature of the system. While these insights may not be as precise as the analytic solutions and can require a lot of computing power, it is possible to add so much more to a model than you can with analytic solutions before they become really hard to solve. For example, in our model we could have looked at what happens if certain species are allowed to lay more than 1 egg, or we could program in that nests with fewer eggs gain more utility for the eggs' owners, or indeed we could add in a space for the agents to live.

## Appendix


We start by considering the payoffs:

| Strategy                  | Cost/Reward  |
|---------------------------|--------------|
| Having your own egg hatch | h            |
| Sitting on eggs           | -e (per egg) |
| Identifying eggs          | -i           |

Here we are assuming $h,e,i >0$ and $h-e-i>0$

From these we can obtain the utilities for each type of bird. We let $N :=$ number of foreign eggs in your own nest , and $x := $ the target nest. $\mathbb{I}_{\textit{S-nest}}(x)$ is a function which returns value 1 if the target nest is a nest of a sitter, and 0 otherwise (as cheaters' nests and identifiers' nests would result in no incubation for the cheater's egg).

$$
\begin{aligned}
    U(S) &=   h - e(1 + N)           \\
    U(I) &=  h - e - i \\
    U(C) &= h\mathbb{I}_{\textit{S-nest}}(x)
\end{aligned}
$$

Now, to determine the expected value of these strategies, we need to determine the distribution of the random variable $N$, and the probability of the event $\textit{S-nest}$. Let the total number of birds in the population be $T$, and the proportion of each strategy be $p_S, p_I, p_C$. We assume that cheaters cannot tell which nests belong sitters and which belong to identifiers. Therefore, when it decides which next to sneak its egg into, each nest of the sitters and identifiers will be picked with probability $\tfrac{1}{T(p_{S} + p_{I})}$, assuming, for now, $p_{I}+p_{S}>0$. For each nest, a cheater choosing its target is a Bernoulli random variable with probability $\tfrac{1}{T(p_{S} + p_{I})}$, where 1 represents the cheater choosing this particular nest. Now, all cheaters have the same probability of choosing an individual nest, and do so independently, hence the number of eggs in a particular nest is the sum of i.i.d Bernoulli variables, which gives
$$
N \sim \text{Binomial}\left(T \times p_C, \tfrac{1}{T(p_{S} + p_{I})}\right) \implies \mathbb{E}(N) = p_C\dfrac{T}{T(p_{S} + p_{I})} = \dfrac{p_{C}}{p_{S} + p_{I}}
$$
where $T \times p_C$ is the total number of cheaters in the population. 


The probability of the event $\textit{S-nest}$ is determined by seeing that among the $T(p_{S} + p_{I})$ total nests available to sneak the egg into, $T \times p_S$ of them will be safe. Hence

$$
\mathbb{P}(\textit{S-nest}) = \dfrac{T \times p_{S}}{T(p_{S} + p_{I})} = \dfrac{p_{S}}{p_{S} + p_{I}}
$$

We can now determine the expected value of each strategy:

$$
\begin{aligned}
    \mathbb{E}\left[ U(S)\right] &=  h - e\left(1 + \mathbb{E}[N]\right)  = h- e\left(1 + \dfrac{p_{C}}{p_{S}+p_{I}}\right)\        \\
    \mathbb{E}\left[ U(I)\right] &=  h-e-i\\ 
    \mathbb{E}\left[ U(C)\right] &= h\mathbb{E}[\mathbb{I}_{\textit{S-nest}}(x)] = h\left(\dfrac{p_{S}}{p_{S} + p_{I}} \right) 
\end{aligned}
$$

We will also consider the expected value for each strategy if there is a population of only cheaters. 
In this case, there will be no sitters to look after the cheaters' eggs, and hence, the cheaters will get a payoff of zero. 
Any hypothetical sitters, after a deviation, would be given T eggs to sit on. 


So we have a formulation that is given by the following two cases:

If $p_{C} \neq 1$

$$
\begin{aligned}
    \mathbb{E}(S; h,e,i) &=   h - e\left(1 + \frac{p_{C}}{p_{S}+p_{I}}\right) = h -  \frac{e}{p_{S}+p_{I}}\\
    \mathbb{E}(I; h,e,i) &=  h - e - i\\
    \mathbb{E}(C; h,e,i) &= h\cdot \frac{p_{S}}{p_{S}+p_{I}}
\end{aligned}
$$

If $p_{C} = 1$

$$
\begin{aligned}
    \mathbb{E}(S; h,e,i) &=   h - e(1 + T)\\
    \mathbb{E}(I; h,e,i) &=  h - e - i\\
    \mathbb{E}(C; h,e,i) &= 0
\end{aligned}
$$

We will now look for Nash equilibria. As discussed before, to form a Nash equilibrium the utility of each type of bird in a population must be equal and, if any types of birds are not in this population, the utility of these types, if they were to be introduced, must not be greater than the utility of the birds that are in the population.

__NE with One Type of Bird__

Consider, $p_{C}=1$. It is clear from Case Two that the expected utility for a type I would be greater, as $h-e-i > 0$. Hence, we will consider when $p_{C} \neq 1$. 
If $p_{S}=1$, there will be a profitable deviation from S to C, hence this will not give us a Nash equilibrium.
If $p_{I}=1$, there will be a profitable deviation from I to S, and so this will also not give us a Nash equilibrium.

__NE with Two Types of Bird__

In a population of just sitters and identifiers, there is no utility in identifying and this is just a cost. Hence, as $h-e-i < h-e$, this will not give us Nash equilibrium.

In a population of just sitters and cheaters, the sitters will get a payoff of $h - \frac{e}{p_{S}}$, which is strictly less than the payoff of the cheaters, namely $h$. So this will not be a Nash equilibrium.

In a population of just identifiers and cheaters, the cheaters will not get a positive payoff, as their eggs will always be identified. Whereas the identifiers will always get strictly positive payoff. Hence, the payoff for the identifiers will be strictly greater than the payoff for the cheaters, so this will not give us a Nash equilibrium.

Therefore, there are not any Nash equilibria when a population is made up of one or two types. Hence, we will look for an equilibrium for a population made up of the three types. 

__NE with Three Types of Bird__

In a NE with all three types of bird, all three expected utilities will have to be equal.

$$E(I; h,e,i)= E(S; h,e,i)= E(C; h,e,i)$$
Hence, by the first equality and that $p_{S} + p_{I} = 1- p_{C}$, we have, $$h - e\left(1 + \frac{p_{C}}{1-p_{C}}\right) = h - e - i$$
Hence, $p_{C} = \frac{i}{i + e}$

By the second equality, we have,
$$h -  \frac{e}{p_{S}+p_{I}} = h\cdot \frac{p_{S}}{p_{S}+p_{I}}$$
Hence, $p_{I} = \frac{e}{h}$.

Therefore, as $p_{C} + p_{I} + p_{S} = 1$, $p_{S} = \frac{e(h-e-i)}{h(i+e)}$

This is the unique Nash equilibrium in this setup.

__Checking for ESS__

Instead of considering the population as many individuals, we will consider change our viewpoint to consider an ‘average’ member of the population who can take any of the actions available to the population types and will take any particular action with a certain probability. In particular, it will take a certain type’s action with probability equal to the proportion of that type in the population.

We will then use the notation $u(a,b)$, to mean the expected utility of a player choosing action $a$, which, in this case, will be a triple $(p_{S},p_{I},p_{C})$, but while the overall population plays action $b$, also a triple of the same form. Note, as this is expected utility, the function is bilinear.

An Evolutionary Stable Strategy is a population state that is resistant to small mutations. This means that, if there is a small change in the population state, the mutated state will give a lower expected average payoff than the original state. Let $x$ be the current state and $y$ be a population that has mutated. Therefore, for this mutated population to not take over, we require that the average payoff of $x$ in a population of $\varepsilon x + (1- \varepsilon) y$ is greater than the average payoff of $y$ in that same population, at least for a small enough $\varepsilon$. The mathematical notation for this is that $\exists \varepsilon >0$ such that:
$$u(x,\varepsilon y + (1- \varepsilon ) x) > u(y, \varepsilon + (1- \varepsilon ) x)$$

Hence, for $x = (p_{S},p_{I},p_{C})$ where these values are as given above, 
$u(y,x) = u(x,x)$. Hence, the condition for an evolutionary stable strategy is equivalent to $u(x,y)> u(y,y)$, using that $u$ is bilinear.

I claim that $x=\left(\frac{e(h-e-i)}{h(i+e)}, \frac{e}{h}, \frac{i}{i + e}\right)$ is not an evolutionary stable strategy.
I propose that $y=(a,0,1-a)$ for small enough $a\in (0,1)$ gives $u(x,y) \leq u(y,y)$
As $y$ is the population state, we have:

$$
\begin{aligned}
    \mathbb{E}(S; h,e,i) &= h -  \frac{e}{a}\\
    \mathbb{E}(I; h,e,i) &=  h - e - i\\
    \mathbb{E}(C; h,e,i) &= h
\end{aligned}
$$

Then

$$u(x,y) = \frac{e(h-e-i)}{h(i+e)}\left(h- \frac{e}{a}\right) + \frac{e}{h}(h-e-i) + \frac{i}{i+e}h$$

and

$$u(y,y) = a(h- \frac{e}{a}) + (1-a)h = h-e$$

Then, for small enough $a>0$, $\frac{e(h-e-i)}{h(i+e)}\left(h- \frac{e}{a}\right)$ will be negative and large enough that $u(x,y) \leq u(y,y)$.
Therefore, this is not an evolutionary stable strategy.

---
title: "Oh Hell! - Reinforcement Learning for solving card games"
date: 2021-12-04
updated: 2021-12-04
authors_plus:
- Albert Nyarko-Agyei
- Alexandru Pascru
- Ron Cvek
contacts_plus:
- "https://www.linkedin.com/in/albert-nyarko-agyei-6ab804188/"
- "https://www.linkedin.com/in/alexandru-pascu/"
- "https://www.linkedin.com/in/ronaldcvek/"
editor: "Keeley Ruane"
editor_contact: "https://www.linkedin.com/in/keeley-ruane-6aab4219b/"
tags:
- reinforcement-learning
- card-games
- agent-learning
categories:
- [Computer Science, Games]
languages:
- Python
description: "In this article we are going to plays cards. Well, not exactly ... with the power of reinforcement learning we are going to train intelligent agents that will play the game for us!"
cover: /banners/cards.jpg
---
{% note info %}
This post is the corresponding write-up for a WDSS project in which Albert Nyarko-Agyei, Alexandru Pascru and Ron Cvek applied reinforcement learning to better understand the mechanics of a British card game—<i>Oh Hell</i>. The rules and an online version of the game can be found [here](https://cardgames.io/ohhell/). Special credits to Henry Charlesworth for providing valuable insights. The main author of the project and the blog-post is Albert Nyarko-Agyei.
{% endnote %}
## Introduction

The idea for this project started when I was introduced to the game, <i>Oh Hell</i>, by one of the contributors to the project. We played a variation where each player is given 7 cards and then the players take it in turn to predict how many rounds they will win. Interestingly, predicting correctly gives you extra points or 'tricks.' So, if many games are being played, a good prediction strategy is needed. 

After bidding, the round starts with the player to the left of the dealer playing a card from their hand. Each player then has to play a card from the same suit if they have one, otherwise any card from their hand is permissible. Once everyone has played a card, the player who played the highest card from the first suit wins the round, gets a trick added to their total, and starts the next round. Two caveats to these rules are:

1.   Along with dealing cards for the game, a trump card is drawn and if a card from with the same suit is played, it will beat every other suit.

2.   The number of tricks bid by the last bidder can not make the total number of tricks bid equal to the number of cards dealt to each player.

Now that we have the rules down, some different strategies might have come across your mind. Horde your trump cards till the end? Bid a low number of tricks? Bid a high number of tricks because you're confident? What is the perfect strategy to this game? Turning to AI and Reinforcement Learning seemed a logical way to answer these questions. 

**Note**: There are two main themes in this project, the programming of agents/models, and the theory behind why certain methods work; feel free to pick which sections interest you.

## The Approach

**Reinforcement learning** is a branch of Machine Learning that deals with the **actions** an **agent(s)** should take based on it's **observation** of an **environment** in order to maximise a **reward**. If our environment is a simple <i>Oh Hell</i> game, we can formulate our problem as designing an agent to predict what action will give the most reward, given that our environment is in a particular **state** and thus what action to take. 

![Main-Components-of-RL](/images/oh-hell/rlvisualisation.jpg 'Main Components of RL')

## Programming the Environment

The first step was to implement a game of <i>Oh Hell</i> in Python. Most games studied under reinforcement learning follow a similar structure, and some build up to a class representing the environment the agent can train in. If your custom environment inherits from an existing base environment, you can use high level implementations of RL algorithms that require that base. For this project [OpenAI's gym](https://github.com/openai/gym) environment class was used. This base class has the abstract methods, step (take a single action) and reset (restart the environment). These methods are called by the final training algorithm.

The rules of <i>Oh Hell</i> use elements of <i>Poker</i> and <i>Uno</i> which have already been implemented countless times. The module [RLCARD](https://github.com/datamllab/rlcard) by MIT has a set of already implemented environments for some card games, including <i>Poker</i> and <i>Uno</i>. Also the structure of RLCARD's environments is very clean, so the base of this project used a lot of their methods. At the time of development, however, the environments in RLCARD were only for two-player games and did not have a PPO implementation (will cover more) so it had to be extended.

Below is the structure of the different classes in the code. Composition was used instead of inheritance; for instance, the Round class creates instances of players, a dealer, and a judger and their interaction is controlled within the Round class. A round in this code represents every player taking a single action, making a bid or playing a single card. A game represents the start of the bidding to the last card being played. 

[![Structure-of-code](/images/oh-hell/gamecode.jpg 'Structure of Code')](https://github.com/LeLingu/OhHellProject/tree/main/rlohhell/games/ohhell)

## Extracting the input state from the environment

Now, the agent needs to be able to 'see' the environment and then make predictions about what action to take. This process can be viewed as a function, so neural networks come in to try and approximate the function that gives the best predictions. If we encode the useful information in the game, the neural network should be able to draw out a strategy. 

There are a few approaches to this particular section, one could encode almost everything in the environment and make it very easy for the neural network to pick out the optimal actions - or you could give the neural network only the basic information. The first method is a useful debugging tool since an agent with all the information about it's environment should have no excuse not to learn. The latter method takes less time to program but would take longer to train and would not necessarily give the best model because some useful information could be neglected.

The encoding for the model at the time of this blog is below, and a detailed explanation of the [encodings](https://github.com/LeLingu/OhHellProject/blob/main/rlohhell/envs/ohhell.py) can be found on the github.

![Encoding](/images/oh-hell/currentencoding.jpg)

## Opponents for the agent and NFSP

After extending the environment to a four-player game, what the agent would train against came into question. The approach that was taken in this project was inspired by the idea of **Neural Fictitious Self-Play** developed by David Silver and Johannes Heinrich, leading researchers in RL. At it's core, the idea is to train the agent against itself. Initially, a basic model was trained against random agents, then a new model was trained against three versions of the last agent. The theory is to repeat this process each time until the new agent beats the old agents. Below is a snippet of the code from the environment that uses this idea: 


```python
'''This section plays the game with the dummy agents until it is time for the training 
agent to play then the agent's observation of the environment can be extracted'''

while self.game.players[self.game.current_player].name != 'Training':
    # The state is extracted from the current game
    current_obs = self._extract_state(self.game.get_state(self.game.current_player))

    # The observation is used in the trained model to predict an action
    fictitious_action, _ = self.trained_model.predict(current_obs)

    # The action is taken 
    _, _ = self.game.step(self._decode_action(fictitious_action))

    # This section was used for training against random agents

    # a = random.choice(self.game.get_legal_actions())
    # _,_ = self.game.step(a)
```

## Choosing an RL algorithm

Coming back to the function we need to approximate, which is formally called the **policy**, there are a few different methods to choose from, however, they can all be categorised into two groups. Methods that generate training data (experience) from the same policy that is being evaluated are called **on-policy**. Methods that have two separate policies, one for generating experience and another for evaluation, are called **off-policy**.

The method we chose for this project was on-policy **Proximal Policy Optimization** or **PPO** by OpenAI. To quote their website directly, RL algorithms have a lot of 'moving parts' which makes the training of agents very unstable. PPO, however, uses a clipped objective function which reduces changes to the current policy so that the performance doesn't suddenly decline whilst training. A detailed explanation of the objective function can be found [here](https://openai.com/blog/openai-baselines-ppo/).


## The Neural Network Architecture

Adding on to our understanding of how to approximate the earlier function, PPO outputs the actions for the agent to take in the form of **logits** whilst it also outputs the **state value**. The logits are unnormalised predictions of the actions to take, the state value is the expected reward the agent will get from the current state if it follows the current policy. This additional evaluation of the state is why PPO is sometimes called an Actor-Critic algorithm. 

With this in mind, shared layers in the <i>Oh Hell</i> agent meant the agent was unable to learn until the actor and critic were spilt into two different networks. The reason for this is not clear, but a common internal conflict that agents face in RL is choosing actions that maximize immediate reward vs long-term rewards or the crucial **Exploration vs Exploitation Dilemma**.

The structure of the neural network that generated the best model is below, with details of how many neurons where used at each level.

![Neural-network-architecture](/images/oh-hell/neuralnetwork.jpg)

## Implementation of Algorithm

To run the PPO algorithm on the custom environment, the package [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) was used. It has a PPO implementation that allows you to customise the layers on a neural network and offers tensorboard support so that you can visualise training results. The entire code that generates the neural network model is found [here](https://github.com/LeLingu/OhHellProject/blob/main/custom_ppo/running_model.py) with explanations of what each section does.

Below are some of the metrics that were tracked by tensorboard during training.

![Viewing-tensorboard-integration](/images/oh-hell/tensorboard.jpeg)

## Initial Results 

The initial models struggled to correctly select which of the 63 actions were actually possible at any given point. In the game design, ineligible actions are replaced with a random action - so these initial models did not improve on what a random agent would have done.

At this stage, one could implement a so-called 'mask' over the unavailable actions which sets the logits of these actions to 0 or change the reward signal to the agent so that it is 'punished' everytime an unavailable action is selected. The latter approach is less coercive and is what was implemented. However, noticeably, it still leaves the agent with the ability to choose unavailable actions. 

## Final Results

The best trained model so far can not answer the original question of the best possible strategy for playing *Oh Hell*. The policy, however, shows a large improvement from a random agent; it will sometimes execute flawless runs, predicting a number of tricks, winning that number, and getting the extra bonus of 10 tricks and with no ineligible actions selected. This model will select an average of just under 2 unavailable actions per game which is a massive improvement from the original 10 out of 11.

![gameplay](/images/oh-hell/gameplay1.jpg)

## Conclusion

This project answered interesting questions of how RL agents are trained and this particular approach of using neural networks, Deep RL being only one of the methods in RL. If there was more time, a Monte Carlo Tree Search could hypothetically be implemented on top of this agent to improve it's performance or a completely custom and more granular PPO implementation along with a mask.

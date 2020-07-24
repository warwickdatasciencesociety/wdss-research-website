---
title: "Money for Nothing: An Arbitrage Paradox"
date: 2020-07-23
updated: 2020-07-23
author: "Yasser Qureshi"
contact: "https://www.linkedin.com/in/yasser-qureshi/"
tags:
- puzzle
- lesson
categories:
- [Economics, Finance]
languages:
description: "Who would have thought that such a seemingly obvious decision could lead to a bank exploiting you for an infinite amount of money? Read on to find out how."
cover: /banners/money-for-nothing.jpg
katex: true
---
Utilising the concept of arbitrage can be a lucrative opportunity when done correctly. Yet somehow, when done incorrectly, the results can be even more propitious (at least for one of the parties involved). In this post, we will walk through a paradox related to arbitrage in which the seemingly obvious fair price for an asset results in a strategy for obtaining infinite wealth.

## The Financial Jargon
{% note warning %}
If you are already familiar with the notions of options and arbitrage, you may wish to skip to the [next section](#the-paradox).
{% endnote %}
To make this post inclusive to all, we will begin by offering a brief, requisite understanding of the financial vocabulary used in this post, before attempting to describe the paradox itself.

In the financial world, it is hard to avoid the words _stocks_ and _shares_, so we will begin by defining these. A stock is a type of security that represents the ownership of a fraction of a company. This entitles the owner of the stock to a fraction of the corporation's assets and profits proportional to how much stock they own. A share is simply the smallest denomination of a company's stock and acts as a unit for measuring one's stake in a company.

Another key financial concept is that of the _option_. These are financial instruments based on the value of underlying securities (such as stocks). Since the value of an option is dependent on the value of another financial asset (or assets), it is a type of derivative. An options contract offers the buyer the opportunity to buy or sell the underlying asset within some fixed timeframe for a predetermined price. The two most common types of options are _calls_ and _puts_; a call allowing the holder to buy the asset whereas a put offers the sale. It is important to note, that an options contract puts the holder under no obligation to buy/sell the asset within the agreed upon timeframe (unlike a futures contract). Instead, they are free to exercise the option only when it benefits them financially.

There are a several components of an options contract, such as the premium, strike price, expiration date, and contract size, but we will focus only on the premium and strike price in this post. The premium is the down payment that the holder of the contract pays for having the right to exercise an options trade. This is paid regardless of whether the holder exercises the option. The strike price is the price at which the holder of the option can buy/sell the underlying security if they decide to exercise it. Note, that this is a fixed price and so does not change, even though the value of the underlying security might.

This brings us to _arbitrage_. Arbitrage is the act of simultaneously buying and selling assets or commodities in different markets or in derivative forms, to take advantage of different prices of the same asset. It exploits the price difference that arises as a result of market inefficiencies and is usually considered useful to markets, as it helps to re-establish efficiency. However, this opportunity is usually captured by automated trading software, making it nearly impossible for anyone to take advantage of directly.

## The Paradox

### Setup

Say one share of stock is currently worth $£100$. On top of this, by some sort of divine wisdom, we know that the share price has a $\frac{2}{3}$ chance of rising to $£120$ by the next day and a $\frac{1}{3}$ chance of dropping to $£90$. In reality, the behaviour of the share price would be governed by a statistical distribution. In this case, this post would still be valid, but the numbers wouldn't be quite as simple to handle.
![Illustration of the possible share price changes (Credit: Freepik.com)](/images/money-for-nothing/share_price.png)
A options contract for the same asset has a strike price of $£105$. This implies that there is a $\frac{2}{3}$ chance of making a profit of $£15$ (the difference between the asset selling price and the strike price) and a $\frac{1}{3}$ of neither losing nor gaining money (since the holder wouldn't exercise the option in this case, as this would lead to losing money).
![Illustration of the options contract value (Credit: Freepik.com)](/images/money-for-nothing/option_value.png)
This leaves us to ask what the fair price for such an option would be. The answer to this seems intuitive; if we have a $\frac{2}{3}$ chance of making $£15$, and a $\frac{1}{3}$ chance of gaining nothing, then on average, we would expect to gain $\frac{2}{3} \times £15 + \frac{1}{3} \times £0 = £10$. Therefore, pricing the option at $£10$ seems to be the only logical option.

This seemed like the obvious answer when I first saw this problem, yet we will see that leads to a paradox. Furthermore, this isn't some sort of trivial, technical paradox, but rather a way for a bank to exploit us to generate an endless stream of cash.

### Breaking Down the Balance Sheet

The process for such exploitation is devilishly simple. The bank starts by selling an option for the price of $£10$ that we agreed on above. They follow this by buying a half-stock for $£50$. We will insist that, by the end of the day, the bank must have a net zero balance sheet, so they also take out a loan. For simplicity, we will assume that the loan is interest-free but the paradox would hold regardless.
![The bank's day zero strategy](/images/money-for-nothing/day_zero.png){% note info %}
Pedants will note that a half-share breaks our definition of a share as the smallest denomination of a stock. This is true, though [fractional share trading](https://www.investopedia.com/terms/f/fractionalshare.asp) lets us get around this. This technically doesn't affect the logic of the paradox though, and we could simply double the quanity of all shares to avoid it.
{% endnote %}
By the following day, the share price will have either increased to $£120$ or decreased to $£90$. Let’s first consider the former possibility.

In this case, the buyer will exercise the option, so the bank will need to pay out $£15$. On top of this, the bank has to pay back the loan of $£40$. It's not all bad news though, as the stock price has now increased, leaving their half-share worth $£60$. When we tally up the wins and losses, we see that the bank has made a tidy profit of $£5$.
![The bank's day one strategy for share price increase](/images/money-for-nothing/day_one_up.png)
In the case where the price drops to $£90$, the result is equally auspicious. The buyer won’t exercise the option, so no money is lost there, though the bank still has to pay back the $£40$ loan. The stock price may have dropped, but this still leaves the bank with a half-share worth $£45$. After crunching the numbers, we should be amazed to see that the bank has again made a profit of $£5$.
![The bank's day one strategy for share price increase](/images/money-for-nothing/day_one_down.png)
There's no funny-business or mathematical slight-of-hand here; by using this strategy, the bank is **guaranteed** to make a profit (at our expense, no less). Additionally, by repeating this process or scaling up the numbers involved, the bank is left with what is essentially a monetary printing press.

Thankfully (or sadly, if banking is your thing), this is not how this problem goes in the real world. The chink is this paradox's armour was our initial assumption of what a fair price for the option would be. Now that we've seen the result of such a decision, it is clear that what may have seemed obviously true at first, was in fact incorrect.

What we failed to account for was the risk associated with the option. Rather than using the raw expected value of the option for our valuation, we should instead use a risk-adjusted version. When we follow this procedure, we see that the correct premium should have been $£5$, not $£10$. We can confirm this by modifying the balance sheets to use this figure, at which point, the bank's easy profit evaporates.
![Day zero after risk adjustment](/images/money-for-nothing/day_zero_adj.png)
We see in this case, that the reduced option price results in the bank requiring a slightly larger loan to equalise losses.
![Day one after risk adjustment](/images/money-for-nothing/day_one_adj.png)
This additional loan repayment balances the sheet on the next day so that no profit is made in either scenario.

## Closing Remarks

This paradox has been overly simplified, and in reality, the forces of supply and demand cut off most opportunity for arbitrage of this form. Nevertheless, the notion of arbitrage is used extensively in practice to price options. For example, in 1973, Fisher Black and Myron Scholes used the method of repeated portfolio replication alongside an arbitrage argument to determine the price of an option. They were awarded with a Nobel Prize for their work, but unfortunately Fischer Black passed away before the award was given.

I hope that this post has brought to light an interesting application of arbritage and inspired the reader to look further into the topic, especially with regard to its practical applications. Thank you for reading.

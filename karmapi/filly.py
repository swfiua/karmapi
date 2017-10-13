""" Fantasy Insured Loss LotterY

So lets play fantasy insured loss estimates.

Here's how the games works.

A natural catastrophe occurs.

Modelling agencies and companies estimate how much they will lose.

Here we try to guess how these loss estimates will change over time.

This is really just a game of magic denoinators.

When an estimate is given what is included is often unclear.

So an estimate from RMS a couple of days prior to Harvey landfall said the wind
losses would be $1-6B.

How did they arrive at this number?
 
1. Estimate the category of storm at landfall.
2. Find events that "match".
3. Weight events according to how good a match.
4. Run best guess of industry exposure through the model.

Problems?
=========

Many.   Not least the model is tuned to previous events.

48 inches of rain did not used to be the norm.

And most residential policies exclude flood, so who cares anyway?

And what about cars: well they are roughly 5-10% of the wind exposure -- your
car is worth way less than your home.

But wait: car insurance covers flood damage.

But we don't have a flood model.  Or if we do it has never seen 4 feet of rain.

Harvey, Irma, Jose, Katia, Maria, Mexico Quake, California fires.

Economic Loss.

Insured loss. 

Reinsurance

ILS.


Track reports over time.

Predict who will still be here in n years time.

Losses are in $1B unless otherwise mentioned. 

Multiple events and multi year contracts.

x% of contracts are aggregate covers and deductibles drop down.

x% are multi year.  Premium is fixed and deductibles drop down when the
threshold is reached.

Bonuses
=======

Report early, report detail.

An early loss report indicates:

* strong analytics, able to make estimates fast.

* confidence in your model of risk.

Detail:

* more detail to support the assertions.  This reduces the uncertainty in the 
  magic denominator. 

* but bragging about a detailed model, that ignores many factors is a negative bonus.



"""

from math import pi
from datetime import date
from collections import defaultdict

import copy

INSURED = 0.8

INSURED_FLOOD = 0.1

INSURED_WIND = 0.9

AUTO_FLOOD = 1.0

# share of contracts that are multi year
MULTI_YEAR = 1.0 / pi

# Drop down deductible
DDD = 1.0 / pi

class Event:

    def __init__(self, name, loss, ifactor=None):

        self.name = name

        self.loss = loss

        self.ifactor = ifactor or INSURED


class Report:

    def __init__(self, name, event, when, value):

        self.name = name
        self.event = event
        self.date = when or date.now()


class Org:

    def __init__(
            self,
            name,
            premium=None,
            noncat=0.0,
            ceded=0.0,
            share = None,
            capital = None,
            skill=None):
        
        self.name = name

        # market capitalisation: how the stock market values the organisation
        self.capital = capital

        # annual written premium
        self.premium = premium or self.capital / 5.0

        # share of premium for noncat lines
        self.noncat = noncat

        # share of premium that is ceded
        self.ceded = ceded

        # underwriting skill
        self.skill = skill

        # estimate of market share
        self.share = share


Orgs = dict(
    renre = Org('renre',
                premium=1.4,
                noncat=0.3,
                ceded=0.3,
                share=0.01 * INSURED,
                capital=5.6),
                
    axis = Org('axis',
               premium=1.5,
               noncat=0.3,
               ceded=0.1,
               capital=4.8),
               
    tmr = Org('tmr',
              premium=1.4,
              noncat=0.2,
              ceded=.25,
              capital=1.4),
              
    partner = Org('partner',
              premium=1.4,
              noncat=0.4,
              ceded=.25,
              capital=6.56),
              
    arch = Org('arch',
               premium=None,
               capital=12.56,
              ),
    aspen = Org('aspen',
                premium=0,
                capital=2.5),
    )


Events = dict(
        harvey =  Event('harvey', 100, 0.2),
        irma =    Event('irma', 100, 0.2),
        maria =   Event('ma,ria', 80, 0.5),
        jose =    Event('jose', 1, 0.3),
        katia =   Event('katia', 1, 0.3),
        mexicoq = Event('mexico', 25, 0.5),
        calfire = Event('calfire', 10, 0.8)
        )

q3 = [x for x in Events.values()]

# Reports so far on losses
Reports = [
    Report(Orgs['renre'], q3, date(2017, 10, 6), 0.625),
    Report(Orgs['partner'], q3, date(2017, 10, 6), 0.475),
    Report(Orgs['axis'], q3, date(2017, 10, 12), 0.585)]

# factor to apply to premium to get reinsurance loss
MAGIC = 0.001

if __name__ == '__main__':

    events16 = {}
    for key, event in Events.items():

        eee = copy.copy(event)

        eee.loss /= pi
    
        events16[key] = eee


    years = {
        2016: events16,
        2017: Events,
        2018: [Events, events16]}

    # Estimate losses
    elosses = {}
    aggloss = defaultdict(float)
    
    for ename, event in Events.items():
        print(ename)
        losses = {}
        for oname, org in Orgs.items():
            loss = event.loss * org.premium * MAGIC
            print(oname, loss)
            aggloss[oname] += loss

        elosses[ename] = losses
        print()

    # show agg losses
    print()
    print('Aggregate Loss')
    for org, loss in aggloss.items():
        print(org, loss)

    # Compare to reports
    for report in Reports:
        pass
    

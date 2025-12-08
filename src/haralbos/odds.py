'''Tools for dealing with odds, moneylines, and implied probabilities'''

def implied_probability(odds):
    '''Calculate the probability implied by odds'''
    if odds < 0:
        return odds / (odds - 100.)
    return 100. / (odds + 100.)

def betting_odds(probability):
    '''Calculates the odds that represent a given probability'''
    if probability < 0.5:
        return 100./probability - 100
    return 100. * probability / (probability - 1.0)

def inverse_odds(odds, vig_probability=0.05):
    '''
    Calculate probability of team losing if `odds` is the odds of team winning 
    Modeled as: (probability of A winning) + (probability of B winning) = 1 + vig_probability
    :param odds: odds of a win
    :param vig_probability: probability that represents the amount of the money that the house keeps
    '''
    prob = implied_probability(odds)
    inverse_prob = 1 + vig_probability - prob
    return betting_odds(inverse_prob)

def calculate_vig_probability(odds_left, odds_right):
    '''
    Given the odds for team A winning and team B winning,
    calculate the house's cut, expressed as a probability
    '''
    return implied_probability(odds_left) + implied_probability(odds_right) - 1.0

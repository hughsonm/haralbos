'''
Tools for calculating conditional probabilities across series of games
'''

SCHEDULE_NBA_SERIES_HOME_GAMES = [True, True, False, False, True, False, True,]
SCHEDULE_MLB_SERIES_HOME_GAMES_BEST_OF_FIVE = [True, True, False, False, True,]
SCHEDULE_MLB_SERIES_HOME_GAMES_BEST_OF_SEVEN = [
    True, True, False, False, False, True, True,]


def series_chance_string(game_chance_str, wins_remaining, losses_remaining):
    '''
    Like series_win_chance, but result expressed as a polynomial
    '''
    if wins_remaining == 0:
        return "1.0"
    if losses_remaining == 0:
        return "0.0"
    win_str = series_chance_string(game_chance_str, wins_remaining-1, losses_remaining)
    loss_str = series_chance_string(game_chance_str, wins_remaining, losses_remaining-1)
    return f'{game_chance_str} * ({win_str}) + (1-{game_chance_str}) * ({loss_str})'


def series_win_chance_home_away(win_chance_home, win_chance_away,wins_remaining,
                                losses_remaining, home_schedule):
    '''
    Similar to series_win_chance, but each game has a different win chance
    depending on home vs away
    
    :param win_chance_home: Win chance at home (probably the higher one)
    :param win_chance_away: Win chance on the road (probably the lower one)
    :param home_schedule: boolean list that says whether game i is a home game
    '''
    if losses_remaining == 0:
        return 0.0
    if wins_remaining == 0:
        return 1.0
    game_index = len(home_schedule) + 1 - (losses_remaining+wins_remaining)
    win_chance = win_chance_home if home_schedule[game_index] else win_chance_away
    series_chance_if_win = series_win_chance_home_away(
        win_chance_home, win_chance_away, wins_remaining-1, losses_remaining, home_schedule)
    series_chance_if_lose = series_win_chance_home_away(
        win_chance_home, win_chance_away, wins_remaining, losses_remaining-1, home_schedule)
    return win_chance * series_chance_if_win + (1-win_chance) * series_chance_if_lose


def series_win_chance(game_win_chance, wins_remaining, losses_remaining):
    '''
    Calculate probability of winning this series, if I need to win some number
    before losing some number
    
    :param game_chance_str: Probability of winning each game in the series
    :param wins_remaining: Number of game wins to get a series win
    :param losses_remaining: Number of game losses I can give up
    '''
    return series_win_chance_home_away(game_win_chance, game_win_chance,
                                       wins_remaining, losses_remaining,
                                       [True] * (wins_remaining+losses_remaining + 1))

# 0 Wins – 50 gems, 1 pack
# 1 Win – 150 gems, 1 pack
# 2 Wins – 800 gems, 1 pack
# 3 Wins –1,000 gems, 2 packs
# 4 Wins – 1,300 gems, 3 packs


def gem_payout(game_win_chance, wins_remaining, losses_remaining):
    '''
    Specialized calculation that applies to MTG Arena Premier Drafts.
    Includes knowledge of gem payouts for each track
    '''
    # Normal premier draft
    # payouts_by_remaining_wins = [2200, 1800, 1600, 1400, 1000, 250, 100, 50]
    # Plus gem-value of packs
    # payouts_by_remaining_wins = [2200+6*100, 1800, 1600+5*100, 1400+4*100,
    #                               1000+2*100, 250+2*100, 100+1*100, 50+1*100]
    # Pick-Two Draft
    # payouts_by_remaining_wins = [1300, 1000, 800, 150, 50]
    # plus gem-value of packs
    payouts_by_remaining_wins = [1300+3*100,
                                 1000+2*100, 800+100, 150+100, 50+100]
    if losses_remaining == 0:
        return payouts_by_remaining_wins[wins_remaining]
    if wins_remaining == 0:
        return payouts_by_remaining_wins[0]
    win_payout = gem_payout(game_win_chance, wins_remaining-1, losses_remaining)
    loss_payout = gem_payout(game_win_chance, wins_remaining, losses_remaining-1)
    return game_win_chance * win_payout + (1-game_win_chance) * loss_payout


def main():
    '''
    Script demonstrating some calculations
    '''
    wins_remaining = 4
    losses_remaining = 2
    required_payout = 900
    bracket = [0.0, 1.0]
    tolerance = 1/1500
    err = 2*tolerance
    while tolerance < err:
        midpoint = 0.5*(bracket[0] + bracket[1])
        midpoint_payout = gem_payout(
            midpoint, wins_remaining, losses_remaining)
        print(f'{midpoint:.5e} - {midpoint_payout:10.2f}')
        err = abs(midpoint_payout - required_payout) / required_payout
        if err < tolerance:
            break
        if midpoint_payout < required_payout:
            bracket[0] = midpoint
        else:
            bracket[1] = midpoint
    break_even_point = 0.5 * (bracket[0] + bracket[1])
    payout = gem_payout(break_even_point, wins_remaining, losses_remaining)
    print(f'With a win-rate of {break_even_point:.3f} you earn {payout} gems per draft')


if __name__ == '__main__':
    main()

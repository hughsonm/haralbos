SCHEDULE_NBA_SERIES_HOME_GAMES = [True, True, False, False, True, False, True,]
SCHEDULE_MLB_SERIES_HOME_GAMES_BEST_OF_FIVE = [True, True, False, False, True,]
SCHEDULE_MLB_SERIES_HOME_GAMES_BEST_OF_SEVEN = [
    True, True, False, False, False, True, True,]


def trophy_chance_string(game_chance_str, wins_remaining, losses_remaining):
    if wins_remaining == 0:
        return "1.0"
    if losses_remaining == 0:
        return "0.0"
    return f'{game_chance_str} * ({trophy_chance_string(game_chance_str, wins_remaining-1, losses_remaining)}) + (1-{game_chance_str}) * ({trophy_chance_string(game_chance_str, wins_remaining, losses_remaining-1)})'


def series_win_chance_home_away(win_chance_home, win_chance_away, wins_remaining, losses_remaining, home_schedule):
    if losses_remaining == 0:
        return 0.0
    if wins_remaining == 0:
        return 1.0
    game_index = len(home_schedule) + 1 - (losses_remaining+wins_remaining)
    win_chance = win_chance_home if home_schedule[game_index] else win_chance_away
    series_chance_if_win = series_win_chance_home_away(
        win_chance_home, win_chance_away, wins_remaining-1, losses_remaining)
    series_chance_if_lose = series_win_chance_home_away(
        win_chance_home, win_chance_away, wins_remaining, losses_remaining-1)
    return win_chance * series_chance_if_win + (1-win_chance) * series_chance_if_lose


def series_win_chance(game_win_chance, wins_remaining, losses_remaining):
    return series_win_chance_home_away(game_win_chance, game_win_chance, wins_remaining, losses_remaining, [True] * (wins_remaining+losses_remaining + 1))


def trophy_chance(game_chance, wins_remaining, losses_remaining):
    return series_win_chance(game_chance, wins_remaining, losses_remaining)

# 0 Wins – 50 gems, 1 pack
# 1 Win – 150 gems, 1 pack
# 2 Wins – 800 gems, 1 pack
# 3 Wins –1,000 gems, 2 packs
# 4 Wins – 1,300 gems, 3 packs


def gem_payout(cc, ww, ll):
    # Normal premier draft
    # payouts_by_remaining_wins = [2200, 1800, 1600, 1400, 1000, 250, 100, 50]
    # Plus gem-value of packs
    # payouts_by_remaining_wins = [2200+6*100, 1800, 1600+5*100, 1400+4*100, 1000+2*100, 250+2*100, 100+1*100, 50+1*100]
    # Pick-Two Draft
    # payouts_by_remaining_wins = [1300, 1000, 800, 150, 50]
    # plus gem-value of packs
    payouts_by_remaining_wins = [1300+3*100,
                                 1000+2*100, 800+100, 150+100, 50+100]
    if ll == 0:
        return payouts_by_remaining_wins[ww]
    if ww == 0:
        return payouts_by_remaining_wins[0]
    return cc * gem_payout(cc, ww-1, ll) + (1-cc) * gem_payout(cc, ww, ll-1)


def main():
    game_chance = 0.549
    wins_remaining = 4
    losses_remaining = 2
    required_payout = 900
    bracket = [0.0, 1.0]
    tolerance = 1/1500
    err = 2*tolerance
    while (tolerance < err):
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
    print(
        f'With a win-rate of {break_even_point:.3f} you earn {gem_payout(break_even_point, wins_remaining, losses_remaining)} gems per draft')
    pass


if __name__ == '__main__':
    main()

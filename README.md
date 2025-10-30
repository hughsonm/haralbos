# haralbos
Tools for probabilities

# Install

## Directly From Github

```bash
# Install via pip, as long as your Gitlab ssh key works
python -m pip install -U git+ssh://git@github.com/hughsonm/haralbos.git
```

## From PyPI

Not yet published.

# Examples

## MTG Arena Premier Draft Trophy Rate

How often should I expect to get 7 wins in a Premier Draft event, if expect to win 55 percent of my matches?

```python
import haralbos as hb

wins_for_a_trophy = 7
loss_count_for_failure = 3
my_win_chance_per_match = 0.55
my_trophy_rate = hb.series_win_chance_home_away(0.55, 0.55, 7, 3)

print(f'If you win {100*my_win_chance_per_match:.1f} percent of your matches, then you can expect to trophy {100*my_trophy_rate:.1f} percent of your Premier Drafts')
# => "If you win 55.0 percent of your matches, then you can expect to trophy 15.0 percent of your Premier Drafts"
```



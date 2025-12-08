def implied_probability(line):
    if line < 0:
        return line / (line - 100.)
    return 100. / (line + 100.)

def betting_line(probability):
    if probability < 0.5:
        return 100./probability - 100
    return 100. * probability / (probability - 1.0)
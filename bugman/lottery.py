from random import sample, choice


WEEK_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def pick_bugmans(devs, days):
    if len(devs) >= len(days):
        losers = sample(devs, len(days))
    elif len(devs) == 1:
        losers = devs * len(days)  # one dev, one bugman...
    else:  # make sure none has two days in a row of duty
        losers = []
        for _ in days:
            try:
                if losers:
                    last = losers[-1]
                    pick = choice([d for d in devs if d != last])
                else:
                    pick = choice(devs)
            except IndexError:
                pick = None
            losers.append(pick)

    return dict(zip(days, [l['username'] for l in losers]))


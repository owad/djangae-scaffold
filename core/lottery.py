from random import sample, choice


def pick_bugmans(usernames, days):
    if len(usernames) >= len(days):
        losers = sample(usernames, len(days))
    elif len(usernames) == 1:
        losers = usernames * len(days)  # one dev, one bugman...
    else:  # make sure none has two days in a row of duty
        if len(usernames) < days:
            usernames = (usernames*5)[:5]

        losers = []
        for _ in days:
            try:
                if losers:
                    last = losers[-1]
                    pick = choice([d for d in usernames if d != last])
                else:
                    pick = choice(usernames)
            except IndexError:
                pick = None
            losers.append(pick)
    return zip(days, [l for l in losers])


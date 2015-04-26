from random import sample, choice


def pick_bugmans(devs, days):
	if len(devs) >= len(days):
		return sample(devs, len(days))
	elif len(devs) == 1:
		return devs * len(days)  # one dev, one bugman...
	else:  # make sure none has two days in a row of duty
		res = []
		for _ in days:
			if res:
				last = res[-1]
				pick = choice([d for d in devs if d != last])
			else:
				pick = choice(devs)
			res.append(pick)
		return res

devs = []


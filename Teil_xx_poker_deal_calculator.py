from random import random


def trial(weights, payouts):
  scores = sorted((random() ** weight, i) for i, weight in enumerate(weights))
  results = [0] * len(payouts)
  for payout, score in zip(payouts, scores):
    results[score[1]] = payout
  return results


def sicm(preisgelder, stacks):
	avg = summe_chips / len(stacks)
	preisgelder += [0] * (len(stacks) - len(preisgelder))
	preisgelder = sorted(preisgelder)
	weights = [avg / s for s in stacks]
	return [sum(player) / SIMS for player in zip(*(trial(weights, preisgelder) for _ in range(SIMS)))]

SIMS = 100_000
stacks      = list(map(int,input('Stacks     : ').split(',')))
preisgelder = list(map(int,input('Preisgelder: ').split(',')))


summe_chips = sum(stacks)
gesamt_pot = sum(preisgelder)
garantiert = preisgelder[-1]
rest_pot = gesamt_pot - garantiert * len(stacks)

icm = sicm(preisgelder, stacks)

for s,p,i in zip(stacks, preisgelder, icm):
  auszahlung = rest_pot / summe_chips * s + garantiert
  print(f'Chip-Chop: {auszahlung:,.0f} ICM: {i:,.0f}, Preisgeld: {p:,.0f}')

 

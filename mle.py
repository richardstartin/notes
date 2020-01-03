import math
from random import seed, random

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)
seed(1)


def exp_rv(rate):
    return (-1.0 / rate) * math.log(random())


def generate(rate, count):
    return np.vectorize(lambda _: exp_rv(rate))(np.arange(count))


samples = generate(0.1, 100)
print(samples)
bincount = len(samples)
cdf = stats.cumfreq(samples, numbins=bincount)

x = cdf.lowerlimit + np.linspace(0, cdf.binsize * cdf.cumcount.size, cdf.cumcount.size)
fig, ax = plt.subplots()
ax.plot(x, np.divide(cdf.cumcount, bincount))
ax.set(xlabel='x', ylabel='P(X ≤ x)', title='Cumulative Distribution')
ax.set_xlim([x.min(), x.max()])
ax.set_ylim([0, 1.5])
ax.grid()
fig.savefig("cdf.png")


t = np.arange(0, 100, 0.01)
y1 = np.vectorize(lambda l: 1.0 - math.exp(-l * 0.05))(t)
y2 = np.vectorize(lambda l: 1.0 - math.exp(-l * 0.1))(t)
y3 = np.vectorize(lambda l: 1.0 - math.exp(-l * 0.15))(t)

fig1, ax2 = plt.subplots()
ax2.plot(x, np.divide(cdf.cumcount, bincount), label='raw data')
ax2.plot(t, y1, label='λ=0.05')
ax2.plot(t, y2, label='λ=0.1')
ax2.plot(t, y3, label='λ=0.15')
ax2.set(xlabel='x', ylabel='P(X ≤ x)',title='Cumulative Distribution With Guesses')
ax2.set_xlim([x.min(), x.max()])
ax2.set_ylim([0, 1.5])
ax2.grid()
ax2.legend()
fig1.savefig("cdf-with-guesses.png")

lambda_estimate = samples.size / np.sum(samples)
print("{:.4f}".format(lambda_estimate))


intensity = 0.1
for n in range(1, 7):
    size = pow(10, n)
    print(size / np.sum(generate(intensity, size)))
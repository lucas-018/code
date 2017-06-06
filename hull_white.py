from math import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys, os

def calcVar(V0, theta, n, mu, xi, a=None):
	dt = theta/n
	nu = np.random.normal(0, 1, n)
	V1 = [V0]
	V2 = [V0]
	change = (a != None)

	for i in range(1, n+1):
		if change:
			mu = a*(np.sqrt(V0) - np.sqrt(V1[i-1]))
		V1 += [V1[i-1]*np.exp((mu - xi*xi/2)*dt + nu[i-1]*xi*np.sqrt(dt))]
		if change:
			mu = a*(np.sqrt(V0) - np.sqrt(V2[i-1]))
		V2 += [V2[i-1]*np.exp((mu - xi*xi/2)*dt - nu[i-1]*xi*np.sqrt(dt))]
	return np.array(V1), np.array(V2)

def BlackScholes(S, K, sigma, theta, r):
	No = norm(0,1)
	d1 = (np.log(S/K) + (r + (sigma*sigma/2))*theta)/(sigma*np.sqrt(theta))
	d2 = d1 - sigma*np.sqrt(theta)
	return S*No.cdf(d1) - K*np.exp(-r*theta)*No.cdf(d2)


def HullWhite1(S, K, sigma0, theta, r, mu, xi, n, N, a=None):
	moy = 0
	for i in range(N):
		V1, V2 = calcVar(sigma0*sigma0, theta, n, mu, xi, a)
		sigma1 = np.sqrt(np.mean(V1))
		sigma2 = np.sqrt(np.mean(V2))
		p1 = BlackScholes(S, K, sigma1, theta, r)
		p2 = BlackScholes(S, K, sigma2, theta, r)
		y = (p1+p2)/2
		moy += y
	moy = moy/N
	return moy

def curbHW1(sigma0, theta, r, mu, xi, n, N, start=0.75, stop=1.25, step = 0.01, a=None):
	beta = start
	tab = []
	l = []
	num = (stop-start)/step
	p_old = 0
	p_new = 0
	while beta < stop:
		tab += [HullWhite1(beta, 1, sigma0, theta, r, mu, xi, n, N, a)]
		l += [BlackScholes(beta, 1, sigma0, theta, r)]
		beta += step
		p_new = int((beta-start)*100/(stop-start))
		if p_new > p_old:
			p_old = p_new
			if p_new in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
				print(p_new, end='')
				sys.stdout.flush()
			else:
				print('#', end='')
				sys.stdout.flush()
	print('\n')
	prop = np.linspace(start, stop, len(tab))
	plt.figure()
	plt.plot(prop, tab, label = "Hull-White")
	plt.plot(prop, l, label = "Black-Scholes")
	plt.legend()
	plt.show()
	bias = 100*(np.array(tab)-np.array(l))/(np.array(l)+1e-10)
	plt.figure()
	plt.plot(prop, bias)
	plt.show()
	return prop, tab, l, bias





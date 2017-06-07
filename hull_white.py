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


def HullWhite1(S, K, sigma0, theta, r, mu, xi, n, N, a=None, rho=None):
	moy = 0
	sigma = 0
	for i in range(N):
		if rho==None:
			V1, V2 = calcVar(sigma0*sigma0, theta, n, mu, xi, a)
			sigma1 = np.sqrt(np.mean(V1))
			sigma2 = np.sqrt(np.mean(V2))
			p1 = BlackScholes(S, K, sigma1, theta, r)
			p2 = BlackScholes(S, K, sigma2, theta, r)
			y = (p1+p2)/2
			moy += y
		else:
			res = calcVarPrice(sigma0*sigma0, S, K, theta, n, r, mu, xi, rho, a)
			moy += res[0]
			sigma += res[1]
	moy = moy/N
	sigma = sigma/N
	return moy, sigma

def curbHW1(sigma0, theta, r, mu, xi, n, N, start=0.75, stop=1.25, step = 0.01, a=None, rho=0):
	beta = start
	tab = []
	l = []
	sig = []
	num = (stop-start)/step
	p_old = 0
	p_new = 0
	while beta < stop:
		res = HullWhite1(beta, 1, sigma0, theta, r, mu, xi, n, N, a, rho)
		tab += [res[0]]
		sig += [res[1]]
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
	plt.figure()
	plt.plot(prop, sig)
	plt.grid()
	plt.show()
	return prop, tab, l, bias, sig




def calcVarPrice(V0, S0, K, theta, n, r, mu, xi, rho, a=None, final = False):
	S1 = [S0]
	S2 = [S0]
	S3 = [S0]
	S4 = [S0]
	V1 = [V0]
	V2 = [V0]
	V3 = [V0]
	V4 = [V0]
	dt = theta/n
	nu = np.random.normal(0, 1, n)
	u = np.random.normal(0, 1, n)
	for i in range(1, n+1):
		S1 += [S1[i-1]*np.exp((r-V1[i-1]/2)*dt + u[i-1]*np.sqrt(V1[i-1]*dt))]
		V1 += [V1[i-1]*np.exp((mu - xi*xi/2)*dt + rho*u[i-1]*xi*np.sqrt(dt) + np.sqrt(1 - rho*rho)*nu[i-1]*xi*np.sqrt(dt))]
		S2 += [S2[i-1]*np.exp((r-V2[i-1]/2)*dt - u[i-1]*np.sqrt(V2[i-1]*dt))]
		V2 += [V2[i-1]*np.exp((mu - xi*xi/2)*dt - rho*u[i-1]*xi*np.sqrt(dt) + np.sqrt(1 - rho*rho)*nu[i-1]*xi*np.sqrt(dt))]
		S3 += [S3[i-1]*np.exp((r-V3[i-1]/2)*dt + u[i-1]*np.sqrt(V3[i-1]*dt))]
		V3 += [V3[i-1]*np.exp((mu - xi*xi/2)*dt + rho*u[i-1]*xi*np.sqrt(dt) - np.sqrt(1 - rho*rho)*nu[i-1]*xi*np.sqrt(dt))]
		S4 += [S4[i-1]*np.exp((r-V4[i-1]/2)*dt - u[i-1]*np.sqrt(V4[i-1]*dt))]
		V4 += [V4[i-1]*np.exp((mu - xi*xi/2)*dt - rho*u[i-1]*xi*np.sqrt(dt) - np.sqrt(1 - rho*rho)*nu[i-1]*xi*np.sqrt(dt))]
	S1 = np.array(S1)
	S2 = np.array(S2)
	S3 = np.array(S3)
	S4 = np.array(S4)
	V1 = np.array(V1)
	V2 = np.array(V2)
	V3 = np.array(V3)
	V4 = np.array(V4)
	p1 = np.exp(-r*theta)*max(S1[n]-K, 0)
	p2 = np.exp(-r*theta)*max(S2[n]-K, 0)
	p3 = np.exp(-r*theta)*max(S3[n]-K, 0)
	p4 = np.exp(-r*theta)*max(S4[n]-K, 0)
	if final:
		sigma1 = V1[n]
		sigma2 = V2[n]
		sigma3 = V3[n]
		sigma4 = V4[n]
		return  (S1[n]+S2[n]+S3[n]+S4[n])/4, (sigma1+sigma2+sigma3+sigma4)/4	
	sigma1 = np.mean(np.sqrt(V1))	
	sigma2 = np.mean(np.sqrt(V2))
	sigma3 = np.mean(np.sqrt(V3))
	sigma4 = np.mean(np.sqrt(V4))
	return (p1+p2+p3+p4)/4, (sigma1+sigma2+sigma3+sigma4)/4


def smile(V0, S0, theta, n, N, r, mu, xi, rho, a=None, num=100, M = None):
	S = []
	V = []
	tab = np.zeros(num) + 1e-10
	E = np.zeros(num)
	p_old = 0
	p_new = 0
	for i in range(N):
		res = calcVarPrice(V0, S0, 1, theta, n, r, mu, xi, rho, a, True)
		S += [res[0]]
		V += [res[1]]
		p_new = int(i*100/N)
		if p_new > p_old:
			p_old = p_new
			if p_new in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
				print(p_new, end='')
				sys.stdout.flush()
			else:
				print('#', end='')
				sys.stdout.flush()
	print('\n')
	S = np.array(S)
	V = np.array(V)
	smin = min(S)
	smax = max(S)
	if M != None:
		smax = min(smax, M)
	stab = np.linspace(smin, smax, num)
	for i in range(N):
		ind = int((S[i]-smin)*(num-1)/(smax-smin))
		if S[i] <= smax:
			tab[ind] += 1
			E[ind] += V[i]
	E = E/tab
	return stab, np.sqrt(E)

  





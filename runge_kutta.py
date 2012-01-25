# -*- coding: utf8 -*-

from math import sqrt

def integrateur_trivial(boules, h):
	eval_accelerations(boules)
	for i in xrange(0, len(boules)):
		boules[i].x += boules[i].dx * h
		boules[i].y += boules[i].dy * h
		boules[i].z += boules[i].dz * h
		boules[i].dx += boules[i].ax  * h
		boules[i].dy += boules[i].ay  * h
		boules[i].dz += boules[i].az * h

def add_vector(x1,x2):
	y = range(len(x1))
	for i in xrange(0, len(x1)):
		y[i] = x1[i] + x2[i]
	return y

def mult_scalar(a,x):
	y = range(len(x))
	for i in xrange(0, len(x)):
		y[i] = a * x[i]
	return y

def runge_kutta(f, x, h):
	k1 = f(x)
	k2 = f(add_vector(x, mult_scalar(h / 2., k1)))
	k3 = f(add_vector(x, mult_scalar(h / 2., k2)))
	k4 = f(add_vector(x, mult_scalar(h , k3)))
	return mult_scalar(1./6., add_vector(add_vector(k1,k4),mult_scalar(2.,add_vector(k2,k3))))

def move(boules, h):
	integrateur_trivial(boules, h)
		
def eval_accelerations(boules):
	for i in xrange(0, len(boules)):
		# Forces de répulsions
		for j in xrange(0, i):
			d2 = (boules[i].x - boules[j].x)**2 + (boules[i].y - boules[j].y)**2 + (boules[i].z - boules[j].z)**2
			if d2 == 0.:
				d2 = 1.
			norme = sqrt(d2)
			ux = (boules[i].x - boules[j].x) / norme
			uy = (boules[i].y - boules[j].y) / norme
			uz = (boules[i].z - boules[j].z) / norme
			
			boules[i].ax -= boules[i].m * boules[j].m / d2 * ux
			boules[i].ay -= boules[i].m * boules[j].m / d2 * uy
			boules[i].az -= boules[i].m * boules[j].m / d2 * uz
			boules[j].ax += boules[i].m * boules[j].m / d2 * ux
			boules[j].ay += boules[i].m * boules[j].m / d2 * uy
			boules[j].az += boules[i].m * boules[j].m / d2 * uz
			
		# Forces de ressorts 
		for p in xrange(0, len(boules[i].links)):
			boule = boules[i].links[p][0]
			l0 = boules[i].links[p][1]
			k = boules[i].links[p][2]
			
			norme = sqrt((boules[i].x - boule.x)**2 + (boules[i].y - boule.y)**2 + (boules[i].z - boule.z)**2)
			if norme == 0.:
				norme = 1
			ux = (boules[i].x - boule.x) / norme
			uy = (boules[i].y - boule.y) / norme
			uz = (boules[i].z - boule.z) / norme
			
			boules[i].ax += k * (norme - l0) * ux
			boules[i].ay += k * (norme - l0) * uy
			boules[i].az += k * (norme - l0) * uz
			boule.ax -= k * (norme - l0) * ux
			boule.ay -= k * (norme - l0) * uy
			boule.az -= k * (norme - l0) * uz

# -*- coding: utf8 -*-

from math import sqrt
from boule import K_FROTTEMENT_FLUIDE

def integrateur_trivial(boules, h):
    eval_accelerations(boules)
    for boule in boules:
        boule.x += boule.dx * h
        boule.y += boule.dy * h
        boule.z += boule.dz * h
        boule.dx += boule.ax * h
        boule.dy += boule.ay * h
        boule.dz += boule.az * h
        boule.ax = boule.ay = boule.az = 0


def add_vector(x1, x2):
    y = range(len(x1))
    for i in xrange(0, len(x1)):
        y[i] = x1[i] + x2[i]
    return y


def mult_scalar(a, x):
    y = range(len(x))
    for i in xrange(0, len(x)):
        y[i] = a * x[i]
    return y


def runge_kutta(f, x, h):
    k1 = f(x)
    k2 = f(add_vector(x, mult_scalar(h / 2., k1)))
    k3 = f(add_vector(x, mult_scalar(h / 2., k2)))
    k4 = f(add_vector(x, mult_scalar(h, k3)))
    return mult_scalar(1. / 6., add_vector(add_vector(k1, k4), mult_scalar(2., add_vector(k2, k3))))


def move(boules, h):
    integrateur_trivial(boules, h)


def eval_accelerations(boules):
    for i, boule in enumerate(boules):
        # Forces de répulsions
        for j in xrange(0, i):
            other = boules[j]
            d2 = (boule.x - other.x) ** 2 + (boule.y - other.y) ** 2 + (boule.z - other.z) ** 2

            norme = sqrt(d2)
            ux = (boule.x - other.x) / norme
            uy = (boule.y - other.y) / norme
            uz = (boule.z - other.z) / norme

            d2 = max(d2, 0.1)

            boule.ax -= other.m / d2 * ux
            boule.ay -= other.m / d2 * uy
            boule.az -= other.m / d2 * uz
            other.ax += boule.m / d2 * ux
            other.ay += boule.m / d2 * uy
            other.az += boule.m / d2 * uz

        # Forces de ressorts
        for other, l0, k in boule.links:
            norme = sqrt((boule.x - other.x) ** 2 + (boule.y - other.y) ** 2 + (boule.z - other.z) ** 2)
            if norme < 10e-4:
                continue

            ux = (boule.x - other.x) / norme
            uy = (boule.y - other.y) / norme
            uz = (boule.z - other.z) / norme


            boule.ax -= k * (norme - l0) * ux / boule.m
            boule.ay -= k * (norme - l0) * uy / boule.m
            boule.az -= k * (norme - l0) * uz / boule.m


        # Forces de frottement
        boule.ax -= K_FROTTEMENT_FLUIDE * (boule.dx) / boule.m
        boule.ay -= K_FROTTEMENT_FLUIDE * (boule.dy) / boule.m
        boule.az -= K_FROTTEMENT_FLUIDE * (boule.dz) / boule.m

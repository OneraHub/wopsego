#!/usr/bin/env python
# coding: utf-8

import numpy as np
from wopsego import Optimization, ValidOptimumNotFoundError

# Objective
def G24(point):
    """
    Function G24
    1 global optimum y_opt = -5.5080 at x_opt =(2.3295, 3.1785)
    """
    p = np.atleast_2d(point)
    return -p[:, 0] - p[:, 1]


# Constraints < 0
def G24_c1(point):
    p = np.atleast_2d(point)
    return (
        -2.0 * p[:, 0] ** 4.0
        + 8.0 * p[:, 0] ** 3.0
        - 8.0 * p[:, 0] ** 2.0
        + p[:, 1]
        - 2.0
    )


def G24_c2(point):
    p = np.atleast_2d(point)
    return (
        -4.0 * p[:, 0] ** 4.0
        + 32.0 * p[:, 0] ** 3.0
        - 88.0 * p[:, 0] ** 2.0
        + 96.0 * p[:, 0]
        + p[:, 1]
        - 36.0
    )


# Grouped evaluation
def f_grouped(point):
    p = np.atleast_2d(point)
    return np.array([G24(p), G24_c1(p), G24_c2(p)]).T


xlimits = [[0, 3], [0, 4]]
cstr_specs = 2 * [{"type": "<", "bound": 0.0}]
optim = Optimization(xlimits, cstr_specs)

# from smt.sampling_methods import LHS
# lhs = LHS(xlimits=np.array(xlimits), criterion='ese', random_state=42)
# xdoe = lhs(5)
# ydoe = f_grouped(xdoe)
# print("Initial DOE")
# print("xdoe={}".format(xdoe))
# print("ydoe={}".format(ydoe))

xdoe = [
    [1.29361118, 3.76645806],
    [0.22472407, 3.09294092],
    [1.83485017, 0.76057145],
    [1.03919637, 1.72479562],
    [2.76066901, 1.27892679],
]
ydoe = [
    [-5.06006925, 0.0964247, 2.76239458][-3.31766499, 0.77462312, -15.4246689][
        -2.59542161, -1.4230771, -3.0242084
    ][-2.76399198, -2.26906368, 1.70116801][-4.03959579, -9.54069818, 0.5686734]
]

optim.tell_doe(xdoe, ydoe)
optim.run(f_grouped, n_iter=20)

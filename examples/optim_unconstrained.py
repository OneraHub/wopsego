#!/usr/bin/env python
# coding: utf-8
#

import numpy as np
from wopsego import Optimization, ValidOptimumNotFoundError

# Objective
def f_obj(x):
    """
    Function Six-Hump Camel Back
    2 global optimum y_opt =-1.0316 located at x_opt = (0.089842, -0.712656) or (-0.089842, 0.712656)
    https://www.sfu.ca/~ssurjano/camel6.html
    """
    x_ = np.atleast_2d(x)
    x1 = np.array(x_)[:, 0]
    x2 = np.array(x_)[:, 1]
    val = (
        4 * x1 ** 2
        - 2.1 * x1 ** 4
        + 1.0 / 3.0 * x1 ** 6
        + x1 * x2
        - 4 * x2 ** 2
        + 4 * x2 ** 4
    )
    return np.atleast_2d(val).T


xlimits = [[-3, 3], [-2, 2]]
optim = Optimization(xlimits)

xdoe = np.array(
    [
        [-0.91502224, 1.89017506],
        [2.57253436, 0.83786997],
        [-2.32304511, -1.12821447],
        [1.65152355, -1.63067708],
        [0.0057155, -0.31036381],
    ]
)
ydoe = f_obj(xdoe)
print("Initial DOE")
print("xdoe={}".format(xdoe))
print("ydoe={}".format(ydoe))

optim.tell_doe(xdoe, ydoe)

# We loop using the iteration budget
# Note: this loop is provided in as the run method of the optim object. See below.
n_iter = 15
for i in range(n_iter):
    x_suggested, status = optim.ask()
    print(
        "{} x suggested = {} with status: {}".format(
            i, x_suggested, Optimization.STATUSES[status]
        )
    )

    # compute objective function at the suggested point
    new_y = f_obj(np.atleast_2d(x_suggested))
    print("new y = {}".format(new_y))

    optim.tell(x_suggested, new_y)
    if optim.is_solution_reached():
        print("Solution is reached")
        break

    try:
        _, y = optim.get_result()
        print("y_opt_tmp = {}".format(y))
        print("")
    except ValidOptimumNotFoundError:  # in case no point in doe respect constraints yet
        pass


x_opt, y_opt = optim.get_result()
print("Found minimum y_opt = {} at x_opt = {}".format(y_opt, x_opt))
print(optim.get_result())
print(optim.get_history())


# For convenience, the previous optimization loop is available as the 'run' method of
# the optimization object.

# to reset the initial DOE, otherwise optimization will go on from previous state
# optim.tell_doe(xdoe, ydoe)

# run the optimization loop again
# optim.run(f_obj, 15)

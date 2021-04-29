import unittest
from wopsego import WhatsOpt, Optimization, ValidOptimumNotFoundError

import numpy as np

# Unconstrained Problem
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


# Constrained Problem

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


class TestWopsego:
    def test_check_login(self):
        wop = WhatsOpt()
        wop.check_login()

    @staticmethod
    def optim_unconstrained_pb_setup():
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
        return optim, xdoe, ydoe

    def test_whitebox_optim_unconstrained(self):
        optim, xdoe, ydoe = TestWopsego.optim_unconstrained_pb_setup()

        optim.tell_doe(xdoe, ydoe)

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

    def test_blackbox_optim_unconstrained(self):
        optim, xdoe, ydoe = TestWopsego.optim_unconstrained_pb_setup()

        optim.tell_doe(xdoe, ydoe)
        optim.run(f_obj, 15)
        optim.get_history()
        print(optim.get_result())

    def test_optim_constrained(self):
        xlimits = [[0, 3], [0, 4]]
        cstr_specs = 2 * [{"type": "<", "bound": 0.0}]

        optim = Optimization(xlimits, cstr_specs)

        # Initial DOE
        xdoe = [
            [1.29361118, 3.76645806],
            [0.22472407, 3.09294092],
            [1.83485017, 0.76057145],
            [1.03919637, 1.72479562],
            [2.76066901, 1.27892679],
        ]
        ydoe = [
            [-5.06006925, 0.0964247, 2.76239458],
            [-3.31766499, 0.77462312, -15.4246689],
            [-2.59542161, -1.4230771, -3.0242084],
            [-2.76399198, -2.26906368, 1.70116801],
            [-4.03959579, -9.54069818, 0.5686734],
        ]
        optim.tell_doe(xdoe, ydoe)
        optim.run(f_grouped, n_iter=20)
        optim.get_history()
        print(optim.get_result())
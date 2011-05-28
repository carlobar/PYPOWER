# Copyright (C) 2010-2011 Power System Engineering Research Center (PSERC)
# Copyright (C) 2010-2011 Richard Lincoln <r.w.lincoln@gmail.com>
#
# PYPOWER is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# PYPOWER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY], without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PYPOWER. If not, see <http://www.gnu.org/licenses/>.

from numpy import array

from pypower.totcost import totcost

from pypower.t.t_begin import t_begin
from pypower.t.t_is import t_is
from pypower.t.t_end import t_end

def t_totcost(quiet=False):
    """Tests for code in C{totcost}.

    @see: U{http://www.pserc.cornell.edu/matpower/}
    """
    n_tests = 22

    t_begin(n_tests, quiet)

    ## generator cost data
    #    1    startup    shutdown    n    x1    y1    ...    xn    yn
    #    2    startup    shutdown    n    c(n-1)    ...    c0
    gencost = array([
        [2, 0, 0, 3,   0.01,   0.1,    1,     0,    0,     0,  0,    0],
        [2, 0, 0, 5,   0.0006, 0.005,  0.04,  0.3,  2,     0,  0,    0],
        [1, 0, 0, 4,   0,      0,     10,   200,   20,   600, 30, 1200],
        [1, 0, 0, 4, -30,  -2400,    -20, -1800,  -10, -1000,  0,    0]
    ])

    t = 'totcost - quadratic',
    t_is(totcost(gencost, [0, 0, 0, 0]), [1, 2, 0, 0], 8, t)
    t_is(totcost(gencost, [1, 0, 0, 0]), [1.11, 2, 0, 0], 8, t)
    t_is(totcost(gencost, [2, 0, 0, 0]), [1.24, 2, 0, 0], 8, t)

    t = 'totcost - 4th order polynomial',
    t_is(totcost(gencost, [0, 0, 0, 0]), [1, 2,      0, 0], 8, t)
    t_is(totcost(gencost, [0, 1, 0, 0]), [1, 2.3456, 0, 0], 8, t)
    t_is(totcost(gencost, [0, 2, 0, 0]), [1, 2.8096, 0, 0], 8, t)

    t = 'totcost - pwl (gen)',
    t_is(totcost(gencost, [0, 0, -10, 0 ]), [1, 2, -200, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 5, 0 ]),   [1, 2, 100, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 10, 0]),   [1, 2, 200, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 15, 0]),   [1, 2, 400, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 20, 0]),   [1, 2, 600, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 25, 0]),   [1, 2, 900, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 30, 0]),   [1, 2, 1200, 0], 8, t)
    t_is(totcost(gencost, [0, 0, 35, 0]),   [1, 2, 1500, 0], 8, t)

    t = 'totcost - pwl (load)',
    t_is(totcost(gencost, [0, 0, 0, 10 ]), [1, 2, 0, 1000], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -5 ]), [1, 2, 0, -500], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -10]), [1, 2, 0, -1000], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -15]), [1, 2, 0, -1400], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -20]), [1, 2, 0, -1800], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -25]), [1, 2, 0, -2100], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -30]), [1, 2, 0, -2400], 8, t)
    t_is(totcost(gencost, [0, 0, 0, -35]), [1, 2, 0, -2700], 8, t)

    t_end

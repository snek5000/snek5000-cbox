"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/fsnet/project/meige/2020/20CONVECTION/numerical/"

"""

import numpy as np

from snek5000_cbox.solver import Simul

params = Simul.create_default_params()

aspect_ratio = 1.0
params.prandtl = 0.71

params.rayleigh = 2.0e08

params.output.sub_directory = "examples_cbox/simple"

params.oper.dim = 2

params.oper.delta_T_lateral = 1.0
params.oper.delta_T_vertical = 1.0

nb_elements = nx = ny = 12
params.oper.nx = nb_elements
params.oper.ny = int(nb_elements * aspect_ratio)
params.oper.nz = int(nb_elements * aspect_ratio)

Lx = params.oper.Lx = 1.0
Ly = params.oper.Ly = Lx * aspect_ratio
Lz = params.oper.Lz = Lx * aspect_ratio


order = params.oper.elem.order = params.oper.elem.order_out = 10

params.oper.mesh_stretch_factor = 0.0  # zero means regular

params.short_name_type_run = f"Ra{params.rayleigh:.3e}_{nx*order}x{ny*order}"

# creation of the coordinates of the points saved by history points
n1d = 5
small = Lx / 10

xs = np.linspace(0, Lx, n1d)
xs[0] = small
xs[-1] = Lx - small

ys = np.linspace(0, Ly, n1d)
ys[0] = small
ys[-1] = Ly - small

coords = [(x, y) for x in xs for y in ys]

if params.oper.dim == 3:

    zs = np.linspace(0, Lz, n1d)
    zs[0] = small
    zs[-1] = Lz - small

    coords = [(x, y, z) for x in xs for y in ys for z in zs]


params.output.history_points.coords = coords
params.oper.max.hist = len(coords) + 1

params.nek.general.end_time = 600
params.nek.general.stop_at = "endTime"

params.nek.general.write_control = "runTime"
params.nek.general.write_interval = 10.0

params.nek.general.variable_dt = True
params.nek.general.target_cfl = 2.0
params.nek.general.time_stepper = "BDF3"
params.nek.general.extrapolation = "OIFS"

params.output.history_points.write_interval = 10

sim = Simul(params)

sim.make.exec("run_fg", resources={"nproc": 4})
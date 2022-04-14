from shutil import rmtree

import pytest

import numpy as np

from snek5000_cbox.solver import Simul
from snek5000 import load


@pytest.mark.slow
def test_simple_simul():

    params = Simul.create_default_params()

    aspect_ratio = params.oper.aspect_ratio = 1.0
    params.prandtl = 0.71

    # for aspect ratio 1, Ra_c = 1.825E08
    params.Ra_side = 1.83e08

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 8
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)
    params.oper.nz = int(nb_elements / aspect_ratio)

    Ly = params.oper.Ly
    Lx = params.oper.Lx = Ly / aspect_ratio

    params.oper.mesh_stretch_factor = 0.1

    params.oper.elem.order = params.oper.elem.order_out = 7

    # creation of the coordinates of the points saved by history points
    n1d = 4
    small = Lx / 10

    xs = np.linspace(0, Lx, n1d)
    xs[0] = small
    xs[-1] = Lx - small

    ys = np.linspace(0, Ly, n1d)
    ys[0] = small
    ys[-1] = Ly - small

    coords = [(x, y) for x in xs for y in ys]

    params.output.history_points.coords = coords
    params.oper.max.hist = len(coords) + 1

    num_steps = params.nek.general.num_steps = 6000
    params.nek.general.write_interval = 500

    params.nek.general.variable_dt = False
    # Negative dt means fixed dt
    dt = params.nek.general.dt = 0.03
    params.nek.general.time_stepper = "BDF2"
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 500
    params.output.history_points.write_interval = 10

    sim = Simul(params)

    sim.make.exec("run_fg", resources={"nproc": 4})

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    assert coords.ndim == 2 and coords.shape == (n1d ** 2, 2)

    times = df[df.index_points == 0].time
    t_max = times.max()

    assert t_max == num_steps * dt
    assert len(times) == num_steps / params.output.history_points.write_interval + 1

    # check a physical result: since there is no probe close to the center,
    # the temperature values at the end are > 0.1 and < 0.4
    temperature_last = df[df.time == t_max].temperature
    assert temperature_last.abs().max() < 0.4
    assert temperature_last.abs().min() > 0.1

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)

import numpy as np
from pathlib import Path

from fluiddyn.clusters.legi import Calcul8 as Cluster
from snek5000 import load


prandtl = 7.0
aspect = 1.0
dim = 2

dir_sim = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/NL_sim/Pr_{prandtl:.2f}/asp_{aspect:.3f}"
path = Path(dir_sim)
sim_dirs = sorted(path.glob("cbox_*"))

walltime = "23:59:00"

sim = load(sim_dirs[0])

prandtl = sim.params.prandtl

aspect_ratio = sim.params.oper.aspect_ratio
restart_file = sorted(sim.output.path_session.glob("cbox0.f*"))[-1]
nx = sim.params.oper.nx
Ra_numbs = [2 * sim.params.Ra_side]

order = 10
stretch_factor = 0.0

end_time = 3000
dt = 0.05
nb_procs = 10

y_periodicity = False
z_periodicity = False

enable_sfd = False

cluster = Cluster()

cluster.commands_setting_env = [
    "PROJET_DIR=/fsnet/project/meige/2020/20CONVECTION",
    "source /etc/profile",
    "source $PROJET_DIR/miniconda3/etc/profile.d/conda.sh",
    "conda activate env-snek",
    "export NEK_SOURCE_ROOT=$HOME/Dev/snek5000/lib/Nek5000",
    "export PATH=$PATH:$NEK_SOURCE_ROOT/bin",
    "export FLUIDSIM_PATH=$PROJET_DIR/numerical/",
]


ny = int(nx * aspect_ratio)
if nx * aspect_ratio - ny:
    raise ValueError

for Ra_side_num in Ra_numbs:

    command = (
        f"run_simul.py -Pr {prandtl} -nx {nx} --dim {dim} "
        f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_procs} "
        f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
        f"--Ra-side {Ra_side_num} --restart-file {restart_file}"
    )

    if y_periodicity:
        command += " --y-periodicity"
    elif z_periodicity:
        command += " --z-periodicity"
    elif enable_sfd:
        command += " --enable-sfd"

    print(command)

    name_run = f"RSW_asp{aspect_ratio:.2f}_Ra{Ra_side_num:.2e}_Pr{prandtl:.1f}_msh{nx*order}x{round(nx*aspect_ratio)*order}"

    cluster.submit_script(
        command,
        name_run=name_run,
        walltime=walltime,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )

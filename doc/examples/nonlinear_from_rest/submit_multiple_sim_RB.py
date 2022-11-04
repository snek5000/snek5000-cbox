import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster


dim = 2

if dim == 3:
    aspect_ratio_z = 4.0

aspect_ratio_y = 1.0

prandtl = 4.38
Ra_numbs = [1e9]

nx = 32
order = 10
stretch_factor = 0.0

end_time = 3000
dt = 0.05

nb_procs = 10
nb_nodes = 1
walltime = "24:00:00"

x_periodicity = False
z_periodicity = False

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


ny = int(nx * aspect_ratio_y)
if nx * aspect_ratio_y - ny:
    raise ValueError
if dim == 3:
    nz = int(ny / aspect_ratio_z)
    if ny / aspect_ratio_z - nz:
        raise ValueError

for Ra_vert_num in Ra_numbs:

    command = (
        f"run_simul.py -Pr {prandtl} -nx {nx} --dim {dim} "
        f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_nodes*nb_procs} "
        f"-a_y {aspect_ratio_y} --stretch-factor {stretch_factor} "
        f"--Ra-vert {Ra_vert_num}"
    )

    if dim == 3:
        command += f" -a_z {aspect_ratio_z}"
    if x_periodicity:
        command += " --x-periodicity"
    if z_periodicity:
        command += " --z-periodicity"

    print(command)

    name_run = (
        f"RB_asp{aspect_ratio_y:.3f}_Ra{Ra_vert_num:.3e}_Pr{prandtl:.2f}"
        f"_msh{nx*order}x{round(nx*aspect_ratio_y)*order}"
    )

    if dim == 3:
        name_run = (
            f"RB_Ay{aspect_ratio_y:.3f}_Az{aspect_ratio_z:.3f}_Ra{Ra_vert_num:.3e}"
            f"_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio_y)*order}"
            f"x{round(ny/aspect_ratio_z)*order}"
        )

    cluster.submit_script(
        command,
        name_run=name_run,
        walltime=walltime,
        nb_nodes=nb_nodes,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )

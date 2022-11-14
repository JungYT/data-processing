import argparse
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(
    description="Enter the file name of the data with file format"
)
parser.add_argument(
    "--data",
    metavar="file_name",
    help="file name of the date to process with file format",
)
parser.add_argument(
    "--copy",
    metavar="copy",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="whether or not to copy the data file to the directory where the figures is saved",
)
parser.add_argument(
    "--save",
    metavar="save_figures",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="whether or not to save the figures",
)
args = parser.parse_args()

df = pd.read_csv(args.data, header=0, index_col=0)

time_mus = df["timestamp_sample"].to_numpy()
time = (time_mus - time_mus[0]) / 1e6
x = df["x"].to_numpy()
y = df["y"].to_numpy()
z = df["z"].to_numpy()
vx = df["vx"].to_numpy()
vy = df["vy"].to_numpy()
vz = df["vz"].to_numpy()
ax = df["ax"].to_numpy()
ay = df["ay"].to_numpy()
az = df["az"].to_numpy()


Path("results", args.data).mkdir(parents=True, exist_ok=True)
path_saved = Path("results", args.data)
if args.copy:
    shutil.copy2("./" + args.data, path_saved)

tex_fonts = {
    "text.usetex": True,
    "font.family": "Times New Roman",
    "axes.grid": True,
}
plt.rcParams.update(tex_fonts)
true_style = "solid"
ref_style = "dashed"
cmd_style = "dotted"
true_color = "r"
ref_color = "b"
cmd_color = "k"

fig, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d"})
ax.plot(
    x,
    y,
    z,
    label="true",
    color=true_color,
    linestyle=true_style,
)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Trajectory")
plt.legend()
if args.save:
    fig.savefig(Path(path_saved, "trajectory.png"), bbox_inches="tight")
plt.close("all")


# Velocity
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, vx, color=true_color, linestyle=true_style, label="true")
# ax[0].plot(t, vel_ref[:, 0], color=ref_color, linestyle=ref_style, label="ref.")
ax[0].set_ylabel(r"$V_x$ (m/s)")
ax[0].axes.xaxis.set_ticklabels([])
ax[1].plot(time, vy, color=true_color, linestyle=true_style)
# ax[1].plot(t, vel_ref[:, 1], color=ref_color, linestyle=ref_style)
ax[1].set_ylabel(r"$V_y$ (m/s)")
ax[1].axes.xaxis.set_ticklabels([])
ax[2].plot(time, vz, color=true_color, linestyle=true_style)
# ax[2].plot(t, vel_ref[:, 2], color=ref_color, linestyle=ref_style)
ax[2].set_ylabel(r"$V_z$ (m/s)")
ax[0].legend()
fig.suptitle("Velocity")
fig.supxlabel("Time (s)")
fig.align_ylabels(ax)
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "velocity.png"), bbox_inches="tight")
plt.close("all")

breakpoint()

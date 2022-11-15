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
    "-d",
    metavar="file_name",
    help="file name of the date to process with file format",
)
parser.add_argument(
    "--copy",
    metavar="bool_copy_data",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="whether or not to copy the data file to the directory where the figures is saved",
)
parser.add_argument(
    "--save",
    metavar="bool_save_figures",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="whether or not to save the figures",
)
parser.add_argument(
    "--latex",
    metavar="latex",
    default=False,
    action=argparse.BooleanOptionalAction,
    help="whether or not to use latex font in the figure label and title",
)
args = parser.parse_args()

df = pd.read_csv(args.d, header=0, index_col=0)

time_mus = df["timestamp_sample"].to_numpy() # Time since system start (microseconds)
time = (time_mus - time_mus[0]) / 1e6 # Time since data is logged (seconds) 
x = df["x"].to_numpy() # North position in NED earth-fixed frame (meter)
y = df["y"].to_numpy() # East position in NED earth-fixed frame (meter)
z = df["z"].to_numpy() # Down position in NED earth-fixed frame (meter)
vx = df["vx"].to_numpy() # North position in NED earth-fixed frame (meter/sec)
vy = df["vy"].to_numpy() # East position in NED earth-fixed frame (meter/sec)
vz = df["vz"].to_numpy() # Down position in NED earth-fixed frame (meter/sec)
ax = df["ax"].to_numpy() # North position in NED earth-fixed frame (meter/sec^2)
ay = df["ay"].to_numpy() # East position in NED earth-fixed frame (meter/sec^2)
az = df["az"].to_numpy() # Down position in NED earth-fixed frame (meter/sec^2)
heading = df["heading"].to_numpy() # Euler yaw angle transforming the tarngent plane relative to NED earth-fixed frame, [-PI ~ PI] (radians)
std_pos_horizontal = df['eph'].to_numpy() # Standard devitation of horizontal position error (meter)
std_pos_vertical = df['epv'].to_numpy() # Standard devitation of vertical position error (meter)
std_vel_horizontal = df['evh'].to_numpy() # Standard devitation of horizontal velocity error (meter/sec)
std_vel_vertical = df['evv'].to_numpy() # Standard devitation of horizontal velocity error (meter/sec)


Path("results", args.d).mkdir(parents=True, exist_ok=True)
path_saved = Path("results", args.d)
if args.copy:
    shutil.copy2("./" + args.d, path_saved)

if args.latex:
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


# Trajectory
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

# Position
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, x, color=true_color, linestyle=true_style, label="true")
# ax[0].plot(t, vel_ref[:, 0], color=ref_color, linestyle=ref_style, label="ref.")
ax[0].set_ylabel("X (m)")
ax[0].axes.xaxis.set_ticklabels([])
ax[1].plot(time, y, color=true_color, linestyle=true_style)
# ax[1].plot(t, vel_ref[:, 1], color=ref_color, linestyle=ref_style)
ax[1].set_ylabel("Y (m)")
ax[1].axes.xaxis.set_ticklabels([])
ax[2].plot(time, z, color=true_color, linestyle=true_style)
# ax[2].plot(t, vel_ref[:, 2], color=ref_color, linestyle=ref_style)
ax[2].set_ylabel("Z (m)")
ax[0].legend()
fig.suptitle("Position")
fig.supxlabel("Time (s)")
fig.align_ylabels(ax)
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "position.png"), bbox_inches="tight")
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

# Heading angle
fig, ax = plt.subplots(1, 1)
ax.plot(time, heading * 180 / np.pi, color=true_color, linestyle=true_style, label='true')
ax.set_ylabel('Heading angle (deg)')
ax.set_xlabel('Time (s)')
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "heading.png"), bbox_inches="tight")
plt.close("all")

# Standard deivation
fig, ax = plt.subplots(2, 2)
ax[0][0].plot(time, std_pos_horizontal, color=true_color, linestyle=true_style, label="true")
ax[0][0].set_ylabel("std pos horizontal (m)")
ax[0][0].axes.xaxis.set_ticklabels([])
ax[0][1].plot(time, std_pos_vertical, color=true_color, linestyle=true_style, label="true")
ax[0][1].set_ylabel("std pos vertical (m)")
ax[0][1].axes.xaxis.set_ticklabels([])


ax[1][0].plot(time, std_vel_horizontal, color=true_color, linestyle=true_style)
ax[1][0].set_ylabel("td vel horizontal (m/s)")
ax[1][1].plot(time, std_vel_vertical, color=true_color, linestyle=true_style)
ax[1][1].set_ylabel("td vel vertical (m/s)")
ax[0][1].legend()
fig.suptitle("Standard devitation of position and velocity error")
fig.supxlabel("Time (s)")
fig.align_ylabels(ax)
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "std.png"), bbox_inches="tight")
plt.close("all")

breakpoint()

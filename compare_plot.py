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
    action="append",
    nargs="+",
    help="file name of the date to process with file format. The order of data must be `state history` `cmd history` ",
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
parser.add_argument(
    "--here",
    metavar="bool_path_figures",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="where to save figure: Here (directory where processing.py code is in) if True or directory where the first data is in",
)
args = parser.parse_args()

data = args.d[0]

path_split = data[0].split("/")
file_name = path_split[-1].split(".")[0]
if args.here:
    Path("results", file_name).mkdir(parents=True, exist_ok=True)
    path_saved = Path("results", file_name)
else:
    tmp2 = "".join(data[0].split("/")[:-1])
    Path(tmp2, "results", file_name).mkdir(parents=True, exist_ok=True)
    path_saved = Path(tmp2, "results", file_name)

if args.copy:
    shutil.copy2(data[0], path_saved)
    shutil.copy2(data[1], path_saved)

if args.latex:
    tex_fonts = {
        "text.usetex": True,
        "font.family": "Times New Roman",
        "axes.grid": True,
    }
    plt.rcParams.update(tex_fonts)

df = [pd.read_csv(data[i], header=0, index_col=0) for i in range(len(data))]

time_mus = df[0][
    "timestamp_sample"
].to_numpy()  # Time since system start (microseconds)
time = (time_mus - time_mus[0]) / 1e6  # Time since data is logged (seconds)
x = df[0]["x"].to_numpy()  # North position in NED earth-fixed frame (meter)
y = df[0]["y"].to_numpy()  # East position in NED earth-fixed frame (meter)
z = df[0]["z"].to_numpy()  # Down position in NED earth-fixed frame (meter)
vx = df[0]["vx"].to_numpy()  # North position in NED earth-fixed frame (meter/sec)
vy = df[0]["vy"].to_numpy()  # East position in NED earth-fixed frame (meter/sec)
vz = df[0]["vz"].to_numpy()  # Down position in NED earth-fixed frame (meter/sec)
ax = df[0]["ax"].to_numpy()  # North position in NED earth-fixed frame (meter/sec^2)
ay = df[0]["ay"].to_numpy()  # East position in NED earth-fixed frame (meter/sec^2)
az = df[0]["az"].to_numpy()  # Down position in NED earth-fixed frame (meter/sec^2)
heading = df[0][
    "heading"
].to_numpy()  # Euler yaw angle transforming the tarngent plane relative to NED earth-fixed frame, [-PI ~ PI] (radians)
std_pos_horizontal = df[0][
    "eph"
].to_numpy()  # Standard devitation of horizontal position error (meter)
std_pos_vertical = df[0][
    "epv"
].to_numpy()  # Standard devitation of vertical position error (meter)
std_vel_horizontal = df[0][
    "evh"
].to_numpy()  # Standard devitation of horizontal velocity error (meter/sec)
std_vel_vertical = df[0][
    "evv"
].to_numpy()  # Standard devitation of horizontal velocity error (meter/sec)


x_cmd = df[1]["x"].to_numpy()  # North position in NED earth-fixed frame (meter)
y_cmd = df[1]["y"].to_numpy()  # East position in NED earth-fixed frame (meter)
z_cmd = df[1]["z"].to_numpy()  # Down position in NED earth-fixed frame (meter)
vx_cmd = df[1]["vx"].to_numpy()  # North position in NED earth-fixed frame (meter/sec)
vy_cmd = df[1]["vy"].to_numpy()  # East position in NED earth-fixed frame (meter/sec)
vz_cmd = df[1]["vz"].to_numpy()  # Down position in NED earth-fixed frame (meter/sec)
ax_cmd = df[1][
    "acceleration[0]"
].to_numpy()  # North position in NED earth-fixed frame (meter/sec^2)
ay_cmd = df[1][
    "acceleration[1]"
].to_numpy()  # East position in NED earth-fixed frame (meter/sec^2)
az_cmd = df[1][
    "acceleration[2]"
].to_numpy()  # Down position in NED earth-fixed frame (meter/sec^2)
Tx_cmd = df[1]["thrust[0]"].to_numpy()
Ty_cmd = df[1]["thrust[1]"].to_numpy()
Tz_cmd = df[1]["thrust[2]"].to_numpy()
yaw_cmd = df[1]["yaw"].to_numpy()
yawspeed_cmd = df[1]["yawspeed"].to_numpy()


true_style = "solid"
ref_style = "dashed"
cmd_style = "dotted"
true_color = "k"
ref_color = "b"
cmd_color = "r"
# Trajectory
fig, ax = plt.subplots(1, 1, subplot_kw={"projection": "3d"})
ax.plot(
    x,
    y,
    -z,
    label="true",
    color=true_color,
    linestyle=true_style,
)
ax.plot(
    x_cmd,
    y_cmd,
    -z_cmd,
    label="cmd",
    color=cmd_color,
    linestyle=cmd_style,
)
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("Trajectory")
ax.grid()
plt.legend()
if args.save:
    fig.savefig(Path(path_saved, "trajectory.png"), bbox_inches="tight")
plt.close("all")

# Position
fig, ax = plt.subplots(3, 1)
ax[0].plot(time, x, color=true_color, linestyle=true_style, label="true")
ax[0].plot(time, x_cmd, color=cmd_color, linestyle=cmd_style, label="cmd")
ax[0].set_ylabel("X (m)")
ax[0].axes.xaxis.set_ticklabels([])
ax[0].grid()
ax[1].plot(time, y, color=true_color, linestyle=true_style)
ax[1].plot(time, y_cmd, color=cmd_color, linestyle=cmd_style)
ax[1].set_ylabel("Y (m)")
ax[1].axes.xaxis.set_ticklabels([])
ax[1].grid()
ax[2].plot(time, z, color=true_color, linestyle=true_style)
ax[2].plot(time, z_cmd, color=cmd_color, linestyle=cmd_style)
ax[2].set_ylabel("Z (m)")
ax[2].grid()
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
ax[0].plot(time, vx_cmd, color=cmd_color, linestyle=cmd_style, label="cmd")
ax[0].set_ylabel(r"$V_x$ (m/s)")
ax[0].axes.xaxis.set_ticklabels([])
ax[0].grid()
ax[1].plot(time, vy, color=true_color, linestyle=true_style)
ax[1].plot(time, vy_cmd, color=cmd_color, linestyle=cmd_style)
ax[1].set_ylabel(r"$V_y$ (m/s)")
ax[1].axes.xaxis.set_ticklabels([])
ax[1].grid()
ax[2].plot(time, vz, color=true_color, linestyle=true_style)
ax[2].plot(time, vz_cmd, color=cmd_color, linestyle=cmd_style)
ax[2].set_ylabel(r"$V_z$ (m/s)")
ax[2].grid()
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
ax.plot(
    time, heading * 180 / np.pi, color=true_color, linestyle=true_style, label="true"
)
ax.plot(time, yaw_cmd * 180 / np.pi, color=cmd_color, linestyle=cmd_style, label="cmd")
ax.set_ylabel("Heading angle (deg)")
ax.set_xlabel("Time (s)")
ax.grid()
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "heading.png"), bbox_inches="tight")
plt.close("all")

# Standard deivation
fig, ax = plt.subplots(2, 2)
ax[0][0].plot(
    time, std_pos_horizontal, color=true_color, linestyle=true_style, label="true"
)
ax[0][0].set_ylabel("std pos horizontal (m)")
ax[0][0].axes.xaxis.set_ticklabels([])
ax[0][0].grid()
ax[0][1].plot(
    time, std_pos_vertical, color=true_color, linestyle=true_style, label="true"
)
ax[0][1].set_ylabel("std pos vertical (m)")
ax[0][1].axes.xaxis.set_ticklabels([])
ax[0][1].grid()

ax[1][0].plot(time, std_vel_horizontal, color=true_color, linestyle=true_style)
ax[1][0].set_ylabel("td vel horizontal (m/s)")
ax[1][0].grid()
ax[1][1].plot(time, std_vel_vertical, color=true_color, linestyle=true_style)
ax[1][1].set_ylabel("td vel vertical (m/s)")
ax[1][1].grid()
ax[0][1].legend()
fig.suptitle("Standard devitation of position and velocity error")
fig.supxlabel("Time (s)")
fig.align_ylabels(ax)
fig.tight_layout()
if args.save:
    fig.savefig(Path(path_saved, "std.png"), bbox_inches="tight")
plt.close("all")

breakpoint()

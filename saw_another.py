import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import PillowWriter


plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.edgecolor"] = "gray"
plt.rcParams["figure.facecolor"] = "darkgray"
plt.rcParams["figure.frameon"] = False
plt.rcParams["legend.facecolor"] = "gray"
plt.rcParams["legend.fontsize"] = 14
plt.rcParams["legend.fancybox"] = True
plt.rcParams["font.size"] = 14


def create_grid(n):
    grid = np.zeros((n // 2, n // 2))  # considering square by n//2 rows and columns
    return grid


def simple_random(n):
    directions = np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])  # vector of directions
    x = [0]
    y = [0]
    for i in range(n):
        dx, dy = directions[np.random.randint(0, 4)]  # directions of the next step
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
    return x, y


def sr_plot_rec(n):
    metadata = dict(title="Simple Random Walk", artist="Lucksinia")
    writer = PillowWriter(fps=30, metadata=metadata)
    x, y = simple_random(n)
    figure = plt.figure()
    figure.set_facecolor("darkgray")
    (l,) = plt.plot([], [], "bo-", linewidth=2)
    (p1,) = plt.plot(0, 0, "go", ms=12, label="Start")
    (p2,) = plt.plot(x[-1], y[-1], "ro", ms=12, label="End")
    plt.title(
        f"Simple random walk of {n} steps:", fontsize=14, fontweight="bold", y=1.05
    )
    plt.axis("equal")
    plt.margins(0.3, 0.3)
    plt.legend()
    x_list = []
    y_list = []
    with writer.saving(figure, "RandomWalker.gif", 300):
        for i in range(n + 1):
            x_list.append(x[i])
            y_list.append(y[i])
            p2.set_data(x_list[-1], y_list[-1])
            l.set_data(x_list, y_list)
            figure.tight_layout()
            writer.grab_frame()


sr_plot_rec(120)

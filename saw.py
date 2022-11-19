import numpy as np
import matplotlib.pyplot as plt


def simple_random(n):
    """
    Generates simple random walk of len(n)
    Args:
        n(int): length of the walk
    Output:
        (x,y)(ndarray, ndarray): Random list of length n
    """

    x = [0]
    y = [0]
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # vectorised directions

    for _ in range(n):
        dx, dy = directions[np.random.randint(0, 4)]  # directions of the next step
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
    print(x)
    return x, y


def sr_plot(n):
    """
    Generates plot of simple random walk of len(n)
    Args:
        n(int): length of the walk
    Output:
        Plot of random walk
    """
    x, y = simple_random(n)
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, "bo-", linewidth=2)
    plt.plot(0, 0, "go", ms=12, label="Start")
    plt.plot(x[-1], y[-1], "ro", ms=12, label="End")
    plt.axis("equal")
    plt.legend(fontsize=14)
    plt.title(
        f"Simple random walk of len({str(n)})", fontsize=14, fontweight="bold", y=1.05
    )
    plt.show()


def saw_miopic(n):
    """
    Generates SAW of len(n)
    Args:
        n(int): length of the walk
    Output:
        (x,y, stuck, steps)(list, list, bool, int):
        Random list of length n
        could not terminate flag
        number of steps in final walk
    """

    x = [0]
    y = [0]
    stuck = 0
    positions = set([(0, 0)])  # all alredy visited
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # vectorised directions

    for i in range(n):
        feasible = []  # avalible directions
        for dx, dy in directions:
            if (x[-1] + dx, y[-1] + dy) not in positions:  # checks if not visited
                feasible.append((dx, dy))

        if feasible:  # if not visited avalible
            dx, dy = feasible[
                np.random.randint(0, len(feasible))
            ]  # directions of the next step
            positions.add((x[-1] + dx, y[-1] + dy))
            x.append(x[-1] + dx)
            y.append(y[-1] + dy)
        else:
            stuck = True
            steps = i + 1
            break

        steps = n + 1

    return x, y, stuck, steps


def miopic_plot(n):
    """
    Generates plot of miopic SAW of len(n)
    Args:
        n(int): length of the walk
    Output:
        Plot of SAW
    """
    x, y, stuck, steps = saw_miopic(n)
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, "bo-", linewidth=2)
    plt.plot(0, 0, "go", ms=12, label="Start")
    plt.plot(x[-1], y[-1], "ro", ms=12, label="End")
    plt.axis("equal")
    plt.legend(fontsize=14)
    if stuck:
        plt.title(
            f"SAW stuck at step {str(steps)}", fontsize=14, fontweight="bold", y=1.05
        )
    else:
        plt.title(f"SAW of len({str(n)})", fontsize=14, fontweight="bold", y=1.05)
    plt.show()


def small_saw(n):
    """
    Generates a SAW of length n by rejection sampling, with early stopping (checks at each step if walk is
    non-intersecting. If it intersects itself, stops prematurely)
    Will be used for n<=10, hence the name small_saw

    Args:
        n (int): the length of the walk
    Returns:
        (x, y) (list, list): SAW of length n
    """
    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    not_saw = 1
    while not_saw:
        x, y = [0], [0]
        positions = set([(0, 0)])
        abort = 0
        i = 0
        while i < n and not (abort):
            dx, dy = deltas[np.random.randint(0, 4)]
            if (x[-1] + dx, y[-1] + dy) in positions:
                abort = 1
                break
            else:
                x.append(x[-1] + dx)
                y.append(y[-1] + dy)
                positions.add((x[-1] + dx, y[-1] + dy))
                i = i + 1
        if not (abort):
            not_saw = 0
    return x, y


def is_saw(x, y, n):
    """
    Checks if walk of length n is self-avoiding

    Args:
        (x,y) (list, list): walk of length n
        n (int): length of the walk
    Returns:
        True if the walk is self-avoiding
    """
    return n + 1 == len(
        set(zip(x, y))
    )  # creating a set removes duplicates, so it suffices to check the size of the set


def dimer(n):
    """
    Generates a SAW of length n by dimerization

    Args:
        n (int): the length of the walk
    Returns:
        (x, y) (list, list): SAW of length n
    """
    if n <= 3:
        x, y, _, _ = saw_miopic(n)  # base case uses the myopic algorithm
        return x, y
    else:
        not_saw = 1
        while not_saw:
            (x_1, y_1) = dimer(n // 2)  # recursive call
            (x_2, y_2) = dimer(n - n // 2)  # recursive call
            x_2 = [
                x + x_1[-1] for x in x_2
            ]  # translates the second walk to the end of the first one
            y_2 = [
                y + y_1[-1] for y in y_2
            ]  # translates the second walk to the end of the first one
            x_concat, y_concat = x_1 + x_2[1:], y_1 + y_2[1:]  # performs concatenation
            if is_saw(x_concat, y_concat, n):  # if walk obtained is SAW, stop
                not_saw = 0
        return x_concat, y_concat


def dimmer_plot(n):
    """
    Plots the output of the dimerization method

    Args:
        n (int): the length of the walk
    Returns:
        Plot of the output of the dimerization algorithm
    """
    x, y = dimer(n)
    plt.figure(figsize=(8, 8))
    plt.plot(x, y, "b.-", linewidth=1)
    plt.plot(0, 0, "go", ms=12, label="Start")
    plt.plot(x[-1], y[-1], "ro", ms=12, label="End")
    plt.axis("equal")
    plt.legend()
    plt.title(
        f" SAW of length {str(n)} generated by dimerization",
        fontsize=14,
        fontweight="bold",
        y=1.05,
    )
    plt.show()


sr_plot(80)
miopic_plot(80)
dimmer_plot(300)

# TODO: Stuff all SAW's in matplotlib animations

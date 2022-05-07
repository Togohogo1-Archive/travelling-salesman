import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure()


def plot_path(x_coord, y_coord, cities, title):
    plt.clf()

    for c1, c2 in zip(cities[1:], cities[:-1]):
        x_points = [x_coord[c1], x_coord[c2]]
        y_points = [y_coord[c1], y_coord[c2]]
        plt.plot(x_points, y_points, "ro-")
        plt.title(title)


def draw_path():
    fig.canvas.draw()
    fig.canvas.flush_events()


def show_final():
    plt.ioff()
    plt.show()

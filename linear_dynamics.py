import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np


def discriminator(dict):
    x = ""
    for key, value in dict.items():
        x += key + '_' + str(value)
    return x


def print_stability_types():
    x = []
    y = []

    for i in range(-1000, 1000, 1):
        xx = i * 0.01
        yy = xx ** 2
        x.append(xx)
        y.append(yy / 4)

    fig = plt.figure()

    axes = fig.add_subplot(111)
    axes.plot(x, y, color='black')
    axes.axhline(0, 0, 1, color='black')
    axes.axvline(0, 0.33, 1, color='black')
    plt.text(0.02, 0.35, 'cycles', rotation=90)
    plt.text(0.4, 0.1, 'τ² - 4Δ = 0', rotation=35)
    plt.text(-2.3, 0.2, 'stable nodes')
    plt.text(-1.5, 1.5, 'stable spirals')
    plt.text(1.5, 0.2, 'unstable nodes')
    plt.text(0.5, 1.5, 'unstable spirals')
    plt.text(-0.3, -0.6, 'saddles')
    axes.set_xlim([-3, 3])
    axes.set_ylim([-1, 2])
    axes.get_xaxis().set_ticks([0])
    axes.get_yaxis().set_ticks([0])
    plt.xlabel('τ')
    plt.ylabel('Δ')
    plt.title('stability types by trace and determinant')
    fig.savefig("stability_types.png")


def lotka_volterra_prey_growth(a, b, m, n):
    return (a - b * n) * m


def lotka_volterra_predator_growth(c, d, m, n):
    return (c * m - d) * n


def plot_phase_space(name,
                     params,
                     prey_growth,
                     predator_growth,
                     fixed_points,
                     iterations,
                     dimensions):
    xmin = 0
    xmax = dimensions[0]
    ymin = 0
    ymax = dimensions[1]
    x = np.arange(xmin, xmax, 0.1)
    y = np.arange(ymin, ymax, 0.1)
    m, n = np.meshgrid(x, y)
    u = prey_growth(m, n)
    v = predator_growth(m, n)
    magnitude = (np.hypot(u, v))
    magnitude[magnitude == 0] = 1
    u /= magnitude
    v /= magnitude
    fig, ax = plt.subplots()
    ax.quiver(x, y, u, v)
    plt.xlabel('prey')
    plt.ylabel('predators')
    colours = cm.rainbow(np.linspace(0, 1, len(fixed_points)))
    for fixed_point, colour in zip(fixed_points, colours):
        x_point = fixed_point[0]['point']
        y_point = fixed_point[1]['point']
        plt.plot([x_point], [y_point], marker='o', markersize=3, color=colour)
        plt.annotate(f'{"{:.3f}".format(x_point)}, {"{:.3f}".format(y_point)}', [x_point, y_point],
                     xytext=(x_point + 0.05, y_point + 0.75), arrowprops={'arrowstyle': '->', 'color': colour},
                     bbox=dict(facecolor='white', edgecolor=colour))
        sample_prey = []
        sample_predators = []
        prey = fixed_point[0]['initial']
        predators = fixed_point[1]['initial']
        ts = 0.01
        for i in range(0, iterations):
            sample_prey.append(min(xmax, prey))
            sample_predators.append(min(ymax, predators))
            change_in_prey = prey_growth(prey, predators)
            change_in_predators = predator_growth(prey, predators)
            prey = max(0, prey + change_in_prey * ts)
            predators = max(0, predators + change_in_predators * ts)
        plt.plot(sample_prey, sample_predators, color=colour)
    plt.title(f'{name} ({params})')

    fig.savefig(f'{name}_{discriminator(params)}.png')


def plot_lotka_volterra(a, b, c, d):
    def prey_growth(m, n):
        return (a - b * n) * m

    def predator_growth(m, n):
        return (c * m - d) * n

    fixed_points = [[{'point': 0, 'initial': 0.1}, {'point': 0, 'initial': 0.1}],
                    [{'point': d / c, 'initial': d / c + 0.1}, {'point': a / b, 'initial': a / b + 0.1}]]
    plot_phase_space("Lotka-Volterra", {'a': a, 'b': b, 'c': c, 'd': d}, prey_growth, predator_growth, fixed_points,
                     1000, [4, 3])


def plot_volterra(a, b, c, d, e):
    def prey_growth(m, n):
        return m * (a - b * m - c * n)

    def predator_growth(m, n):
        return (e * m - d) * n

    fixed_points = [[{'point': 0, 'initial': 0.1}, {'point': 0, 'initial': 0.1}],
                    [{'point': a / b, 'initial': a / b + 0.1}, {'point': 0, 'initial': 0.1}],
                    [{'point': d / e, 'initial': d / e + 0.125},
                     {'point': (a - ((b * d) / e)) / c, 'initial': (a - ((b * d) / e)) / c + 1}]]
    plot_phase_space("Volterra", {'a': a, 'b': b, 'c': c, 'd': d, 'e': e}, prey_growth, predator_growth, fixed_points,
                     30000, [1, 2])


plot_lotka_volterra(0.67, 1.33, 1, 1)
plot_lotka_volterra(0.67, 1.33, 1.1, 0.9)
plot_lotka_volterra(1.1, 0.9, 1.1, 0.9)

plot_volterra(0.05, 0.1, 0.1, 0.05, 0.2)

print_stability_types()

import matplotlib.pyplot as plt


def boxplot(res, title, ylabel, xlabel):
    fig, ax = plt.subplots()

    counts = list()
    xticks = list()
    for x in res:
        counts.append(res[x])
        xticks.append(x)

    step = xticks[1] - xticks[0]
    minx = xticks[0] - step
    maxx = xticks[len(xticks)-1] + step

    ax.boxplot(counts, positions=xticks, widths=8.5)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.set(xlim=(minx, maxx), xticks=range(minx, maxx, step))

    plt.show()
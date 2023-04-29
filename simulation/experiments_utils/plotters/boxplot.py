import matplotlib.pyplot as plt


def plotSeries(seriesDict, title, ylabel, xlabel):
    fig, ax = plt.subplots()

    for seriesName in seriesDict:
        ax.plot(seriesDict[seriesName].x_values, seriesDict[seriesName].y_values, linewidth=1, markersize=4, marker='o', label=seriesName)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.legend()
    plt.show()
import matplotlib.pyplot as plt


def plotSeries(seriesDict, title, ylabel, xlabel, filename, labelsBySeriesName):
    fig, ax = plt.subplots()

    for seriesName in seriesDict:
        ax.plot(seriesDict[seriesName].x_values, seriesDict[seriesName].y_values, linewidth=1, markersize=2, marker='o', label=labelsBySeriesName[seriesName])

    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    if filename != "":
        plt.savefig(filename)
    else:
        plt.show()
import matplotlib.pyplot as plt


def boxplot(res, title, ylabel, xlabel):
    fig, ax = plt.subplots()

    y_values = list()
    x_values = list()
    for x in res:
        y_values.append(sum(res[x])/len(res[x]))
        x_values.append(x)


    ax.plot(x_values, y_values, linewidth=1, markersize=4, marker='o')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    plt.show()
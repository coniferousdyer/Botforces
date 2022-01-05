import discord
import matplotlib.pyplot as plt
import numpy as np


def plot_rating_bar_chart(rating_dict):
    """
    Plots the rating bar chart.
    """

    x = np.array(list(rating_dict.keys()))
    y = np.array(list(rating_dict.values()))

    plt.clf()
    plt.bar(x, y)
    plt.xticks(fontsize=7, rotation=45)
    plt.xlabel("Rating", fontsize=7)
    plt.ylabel("Number", fontsize=7)

    for i in range(len(y)):
        plt.annotate(
            str(y[i]), xy=(x[i], y[i]), ha="center", va="bottom"
        ).set_fontsize(7)

    # Saving file temporarily
    plt.savefig("figure.png")
    File = discord.File("figure.png")

    return File


def plot_index_bar_chart(tag_dict):
    """
    Plots the index bar chart.
    """

    x = np.array(list(tag_dict.keys()))
    y = np.array(list(tag_dict.values()))

    plt.clf()
    plt.bar(x, y, color="green")
    plt.xticks(fontsize=7)
    plt.xlabel("Index", fontsize=7)
    plt.ylabel("Number", fontsize=7)

    for i in range(len(y)):
        plt.annotate(
            str(y[i]), xy=(x[i], y[i]), ha="center", va="bottom"
        ).set_fontsize(7)

    # Saving file temporarily
    plt.savefig("figure.png")
    File = discord.File("figure.png")

    return File


def plot_tags_bar_chart(tag_dict):
    """
    Plots the tags bar chart.
    """

    x = np.array(list(tag_dict.keys()))
    y = np.array(list(tag_dict.values()))

    plt.clf()
    plt.bar(x, y, color="red")
    plt.xticks(fontsize=7, rotation=90)
    plt.ylabel("Number", fontsize=7)

    for i in range(len(y)):
        plt.annotate(
            str(y[i]), xy=(x[i], y[i]), ha="center", va="bottom"
        ).set_fontsize(7)

    # Saving file temporarily
    plt.savefig("figure.png")
    File = discord.File("figure.png")

    return File
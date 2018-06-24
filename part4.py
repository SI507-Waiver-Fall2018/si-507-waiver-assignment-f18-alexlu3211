# Full Name: Alex Lu
# UMID     : 54523810

import plotly.plotly as py
import plotly.graph_objs as go


def plot(nouns):
    x_axis = []
    y_axis = []

    for word in nouns:
        x_axis.append(word[0])
        y_axis.append(int(word[1]))

    data = [go.Bar(x=x_axis, y=y_axis)]
    layout = go.Layout(title="Top 5 Nouns", width=800, height=640)

    chart = go.Figure(data=data, layout=layout)
    py.image.save_as(chart, filename="part4_viz_image.png")


if __name__ == '__main__':
    with open('noun_data.csv', 'r') as f:
        nouns = []
        for line in f:
            noun = line.split(',')
            nouns.append((noun[0], noun[1][:-1]))

    nouns = nouns[1:]
    plot(nouns)


# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 15:39:35 2018

@author: latti
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 14 10:33:45 2018

@author: latti
"""

import json
import operator
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urlparse
import urllib
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from bokeh.io import show, output_file
from bokeh.plotting import figure, show, ColumnDataSource
from bokeh.models.graphs import from_networkx
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LabelSet , LinearColorMapper
#from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label

#connections = [("cnn.com","twitter.com"),("qz.com","cnn.com"),("twitter.com","reddit.com"),("qz.com","twitter.com")]
#levels = {"twitter.com":1, "cnn.com": 2, "qz.com":2, "fox.com":1, "reddit.com":3}
#occurance = {"twitter.com":100, "cnn.com": 200, "qz.com":20, "fox.com":5, "reddit.com":50}
occurance = pickle.load(open("occurance150.p", "rb"))
connections = pickle.load(open("connections150.p", "rb"))
levels = pickle.load(open("levels150.p", "rb"))
    
keys = list(occurance.keys())
values = list(occurance.values())
    

#GRAPHING
minHits = 10
graphTitle = "150 Origin URLs, Minimum of " + str(minHits) + " Hits"
htmlFileName = "LABELhundredFiftyMin" + str(minHits) + ".html"
########################
G = nx.Graph()

nodesList = []
finNames = []
finHits = []
finLevels = []
for names in keys:
    if occurance[names] >= minHits:
        nodesList.append((names, {"name":names, "hits":occurance[names]}))
        finNames.append(names)
        finHits.append(occurance[names])
        finLevels.append(levels[names])
        
finalConnections = []
for m in connections:
    if occurance[m[0]] >= minHits and occurance[m[1]] >= minHits:
        finalConnections.append(m)

#current_palette = sns.color_palette()
#sns.palplot(current_palette)
colors = ["windows blue", "amber", "faded green"]
current_palette = sns.xkcd_palette(colors)
sns.palplot(current_palette)
pal_hex_lst = current_palette.as_hex()
mapper = LinearColorMapper(palette=pal_hex_lst, low=1, high=3)

G.add_nodes_from(nodesList)
G.add_edges_from(finalConnections)
nx.set_node_attributes(G, occurance, 'node_size')
nx.set_node_attributes(G, finNames, 'namez')
nx.set_node_attributes(G, levels, 'node_color')
#plt.subplot(121)
pos=nx.spring_layout(G, k=0.5)


source = ColumnDataSource(dict(
    namedata=finNames,
    hitsdata=finHits,
    leveldata=finLevels
))


#nx.draw(G, node_size = values, with_labels = False, node_color = levels, label_pos=0.3, font_size = 4, edge_color = "blue", width = 0.1, pos=pos)
#plt.savefig("Graph50k.5.png", format="PNG", dpi=1000)
#print(occurance)
hover = HoverTool(
       tooltips=[("Site", "@name"), ("Hits", "@hits")]
   )
plot = Plot(plot_width=1200, plot_height=700,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.add_tools(hover, BoxZoomTool(), ResetTool())
plot.title.text = graphTitle
plot.title.text_font_size = "25px"
plot.title.align = "center"
graph = from_networkx(G, pos, scale=2, center=(0,0))

graph.node_renderer.glyph = Circle(size='node_size', fill_color={'field': 'node_color', 'transform': mapper}, name='namez')
#graph.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
#labels = LabelSet(
#            text='namesdata',
#            level='glyph', 
#            source=source)
#plot.add_layout(labels)
plot.renderers.append(graph)
output_file(htmlFileName)
show(plot)
   


    
    
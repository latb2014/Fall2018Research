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


def urlToDomain(url):
    domain = urlparse(url).netloc
    return domain
def url_is_alive(url):
    """
    Checks that a given URL is reachable.
    :param url: A URL
    :rtype: bool
    """
    

    try:
        request = urllib.request.Request(url)
        request.get_method = lambda: 'HEAD'
        urllib.request.urlopen(request)
        return True
    except ValueError:
        return False
    except urllib.request.HTTPError:
        return False


def exploreLinks(url, whitelist, blacklist, level, connections, levels):    
    if level >= 3:
        return
        
    try:
        page = requests.get(url)
    except:
        return
    level = level + 1
    soup = BeautifulSoup(page.content, 'lxml')
    parentUrl = urlToDomain(url)
    print("Enter " + parentUrl)
    for paragraph in soup.find_all('p'):
        for link in paragraph.find_all('a'):
            childSite = link.get('href')
            if childSite == None:
                continue
            childDomain = urlToDomain(childSite)
            if childDomain == None:
                continue
            if isinstance(childDomain, bytes):
                childDomain = childDomain.decode("utf-8")
            if childDomain == parentUrl:
                continue
            if childDomain.strip() == "":
                continue
            if childDomain in whitelist:
                whitelist[childDomain] += 1
            else:
                whitelist[childDomain] = 1
                levels[childDomain] = level;
                
            connections.append((parentUrl, childDomain))
            exploreLinks(childSite, whitelist, blacklist, level, connections, levels)
    return


json_data = []
boy = 0
with open('conspiracy_submissions.txt', 'r') as file:
    for line in file:
        json_data.append(json.loads(line))
        boy = boy +1
print(boy)

links = []
count = 0
for item in json_data:
    if count >= 250:
        break
    if count < 150:
        count = count + 1
        continue
    if item['is_self'] == 'False':
        if isinstance(item['url'], bytes):
                item['url'] = item['url'].decode("utf-8")
        links.append(item['url'])
        count = count + 1
        
    

blacklist = {}
occurance = {}

print("\n\nTime to scrape\n\n")
connections = []
levels = {}
#input the first level
for orgins in links:
    childDomain = urlToDomain(orgins)
    if childDomain.strip() == "":
        continue
    if childDomain in occurance:
        occurance[childDomain] += 1
    else:
        occurance[childDomain] = 1
        levels[childDomain] = 1
    connections.append((childDomain, childDomain))
        

for url in links:
    exploreLinks(url, occurance, blacklist, 1, connections, levels)
    
    
occuranceOverall = pickle.load(open("occurance150.p", "rb"))
connectionsOverall = pickle.load(open("connections150.p", "rb"))
levelsOverall = pickle.load(open("levels150.p", "rb"))
    
for key, value in occurance.items():
    occuranceOverall[key] = occuranceOverall[key] + value
        
for key, value in connections.items():
    connectionsOverall[key] = connectionsOverall[key] + value
    
for key, value in levels.items():
    levelsOverall[key] = levelsOverall[key] + value


pickle.dump(occuranceOverall, open("occurance250.p", "wb"))
pickle.dump(connectionsOverall, open("connections250.p", "wb"))
pickle.dump(levelsOverall, open("levels250.p", "wb"))

#keys = list(occurance.keys())
#values = list(occurance.values())
#    
#
##GRAPHING
#minHits = 10
#########################
#G = nx.Graph()
#
#nodesList = []
#for names in keys:
#    if occurance[names] > minHits:
#        nodesList.append((names, {"name":names, "hits":occurance[names]}))
#finalConnections = []
#for m in connections:
#    if occurance[m[0]] > minHits and occurance[m[1]] > minHits:
#        finalConnections.append(m)
#
#palette = sns.cubehelix_palette(21)
#pal_hex_lst = palette.as_hex()
#mapper = LinearColorMapper(palette=pal_hex_lst, low=0, high=21)
#
#G.add_nodes_from(nodesList)
#G.add_edges_from(finalConnections)
#nx.set_node_attributes(G, occurance, 'node_size')
#nx.set_node_attributes(G, levels, 'node_color')
##plt.subplot(121)
#pos=nx.spring_layout(G, k=0.5)
##nx.draw(G, node_size = values, with_labels = False, node_color = levels, label_pos=0.3, font_size = 4, edge_color = "blue", width = 0.1, pos=pos)
##plt.savefig("Graph50k.5.png", format="PNG", dpi=1000)
#hover = HoverTool(
#       tooltips=[("Site", "@name"), ("Hits", "@hits")]
#   )
#plot = Plot(plot_width=400, plot_height=400,
#            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
#plot.add_tools(hover, BoxZoomTool(), ResetTool())
#
#graph = from_networkx(G, pos, scale=2, center=(0,0))
#
#graph.node_renderer.glyph = Circle(size='node_size', fill_color={'field': 'node_color', 'transform': mapper})
##graph.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
#
#plot.renderers.append(graph)
#
#output_file("networkx_graph.html")
#show(plot)
   


    
    
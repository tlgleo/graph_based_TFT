import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from display_functions import *
from tournament import *
from agents import *
from run_tournament import *
from social_metrics import *
import os

tournament_demo = tournament_double_circular_6players
n_agents = tournament_demo.n_agents


list_names = ['T1']* n_agents
list_all_agents = [Agent_TFT_Beta(i, name, n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, minCost=True) for i,name in enumerate(list_names)]
#metrics_TFT_NoGraph = compute_metrics(tournament_demo, list_all_agents[:n_agents], 100, metrics_fig='figure_metricsNoGraph.png')

metrics_1alpha = compute_metrics(tournament_demo, list_all_agents[:n_agents], 100, metrics_fig='01_figure_metricsGraph5.svg')

plt.clf()







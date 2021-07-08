import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from display_functions import *
from tournament import *
from agents import *
from run_tournament import *
from social_metrics import *
from utils import *
import pandas as pd
import os

"""
We provide here: some examples of evaluation 

---- eval_choice = 1 
Impact of the choice of graph-processing (no Graph / Ford-Fulkerson / Min-cost)
with agent TFT_beta
-------------

---- eval_choice = 2 
Impact of the choice of TFT function (alpha / beta / gamma)
with agent grTFT mincost
-------------

---- eval_choice = 3
Impact of the beta coefficient 
with agent grTFT Beta mincost
-------------

---- eval_choice = 4
Impact of the r0 
with agent grTFT Beta mincost
-------------

"""

# Select the tournament:
tournament_demo = tournament_circular_3players
name_tournament = 'circular_3Players'
dataframe = False

# Select an example of evaluation
eval_choice = 2

if eval_choice == 1:
    # Study of graph algorithm

    n_agents = tournament_demo.n_agents

    label1 = 'grTFT_minCost'
    label2 = 'grTFT_Fulkerson'
    label3 = 'NoGraphTFT'

    name_expe = "eval-graph_"+name_tournament+'.svg'

    list_all_agents_1 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.6, beta_adaptive=0.6, r_incentive=0.7, minCost= True) for i in range(n_agents)]
    list_all_agents_2 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.6, beta_adaptive=0.6, r_incentive=0.7, minCost= False) for i in range(n_agents)]
    list_all_agents_3 = [Agent_TFT_NoGraph_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.6, beta_adaptive=0.6, r_incentive=0.7) for i in range(n_agents)]


if eval_choice == 2:
    # Study of TFT function

    n_agents = tournament_demo.n_agents

    label1 = 'TFT_alpha'
    label2 = 'TFT_beta'
    label3 = 'TFT_gamma'

    name_expe = "eval-TFT_"+name_tournament+'.svg'

    list_all_agents_1 = [Agent_TFT(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_2 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_3 = [Agent_TFT_Gamma(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.4, gamma_proba=0.05) for i in range(n_agents)]


if eval_choice == 3:
    # Study of parameter beta

    n_agents = tournament_demo.n_agents

    label1 = r'$\beta = 0.0$'
    label2 = r'$\beta = 0.2$'
    label3 = r'$\beta = 0.5$'

    name_expe = "eval-coeffBeta_"+name_tournament+'.svg'

    list_all_agents_1 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.0, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_2 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.2, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_3 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.5, r_incentive=0.4) for i in range(n_agents)]


if eval_choice == 4:
    # Study of parameter r0

    n_agents = tournament_demo.n_agents

    label1 = 'r = 0.1'
    label2 = 'r = 0.2'
    label3 = 'r = 0.4'

    name_expe = "eval-coeffr0"+name_tournament+'.svg'

    list_all_agents_1 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.1) for i in range(n_agents)]
    list_all_agents_2 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.2) for i in range(n_agents)]
    list_all_agents_3 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.4) for i in range(n_agents)]



if eval_choice == 5:
    # Study of TFT function after a repentant behavior

    n_agents = tournament_demo.n_agents

    label1 = 'TFT_alpha'
    label2 = 'TFT_beta'
    label3 = 'TFT_gamma'

    name_expe = "eval-TFT_"+name_tournament+'.svg'

    list_all_agents_1 = [Agent_TFT(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_2 = [Agent_TFT_Beta(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.4) for i in range(n_agents)]
    list_all_agents_3 = [Agent_TFT_Gamma(i, '', n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop, alpha_inertia=0.8, beta_adaptive=0.6, r_incentive=0.4) for i in range(n_agents)]



metrics_1 = compute_metrics(tournament_demo, list_all_agents_1[:n_agents], 100, metrics_fig='figure_metrics1.png')
metrics_1 = transform_list_metrics(metrics_1)
plt.clf()

metrics_2 = compute_metrics(tournament_demo, list_all_agents_2[:n_agents], 100, metrics_fig='figure_metrics2.png')
metrics_2 = transform_list_metrics(metrics_2)
plt.clf()

metrics_3 = compute_metrics(tournament_demo, list_all_agents_3[:n_agents], 100, metrics_fig='figure_metrics3.png')
metrics_3 = transform_list_metrics(metrics_3)
plt.clf()


if dataframe:
    results = np.array([metrics_1, metrics_2, metrics_3])
    results = np.transpose(results)
    DF = pd.DataFrame(results)
    DF.to_csv(name_expe +  '_dataframe.csv')


list_metrics = [metrics_1, metrics_2, metrics_3]
labels_metrics = ["Efficiency", "    Speed",  "         Forgiveness", "Incentive        \ncompatibility        ", "Safety    "] # spaces present for clarity of radar chart
labels_algos = [label1, label2, label3]
output_fig = name_expe + '_radar_chart.svg'

#radar_chart(list_metrics, labels_metrics, labels_algos, output_fig)

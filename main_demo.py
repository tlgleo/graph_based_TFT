from tournament import *
from agents import *
from run_tournament import *
from utils import *


# To create one customized tournament, go in tournament.py
# List of proposed tournaments:
tournaments_lists = [tournament_classic_2players,
                     tournament_circular_3players,
                     tournament_full_3players,
                     tournament_circular_4players,
                     tournament_double_circular_4players,
                     tournament_circular_5players,
                     tournament_double_circular_5players,
                     tournament_circular_6players,
                     tournament_double_circular_6players,
                     tournament_random_6players
                    ]

# some presets games are defined below:
# choose 0 to customize a game and modify the tournament choice and the agents list
choice_example = 1
video_render = True # if ffmpeg installed

if choice_example == 0:
    # CUSTOM, modify the tournament and the agents

    choice_tournament = 8
    t_max = 20

    list_agents_keys = ['GT3', 'GT3', 'GT3', 'GT3', 'GT3', 'GT3']
    # it is possible to modify parameters of agents below in the creation of list of agents

    name_expe = 'NAME_OF_EXPE'

elif choice_example == 1:
    # 6 grTFT MinCostBeta in a 6-player double circular dilemma
    choice_tournament = 8
    t_max = 100
    list_agents_keys = ['GT2', 'GT2', 'GT2', 'GT2', 'GT2', 'GT2']
    name_expe = 'DoubleCircular-6P_MinCostBeta'

elif choice_example == 2:
    # 4 grTFT MinCostBeta + 1 Repentant Traitor (defects between 30 and 60) and a Traitor (defects after 50)
    # in a 6-player double circular dilemma
    choice_tournament = 8
    t_max = 100
    list_agents_keys = ['Tra1', 'GT2', 'GT2', 'Tra2', 'GT2', 'GT2']
    name_expe = 'DoubleCircular-6Players_2Traitors-vs-4grTFT_MinCostBeta'

elif choice_example == 3:
    # 4 grTFT MinCostGamma + 1 Repentant Traitor (defects between 30 and 60) and a Traitor (defects after 50)
    # in a 6-player double circular dilemma
    choice_tournament = 8
    t_max = 100
    list_agents_keys = ['Tra1', 'GT3', 'GT3', 'Tra2', 'GT3', 'GT3']
    name_expe = 'DoubleCircular-6Players_2Traitors-vs-4grTFT_MinCostGamma'

elif choice_example == 4:
    # 3 grTFT MinCostGamma + 1 Repentant Traitor (defects between 30 and 60) and a Traitor (defects after 50)
    # in a 5-player double circular dilemma
    choice_tournament = 6
    t_max = 100
    list_agents_keys = ['Tra1', 'GT3', 'GT3', 'Tra2', 'GT3']
    name_expe = 'DoubleCircular-5Players_2Traitors-vs-3grTFT_MinCostGamma'

elif choice_example == 5:
    # 2 grTFT MinCostGamma + 1 Repentant Traitor (defects between 30 and 60) and a Traitor (defects after 50)
    # in a 4-player double circular dilemma
    choice_tournament = 4
    t_max = 100
    list_agents_keys = ['Tra1', 'GT3', 'Tra2', 'GT3']
    name_expe = 'DoubleCircular-4Players_2Traitors-vs-2grTFT_MinCostGamma'

elif choice_example == 6:
    # 2 grTFT + 1 Repentant Traitor in a 3-player circular dilemma
    choice_tournament = 1
    t_max = 100
    list_agents_keys = ['Tra1', 'GT2', 'GT2']
    name_expe = 'Circular-3Players_2grTFTbeta-1Traitor'

elif choice_example == 7:
    # 2 grTFT + 1 Repentant Traitor in a 3-player circular dilemma
    choice_tournament = 1
    t_max = 100
    list_agents_keys = ['Tra1', 'GT2', 'GT2']
    name_expe = 'Circular-3Players_grTFT_mincost-beta-1Traitor'


# RUNNING THE TOURNAMENT AND MAKING RENDERING VIDEO
tournament_demo = tournaments_lists[choice_tournament]
n_agents = tournament_demo.n_agents
list_agents_keys = list_agents_keys[:n_agents]
list_names = create_list_names_agents(list_agents_keys)
list_agents = []

for i, key in enumerate(list_agents_keys):
    if key == 'T1': # a TFT without graph with TFT_alpha
        list_agents.append(Agent_TFT_NoGraph(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max = 1.0,
                    alpha_inertia = 0.6, r_incentive = 0.3))

    elif key == 'T2': # a TFT without graph with TFT_beta
        list_agents.append(Agent_TFT_NoGraph_Beta(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max=1.0,
                    alpha_inertia = 0.6, r_incentive = 0.3, beta_adaptive = 0.6))

    elif key == 'T3': # a TFT without graph with TFT_gamma
        list_agents.append(Agent_TFT_NoGraph_Gamma(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max=1.0,
                    alpha_inertia = 0.6, r_incentive = 0.3, beta_adaptive = 0.6, gamma_proba = 0.05))

    elif key == 'GT1': # a grTFT with Ford-Fulkerson approach and TFT_beta
        list_agents.append(Agent_TFT(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max=1.0,
                    alpha_inertia = 0.6, r_incentive = 0.3,                   minCost=True))

    elif key == 'GT2': # a grTFT with min-cost approach and TFT_beta
        list_agents.append(Agent_TFT_Beta(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max=1.0,
                    alpha_inertia=0.6, r_incentive=0.3, beta_adaptive=0.6,
                    minCost=True))

    elif key == 'GT3': # a grTFT with min-cost approach and TFT_gamma
        list_agents.append(Agent_TFT_Gamma(i, list_names[i], n_agents=n_agents,
                    max_coop_matrix=tournament_demo.max_coop, debit_max=1.0,
                    alpha_inertia=0.6, r_incentive=0.3, beta_adaptive=0.6, gamma_proba=0.05,
                    minCost=True))

    elif key == 'Tra1': # Traitor defecting after 30 steps and cooperates again at t = 60
        list_agents.append(Agent_Traitor(i, list_names[i], n_agents = n_agents,
        max_coop_matrix = tournament_demo.max_coop, debit_max = 1.0, t_traitor=30))

    elif key == 'Tra2': # Traitor defecting after 50 steps
        list_agents.append(Agent_Traitor(i, list_names[i], n_agents = n_agents,
        max_coop_matrix = tournament_demo.max_coop, debit_max = 1.0, t_traitor=50))

    elif key == 'Ln': # Late Nice or Repentant Defector defects then cooperates after 25 steps
        list_agents.append(Agent_LateNice(i, list_names[i], n_agents = n_agents,
        max_coop_matrix = tournament_demo.max_coop, debit_max = 1.0, t_coop=25))

    elif key == 'N': # Nice/Cooperator
        list_agents.append(Agent_Nice(i, list_names[i], n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop))

    elif key == 'D': # Defector/Egoist
        list_agents.append(Agent_Egoist(i, list_names[i], n_agents=n_agents, max_coop_matrix=tournament_demo.max_coop))


# Run the tournament_demo with list_agents
run_tournament(tournament_demo, list_agents, n_steps=t_max,
               name_expe=name_expe,
               print_every=10,
               video_render=video_render)


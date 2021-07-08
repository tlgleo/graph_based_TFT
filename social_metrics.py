import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
from run_tournament import *
import statistics as st


def mean_std(values, rd = 3):
    m = st.mean(values)
    std = st.stdev(values)
    return (np.round(m, rd) , np.round(std, rd))

def efficiency(payoffs_agents, payoffs_nices, payoffs_defectors):
    n_agents = len(payoffs_agents)
    t_max = len(payoffs_agents[0])
    social_welfare = [sum([payoffs_agents[i][t] for i in range(n_agents)]) for t in range(t_max)]
    social_welfare_opt = [sum([payoffs_nices[i][t] for i in range(n_agents)]) for t in range(t_max)]
    social_welfare_worse = [sum([payoffs_defectors[i][t] for i in range(n_agents)]) for t in range(t_max)]
    efficiency_output = [(social_welfare[t]-social_welfare_worse[0])/(social_welfare_opt[0]-social_welfare_worse[0]) for t in range(t_max)]
    return np.round(efficiency_output[-1],3), efficiency_output


def speed(efficiency_list, delta_T=20):
    delta_T = min(len(efficiency_list), delta_T)
    print(delta_T)
    final_efficiency = efficiency_list[-1]
    print(final_efficiency)
    x = np.arange(delta_T)
    if final_efficiency == 0:
        output = 0.0
    else:
        output = metrics.auc(x, efficiency_list[:delta_T])/(delta_T*final_efficiency)
    return np.round(output, 3)


def incentive_compatibility(curve_payoffs_1nice, curve_payoffs_1egoist, payoffs_nices, payoffs_egoists):
    output = sum(curve_payoffs_1nice) - sum(curve_payoffs_1egoist)
    output /= sum(payoffs_nices) - sum(payoffs_egoists)
    return np.clip(np.round(output, 3), 0, 1)


def safety(curve_payoffs_1Agent_allDef, curve_payoffs_egoists, curve_payoffs_1Nice_allDef):
    output = sum(curve_payoffs_1Agent_allDef) - sum(curve_payoffs_egoists)
    output /= sum(curve_payoffs_egoists) - sum(curve_payoffs_1Nice_allDef)
    return np.round(output, 3)


def forgiveness_old(all_agents_payoffs, lateNice_vs_agents_payoffs, t_max=100, tau1 = 50, delta_T = 20):
    v_late_nice_0 = lateNice_vs_agents_payoffs[tau1+1]
    v_optimal_final = all_agents_payoffs[-1]
    delta_T = min(delta_T, (t_max-tau1-1))
    cst_norm = delta_T*(v_optimal_final-v_late_nice_0)
    x = np.arange(delta_T)
    output = metrics.auc(x, lateNice_vs_agents_payoffs[tau1+1:tau1+1+delta_T])
    output -= v_late_nice_0*(delta_T-1)
    output /= cst_norm
    if abs(v_optimal_final-v_late_nice_0) < 1e-3:
        return 1.0
    else:
        return np.clip(np.round(output, 3), 0, 1)


def forgiveness(lateNice_vs_agents_payoffs, payoffs_nices, payoffs_defectors, tau1 = 20):

    n_agents = len(lateNice_vs_agents_payoffs)
    t_max = len(lateNice_vs_agents_payoffs[0])
    social_welfare = [sum([lateNice_vs_agents_payoffs[i][t] for i in range(n_agents)]) for t in range(tau1, t_max)]
    social_welfare_opt = [sum([payoffs_nices[i][t] for i in range(n_agents)]) for t in range(tau1, t_max)]
    social_welfare_worse = [sum([payoffs_defectors[i][t] for i in range(n_agents)]) for t in range(tau1, t_max)]
    output = [(social_welfare[t] - social_welfare_worse[0]) / (social_welfare_opt[0] - social_welfare_worse[0]) for t in range(t_max- tau1)]

    return np.round(np.mean(output),3)



def reset_agents(list_of_agents):
    for a in list_of_agents:
        a.reset()

def compute_metrics(tournament, list_of_nA_agents, t_max, delta_T = 20, tau1=50, metrics_fig='output_metrics.png', repentant_behavior=False):

    n_agents = tournament.n_agents
    coop_max_matrix = tournament.max_coop

    assert len(list_of_nA_agents) >= n_agents

    t_coop_LN = tau1

    # LIST of n_agents instances of the Agent we want to study
    list_all_agents = list_of_nA_agents

    # LIST of: One Late Nice + (n_agents-1) instances of the Agent
    list_agents_LN = [Agent_LateNice(0, 'LateNice', n_agents=n_agents, max_coop_matrix=coop_max_matrix,
                                     t_coop=t_coop_LN)] + list_all_agents[1:]

    # LIST of:  One instance of a Nice agent (Cooperator) + (n_agents-1) instances of the Agent
    list_agents_1Coop = [Agent_Nice(0, 'Nice', n_agents=n_agents, max_coop_matrix=coop_max_matrix)] + list_all_agents[1:]

    # LIST of:  One instance of a Egoist agent (Defector) + (n_agents-1) instances of the Agent
    list_agents_1Def = [Agent_Egoist(0, 'Egoist', n_agents=n_agents, max_coop_matrix=coop_max_matrix)] + list_all_agents[1:]

    # LIST of:  One instance of n_agents Nice agents
    list_all_Nices = [Agent_Optimal(i, 'Opt', n_agents=n_agents, max_coop_matrix=coop_max_matrix, optimal_subgraph = tournament.optimal_graph) for i in range(n_agents)]

    # LIST of:  One instance of n_agents Egoist agents
    list_all_Defectors = [Agent_Egoist(i, 'E', n_agents=n_agents, max_coop_matrix=coop_max_matrix) for i in range(n_agents)]

    # LIST of:  One instance of a the Agent + (n_agents-1) Egoist agents
    list_1Agent_all_Def = [list_all_agents[0]] + [Agent_Egoist(i+1, 'E', n_agents=n_agents, max_coop_matrix=coop_max_matrix) for i in range(n_agents-1)]

    # LIST of:  One Nice Agent + (n_agents-1) Egoist agents
    list_1Nice_all_Def = [Agent_Nice(0, 'N', n_agents=n_agents, max_coop_matrix=coop_max_matrix)] + [
        Agent_Egoist(i + 1, 'E', n_agents=n_agents, max_coop_matrix=coop_max_matrix) for i in range(n_agents - 1)]



    # RUNNING Tournaments with different lists of Agents to compute metrics
    N_runs = 8
    k = 1

    tournament.reset()
    reset_agents(list_agents_LN)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents_LateNice = run_tournament(tournament=tournament, list_agents=list_agents_LN, n_steps=t_max, render=False, name_expe='late-test', print_steps=False)

    tournament.reset()
    reset_agents(list_all_agents)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents = run_tournament(tournament=tournament, list_agents=list_all_agents, n_steps=t_max, render=False, name_expe="test_all_TFT", print_steps=False)

    tournament.reset()
    reset_agents(list_all_Nices)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_nices = run_tournament(tournament=tournament, list_agents=list_all_Nices, n_steps=t_max, render=False, print_steps=False)

    tournament.reset()
    reset_agents(list_all_Defectors)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_defectors = run_tournament(tournament=tournament, list_agents=list_all_Defectors, n_steps=t_max, render=False, print_steps=False)

    tournament.reset()
    reset_agents(list_agents_1Def)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents_1Egoist = run_tournament(tournament=tournament, list_agents=list_agents_1Def, n_steps=t_max, render=False, print_steps=False)

    tournament.reset()
    reset_agents(list_agents_1Coop)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents_1Nice = run_tournament(tournament=tournament, list_agents=list_agents_1Coop, n_steps=t_max, render=False, print_steps=False)

    tournament.reset()
    reset_agents(list_1Agent_all_Def)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents_1Agent_all_Def = run_tournament(tournament=tournament, list_agents=list_1Agent_all_Def, n_steps=t_max, render=False, print_steps=False)

    tournament.reset()
    reset_agents(list_1Nice_all_Def)
    print()
    print("#### RUN EVAL TOURNAMENT "+str(k)+'/'+str(N_runs))
    k += 1
    payoffs_agents_1Nice_all_Def = run_tournament(tournament=tournament, list_agents=list_1Nice_all_Def, n_steps=t_max, render=False, print_steps=False)


    curve_payoffs_LN = payoffs_agents_LateNice[0]
    curve_payoffs_agents = payoffs_agents[0]
    curve_payoffs_nices = payoffs_nices[0]
    curve_payoffs_1egoist = payoffs_agents_1Egoist[0]
    curve_payoffs_1nice = payoffs_agents_1Nice[0]
    curve_payoffs_egoists = payoffs_defectors[0]
    curve_payoffs_1Agent_allDef = payoffs_agents_1Agent_all_Def[0]
    curve_payoffs_1Nice_allDef = payoffs_agents_1Nice_all_Def[0]


    plt.plot(curve_payoffs_LN, label='Repentant defector', color = 'purple')
    plt.plot(curve_payoffs_agents, label='Agent vs (N-1) agents', color = 'orange')
    plt.plot(curve_payoffs_nices, label='Optimal - all cooperators', color = 'green')

    plt.plot(curve_payoffs_egoists, label='Worst - all defectors', color = 'brown')
    #plt.plot(curve_payoffs_1Agent_allDef, label='Agent vs all defectors', color = 'orange')
    #plt.plot(curve_payoffs_1Nice_allDef, label='Cooperator vs all defectors', color = 'green')
    plt.plot(curve_payoffs_1nice, label='Nice vs (N-1) agents', color='pink')
    plt.plot(curve_payoffs_1egoist, label = 'Egoist vs (N-1) agents', color = 'red')

    plt.legend(loc=0)
    plt.xlabel('steps')
    plt.ylabel('payoff')
    plt.savefig(metrics_fig)
    plt.clf()

    ef, evo_efficiency = efficiency(payoffs_agents, payoffs_nices, payoffs_defectors)
    sp = speed(evo_efficiency, delta_T=delta_T)
    ic = incentive_compatibility(curve_payoffs_1nice, curve_payoffs_1egoist, curve_payoffs_nices, curve_payoffs_egoists)
    sf = safety(curve_payoffs_1Agent_allDef, curve_payoffs_egoists, curve_payoffs_1Nice_allDef)
    #fg = forgiveness(payoffs_agents[0], payoffs_agents_LateNice[0], t_max=t_max, tau1=tau1, delta_T=delta_T)
    fg = forgiveness(payoffs_agents_LateNice, payoffs_nices, payoffs_defectors, tau1=t_coop_LN)


    print()
    print("Efficiency = ", ef)
    print("Speed = ", sp)
    print("IC = ", ic)
    print("Safety = ", sf)
    print("Forgiveness = ", fg)

    return [ef, sp, fg, ic, sf]


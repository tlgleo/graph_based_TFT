import numpy as np
from display_functions import *
from examples_graphs import *

class Tournament:

    def __init__(self, max_coop_matrix, debit_max, payoffs_list = [0,1,3,5], name_expe="expe"):
        assert len(max_coop_matrix.shape) == 2
        (n,m) = max_coop_matrix.shape
        assert m == n
        self.n_agents = n
        self.max_coop = max_coop_matrix
        self.debit_max = debit_max
        self.payoffs_IPD = payoffs_list
        self.rewards_agents = [[] for _ in range(self.n_agents)]
        self.coop_vectors = [np.zeros([self.n_agents, self.n_agents])]
        self.name_expe = name_expe
        self.step_t = 0
        self.last_rewards = np.zeros(self.n_agents)
        self.ext = '.png'
        self.optimal_graph = self.max_coop

    def reset(self):
        self.step_t = 0
        self.rewards_agents = [[] for _ in range(self.n_agents)]
        self.coop_vectors = [np.zeros([self.n_agents, self.n_agents])]
        self.last_rewards = np.zeros(self.n_agents)

    def get_obs(self):
        return self.coop_vectors[-1]

    def get_obs_perso(self, ident):
        # to modify
        return self.coop_vectors[-1]

    def prisoner_dilemma(self, c1, c2):
        (S,P,R,T) = self.payoffs_IPD
        r1 = c1*c2*R + (1-c1)*(1-c2)*P + c1*(1-c2)*S + c2*(1-c1)*T
        r2 = c1*c2*R + (1-c1)*(1-c2)*P + c1*(1-c2)*T + c2*(1-c1)*S
        return (r1,r2)

    def render(self, labels = ['A', 'B', 'C', 'D', 'E', 'F'], output_name = None):
        if not output_name:
            output_name = self.name_expe + '_' + str(self.step_t) + self.ext

        fig, axs = plt.subplots(1, 3, figsize=(25,10))
        list_rates = [1.0] * self.n_agents
        colors = ['gray'] * self.n_agents
        labels = labels[:self.n_agents]

        show_cooperation_graph(axs[0], labels, list_rates, self.max_coop,
                               max_rates=np.ones([self.n_agents, self.n_agents]), cmap='Blues')
        axs[0].set_title('Maximum Cooperation Graph', fontsize=20)

        show_cooperation_graph(axs[1], labels, list_rates, self.coop_vectors[-1], max_rates=self.max_coop, cmap='Greens')
        axs[1].set_title('Cooperation Graph\nStep '+str(self.step_t), fontsize=20)

        show_histo(axs[2], list(self.last_rewards), labels, colors, max_gain=9)
        axs[2].set_title('Current payoffs', fontsize=20)

        #plt.show()
        fig.savefig(output_name, transparent=False)
        plt.close(fig)


    def round(self, coop_vectors_matrix):
        # output = n_agents rewards
        assert len(coop_vectors_matrix.shape) == 2
        (n,m) = coop_vectors_matrix.shape
        assert m == n

        #accurate_coop_vectors_matrix = np.multiply(self.max_coop, coop_vectors_matrix)

        # capacities max of cooperation
        accurate_coop_vectors_matrix = np.minimum(self.max_coop, coop_vectors_matrix)

        # debit max of cooperation
        outgoing_flow = np.sum(accurate_coop_vectors_matrix, axis=1) + 1e-10
        normalise = np.minimum(1.0, np.array(self.debit_max)/outgoing_flow)

        for i in range(n):
            accurate_coop_vectors_matrix[i,:] *= normalise[i]

        rewards = np.zeros(self.n_agents)

        for i in range(self.n_agents):
            for j in range(self.n_agents):
                if i > j:
                    (c_i, c_j) = accurate_coop_vectors_matrix[i,j], accurate_coop_vectors_matrix[j,i]
                    (r_i, r_j) = self.prisoner_dilemma(c_i, c_j)
                    rewards[i] += r_i #* self.max_coop[j,i]
                    rewards[j] += r_j #* self.max_coop[i,j]


        #self.coop_vectors.append(coop_vectors_matrix)
        self.coop_vectors.append(accurate_coop_vectors_matrix)
        self.step_t += 1
        self.last_rewards = rewards

        for i,r in enumerate(rewards):
            self.rewards_agents[i].append(r)

        return rewards

# examples of tournaments

tournament_classic_2players = Tournament(Classic_2_players, debit_max_simple(2))

tournament_circular_3players = Tournament(Circular_3_players, debit_max_simple(3))
tournament_full_3players = Tournament(Full_3_players, debit_max_simple(3))
tournament_full_3players.optimal_graph = Circular_3_players

tournament_circular_4players = Tournament(Circular_4_players, debit_max_simple(4))
tournament_double_circular_4players = Tournament(Double_circular_4_players, debit_max_simple(4))
tournament_double_circular_4players.optimal_graph = Circular_4_players

tournament_circular_5players = Tournament(Circular_5_players, debit_max_simple(5))
tournament_double_circular_5players = Tournament(Double_circular_5_players, debit_max_simple(5))
tournament_double_circular_5players.optimal_graph = Circular_5_players

tournament_circular_6players = Tournament(Circular_6_players, debit_max_simple(6))
tournament_double_circular_6players = Tournament(Double_circular_6_players, debit_max_simple(6))
tournament_double_circular_6players.optimal_graph = Circular_6_players

tournament_random_6players = Tournament(Random_6_players, debit_max_simple(6))
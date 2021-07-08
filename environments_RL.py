from tournament import *
from agents import *

class Environment_TFT:
    # CREATE a N player env similar to Gym
    # with step()
    def __init__(self, tournament, list_agents_TFT, list_ident_TFT, list_ident_RL_agents,
                 r_norm=1.0):
        self.tournament = tournament
        self.payoffs_IPD = self.tournament.payoffs_IPD
        self.list_agents_TFT = list_agents_TFT
        self.list_ident_TFT = list_ident_TFT
        self.list_ident_RL_agents = list_ident_RL_agents
        self.n_TFT = len(self.list_agents_TFT)
        self.n_agents = self.tournament.n_agents
        self.t = 0
        self.reward_norm = r_norm if r_norm is not None else self.n_agents*self.payoffs_IPD[-1]
        self.steps_max = 10000

    def reset(self):
        self.t = 0
        for a in self.list_agents_TFT:
            a.reset()


    def step(self, actions):
        # list of (n_agents - n_TFT) actions
        assert (len(actions) + self.n_TFT) == self.n_agents

        #Creation of matrix of actions:
        obser_coop_matrix = self.tournament.get_obs()
        actions_matrix = np.zeros([self.n_agents, self.n_agents])

        # actions of TFT agents:
        for ident, a in zip(self.list_ident_TFT, self.list_agents_TFT):
            obs_coop = obser_coop_matrix
            action = a.act(obs_coop, self.t)
            actions_matrix[ident, :] = action

        for i, ident in enumerate(self.list_ident_RL_agents):
            action = actions[i]
            actions_matrix[ident, :] = action

        rewards = self.tournament.round(actions_matrix)

        rewards_RL = [rewards[k]/self.reward_norm for k in range(self.list_ident_RL_agents)]

        next_states = [actions_matrix] * len(self.list_agents_TFT)
        dones = [self.t >= self.steps_max] * len(self.list_agents_TFT)
        infos = []

        return next_states, rewards_RL, dones, infos


list
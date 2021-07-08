import numpy as np
import matplotlib.pyplot as plt
from display_functions import *
from tournament import *
from agents import *
import os



def run_tournament(tournament, list_agents, n_steps = 100,
                   name_expe = None, render = True, ext = '.png',
                   video_render = True,
                   print_every = 25, print_steps = True):

    tournament.reset()
    n_agents = tournament.n_agents
    assert n_agents==len(list_agents)

    names_agents = [a.name for a in list_agents]

    # CREATION of Paths for render - BEGIN
    if render:
        if not os.path.exists('./experiences/'):
            os.mkdir('./experiences/')
        if not name_expe:
            name_expe = tournament.name_expe
        if not os.path.exists('./experiences/'+ name_expe):
            os.mkdir('./experiences/'+ name_expe)
        path_render = './experiences/' + name_expe + '/images/'
        if not os.path.exists(path_render):
            os.mkdir(path_render)
    # CREATION of Paths for render - END

    # RUNNING tournament: n_steps
    for t in range(n_steps):
        obser_coop_matrix = tournament.get_obs()
        coop_vectors_matrix = np.zeros([n_agents, n_agents])
        for i,a in enumerate(list_agents):
            #obs_coop = obser_coop_matrix[i,:]
            obs_coop = obser_coop_matrix
            output_vectors = a.act(obs_coop, t)
            coop_vectors_matrix[i,:] = output_vectors
        tournament.round(coop_vectors_matrix)

        if render:
            output_fig = path_render + str(t) + ext
            tournament.render(names_agents, output_fig)
            plt.close()

        if print_steps:
            if t % print_every == 0:
                print("step " + str(t) + "/"+str(n_steps))

    # CREATION of video (with ffmpeg)
    if render and video_render:
        name_video = name_expe + '_video.mp4'
        r_video = 3
        r_video2 = 20
        video_command = "ffmpeg -r " + str(r_video)+ " -i %d.png -c:v libx264 -r " + str(r_video2) + " -pix_fmt yuv420p ../" + name_video
        video_command = "cd "+ path_render + "\n" + video_command
        os.system(video_command)

    # OUTPUTS the list of payoffs (evolution) of all agents
    return tournament.rewards_agents
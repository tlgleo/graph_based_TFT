from display_functions import *

def generate_double_graph(coop_max_matrix, coop_rates_matrix, current_payoffs, output_name,
                          fig_size = (28, 10), labels = ["A", "B", "C", "D", "E", "F", "G"],
                          colors = ["gray"]*10, max_gain = 10):

    fig, axs = plt.subplots(1, 3, figsize=fig_size)
    (n,_) = np.shape(coop_rates_matrix)
    list_rates = [1.0]*n
    show_cooperation_graph(axs[0], labels, list_rates, coop_max_matrix, max_rates=np.ones([n,n]), cmap='Blues')
    axs[0].set_title('Maximum Cooperation Graph', fontsize=20)
    show_cooperation_graph(axs[1], labels, list_rates, coop_rates_matrix, max_rates=coop_max_matrix, cmap='Greens')
    axs[1].set_title('Cooperation Graph', fontsize=20)

    show_histo(axs[2], current_payoffs, labels, colors, max_gain=max_gain)
    axs[2].set_title('Current payoffs', fontsize=20)

    fig.savefig(output_name, transparent=False)
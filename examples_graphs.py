import numpy as np

# Some examples of graph with adjacency matrix

Classic_2_players = np.array(
    [ [0.0, 1.0],
      [1.0, 0.0]
    ]
    )

Full_3_players = np.array(
    [ [0.0, 1.0, 1.0],
      [1.0, 0.0, 1.0],
      [1.0, 1.0, 0.0]
    ]
    )

Circular_3_players = np.array(
    [ [0.0, 1.0, 0.0],
      [0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0]
    ]
    )


Circular_4_players = np.array(
    [ [0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0, 0.0],
    ]
    )


Double_circular_4_players = np.array(
    [ [0.0, 1.0, 1.0, 0.0],
      [0.0, 0.0, 1.0, 1.0],
      [1.0, 0.0, 0.0, 1.0],
      [1.0, 1.0, 0.0, 0.0],
    ]
    )


Semi_circular_4_players = np.array(
    [ [0.0, 1.0, 0.5, 0.0],
      [0.0, 0.0, 1.0, 0.5],
      [0.5, 0.0, 0.0, 1.0],
      [1.0, 0.5, 0.0, 0.0],
    ]
    )

Circular_5_players = np.array(
    [ [0.0, 1.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0, 0.0, 0.0],
    ]
    )

Double_circular_5_players = np.array(
    [ [0.0, 1.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 1.0],
      [1.0, 0.0, 0.0, 0.0, 1.0],
      [1.0, 1.0, 0.0, 0.0, 0.0],
    ]
    )

Circular_6_players = np.array(
    [ [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    ]
    )

Double_circular_6_players = np.array(
    [ [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 1.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0, 1.0],
      [1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
      [1.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    ]
    )

Semi_circular_6_players = np.array(
    [ [0.0, 1.0, 0.5, 0.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.5, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 0.5, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0, 0.5],
      [0.5, 0.0, 0.0, 0.0, 0.0, 1.0],
      [1.0, 0.5, 0.0, 0.0, 0.0, 0.0],
    ]
    )


Random_6_players = np.array(
    [ [0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 0.0, 1.0],
      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
    ]
    )


# Vectors of source max (debit max) of cooperation
def debit_max_simple(n_agents):
    return [1.0] * n_agents

def debit_max_full(n_agents):
    return [1.0*n_agents] * n_agents

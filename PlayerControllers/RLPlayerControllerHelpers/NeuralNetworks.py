from typing import List
import torch.nn as nn
import torch_geometric.nn as tgnn

from CatanGame.Board import Board


class ActionTranslater(nn.Module):
    def __init__(self, in_dim: int,
                 hidden_dims: List[int],
                 representation_dim: int,
                 dropout: int = 0):
        """
        Translates an action to a latent representation understandable by main Q-net.
        Implementation: Multi layer perceptron
        :param in_dim: dimension of input representation of action
        :param hidden_dims: list of internal hidden layer dimensions
        :param representation_dim: dimension of output representation of action
        :param dropout: probability of performing dropout.  0 for no dropout
        """
        super().__init__()
        self.modules = []
        in_dim = in_dim
        for layer_dim in hidden_dims:
            self.modules.append(nn.Sequential(
                nn.Linear(in_features=in_dim, out_features=layer_dim),
                nn.ReLU(),
                nn.Dropout(p=dropout)
            ))
            in_dim = layer_dim
        self.modules.append(nn.Linear(in_features=in_dim, out_features=representation_dim))

        def forward(action):
            """
            :param action: Action to evaluate.  Shape=(inD,) where inD is in_dim given in __init__
            :return: representation of action.  Shape=(outD,) where outD is representation_dim given in __init__
            """
            assert self.modules
            for layer in self.modules:
                result = layer(action)
            return result

        def backward(grad):
            raise NotImplementedError() # TODO: implement



class Q_net(ActionTranslater):
    def __init__(self, in_dim: int, hidden_dims: List[int]):
        super().__init__(in_dim, hidden_dims, 1)


class BoardTranslater(nn.Module):
    def __init__(self,
                 GCN_hidden_channels: List[int],
                 perceptron_hidden_dims: List[int],
                 board_representation_dim: int,
                 dropout: int = 0):
        """
        Translates a the board to a latent representation understandable by main Q-net.
        Implementation: GCNConv+batchnorm layers followed by FC layers
        :param GCN_layer_num: number of GCNConv+batchnorm layers
        :param perceptron_hidden_dims: list of FC hidden layer dimensions
        :param board_representation_dim: dimension of output representation of board
        :param dropout: probability of performing dropout.  0 for no dropout
        """
        super().__init__()
        self.GCN_modules = []
        self.FC_modules = []

        #GCNConv+pooling+batchnorm+relu layers
        in_channels =
        for GCN_layer_channels in GCN_hidden_channels:
            self.GCN_modules.append(tgnn.GCNConv(in_channels=in_channels, out_channels=GCN_layer_channels))
            self.GCN_modules.append(nn.ReLU())
            self.GCN_modules.append(tgnn.BatchNorm(in_channels=GCN_layer_channels))
            in_channels = GCN_layer_channels

        # FC layers
        self.FC_modules.append(nn.Flatten())
        in_dim =  # TODO: calculate the output size from the Flatten module
        for FC_layer_dim in perceptron_hidden_dims:
            self.FC_modules.append(nn.Sequential(
                nn.Linear(in_features=in_dim, out_features=FC_layer_dim),
                nn.ReLU(),
                nn.Dropout(p=dropout)
            ))
            in_dim = FC_layer_dim
        self.FC_modules.append(nn.Linear(in_features=in_dim, out_features=board_representation_dim))

        def forward(board: Board):
            """
            :param board:
            :return: representation of board understandable by Q_net
            """
            result = board.graph.
            data = to_data(result)# TODO: convert board to torch_geometric.Data
            for layer_num in range(start=0, stop=len(self.GCN_modules), step=3):
                result, edge_index, edge_weights = data.x, data.edge_index, data.edge_weights
                result = self.GCN_modules[layer_num](result, edge_index, edge_weights)
                result = self.GCN_modules[layer_num + 1](result)
                result = self.GCN_modules[layer_num + 2](result)

            for layer in self.FC_modules:
                result = layer(result)
            return result

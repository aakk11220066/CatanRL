from typing import List
import torch.nn as nn
import torch_geometric.nn as tgnn
from math import inf as infinity

from CatanGame.Board import Board


class ThiefLocationTranslater(nn.Module):
    def __init__(self, proposed_thief_loc_dim: int,
                 hidden_dims: List[int],
                 thief_loc_representation_dim: int,
                 dropout: int = 0):
        """
        Translates a batch of possible new thief locations to a latent representation understandable by main Q-net.
        Implementation: Multi layer perceptron
        :param proposed_thief_loc_dim: dimension of input representation of new thief location
        :param hidden_dims: list of internal hidden layer dimensions
        :param thief_loc_representation_dim: dimension of output representation of new thief location
        :param dropout: probability of performing dropout.  0 for no dropout
        """
        super().__init__()
        self.modules = []
        in_dim = proposed_thief_loc_dim
        for layer_dim in hidden_dims:
            self.modules.append(nn.Sequential(
                nn.Linear(in_features=in_dim, out_features=layer_dim),
                nn.ReLU(),
                nn.Dropout(p=dropout)
            ))
            in_dim = layer_dim
        self.modules.append(nn.Linear(in_features=in_dim, out_features=thief_loc_representation_dim))

        def forward(proposed_thief_movements):
            """
            :param proposed_thief_movements: batch of possible movements.  Shape=(N, inD) where N is the size of batch
                and inD is proposed_thief_loc_dim given in __init__
            :return: batch of representations of proposed thief movements.  Shape=(N, outD) where N is the size of batch
                and outD is board_representation_dim given in __init__
            """
            for layer in self.modules:
                result = layer(proposed_thief_movements)
            return result

        def backward(grad):
            raise NotImplementedError() # TODO: implement

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

        #GCNConv+pooling+batchnorm layers
        in_channels =
        for GCN_layer_channels in GCN_hidden_channels:
            self.GCN_modules.append(tgnn.GCNConv(in_channels=in_channels, out_channels=GCN_layer_channels))
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
            for layer in self.modules:
                result = layer(result)
            return result
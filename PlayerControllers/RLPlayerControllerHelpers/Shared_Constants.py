from enum import Enum

REPLAY_MEM_SIZE = 20000
DROPOUT = 0.3
ACTION_LATENT_DIM = 5

THIEF_MOVEMENT_REP = 0
THIEF_MANIFEST_DIM = 2 # Coordinate
THIEF_HIDDEN_DIMS = [2]

TRADE_REP = 1
TRADE_MANIFEST_DIM = 2 # which resource to trade, to which
TRADE_HIDDEN_DIMS = [2]

# building type, card type (for development cards) OR coordinate1 (for buildings), coordinate2 (for road)
PURCHASE_REP = 2
PURCHASE_MANIFEST_DIM = 5
PURCHASE_HIDDEN_DIMS = [7]

GCN_HIDDEN_CHANNELS = [2, 2]
PERCEPTRON_DIM_COEFF = 2
BOARD_LATENT_DIM_COEFF = 2

QNET_HIDDEN_DIMS = [10, 5]

class ActionType(Enum):
    FIRST_BUILDING = 0
    SECOND_BUILDING = 1
    THIEF_PLACEMENT = 2
    BUILDINGS_PURCHASE = 3
    TRADE_RESOURCES = 4

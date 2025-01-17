Catan Reinforcement Learning platform


*Structure:*
 - CatanGame is played by mindless players with fields to guide their actions
 - PlayerControllers indirectly control these fields to set strategy for Players
 - Supervisor holds PlayerControllers and their corresponding GymInterfaces and a central CatanGame.
 - Supervisor asks each PlayerController in turn what its desired actions are (turn-phase by turn-phase) and passes these to the corresponding GymInterface, and passes along the returned observation and reward back to PlayerController
 - GymInterface holds link to central game held by Supervisor and carries out PlayerController's desires by giving the Players the requests from the PlayerControllers and then activating the relevant Player methods
 
*Observations:*
Observations consist of a tuple (Board, current resources available)

*Actions:*
Each action is a dictionary that must map the key "action_type" to a Shared_Values.ActionType.  Remaining key-value pairs is action-contextual.  Current actions implemented:
 - FIRST_BUILDING: action for building first buildings in game, at init time.  Contains contextual key 'building_locations' which is a dictionary mapping "settlement" and "road" to locations for the above
 - SECOND_BUILDING: action for building second buildings in game, at init time.  Contains contextual key 'building_locations' which is a dictionary mapping "settlement" and "road" to locations for the above
 - THIEF_PLACEMENT: action for rolling dice.  Contains a single contextual key 'desired_thief_location' describing where to move the thief if a 7 is rolled.
 - TRADE_RESOURCES: action for trading resources with the bank.  Contains a single contextual key 'desired_trades' mapped to a list of trade-tuples, each of which bears the resource to trade from (first element) and the resource to trade to (second element)
 - BUILDINGS_PURCHASE: action for purchasing buildings.  Contains a single contextual key 'purchases' which describes a dictionary of purchases to make (keyed by building to purchase, valued at coordinates for where to build these).

Each action assumes it was given legal input (although it will raise errors otherwise), please ensure legality of requests emanating from PlayerControllers.
To add a new action: add function signature to PlayerController (as an abstract method), implement in all inheritors from PlayerController, add treatment of action to GymInterface.step (i.e. pass along data to Player and then activate it), and implement activation method of Player for GymInterface to call.

*Reinforcement Learning agent:*
RLPlayerController class inherits from PlayerController and provides guidance to the Player it is assigned to via a Q-learning framework.  The input is run through relevant translaters (implemented with neural networks) implemented in NeuralNetwors.py to extract features from the input, and then presented to Q-net, a deep learning framework designed to make wise decisions about the optimal next move.  The Q-net is trained on randomly sampled experiences (state-action pairs) from the Replay Buffer, which is in turn supplied by the RLPlayerController upon receiving the results from its previous action.  The RL agent then makes an epsilon-greedy choice, deciding randomly with probability 1-epsilon if to follow the guidance provided by the Q-net and make the best choice based on its advice, or play a random action.  Currently the random action is uniformly distributed, however this may be implemented to make a multinomially advised choice instead, guided by the output from the Q-net.     
import pickle

from config import AlphaZeroConfig
from reinforcement_learning_train.util.action_encoder import ActionEncoder
from reinforcement_learning_train.util.stacked_state import StackedState
from model.state import State
from ai_modules.ai_elements import AIElements
from copy import deepcopy
import numpy as np
from reinforcement_learning_train.alpha_zero.mcts import MCTreeSearch
from reinforcement_learning_train.util.alphazero_util import parse_global_list_training, HelperTrainingExample, \
    mirror_stacked_state
from keras.models import clone_model

def fit_train(global_list_training, ae, model_deep_net,
              episode=AlphaZeroConfig.EPISODE,
              mtcs_sims=AlphaZeroConfig.MCTS_SIMULATION,
              best_model=None,
              greedy_episode=AlphaZeroConfig.GREEDY_EPISODE):
    """
    Train the model of neural network using the data generated from the MCTS simulation.
    :param global_list_training: the list of the data that will be used to the input of neural network
    :param ae: Action Encoder object
    :param model_deep_net: a Keras neural network model.
    :param episode: Number of game episodes
    :param mtcs_sims: Number of MCTS simulation
    :param best_model: a Keras neural network model which represents the best model
    :return:
    """
    if best_model is None:
        # If the training is from the start
        best_model = clone_model(model_deep_net.model)
        best_model.set_weights(model_deep_net.model.get_weights())
        best_model.save(AlphaZeroConfig.BEST_MODEL_PATH)

    for eps in range(episode):
        print("Episode %d" % (eps))
        print("==============")

        # If episode is below of 1/8 of episode, force attack or promote if possible.
        greed_is_good = True if eps < greedy_episode else False
        state = State()
        state.initial_state()
        stacked_state = StackedState(state)
        mcts = MCTreeSearch(model_deep_net.model, 1, mtcs_sims, ae, stacked_state)

        new_list_training = do_self_play_episode(stacked_state, mcts, ae, greed_is_good)
        global_list_training.extend(new_list_training)

        # Checkpoint list_training
        pickle.dump(global_list_training, open("global_list_training.p","wb"))
        deep_repr_state, action_proba, reward = parse_global_list_training(global_list_training)
        print("Fitting the model!")
        print("------------")
        model_deep_net.model.fit([deep_repr_state], [action_proba, reward],
                                 batch_size=AlphaZeroConfig.BATCH_SIZE_FIT,
                                 epochs=AlphaZeroConfig.EPOCHS_FIT)
        model_deep_net.model.save(AlphaZeroConfig.CURRENT_MODEL_PATH)
        print("------------")
        print("Arena!")

        dict_score = fight_agent(AlphaZeroConfig.BEST_MODEL_PATH,
                                 AlphaZeroConfig.CURRENT_MODEL_PATH, ae)
        from pprint import pprint
        print("Arena is done! 1: Best Model, 0: Current Model")
        pprint(dict_score)
        if dict_score[0] >= dict_score[1] * AlphaZeroConfig.WIN_DIFFERENCE_ARENA:
            # Change the best model
            print("Change Best Model!")
            best_model = clone_model(model_deep_net.model)
            best_model.set_weights(model_deep_net.model.get_weights())
        else:
            # Redo the trained model into previous best model
            print("Redo the current model into best model")
            model_deep_net.model = clone_model(best_model)

            # We need to do this to compile the model.
            model_deep_net.model.set_weights(model_deep_net.model.get_weights())
            from keras.optimizers import Adam
            model_deep_net.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(0.001))
        best_model.save("best_model.hdf5")
        model_deep_net.model.save("checkpoint.hdf5")

def fight_agent(best_model:str, current_model:str, ae,
                round_fight=AlphaZeroConfig.ROUND_ARENA,
                max_turn=AlphaZeroConfig.MAX_TURN_ARENA,
                max_simulation=AlphaZeroConfig.MAX_SIMULATION_ARENA):
    """
    The pitted 2 agents. We will check who is the best here.
    :param best_model: The current best model file path
    :param current_model: The current model file path
    :param ae: The Action Encoder
    :param round_fight: number of round to determine the winner
    :param max_turn: The maximum turn of the game. If the current turn is higher than max turn.
        It will be cut and the outcome of the game is draw.
    :param max_simulation: The maximum of simulation
    :return: dict, The dictionary of the score
    """
    from ai_modules.reinforcement_algorithm import AlphaZeroAgent

    loss_win = {
        0: 0,
        1: 0
    }
    for round in range(round_fight):
        print("ROUND {}".format(round+1))
        terminal = False
        count_turn = 1
        state = State()
        state.initial_state()
        best_model_agent = AlphaZeroAgent(state, max_simulation, best_model)  # 1
        current_model_agent = None # 0
        while not terminal and count_turn <= max_turn:
            print("=======TURN {} ========".format(count_turn))
            state.print_board()
            current_player_turn = state.get_player_turn()
            if current_player_turn == 1:
                key, dict_key = best_model_agent.choose_action(state)
                state = AIElements.result_function(state, dict_key)
                if current_model_agent is not None:
                    current_model_agent.enemy_turn_action(key, state)
            else:
                if current_model_agent is None:
                    current_model_agent = AlphaZeroAgent(state, max_simulation, current_model)
                key, dict_key = current_model_agent.choose_action(state)
                state = AIElements.result_function(state, dict_key)
                best_model_agent.enemy_turn_action(key, state)
            print("Player %d choose action %s" % (current_player_turn, key))

            game_ended = state.is_terminal()
            if game_ended:
                print("Player {} Win".format(count_turn % 2))
                loss_win[(current_player_turn) % 2] += 1
                terminal = True
            count_turn += 1
            if count_turn > max_turn:
                print("ROUND {} DRAW".format(round+1))
    return loss_win


def do_self_play_episode(
        stacked_state,
        mcts, ae:ActionEncoder,
        greed=False,
        pov=0,
        temperature_turn_end = AlphaZeroConfig.TEMPERATURE_END_STEP,
        greedy_turn = AlphaZeroConfig.GREEDY_TURN_MIN,
        max_turn_episode = AlphaZeroConfig.MAX_TURN_SIMULATION):
    """
    Self play an episode. This function will simulate MCTS every turns.
    :param stacked_state: The state that is stacked.
    :param mcts: a MCTS that will be simulated every turns.
    :param ae: Action Encoder
    :param greed: Hack that will be used to make the agent prioritize attacking and promoting.
    :param pov: The chosen point of view of player
    :param temperature_turn_end: Make the temperature to 0 on the given turn
    :return: Training data that will be appended to the global list of training data
    """
    terminal = False
    counter_step = 0
    list_training = []
    while not terminal:
        counter_step += 1
        print("Step : %d" % (counter_step))
        print("Turn : %d" % (stacked_state.head.turn))
        print("Player in state : %d" % (stacked_state.head.get_player_turn()))
        print("Player in tree : %d" % (mcts.root.stacked_state.head.get_player_turn()))

        temperature = 1
        if counter_step > temperature_turn_end:
            temperature = 0

        # Hack if counter_step > greedy_turn, greedily attack enemies
        if counter_step > greedy_turn and greed:
            print("Greedy Mode Activate")
            mcts.self_play(greed)
        else:
            mcts.self_play()
        action_proba = np.array(mcts.get_action_proba(temperature))

        action = np.random.choice(len(action_proba), p=action_proba)
        action_key = ae.inverse_transform([action])[0]
        possible_action = AIElements.get_possible_action(stacked_state.head)
        # Append list training
        if stacked_state.head.get_player_turn() != pov:
            training_data_tobe = HelperTrainingExample(mirror_stacked_state(deepcopy(stacked_state)),
                                                    (stacked_state.head.get_player_turn()),
                                                       ae.array_mirrored(action_proba))
        else:
            training_data_tobe = HelperTrainingExample(deepcopy(stacked_state),
                                                   stacked_state.head.get_player_turn(),
                                                   action_proba)
        print("Action_proba shape {}".format(action_proba.shape))

        list_training.append(training_data_tobe)

        # TODO : add v_treshold to cut
        stacked_state.head.print_board()
        print('Mirrored')
        mirror_stacked_state(deepcopy(stacked_state)).head.print_board()

        print("Player %d choose action %s" % (stacked_state.head.get_player_turn(), action_key))
        print("Next mean action value : %.4f" % (mcts.root.q_state_action[action_key]))

        new_state = AIElements.result_function(stacked_state.head, possible_action[action_key])
        stacked_state.append(new_state)
        mcts.update_root(action_key)
        
        terminal = stacked_state.head.is_terminal()
        if terminal:
            # Update the reward in list_training
            mcts.self_play()  # to fill the v variable
            reward = mcts.root.v # reward should be -1
            loser_player = stacked_state.head.get_player_turn()
            for i in list_training:
                if i.current_player == loser_player:
                    i.reward = reward
                else:
                    i.reward = -reward
        if counter_step > max_turn_episode:
            # Terminate episode, set reward to 0
            reward = 0
            for i in list_training:
                i.reward = reward
            terminal = True
        print("-----")
    return list_training
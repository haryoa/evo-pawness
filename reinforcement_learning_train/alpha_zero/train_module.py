import pickle

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

def fit_train(global_list_training, ae, model_deep_net, episode=100, mtcs_sims=25, best_model=None, maximizer=0):
    """
        Do num of iter
        TODO add rotate board
    """
    if best_model is None:
        best_model = clone_model(model_deep_net.model)
        best_model.set_weights(model_deep_net.model.get_weights())
        best_model.save("best_model.hdf5")

    for eps in range(episode):
        print("Episode %d" % (eps))
        print("==============")

        # If episode is below of 1/4 of episode, force attack
        greed_is_good = True if eps < 1/8 * episode else False
        #greed_is_good = False
        state = State()
        state.initial_state()
        stacked_state = StackedState(state)
        mcts = MCTreeSearch(model_deep_net.model, 1, mtcs_sims, ae, stacked_state)

        new_list_training = do_self_play_episode(stacked_state, mcts, ae, greed_is_good)
        global_list_training.extend(new_list_training)

        # Checkpoint list_training
        pickle.dump(global_list_training, open("global_list_training.p","wb"))
        deep_repr_state, action_proba, reward = parse_global_list_training(global_list_training)
        print("Fit mode on :)")
        print("------------")
        model_deep_net.model.fit([deep_repr_state], [action_proba, reward], batch_size=32, epochs=11)
        model_deep_net.model.save("checkpoint.hdf5")
        print("------------")
        print("FIGHT!!!")

        dict_score = fight_agent('best_model.hdf5', 'checkpoint.hdf5', ae)
        from pprint import pprint
        print("DONE!! 0: Best Model, 1: Current Model")
        pprint(dict_score)
        if dict_score[0] > dict_score[1] * 1.5:
            # CHANGE BEST MODEL
            print("Change Best Model!")
            best_model = clone_model(model_deep_net.model)
            best_model.set_weights(model_deep_net.model.get_weights())
        else:
            # REROLL CURRENT MODEL INTO BEST MODEL
            print("Redo the current model into best model")
            model_deep_net.model = clone_model(best_model)
            model_deep_net.model.set_weights(model_deep_net.model.get_weights())
            from keras.optimizers import Adam
            model_deep_net.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(0.001))
        best_model.save("best_model.hdf5")
        model_deep_net.model.save("checkpoint.hdf5")
        # (score_best, score_current) = fight(best_model, model_deep_net.model, ae, 4)
        # print("DONEE!! SCORE BEST %d - %d CURRENT"  % (score_best, score_current))
        # if score_current * 1.5 > score_best:
        #     print("CHANGE THE MBEST MODEL")
        #     best_model = clone_model(model_deep_net.model)
        #     best_model.set_weights(model_deep_net.model.get_weights())

def fight_agent(best_model:str, current_model:str, ae, round_fight=3, max_turn=200, max_simulation=27):
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
        best_model_agent = AlphaZeroAgent(state, 0, max_simulation, best_model) # 1
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
                    current_model_agent = AlphaZeroAgent(state, 0, max_simulation, current_model)
                key, dict_key = current_model_agent.choose_action(state)
                state = AIElements.result_function(state, dict_key)
                best_model_agent.enemy_turn_action(key, state)
            print("Player %d choose action %s" % (current_player_turn, key))

            game_ended = state.is_terminal()
            if game_ended:
                print("Player {} Win".format(count_turn % 2))
                loss_win[(current_player_turn + 1) % 2] += 1
                terminal = True
            count_turn += 1
            if count_turn > max_turn:
                print("ROUND {} RESULTED IN DRAW".format(round+1))
    return loss_win


def do_self_play_episode(stacked_state, mcts , ae:ActionEncoder, greed=False, maximizer=0, temperature_turn_end = 131):
    # TODO : ADD MAX
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

        # Hack if counter_step > 50, greedily attack enemies
        if counter_step > 50 and greed:
            print("Greedy Mode Activate")
            mcts.self_play_till_leaf(greed)
        else:
            mcts.self_play_till_leaf()
        action_proba = np.array(mcts.get_action_proba(temperature))

        action = np.random.choice(len(action_proba), p=action_proba)
        action_key = ae.inverse_transform([action])[0]
        possible_action = AIElements.get_possible_action(stacked_state.head)
        # Append list training
        if stacked_state.head.get_player_turn() != maximizer:
            training_data_tobe = HelperTrainingExample(mirror_stacked_state(deepcopy(stacked_state)),
                                                    (stacked_state.head.get_player_turn()),
                                                       ae.array_mirrored(action_proba))
        else:
            training_data_tobe = HelperTrainingExample(deepcopy(stacked_state),
                                                   stacked_state.head.get_player_turn(),
                                                   action_proba)
        print("Action_proba shape {}".format(action_proba.shape))
        # mirror_training = HelperTrainingExample(mirror_stacked_state(deepcopy(stacked_state)),
        #                                         (stacked_state.head.get_player_turn()+1)%2,
        #                                         ae.array_mirrored(action_proba))

        list_training.append(training_data_tobe)
        # list_training.append(mirror_training)

        # TODO : add v_treshold to cut
        stacked_state.head.print_board()
        print('Mirrored')
        mirror_stacked_state(deepcopy(stacked_state)).head.print_board()

        print("Player %d choose action %s" % (stacked_state.head.get_player_turn(), action_key))
        print("Next mean action value : %.4f" % (mcts.root.q_state_action[action_key]))
        # print("All Q_Value : ")
        # from pprint import pprint
        # pprint(mcts.root.num_state_action)
        new_state = AIElements.result_function(stacked_state.head, possible_action[action_key])
        stacked_state.append(new_state)
        mcts.update_root(action_key)
        
        terminal = stacked_state.head.is_terminal()
        if terminal:
            # Update the reward in list_training
            mcts.self_play_till_leaf()  # to fill the v variable
            reward = mcts.root.v # reward should be -1
            loser_player = stacked_state.head.get_player_turn()
            for i in list_training:
                if i.current_player == loser_player:
                    i.reward = reward
                else:
                    i.reward = -reward
        if counter_step > 250:
            # Terminate episode, set reward to 0
            reward = 0
            for i in list_training:
                i.reward = reward
            terminal = True
        print("-----")
    return list_training
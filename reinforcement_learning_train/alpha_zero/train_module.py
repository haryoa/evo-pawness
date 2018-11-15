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

def fit_train(global_list_training, ae, model_deep_net, episode=100, mtcs_sims=25, best_model=None):
    """
        Do num of iter
        TODO add rotate board
    """
    if best_model is None:
        best_model = clone_model(model_deep_net.model)
        best_model.set_weights(model_deep_net.model.get_weights())

    for eps in range(episode):
        print("Episode %d" % (eps))
        print("==============")

        # If episode is below of 1/4 of episode, force attack
        greed_is_good = True if eps < 1/4 * episode else False
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
        best_model.save("best_model.hdf5")
        print("------------")
        # print("FIGHT!!!")
        # (score_best, score_current) = fight(best_model, model_deep_net.model, ae, 4)
        # print("DONEE!! SCORE BEST %d - %d CURRENT"  % (score_best, score_current))
        # if score_current * 1.5 > score_best:
        #     print("CHANGE THE MBEST MODEL")
        #     best_model = clone_model(model_deep_net.model)
        #     best_model.set_weights(model_deep_net.model.get_weights())

def fight(best_model, current_model, ae, round_fight = 10):
    state = State()
    state.initial_state()
    stacked_state: StackedState = StackedState(state)
    score_best = 0
    score_current = 0
    mcts_best = None
    mcts_current = None
    ## First 25 best is first, then 25 best is last
    for isi in range(int(round_fight/2)):
        mcts_best = None
        mcts_current = None
        print("ROUND %d", isi )
        terminal = False
        count_turn = 0
        while not terminal and count_turn < 90:
            print("TURN %d" % count_turn)
            count_turn += 1
            if mcts_best is None:
                mcts_best = MCTreeSearch(best_model,1,25,ae,stacked_state) #BLACK
            stacked_state, action_key = best_turn_fight(mcts_best,ae,stacked_state)

            if mcts_current is not None:
                mcts_current.self_play_till_leaf()
                mcts_current.update_root(action_key)

            if stacked_state.head.is_terminal():
                terminal = True
                reward = stacked_state.head.sparse_eval(1)
                if reward > 0:
                    score_best += 1
                elif reward < 0:
                    score_current += 1

            if mcts_current is None:
                mcts_current = MCTreeSearch(current_model, 1, 25, ae, stacked_state)  # WHITE


            stacked_state, action_key = current_turn_fight(mcts_current, ae, stacked_state)
            mcts_best.self_play_till_leaf()
            mcts_best.update_root(action_key)

            if stacked_state.head.is_terminal():
                terminal = True
                reward = stacked_state.head.sparse_eval(1)
                if reward > 0:
                    score_best += 1
                elif reward < 0:
                    score_current += 1

    for isi in range(int(round_fight / 2)):
        print("ROUND %d" %(isi) )
        mcts_best = None
        mcts_current = None
        terminal = False
        count_turn = 0
        while not terminal and count_turn < 90:
            print("turn %d" % (count_turn))

            count_turn += 1

            if mcts_current is None:
                mcts_current = MCTreeSearch(current_model, 1, 25, ae, stacked_state)  # BLACK
            stacked_state,action_key = current_turn_fight(mcts_current, ae, stacked_state)
            if mcts_best is not None:
                mcts_best.update_root(action_key)

            if stacked_state.head.is_terminal():
                terminal = True
                reward = stacked_state.head.sparse_eval(1)
                if reward > 0:
                    score_current += 1
                elif reward < 0:
                    score_best += 1
            if mcts_best is None:
                mcts_best = MCTreeSearch(best_model, 1, 25, ae, stacked_state)  # BLACK

            stacked_state,action_key = best_turn_fight(mcts_best, ae, stacked_state)
            mcts_current.update_root(action_key)

            if stacked_state.head.is_terminal():
                terminal = True
                reward = stacked_state.head.sparse_eval(1)
                if reward > 0:
                    score_current += 1
                elif reward < 0:
                    score_best += 1
    return (score_best, score_current)

def best_turn_fight(mcts_best, ae, stacked_state):
    mcts_best.self_play_till_leaf()
    action_proba = np.array(mcts_best.get_action_proba())
    action = np.random.choice(len(action_proba), p=action_proba)
    action_key = ae.inverse_transform([action])[0]
    possible_action = AIElements.get_possible_action(stacked_state.head)
    new_state = AIElements.result_function(stacked_state.head, possible_action[action_key])
    stacked_state.append(new_state)
    mcts_best.update_root(action_key)
    return stacked_state, action_key

def current_turn_fight(mcts_current, ae, stacked_state):
    mcts_current.self_play_till_leaf()
    action_proba = np.array(mcts_current.get_action_proba())
    action = np.random.choice(len(action_proba), p=action_proba)
    action_key = ae.inverse_transform([action])[0]
    possible_action = AIElements.get_possible_action(stacked_state.head)
    new_state = AIElements.result_function(stacked_state.head, possible_action[action_key])
    stacked_state.append(new_state)
    mcts_current.update_root(action_key)
    return stacked_state, action_key

def do_self_play_episode(stacked_state, mcts , ae:ActionEncoder, greed=False):
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
        if counter_step > 31:
            temperature = 0

        # Hack if counter_step > 200, greedily attack enemies
        if counter_step > 60 and greed:
            print("Greedy Mode Activate")
            mcts.self_play_till_leaf(greed)
        else:
            mcts.self_play_till_leaf()
        action_proba = np.array(mcts.get_action_proba(temperature))
        print(action_proba.sum())
        action = np.random.choice(len(action_proba), p=action_proba)
        action_key = ae.inverse_transform([action])[0]
        possible_action = AIElements.get_possible_action(stacked_state.head)
        # Append list training
        training_data_tobe = HelperTrainingExample(deepcopy(stacked_state),
                                                   stacked_state.head.get_player_turn(),
                                                   action_proba)
        print("Action_proba shape {}".format(action_proba.shape))
        mirror_training = HelperTrainingExample(mirror_stacked_state(deepcopy(stacked_state)),
                                                stacked_state.head.get_player_turn(),
                                                ae.array_mirrored(action_proba))

        list_training.append(training_data_tobe)
        list_training.append(mirror_training)

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
            mcts.self_play_till_leaf()  # to fill the v variable
            reward = mcts.root.v
            for i in list_training:
                if i.current_player == stacked_state.head.get_player_turn():
                    i.reward = reward
                else:
                    i.reward = -reward
        if counter_step > 230:
            # Terminate episode, set reward to 0
            reward = 0
            for i in list_training:
                i.reward = reward
            terminal = True
        print("-----")
    return list_training
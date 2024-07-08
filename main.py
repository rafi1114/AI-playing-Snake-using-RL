import random
import numpy as np
from collections import deque
from game import Game
from plotter import plot
from qmodel import qsimple

LR = 0.01
MODE = 0 #0 for Training, 1 for Testing
class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.q_simple = qsimple(lr=LR, gamma=self.gamma, n_state=4096, n_action=4)

## Updated for my snake
    def get_state(self, gm, dir, snkx, snky, apx, apy):
        point_l = [snkx-40, snky] 
        point_r = [snkx+40, snky]
        point_u = [snkx, snky-40] 
        point_d = [snkx, snky+40] 
        
        dir_l = dir == 'left'
        dir_r = dir == 'right'
        dir_u = dir == 'up'
        dir_d = dir == 'down'

        state = [  
            # Danger left
            gm.bad_collision(point_l[0], point_l[1]),                                           #State contains the danger ahead, current direction, general food direction
            # Danger right
            gm.bad_collision(point_r[0], point_r[1]), 
            # Danger Up
            gm.bad_collision(point_u[0], point_u[1]),  
            # Danger Down
            gm.bad_collision(point_d[0], point_d[1]),
            
            # # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            apx < snkx,  # food left
            apx > snkx+40,  # food right
            apy < snky,  # food up
            apy > snky+40  # food down
            ]
        #print(state)
        return np.array(state, dtype=int)

    
    def train_qtable(self, state, action, reward, next_state, done, n_games):
        encoded_state = self.encode_state(state)
        encoded_next_state = self.encode_state(next_state)
        self.q_simple.q_train(encoded_state, action, reward, encoded_next_state, done, n_games)


    def q_action(self, statez):
        self.epsilon = 40000 - self.n_games
        encoded_state = self.encode_state(statez)
        if random.randint(0, 40000) < self.epsilon:
            move = random.randint(0, 3)
        else:
            prediction = self.q_simple.q_action(encoded_state)
            move = prediction
        return move
    
    def tested_action(self, statez):
        encoded_state = self.encode_state(statez)
        prediction = self.q_simple.tested_model(encoded_state)
        move = prediction
        return move

    
    def encode_state(self, state):
        encoded_state = 0
        factor = 1
        for value in state:
            encoded_state += value * factor
            factor *= 2  # Assuming binary features
        return encoded_state


def simple_train():
    plot_scores = []
    plot_mean_scores = []
    # total_score = 0
    # plot_rewards = []
    # plot_mean_rewards = []
    # total_reward = 0
    record = 0
    agent = Agent()
    game = Game()
    dir, snkx, snky, apx, apy = game.location()
    rolling_scores = deque(maxlen=20)
    # rolling_rewards = deque(maxlen=20)
    while True:
        if agent.n_games == 100000:
            break
        # get old state
        state_old = agent.get_state(game, dir, snkx, snky, apx, apy)
        #print(state_old)
        # get move
        final_move = agent.q_action(state_old)
        #print(final_move)

        # perform move and get new state
        reward, done, score = game.run(final_move, agent.n_games)
        #print(reward)
        state_new = agent.get_state(game, dir, snkx, snky, apx, apy)
        #print(state_new)

        # train short memory
        agent.train_qtable(state_old, final_move, reward, state_new, done, agent.n_games)

        dir, snkx, snky, apx, apy = game.location()

        if done:
            # train long memory, plot result
            agent.n_games += 1

            if score > record:
                record = score
                agent.q_simple.save_model()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot_rewards.append(reward)
            # rolling_rewards.append(reward)
            # if len(rolling_rewards) == 20:  # Ensure we have 20 scores before computing the mean
            #     mean_rewards = sum(rolling_rewards) / 20
            # else:
            #      mean_rewards = sum(rolling_rewards) / len(rolling_rewards)
            # plot_mean_rewards.append(mean_rewards)
            # plot(plot_rewards, plot_mean_rewards)

            plot_scores.append(score)
            rolling_scores.append(score)
            if len(rolling_scores) == 20:  # Ensure we have 20 scores before computing the mean
                mean_score = sum(rolling_scores) / 20
            else:
                 mean_score = sum(rolling_scores) / len(rolling_scores)
            plot_mean_scores.append(mean_score)
            #plot(plot_scores, plot_mean_scores)

            game.reset()

def simple_test():

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    plot_rewards = []
    plot_mean_rewards = []
    total_reward = 0
    record = 0
    agent = Agent()
    game = Game()
    dir, snkx, snky, apx, apy = game.location()
    rolling_scores = deque(maxlen=20)
    rolling_rewards = deque(maxlen=20)
    while True:
        if agent.n_games == 100000:
            break
        # get old state
        state_old = agent.get_state(game, dir, snkx, snky, apx, apy)
        #print(state_old)
        # get move
        final_move = agent.tested_action(state_old)
        #print(final_move)

        # perform move and get new state
        reward, done, score = game.run(final_move, agent.n_games)
        #print(reward)
        state_new = agent.get_state(game, dir, snkx, snky, apx, apy)
        #print(state_new)

        dir, snkx, snky, apx, apy = game.location()

        if done:
            # train long memory, plot result
            agent.n_games += 1
            if score > record:
                record = score

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            # plot_rewards.append(reward)
            # rolling_rewards.append(reward)
            # if len(rolling_rewards) == 20:  # Ensure we have 20 scores before computing the mean
            #     mean_rewards = sum(rolling_rewards) / 20
            # else:
            #      mean_rewards = sum(rolling_rewards) / len(rolling_rewards)
            # plot_mean_rewards.append(mean_rewards)
            # plot(plot_rewards, plot_mean_rewards)

            plot_scores.append(score)
            rolling_scores.append(score)
            if len(rolling_scores) == 20:  # Ensure we have 20 scores before computing the mean
                mean_score = sum(rolling_scores) / 20
            else:
                 mean_score = sum(rolling_scores) / len(rolling_scores)
            plot_mean_scores.append(mean_score)
            #plot(plot_scores, plot_mean_scores, training=False)

            game.reset()

if __name__ == '__main__':
    if MODE == 0:
        simple_train()
    else:
        simple_test()
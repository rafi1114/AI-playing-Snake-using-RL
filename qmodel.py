import numpy as np
import pickle

f = open('simple3.pkl', 'rb')
q_tested = pickle.load(f)
f.close()


class qsimple():
    def __init__(self, lr, gamma, n_state, n_action):
        self.q = np.zeros((n_state, n_action))
        self.learning_rate = lr
        self.gamma = gamma
        self.q_tested = q_tested


    def q_train(self, state, action, reward, new_state, done, n_games):
        if n_games == 40000:
            self.learning_rate = 0.001
        self.q[state, action] = self.q[state, action] + self.learning_rate * (reward + self.gamma*np.max(self.q[new_state,:])-self.q[state, action])
        state = new_state
        #print(self.q)

    def q_action(self, state):
        action = np.argmax(self.q[state, :])
        return action
    
    def save_model(self):
        f = open("simple4.pkl", "wb")
        pickle.dump(self.q, f)
        f.close()

    def tested_model(self, state): 
        action = np.argmax(self.q_tested[state, :])
        return action

if __name__ == '__main__':
    qsimple.q_train()
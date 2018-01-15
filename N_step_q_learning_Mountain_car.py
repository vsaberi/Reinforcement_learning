import gym
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from gym import wrappers
import datetime import datetime

#use some code already written
import Mountain_car_q_learning
from Mountain_car_q_learning import plot_cost_to_go, FeatureTransformer, Model, plot_running_average



class SGDRegressor:

    def __init__(self):
        self.w=None
        self.lr=10e-3

    def partial_fit(self,X,Y):

        if self.w is None:
            D=X.shape[1]
            w=np.random.random(D)/np.sqrt(D)
        self.w+=self.lr*(Y-X.dot(self.w)).dot(X)

    def predict(self,X):
        return X.dot(self.w)


#replace SKLearn Regressor
Mountain_car_q_learning.SGDRegressor=SGDRegressor




def play_episode(env,model,eps,gamma,n=5):
    s=env.reset()
    done=False
    totalrewards=0
    rewards=[]
    states=[]
    actions=[]
    t=0

    #array of [gamma^0, gamma^1, ...., gamma^(n-1)]
    multiplier=np.array([gamma]*n)**np.arange(n)

    while not done and t<200:

        action=model.greedy_policy(s,eps)
        states.append(s)
        actions.append(action)

        s_previous=s
        s,reward,done,info=env.step(action)

        rewards.append(reward)


        if len(rewards)>=n:

            G=multiplier.dot(rewards[-n:])+(gamma**n)*np.max(model.predict(s)[0])
            model.update(states[-n],actions[-n],G)

        totalrewards+=reward
        t+=1

    #empty the cache (keep only n-1 last observations)
    rewards=rewards[-n+1:]
    states=states[-n+1:]
    actions=actions[-n+1:]



    #given n-1 last observations we do not have enough rewards to use N-step method
    #if the mission is successful we consider some extra 0 rewards
    #if the mission id failed we consider some extra -1 rewards

    if t<200:          #successful

        while len(rewards)>0:

            G=multiplier[:len(rewards)].dot(rewards)
            model.update(states[0],actions[0],G)
            rewards.pop(0)
            states.pop(0)
            actions.pop(0)

    else:

        while len(rewards)>0:

            G=multiplier.dot(rewards+)







"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value


# START EDITING HERE
def KL(x,y) :
    if x == 0 :
        return (1-x)*math.log((1-x)/(1-y))
    elif x == 1 :
        return x*math.log(x/y)
    return x*math.log(x/y) + (1-x)*math.log((1-x)/(1-y))

def find_sol(values, upper_bound) :
    
    epsilon = 1e-4
    l=np.copy(values)
    r=np.ones(values.shape[0])
    for i in range(values.shape[0]) :
        while r[i] - l[i]  > epsilon :
            m =  (r[i] + l[i])/2
            kl_value = KL(values[i],m) 
            if kl_value < upper_bound[i]  :
                l[i] = m
            elif kl_value > upper_bound[i] :
                r[i] = m
            else :
                l[i] = m
                r[i] = m
    return (l+r)/2            
# You can use this space to define any helper functions that you need
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)        
        self.curr_time = 0
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if ( self.curr_time < self.counts.shape[0]) :
            return self.curr_time
        return np.argmax(self.values[self.counts != 0] + np.sqrt(2*np.log(self.curr_time)/self.counts[self.counts!=0]))
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        self.curr_time +=1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE
        


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)        
        self.curr_time = 0
        self.c = 3
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        if ( self.curr_time < self.counts.shape[0]) :
            return self.curr_time
        return np.argmax(find_sol(self.values,(math.log(self.curr_time)+self.c*math.log(math.log(self.curr_time)))/self.counts))
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.counts[arm_index] += 1
        self.curr_time +=1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value
        # END EDITING HERE


class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.success = np.zeros(num_arms)
        self.failures = np.zeros(num_arms)        
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(np.random.beta(self.success+1,self.failures+1))
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        if ( reward == 1) :
            self.success[arm_index] += 1
        else :
            self.failures[arm_index] += 1
        # END EDITING HERE

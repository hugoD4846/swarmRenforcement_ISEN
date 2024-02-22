import random
import math
import gymnasium as gym
import numpy as np
import swarmbot
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from swarmbot.envs.model.agent import Agent
from swarmbot.envs.swarm_bot_game import SwarmBotGame

GAMMA = 0.99
NUM_EPISODES = 10001
SHOW_EVERY = 1000
MIN_EXPLORE_RATE = 0.01
MIN_LEARNING_RATE = 0.9
NUMBER_OF_ENTITY = 1
 
env = gym.make('swarmbot:isen/swarmbot-v0.1', nb_entity=NUMBER_OF_ENTITY, render_mode = "human")

Q = np.random.rand(99999999, 5)
print(Q)
learning_curv = []
winrate = []

def get_Box(obv):
    target_x, target_y, dist_agent, angle_agent, x, y, angle, agent_repartition = obv
    
    box_number = 0
    box_number += math.ceil((target_x+15) * 9/(SwarmBotGame.WINDOW_WIDTH+30))
    box_number += math.ceil((target_y+15) * 9/(SwarmBotGame.WINDOW_HEIGHT+30)) * (10**1)
    box_number += math.ceil((dist_agent + 1) * 9/Agent.AGENT_VISION_SIZE) * (10**2)
    box_number += math.ceil((angle_agent + 1) * 9/Agent.AGENT_VISION_ANGLE) * (10**3)
    box_number += math.ceil((x+15) * 9/(SwarmBotGame.WINDOW_WIDTH+30)) * (10**4)
    box_number += math.ceil((y+15) * 9/(SwarmBotGame.WINDOW_HEIGHT+30)) * (10**5)
    box_number += math.ceil((angle) * 9/(360)) * (10**6)
    box_number += math.ceil((agent_repartition)) * (10**7)

    return box_number

def update_explore_rate(episode):
    return max(MIN_EXPLORE_RATE, min(1, 1.0 - np.log10((episode + 1) / 25)))

def update_learning_rate(episode):
    return max(MIN_LEARNING_RATE, (min(0.5, 1.0 - np.log10((episode + 1) / 50))))

def update_action(state, explore_rate):
    if random.random() < explore_rate:
        return env.action_space.sample()
    else:
        return np.argmax(Q[state])

def q_learn():
    global learning_curv
    global winrate
    total_reward = 0
    total_completions = 0
    explore_rate = update_explore_rate(0)
    learning_rate = update_learning_rate(0)
    
    for i in range(NUM_EPISODES):
        
        if i%SHOW_EVERY==0:
            render_mode = "human"
        else:
            render_mode = None
        env = gym.make('swarmbot:isen/swarmbot-v0.1', nb_entity=NUMBER_OF_ENTITY, render_mode = render_mode)
        observations = env.reset()[0]
        state_tab = [[get_Box(observation),0]for observation in observations]
        for _ in range(7200):
            for id_entity, state in enumerate(state_tab):
                env.render()
                action = update_action(state[0], explore_rate)
                observation, reward, terminated, truncated, info = env.step((id_entity, action) )
                total_reward += reward
                if render_mode == "human":
                    print(observation)
                state[1] = get_Box(observation)

                Q[state[0], action] += learning_rate*(reward + GAMMA*np.amax(Q[state[1]])- Q[state[0], action])
                state[0] = state[1]
                if truncated:
                    break
                if terminated:
                    total_completions += 1
                    break
            
            if truncated or terminated:
                break
        
        total_reward /= NUMBER_OF_ENTITY
        learning_rate = update_learning_rate(i)
        explore_rate = update_explore_rate(i)
        print("Completions : ", total_completions)
        print("REWARD/TIME: ", total_reward/(i+1))
        learning_curv.append((total_reward/(i+1)))
        print("Trial: ", i)
        print("Win Rate: ", (total_completions / (i+1)) * 100)
        winrate.append(((total_completions / (i+1)) * 100))
        #print("Final Q values: ", Q)
    env.close()

q_learn()
figure, axis = plt.subplots(1, 2)
axis[0].plot(learning_curv, color='g', label='learning_curv')
axis[1].set_ylim([0, 100])
axis[1].plot(winrate, color='r', label='winrate')
plt.show()
# x = np.linspace(0, 9, 10).astype(int)
# y = np.linspace(0, 9, 10).astype(int)
# z = np.zeros((100,)).astype(int)
# _x,_y = np.meshgrid(x, y)
# X, Y = _x.ravel(), _y.ravel()
# position_related_data = np.array_split(Q, 99)
# for idx, position in enumerate(position_related_data):
#     decision_map = list(map(np.argmax, position))
#     z[idx] = max(decision_map, key=decision_map.count)
# ax = plt.axes(projection='3d')
# bottom = np.zeros_like(z)
# width = depth = 1
# ax.bar3d(X, Y, bottom, width, depth, z, shade=True)
# plt.show()

# episodes = 100
# show_every = 1
# for episode in range(episodes):
#     if episode%1000 == 0:
#         print("Episode " + str(episode))
#     if episode%show_every==0:
#         render_mode = "human"
#     else:
#         render_mode = None
#     state = env.reset()
#     terminated = truncated = False
#     while not (terminated or truncated):
#         action = env.action_space.sample()  # this is where you would insert your policy
#         observation, reward, terminated, truncated, info = env.step(action)
# env.close()

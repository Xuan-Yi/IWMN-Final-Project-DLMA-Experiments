from sim_tools.configs.basic_config import BasicConfig
from sim_tools.environments.basic_env import BasicEnvironment
from sim_tools.plot_funcs.plot_throughput import PlotThroughput

import numpy as np

import os
import tensorflow as tf

from keras.models import Model
from keras.layers import Dense, Input, Add
from keras.optimizers import RMSprop, Adam
from keras.initializers import glorot_normal

import matplotlib.pyplot as plt
from tqdm import tqdm

EXPERIMENT_NAME = '1 TDMA + 1 EB-ALOHA'

# configs
config = BasicConfig()
config.n_DQN = 0
config.n_TDMA = 1
config.n_EB_Aloha = 1
config.n_q_Aloha = 0

config.max_iter = 1000
config.N = 100
config.alpha = 1  # default 0


# environment
env = BasicEnvironment()

agent_reward_list = []
tdma_reward_list = []
eb_Aloha_reward_list = []
q_Aloha_reward_list = []

# simulation
for i in tqdm(range(config.max_iter)):
    dqn_rewards, tdma_rewards, eb_Aloha_rewards, q_Aloha_rewards = env.step()

    agent_reward_list.append(dqn_rewards)
    tdma_reward_list.append(tdma_rewards)
    eb_Aloha_reward_list.append(eb_Aloha_rewards)
    q_Aloha_reward_list.append(q_Aloha_rewards)

# save results
agent_arr = np.array(agent_reward_list, dtype=np.float32)
tdma_arr = np.array(tdma_reward_list, dtype=np.float32)
eb_Aloha_arr = np.array(eb_Aloha_reward_list, dtype=np.float32)
q_Aloha_arr = np.array(q_Aloha_reward_list, dtype=np.float32)

M, E, F, B, X, W, q = config.M, config.E, config.F, config.B, config.X, config.W, config.q
n_DQN, n_TDMA, n_EB_Aloha, n_q_Aloha = config.n_DQN, config.n_TDMA, config.n_EB_Aloha, config.n_q_Aloha
max_iter = config.max_iter

if not os.path.isdir('./rewards'):
    os.mkdir('./rewards')
file_path = f'rewards/{EXPERIMENT_NAME}_rewards_dqn{n_DQN}_t{n_TDMA}_ea{n_EB_Aloha}_qa{n_q_Aloha}_M{M}_E{E:.0E}_F{F}_B{B}_X{X}_W{W}_q{q}_{max_iter:.0E}.npz'
np.savez(file_path, agent=agent_arr, tdma=tdma_arr,
         eb_Aloha=eb_Aloha_arr, q_Aloha=q_Aloha_arr)

# plot throughput
fig1 = plt.figure()
PlotThroughput(file_path, config)

plt.show()
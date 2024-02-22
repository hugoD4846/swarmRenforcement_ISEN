import gymnasium as gym
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()

episodes = 100000
show_every = 10000
for episode in range(episodes):
    if episode%1000 == 0:
        print("Episode " + str(episode))
    if episode%show_every==0:
        render_mode = "human"
    else:
        render_mode = None
    env = gym.make('swarmbot:isen/swarmbot-v0.1', nb_entity=1, render_mode = render_mode)
    state = env.reset()
    terminated = truncated = False
    while not (terminated or truncated):
        action = env.action_space.sample()  # this is where you would insert your policy
        observation, reward, terminated, truncated, info = env.step(action)
env.close()

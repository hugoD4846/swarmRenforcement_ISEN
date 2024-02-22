from gymnasium.envs.registration import register

register(
     id="isen/swarmbot-v0.1",
     entry_point="swarmbot.envs:SwarmBotGame",
     max_episode_steps=300,
)
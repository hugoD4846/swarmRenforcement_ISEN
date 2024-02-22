import math
from typing import Any
import random
import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces
from .model.agent import Agent
from .model.target import Target
from .model.entity import Entity

BG_COLOR = "#2c3e50"
ENTITY_SPACING = 100

class SwarmBotGame(gym.Env):
    speed = 0
    v_angle = 0
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 60}
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH = 400
    def __init__(self, nb_entity : int, render_mode=None) -> None:
        self.observation_space = spaces.Box(
            low=np.array([-1, -1, -1, -1, 0, 0, 0, 0]).astype(int),
            high=np.array([
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT,
                Agent.AGENT_VISION_SIZE,
                Agent.AGENT_VISION_ANGLE,
                self.WINDOW_WIDTH,
                self.WINDOW_HEIGHT,
                360,
                np.std([0, 7200])
                ]).astype(int),
        )
        self.action_space = spaces.Discrete(5)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.nb_entity = nb_entity
        self.window = None
        self.clock = None
        self.font = None
        self.entities : list[Agent] = []
        self.target = None
        self.target_in_vision_streak = np.zeros(nb_entity)
        self.stationnary_streak = np.zeros(nb_entity)
        self.agent_repartition = np.zeros((nb_entity, 10, 10))
        

    def _get_obs(self, agent: Agent, on_agent_repartition_update: bool):
        
        if agent.know_target_position:
            obs = [
                self.target.x,
                self.target.y,
                -1,
                -1
            ]
        else :
            obs = [-1]*4
        obs.append(agent.x)
        obs.append(agent.y)
        obs.append(agent.angle)
        obs.append(1 if on_agent_repartition_update else 0)
        return obs

    def _get_info(self, agent):
        return {
            "distance avec target": agent.get_dist_with_entity(self.target),
        }

    def reset(self, *, seed = None, options = None) -> tuple[Any, dict[str, Any]]:
        super().reset(seed=seed, options=options)
        self.agent_repartition = np.zeros((self.nb_entity,10, 10))
        modulo_square = math.ceil(self.nb_entity ** .5)
        nb_row =  math.ceil(self.nb_entity / modulo_square)
        self.entities : list[Agent] = []
        for entity_id in range(self.nb_entity):
            row = entity_id // modulo_square
            self.entities.append(
                Agent(
                    entity_id,
                    ((self.WINDOW_WIDTH - ((modulo_square - 1) * ENTITY_SPACING))// 2)
                    +
                    ((ENTITY_SPACING * (entity_id % modulo_square) )),
                    ((self.WINDOW_HEIGHT - ((nb_row - 1) * ENTITY_SPACING))// 2)
                    +
                    ((ENTITY_SPACING * (row) ))
                )
            )

        self.target = Target(-1, random.randint(self.WINDOW_WIDTH//10,self.WINDOW_WIDTH*0.9), random.randint(self.WINDOW_HEIGHT//10,self.WINDOW_HEIGHT*0.9))
        self.target_in_vision_streak = np.zeros(self.nb_entity)
        self.stationnary_streak = np.zeros(self.nb_entity)
        if self.render_mode == "human":
            self._render_frame()

        return [self._get_obs(entity, False)for entity in self.entities], self._get_info(self.entities[0])

    def controller(self, entity_id, entity: Agent ,action):
        if action == 0:
            entity.move(0,Entity.ENTITY_SIZE / 2)
        if action == 1:
            entity.move(Agent.AGENT_VISION_ANGLE/3 ,0)
        if action == 2:
            entity.move(-(Agent.AGENT_VISION_ANGLE/3),0)
        if action == 3:
            pass
        if action == 4:
            entity.attack(self)
        entity.is_out_of_bound = (
            (
                entity.x < 0
                or
                entity.x > self.WINDOW_WIDTH
            )
            or
            (
                entity.y < 0
                or
                entity.y > self.WINDOW_HEIGHT
            )
        )
        if not entity.is_out_of_bound:
            self.agent_repartition[entity_id][round(entity.y* (9/(self.WINDOW_HEIGHT)))][round(entity.x* (9/(self.WINDOW_WIDTH)))] = 1
    
    def step(self, action):
        entity_id = action[0]
        entity: Agent = self.entities[entity_id]
        action = action[1]
        prev_position = (entity.x, entity.y)
        target_in_vision_prev_action = entity.is_in_vision(self.target)
        agent_repartition_prev_action = sum(np.count_nonzero(x) for x in self.agent_repartition[entity_id])
        self.controller(entity_id, entity, action)
        target_in_vision_post_action = entity.is_in_vision(self.target)
        if target_in_vision_post_action:
            entity.know_target_position = True
        agent_repartition_post_action = sum(np.count_nonzero(x) for x in self.agent_repartition[entity_id])
        
        # STREAK
        if (target_in_vision_prev_action and target_in_vision_post_action):
            self.target_in_vision_streak[entity_id] += 1
        else:
            self.target_in_vision_streak[entity_id] = 0
            
        if (target_in_vision_post_action and prev_position == (entity.x, entity.y)):
            self.stationnary_streak[entity_id] += 1
        else:
            self.stationnary_streak[entity_id] = 0
        observation = self._get_obs(entity, agent_repartition_post_action != agent_repartition_prev_action)
        
        info = self._get_info(entity)
        reward = (
            (
                900 if target_in_vision_post_action
                else 0
            ),
            -
            (
                (200 * self.stationnary_streak[entity_id]) if not target_in_vision_post_action else 0
            ),
            +
            (
                50 * self.target_in_vision_streak[entity_id]
            ),
            +
            (
                50000 if (action == 4 and target_in_vision_post_action) else 0
            ),
            -
            (
                2000 if ((not target_in_vision_post_action) and target_in_vision_prev_action) else 0
            ),
            -
            (
                (10 * (100 - agent_repartition_post_action) if (action != 0 and not target_in_vision_post_action )else 0)
            ),
            -
            (
                100000 if entity.is_out_of_bound else 0
            ),
        )
        
        if self.render_mode == "human":
            print(reward)
        reward = sum(reward)

        if self.render_mode == "human":
            self._render_frame()
        
        if entity.is_out_of_bound:
            print("OUT OF BOUND")

        return observation, reward, self.target.health < 0, sum(entity.is_out_of_bound == 1 for entity in self.entities), info

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
        return None

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.font.init()
            self.font = pygame.font.SysFont('Comic Sans MS', 30)
            self.window = pygame.display.set_mode(
                (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
            )
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.fill(BG_COLOR)
            for entity in self.entities:
                entity.render(self)
            self.target.render(self)
            pygame.event.pump()
            pygame.display.flip()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
            return None
        return np.transpose(
            np.array(pygame.surfarray.pixels3d(self.window)), axes=(1, 0, 2)
        )

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

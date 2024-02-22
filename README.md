# swarmRenforcement_ISEN

swarmRenforcement is an IA model to solve the question:

> how to find and treat a target using a swarn of agent.

## Objectives

A target is placed randomly on an empty field 5 agents are placed in the center of the field.

Once the target is found it can be attacked removing 1 hp per seconds and per agent attacking 

The target has 50 hp points

The goal is too remove target the quickest

## Agent capabilities

### Observation


#### vision

| Num | Action      | Min | Max | type |
|-----|-------------|-----|-----|------|
|  0  |dist_target  |  -1 | 150 | int  |
|  1  |angle_target |  -1 | 90  | int  |
|  4  |dist_agent   |  -1 | 150 | int  |
|  5  |angle_agent  |  -1 | 90  | int  |
|  4  |agent_x      |  0  | window_width | int  |
|  5  |agent_y      |  0  | window_height  | int  |

hit box forward detecting :
  - other agents (including their found state)
  - target
  - walls

### Action

#### Direction

| Num | Action |
|-----|--------|
|  0  |forward |
|  1  |left    |
|  2  |right   |
|  3  |signal  |
|  4  |attack  |

- go forward 10 unit
- tilt left 10 degree
- tilt right 10 degree
- send a found signal to a 150 units radius
- transmit found signal to a 150 units radius
- attack in a range of 50 units removing 1 hp per sec if target is in range

## Road Map
- game environment
- single agent
- multiple agents
- multiple communicated agent

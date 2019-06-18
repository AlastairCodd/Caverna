import tensorflow as tf
from gym import Env

class GameRunner(object):
    def __init__(
		self, 
		model, 
		env: Env, 
		memory, 
		max_eps, 
		min_eps,
        decay, 
        render: bool = True):
        self._env = env
        self._model = model
        self._memory = memory
        self._render = render
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._decay = decay
        self._eps = self._max_eps
        self._steps = 0
        self._reward_store = []
        self._max_x_store = []
       
    def run(self):
        observation = self._env.reset() #this is a vector in input space
        
        while True:
            for player in self._players
                action = player._choose_action(observation) #this is a vector in output space
                post_player_observation, reward, done, info = self._env.step(action)
import tensorflow as tf

class GameRunner(object):
    def __init__(
		self, 
		sess: tensorflow,
		model, 
		env, 
		memory, 
		max_eps, 
		min_eps,
        decay, render=True):
        self._sess = sess
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
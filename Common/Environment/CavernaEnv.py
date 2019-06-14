from gym import Env

class CavernaEnv(Env):
	
	def reset(self):
		raise NotImplementedError()
        
    def render(self):
        raise NotImplementedError()
        
    def step(self, action):
        raise NotImplementedError()
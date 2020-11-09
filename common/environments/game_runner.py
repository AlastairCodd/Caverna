from typing import List

import tensorflow as tf
from gym import Env
from numpy import random, array


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
        self._env = None
        self._model = model  # a tensorflow model object
        self._memory = memory  # where the (observation, action, next_observation, reward, info) is stored
        self._render: bool = render
        self._max_eps: float = max_eps
        self._min_eps: float = min_eps
        self._decay: float = decay

        self._eps: float = self._max_eps  # initialise the epsilon value
        self._max_invalid_actions_per_turn: int = 3

    def run(self):
        s = self._env.reset()  # t his is a vector in input space

        current_invalid_actions: List[array] = []
        if len(current_invalid_actions) < self._max_invalid_actions_per_turn:
            q_s_a: array = self._choose_action( s ) # this is a vector in output space

            (next_s, r, done, info) = self._env.step(q_s_a)
            # next state here is from the perspective of the next player (player id is for next player, as well as

            if done:
                if "invalid reason" in info:
                    self._memory.add_failed_sample(s, q_s_a, next_s, r, info["invalid reason"])
                else:
                    self._memory.add_successful_sample(s, q_s_a, next_s, r)
                    return
            else:
                self._memory.add_successful_sample(s, q_s_a, next_s, r)
                return

        # for each player
            # do
            # get next action given current state and previous invalid actions
                # -> [card type, card args[input choice, additional args], resource conversions, dwarf used]
            # apply action
                # -> [next state for next player, reward, done, info]
            # if done and info contains "invalid reason"
                # then if there is a retry available
                    # add action to invalid actions
                    # retrpoiny from get next action
            # add (observation, action, next state, reward, info) to memory
            # convert next_state into next_state_for_next_player
            # set observation to next_state_for_next_player

    def _choose_action(self, state: array) -> array:
        """Get either a random (but valid) action or the result of the network

        :param state: The current state of the system. This cannot be null. 
        :return: Returns an array of floats, length of which is the number of outputs of the model
        """
        if state is None:
            raise ValueError("Observation state cannot be null.")
        if random.random() < self._eps:
            return self._env.get_random_action()
        else:
            return self._model.predict_one(state)
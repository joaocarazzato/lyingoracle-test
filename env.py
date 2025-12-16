import random
from typing import Tuple
from verifiers.types import Messages, State
import verifiers as vf

class LyingOracleEnv(vf.MultiTurnEnv):
    def __init__(self, lowest_number, max_number, max_steps: int = 100, hidden: int = None):
        self.lowest_number = lowest_number if lowest_number is not None else 1
        self.max_number = max_number if max_number is not None else 100
        self.hidden = hidden if hidden is not None else random.randint(self.lowest_number, self.max_number)
        self.t = 0
        self.max_steps = max_steps
        self.done = False

        print(f"[DEBUG] Hidden number is {self.hidden}")

    def step(self, action: int):
        liar_oracle_threshold = 4  # Muda mais cedo para testar

        self.t += 1

        # verdade objetiva
        truth = self.hidden > action

        # oracle mente após t >= liar_oracle_threshold
        oracle_answer = truth if self.t < liar_oracle_threshold else not truth

        # reward POR PASSO
        reward = 1.0 if action == self.hidden else -0.01

        if action == self.hidden or self.t >= self.max_steps:
            self.done = True

        obs = {
            "oracle_answer": oracle_answer,
            "t": self.t
        }

        return obs, reward, self.done, "Truth" if self.t < liar_oracle_threshold else "Lying"


    async def env_response(self, messages: Messages, state: State, **kwargs) -> Tuple[Messages, State]:

        action = int(messages[-1]["content"])
        obs, reward, done = self.step(action)

        # resposta mínima do oracle
        response = str(obs["oracle_answer"])

        # estado opcional (útil para o agente)
        state = {
            "t": obs["t"],
            "reward": reward,
            "done": done
        }

        return messages + [
            {"role": "environment", "content": response}
        ], state

# agent.py
import random

class LyingOracleAgent:
    def __init__(self, lowest_number, max_number):
        self.lower = lowest_number if lowest_number is not None else 1
        self.upper = max_number if max_number is not None else 100

        self.oracle_truthful = True
        self.contradictions = 0
        self.max_contradictions = 3  # Número de contradições antes de mudar a hipótese
        self.prev_interval_size = self.upper - self.lower
        self.stagnation = 0
        self.max_stagnation = 5
        self.query_history = {}  # k -> oracle_answer
        self.flip_evidence = 0
        self.max_flip_evidence = 2
        self.initial_lower = self.lower
        self.initial_upper = self.upper
        self.query_history = {}

    def act(self):
        # Se já testamos este k, repita para verificar consistência
        if self.query_history:
            k, (t_last, _) = next(iter(self.query_history.items()))
            if self.t - t_last > 1:
                return self.oracle_truthful, k

        k = (self.lower + self.upper) // 2
        return self.oracle_truthful, k


    def reset_beliefs(self):
        self.lower = self.initial_lower
        self.upper = self.initial_upper
        self.prev_interval_size = self.upper - self.lower
        self.stagnation = 0
        self.query_history.clear()


    def observe(self, action, oracle_answer, t):
        self.t = t

        # Evidência temporal
        if action in self.query_history:
            _, last_answer = self.query_history[action]
            if oracle_answer != last_answer:
                self.flip_evidence += 1
        else:
            self.query_history[action] = (t, oracle_answer)

        if self.flip_evidence >= self.max_flip_evidence:
            self.oracle_truthful = not self.oracle_truthful
            self.flip_evidence = 0
            self.reset_beliefs()
            return

        effective_answer = oracle_answer if self.oracle_truthful else not oracle_answer

        if effective_answer:
            proposed_lower = max(self.lower, action + 1)
            proposed_upper = self.upper
        else:
            proposed_lower = self.lower
            proposed_upper = min(self.upper, action)

        if proposed_lower > proposed_upper:
            self.oracle_truthful = not self.oracle_truthful
            self.reset_beliefs()
            return

        self.lower, self.upper = proposed_lower, proposed_upper





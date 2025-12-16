# agent.py
import random

class LyingOracleAgent:
    def __init__(self, lowest_number, max_number):
        self.lower = lowest_number if lowest_number is not None else 1
        self.upper = max_number if max_number is not None else 100

        self.oracle_truthful = True
        self.query_history = {}
        self.initial_lower = self.lower
        self.initial_upper = self.upper
        self.t = 0

    def act(self):
        # Busca binária no intervalo atual
        k = (self.lower + self.upper) // 2
        return self.oracle_truthful, k


    def reset_beliefs(self):
        self.lower = self.initial_lower
        self.upper = self.initial_upper
        self.query_history.clear()


    def observe(self, action, oracle_answer, t):
        self.t = t

        # Interpreta a resposta baseado na crença atual
        effective_answer = oracle_answer if self.oracle_truthful else not oracle_answer

        # Atualiza intervalo de busca binária
        if effective_answer:  # hidden > action
            proposed_lower = action + 1
            proposed_upper = self.upper
        else:  # hidden <= action
            proposed_lower = self.lower
            proposed_upper = action - 1

        # Detecta contradição: intervalo ficou impossível
        if proposed_lower > proposed_upper:
            # Troca de crença e reseta
            self.oracle_truthful = not self.oracle_truthful
            self.reset_beliefs()
            self.query_history.clear()
            print(f"[Agent] Detected contradiction at t={t}. Switching belief to: {'Truth' if self.oracle_truthful else 'Lie'}")
            return

        # Atualiza o intervalo
        self.lower, self.upper = proposed_lower, proposed_upper
        
        # Registra no histórico para detecção secundária
        self.query_history[action] = (t, oracle_answer)





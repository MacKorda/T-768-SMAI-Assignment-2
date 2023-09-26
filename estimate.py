import numpy as np
from scipy.stats import norm

class Estimator:

    def __init__(self, num_gates, capacity, avg, std):
        assert (num_gates > 0)
        self.num_gates = num_gates
        self.capacity = capacity
        self.avg = avg
        self.std = std

    def get_giveaway(self, gates):
        return 0

class InformedEstimator(Estimator):

    def __init__(self, num_gates, capacity, avg, std):
        Estimator.__init__(self, num_gates, capacity, avg, std)
        self.expected_giveaways = {weight: 0 for weight in range(0, self.capacity + 1)}
        self.giveaway_records = [list() for _ in range(self.capacity + 1)]
        self.compute()
        return

    def compute(self):
        # You implement this (optional) in case you want to do some onetime pre-computations.
        self.bootstrap(1000, 5000)

    def sample_items(self, n):
        return [max(0, int(np.random.normal(self.avg, self.std))) for _ in range(n)]

    def greedy_placement(self, items):
        gate_weights = [0] * self.num_gates
        gate_values = [[0]] * self.num_gates

        for item in items:
            min_giveaway_gate = min(range(self.num_gates), key=lambda g: self.expected_giveaways.get(gate_weights[g] + item, 0))

            if gate_weights[min_giveaway_gate] + item > self.capacity:
                giveaway = gate_weights[min_giveaway_gate] + item - self.capacity
                for weight in gate_values[min_giveaway_gate]:
                    self.giveaway_records[weight].append(giveaway)
                gate_values[min_giveaway_gate] = [0]
                gate_weights[min_giveaway_gate] = 0

            else:
                gate_weights[min_giveaway_gate] += item
                gate_values[min_giveaway_gate].append(gate_weights[min_giveaway_gate])


    def update_heuristic(self):
        for weight, giveaways in enumerate(self.giveaway_records):
            if giveaways:
                self.expected_giveaways[weight] = sum(giveaways) / len(giveaways)


    def smooth_values(self, window_size=5):
        keys = list(self.expected_giveaways.keys())
        values = list(self.expected_giveaways.values())
        smoothed_values = []

        for i in range(len(keys)):
            start_idx = max(0, i - window_size)
            end_idx = min(len(keys), i + window_size + 1)
            
            avg_value = sum(values[start_idx:end_idx]) / len(values[start_idx:end_idx])
            
            smoothed_values.append(avg_value)

        self.expected_giveaways = dict(zip(keys, smoothed_values))


    def bootstrap(self, n, iterations):
        for i in range(iterations):
            items = self.sample_items(n)
            self.greedy_placement(items)
            self.update_heuristic()
            self.smooth_values(window_size=5)

        
    def get_giveaway(self, gates):
        return sum([self.expected_giveaways.get(g, 0) for g in gates])



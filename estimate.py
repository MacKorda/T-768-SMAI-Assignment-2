import math


class Estimator:

    def __init__(self, num_gates, capacity, avg, std):
        assert (num_gates > 0)
        self.num_gates = num_gates
        self.capacity = capacity
        self.avg = avg
        self.std = std

    def get_giveaway(self, gates):
        # Estimate the future giveaway for the partially filled boxes at the gates.
        return 0


class InformedEstimator(Estimator):

    def __init__(self, num_gates, capacity, avg, std):
        Estimator.__init__(self, num_gates, capacity, avg, std)
        self.compute()
        return

    def compute(self):
        # You implement this (optional) in case you want to do some onetime pre-computations.
        self.multiplier = self.avg / self.std

    def get_giveaway(self, gates):
        # You implement this.
        # Estimate the future giveaway for the partially filled boxes at the gates.
        total_weight = sum(gates) # total weight of the boxes at the gates.
        giveaway = max(0, total_weight - self.num_gates * self.capacity) # excess weight (giveaway) above the capacity.
        heuristic_estimate = giveaway * self.multiplier # Apply the heuristic multiplier to the giveaway.
        return heuristic_estimate

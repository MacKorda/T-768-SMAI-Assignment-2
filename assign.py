from timeit import default_timer as timer

class Assign:

    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator

    def get_estimator(self):
        return self.estimator

    def assign(self, cars, gates, capacity, time):
        
        def time_is_up(start, time):
            if time == 0:
                return False
            return timer() - start >= time

        def do_assign(w, g):
            filled = False
            giveaway = 0
            gates[g] += w
            if gates[g] >= capacity:
                giveaway = gates[g] - capacity
                gates[g] = 0
                filled = True
            return (filled, giveaway)

        def undo_assign(w, g, info):
            filled, giveaway = info
            if filled:
                gates[g] = (capacity + giveaway) - w
            else:
                gates[g] -= w
            return

        def dfbnb(car_idx, g_curr, f_best, start_time):

            h = self.estimator.get_giveaway(gates)
            f_curr = g_curr + h

            if time_is_up(start_time, time) or g_curr >= f_best:
                return float('inf')

            if car_idx == len(cars):
                return f_curr

            min_giveaway = float('inf')
            for g in range(len(gates)):
                info = do_assign(cars[car_idx], g)
                filled, giveaway = info
                next_giveaway = dfbnb(car_idx + 1, g_curr + giveaway, f_best, start_time)
                min_giveaway = min(min_giveaway, next_giveaway)
                if next_giveaway < f_best:
                    f_best = next_giveaway  
                undo_assign(cars[car_idx], g, info)
            return min_giveaway



        start_time = timer()
        f_best = float('inf')
        best_gate = 0

        for g in range(len(gates)):
            info = do_assign(cars[0], g)
            filled, giveaway = info
            curr_giveaway = dfbnb(1, giveaway, f_best, start_time)
            
            if curr_giveaway < f_best:
                f_best = curr_giveaway
                best_gate = g

            undo_assign(cars[0], g, info)

        return best_gate

from timeit import default_timer as timer


class Assign:

    def __init__(self, debug, estimator):
        self.debug = debug
        self.estimator = estimator
        return

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

        def dfbnb(car_idx, curr_giveaway, best_giveaway, start_time):
            if time_is_up(start_time, time) or curr_giveaway > best_giveaway:
                return float('inf')

            if car_idx == len(cars):
                return curr_giveaway

            heuristic = self.estimator.get_giveaway(gates)
            if curr_giveaway + heuristic >= best_giveaway:
                return float('inf')

            min_giveaway = float('inf')
            for g in range(len(gates)):
                info = do_assign(cars[car_idx], g)
                filled, giveaway = info
                next_giveaway = dfbnb(car_idx + 1, curr_giveaway + giveaway, best_giveaway, start_time)
                min_giveaway = min(min_giveaway, next_giveaway)

                if next_giveaway < best_giveaway:
                    best_giveaway = next_giveaway

                undo_assign(cars[car_idx], g, info)

            return min_giveaway

        start_time = timer()
        best_giveaway = float('inf')
        best_gate = 0
        
        for g in range(len(gates)):
            info = do_assign(cars[0], g)
            filled, giveaway = info
            curr_giveaway = dfbnb(1, giveaway, best_giveaway, start_time)
            
            if curr_giveaway < best_giveaway:
                best_giveaway = curr_giveaway
                best_gate = g

            undo_assign(cars[0], g, info)

        return best_gate

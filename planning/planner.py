from planning.monte_carlo import monte_carlo_prediction


class MultiGoalPlanner:

    def __init__(self, agents, goals, futures=10):
        self.agents = agents
        self.goals = goals
        self.futures = futures

    def evaluate_goals(self):

        results = []

        for goal in self.goals:

            prediction = monte_carlo_prediction(
                self.agents,
                goal,
                futures=self.futures
            )

            results.append({
                "goal": goal,
                "average_time": prediction["average_time"],
                "fastest": prediction["fastest"],
                "slowest": prediction["slowest"]
            })

        return results

    def recommend_goal(self):

        results = self.evaluate_goals()

        best = min(results, key=lambda r: r["average_time"])

        return best, results
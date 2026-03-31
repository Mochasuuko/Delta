import random


def run_future(agents, goal):

    results = []

    for agent in agents:

        varied_speed = agent.speed * random.uniform(0.9, 1.1)

        distance = agent.distance_to(goal)

        time = distance / varied_speed

        results.append(time)

    return max(results)


def monte_carlo_prediction(agents, goal, futures=10):

    outcomes = []

    for _ in range(futures):

        t = run_future(agents, goal)

        outcomes.append(t)

    avg = sum(outcomes) / len(outcomes)

    return {
        "runs": outcomes,
        "average_time": avg,
        "fastest": min(outcomes),
        "slowest": max(outcomes)
    }
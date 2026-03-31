# simulation/engine.py

from agents.agent import Agent
from scenario.builder import ScenarioBuilder
from planning.planner import MultiGoalPlanner

def run_simulation():
    builder = ScenarioBuilder()
    builder.set_environment(width=25, height=25)

    # Create agents with positions and speed
    builder.add_agent(Agent("A", (5,10), speed=1))
    builder.add_agent(Agent("B", (8,10), speed=1))
    builder.add_agent(Agent("C", (13,10), speed=1))

    scenario = builder.build()
    environment = scenario['environment']
    agents = scenario['agents']

    # Define goals
    goals = [(25,10),(0,10)]

    # Planner computes best goal
    planner = MultiGoalPlanner()
    analysis = planner.evaluate_goals(agents, goals)
    recommended_goal = analysis['best_goal']
    predicted_time = analysis['best_time']

    # Stats
    stats = {
        "Predicted Exit": str(recommended_goal),
        "Evac Time": f"{round(predicted_time,2)} s",
        "Futures": 10,
        "Confidence": "82%"
    }

    return environment, agents, recommended_goal, stats
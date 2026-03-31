from agents.agent import Agent


class ScenarioBuilder:

    def __init__(self):
        self.environment = None
        self.agents = []
        self.goal = None

    def set_environment(self, width, height):
        self.environment = {
            "width": width,
            "height": height
        }

    def add_agent(self, name, position, speed=1.4):
        agent = Agent(name, position, speed)
        self.agents.append(agent)

    def set_goal(self, position):
        self.goal = position

    def build(self):

        if not self.environment:
            raise ValueError("Environment not defined")


        return {
            "environment": self.environment,
            "agents": self.agents,
            "goal": self.goal
        }
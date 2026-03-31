# Delta/ui/simulation_panel.py

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SimulationPanel(QWidget):
    def __init__(self, environment, agents, recommended_goal, stats, ui_colors):
        super().__init__()

        self.environment = environment
        self.agents = agents
        self.goal = recommended_goal
        self.stats = stats
        self.ui_colors = ui_colors  # dict for background, text, highlight colors

        # ---------------------------
        # Layout: Tactical Map + Stats
        # ---------------------------
        main_layout = QHBoxLayout()

        # Matplotlib Figure
        self.fig = Figure(figsize=(5,5))
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)

        main_layout.addWidget(self.canvas, 3)

        # Stats Panel
        stats_layout = QVBoxLayout()
        title = QLabel("DELTA ANALYSIS")
        title.setStyleSheet(f"color:{ui_colors['text']}; font-weight:bold; font-size:16px;")
        stats_layout.addWidget(title)

        for key, value in stats.items():
            label = QLabel(f"{key}: {value}")
            label.setStyleSheet(f"color:{ui_colors['text']}; font-size:14px;")
            stats_layout.addWidget(label)

        stats_layout.addStretch()
        main_layout.addLayout(stats_layout, 1)

        self.setLayout(main_layout)

        # ---------------------------
        # Draw initial tactical map
        # ---------------------------
        self._setup_map()
        self._draw_map()

    def _setup_map(self):
        self.ax.set_xlim(0, self.environment['width'])
        self.ax.set_ylim(0, self.environment['height'])
        self.ax.set_facecolor(self.ui_colors['background'])
        self.ax.set_xticks(range(0, self.environment['width']+1, 5))
        self.ax.set_yticks(range(0, self.environment['height']+1, 5))
        self.ax.grid(True, color=self.ui_colors['grid'], linestyle='--', linewidth=0.5)

    def _draw_map(self):
        # Draw goals
        gx, gy = self.goal
        self.ax.scatter(gx, gy, s=200, marker='s', color=self.ui_colors['highlight'], label="Goal")

        # Draw agents
        self.agent_plots = []
        for agent in self.agents:
            plot, = self.ax.plot(agent.x, agent.y, 'o', color=self.ui_colors['agents'], markersize=10)
            self.agent_plots.append(plot)

        # For path lines
        self.paths = [[] for _ in self.agents]

        self.canvas.draw()

    def animate_agents(self):
        import math
        import matplotlib.animation as animation

        goal_x, goal_y = self.goal

        def update(frame):
            for i, agent in enumerate(self.agents):
                dx = goal_x - agent.x
                dy = goal_y - agent.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0.1:
                    step = 0.25
                    agent.x += step * dx / distance
                    agent.y += step * dy / distance

                self.paths[i].append((agent.x, agent.y))

                # update dot
                self.agent_plots[i].set_data([agent.x], [agent.y])

                # update path line
                xs = [p[0] for p in self.paths[i]]
                ys = [p[1] for p in self.paths[i]]
                if hasattr(self, f'line_{i}'):
                    getattr(self, f'line_{i}').set_data(xs, ys)
                else:
                    line, = self.ax.plot(xs, ys, linestyle='--', color=self.ui_colors['path'])
                    setattr(self, f'line_{i}', line)

            return self.agent_plots

        ani = animation.FuncAnimation(self.fig, update, frames=200, interval=40, blit=True)
        self.canvas.draw()
        return ani
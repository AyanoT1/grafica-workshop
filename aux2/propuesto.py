import pyglet
import numpy as np
import os
import pyglet.gl as pygl
import random
from pathlib import Path

WIDTH = 600
HEIGHT = 600
DEFINITION = 100

class CircleWindow(pyglet.window.Window):
    def __init__(self, width, height, title, *args, **kwargs):
        super().__init__(width, height, caption=title, *args, **kwargs)
        self.set_minimum_size(240, 240)
        
        # Import shaders
        shader_dir = Path(os.path.dirname(__file__)) / "assets"
        with open(shader_dir / "vertex_program.glsl") as f:
            vertex_source = f.read()

        with open(shader_dir / "fragment_program.glsl") as f:
            fragment_source = f.read()

        # Compile shaders
        vert_program = pyglet.graphics.shader.Shader(vertex_source, "vertex")
        frag_program = pyglet.graphics.shader.Shader(fragment_source, "fragment")

        # Create pipeline
        self.pipeline = pyglet.graphics.shader.ShaderProgram(vert_program, frag_program)

        # Create initial circle
        circle = self.create_circle(0.2, 0.0, 0.5)

        # Initialize the circle in the pipeline
        self.circle_gpu = self.pipeline.vertex_list(3 * DEFINITION, pygl.GL_TRIANGLES)

        # Push the circle to the pipeline
        self.circle_gpu.position[:] = circle

    def create_circle(self, x, y, radius):
        N = DEFINITION
        positions = np.zeros(9 * N, dtype=np.float32)
        theta = 2 * np.pi / N
        for i in range(N):
            j = 9 * i
            # center
            positions[j:j+3] = [x, y, 0.0]
            # p0
            dtheta0 = i * theta
            x0 = x + radius * np.cos(dtheta0)
            y0 = y + radius * np.sin(dtheta0)
            positions[j+3:j+6] = [x0, y0, 0.0]
        
            # p1
            dtheta1 = dtheta0 + theta
            x1 = x + radius * np.cos(dtheta1)
            y1 = y + radius * np.sin(dtheta1)
            positions[j+6:j+9] = [x1, y1, 0.0]

        return positions

    def update(self, dt):
        # Create a new circle with random radius
        circle = self.create_circle(0.2, 0.0, 0.5 + random.random() * 0.1)
        # Update the GPU buffer
        self.circle_gpu.position[:] = circle

    def on_draw(self):
        # Clear the screen
        self.clear()
        pygl.glClearColor(0.1, 0.1, 0.1, 0.0)

        # Draw the circle
        with self.pipeline:
            self.circle_gpu.draw(pygl.GL_TRIANGLES)

if __name__ == "__main__":
    # Create a single window that handles everything
    window = CircleWindow(WIDTH, HEIGHT, "Auxiliar 2", resizable=True)
    
    # Schedule the update function
    pyglet.clock.schedule_interval(window.update, 1/20)
    
    # Run the application
    pyglet.app.run()
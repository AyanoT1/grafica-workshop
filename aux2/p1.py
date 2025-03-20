import pyglet
import numpy as np
import os
import pyglet.gl as pygl
from pathlib import Path


WIDTH = 600
HEIGHT = 600
DEFINITION = 100

window = pyglet.window.Window(WIDTH, HEIGHT, "Auxiliar 2")

def create_circle(x, y, radius):
    N = DEFINITION
    positions = np.zeros(9*N, dtype=np.float32)
    theta = 2 * np.pi / N
    for i in range(N):
        j = 9*i
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

if __name__ == "__main__":

    # Import shaders
    with open(Path(os.path.dirname(__file__)) / "assets/vertex_program.glsl") as f:
        vertex_source = f.read()

    with open(Path(os.path.dirname(__file__)) / "assets/fragment_program.glsl") as f:
        fragment_source = f.read()


    # Compile shaders
    vert_program = pyglet.graphics.shader.Shader(vertex_source, "vertex")
    frag_program = pyglet.graphics.shader.Shader(fragment_source, "fragment")

    # Create pipeline
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_program, frag_program)

    # Create circle with the function defined above
    circle = create_circle(0.2, 0.0, 0.5)

    # Initialize the circle in the pipeline
    circle_gpu = pipeline.vertex_list(3*DEFINITION, pygl.GL_TRIANGLES)

    # Push the circle to the pipeline
    circle_gpu.position[:] = circle

    @window.event
    def on_draw():

        # Clear the screen
        window.clear()
        pygl.glClearColor(0.1, 0.1, 0.1, 0.0)

        with pipeline as _:
            circle_gpu.draw(pygl.GL_TRIANGLES)

    
    pyglet.app.run()

    

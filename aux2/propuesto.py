import random
import pyglet
import numpy as np
from pyglet.gl import *


WIDTH = 600
HEIGHT = 600
DEFINITION = 100

class Controller(pyglet.window.Window):
    def __init__(self, title, *args, **kargs):
        super().__init__(*args, **kargs)
        # Evita error cuando se redimensiona a 0
        self.set_minimum_size(240, 240)
        self.set_caption(title)

    def update(self, dt):
        circle = create_circle(0.2, 0.0, 0.5 + random.random() * 0.05)
        circle_gpu.position[:] = circle

def create_circle(x, y, radius):
    N = DEFINITION
    positions = np.zeros(9*N, dtype=np.float32)
    theta = 2 * np.pi / N
    for i in range(N):
        j = 9*i
        # centro
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
    # Creamos nuestros shaders
    vertex_source = """
#version 330

in vec3 position;

out vec3 fragColor;

void main() {
    fragColor = vec3(1.0f, 1.0f, 1.0f);
    gl_Position = vec4(position, 1.0f);
}
    """

    fragment_source = """
#version 330

in vec3 fragColor;
out vec4 outColor;

void main()
{
    outColor = vec4(fragColor, 1.0f);
}
    """

    controller = Controller("Auxiliar 1", width=WIDTH,
                            height=HEIGHT, resizable=True)

    # Compilamos los shaders
    vert_program = pyglet.graphics.shader.Shader(vertex_source, "vertex")
    frag_program = pyglet.graphics.shader.Shader(fragment_source, "fragment")

    # Creamos nuestro pipeline de rendering
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_program, frag_program)

    # Creamos el circulo
    circle = create_circle(0.2, 0.0, 0.5)

    # Creamos el circulo en la gpu
    circle_gpu = pipeline.vertex_list(3*DEFINITION, GL_TRIANGLES)

    # Copiamos los datos
    circle_gpu.position[:] = circle

    @controller.event
    def on_draw():

        # Esta linea limpia la pantalla entre frames
        controller.clear()
        glClearColor(0.1, 0.1, 0.1, 0.0)

        pipeline.use()
        circle_gpu.draw(GL_TRIANGLES)

    pyglet.clock.schedule_interval(controller.update, 1/10)
    pyglet.app.run()

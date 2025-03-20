#version 330

in vec3 position;
out vec3 fragColor;

void main() {
  fragColor = vec3(1.0f, 1.0f, 1.0f);
  gl_Position = vec4(position, 1.0f);
}
#version 330 core

out vec4 fragColor;
in vec3 vertColor; // we set this variable in the OpenGL code.
in vec2 vertTexCoord;

uniform sampler2D texture0;
uniform sampler2D texture1;

uniform sampler2D texture_diffuse1;
uniform sampler2D texture_diffuse2;
uniform sampler2D texture_diffuse3;
uniform sampler2D texture_specular1;
uniform sampler2D texture_specular2;

void main()
{
	fragColor = texture(texture_diffuse1, vertTexCoord);
};
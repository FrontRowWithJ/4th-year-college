#ifndef LIBS_H
#define LIBS_H


#include <iostream>

#include <glm.hpp>
#include <gtc/matrix_transform.hpp>
#include <gtc/type_ptr.hpp>

#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <time.h>
#include <vector>
#include <array>
#include <string>
#include <fstream>
#include <algorithm>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include "Model.h"
#include "Camera.h"
#include "MyShader.h"
#include "Menu.h"

class MPoint {
public:
	float x;
	float y;
	float z;
	MPoint(float x, float y) {
		this->x = x;
		this->y = y;
		this->z = 0.f;
	}
	MPoint(float x, float y, float z) {
		this->x = x;
		this->y = y;
		this->z = z;
	}
};

typedef MPoint MColor;

typedef std::uint32_t tex_id;		// texture id

typedef struct {
	tex_id id;
	int width;
	int height;
	int nrChannels;
} MyTexture;

typedef struct {
	int width;
	int height;
	int nrChannels;
} ImageData;

auto constexpr NUM_OF_DIMS = 3;
auto constexpr POSITION = 0;
auto constexpr COLOR = 1;
auto constexpr TEX_COORD = 2;

void framebuffer_size_callback(GLFWwindow* window, int width, int height);
void processInput(GLFWwindow* window);
void clearWindow(float r, float g, float b, float a);
void clearWindow(MColor color, float a);
MyTexture genTexture(char const* filename, GLenum format);
ImageData loadTexture(char const* filename, GLenum format);

#endif
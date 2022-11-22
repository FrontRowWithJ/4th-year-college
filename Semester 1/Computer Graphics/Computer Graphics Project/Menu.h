#ifndef  MENU_H
#define MENU_H


// std library
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <functional>
#include <chrono>
#include <thread>
//#include <windows.h> //different header file in linux
#include <future>

#include <glad/glad.h>
#include "MyShader.h"

#include "Camera.h"


class Point {
public:
	float x;
	float y;
	float z;
	Point(float x, float y) {
		this->x = x;
		this->y = y;
		this->z = 0.f;
	}
	Point(float x, float y, float z) {
		this->x = x;
		this->y = y;
		this->z = z;
	}

	Point operator+(const Point& first) const {
		return Point(x + first.x, y + first.y, z + first.z);
	}
};

typedef Point Color;

typedef std::vector<std::function<void(GLFWwindow*, double, double)>> MouseCBList;
typedef std::vector<std::function<void(GLFWwindow*, int, int, int)>> MouseButtonCBList;
typedef std::vector<std::function<void(GLFWwindow*, double, double)>> ScrollCBList;
typedef std::vector<std::function<void(GLFWwindow*)>> KeyCBList;

template <typename... ParamTypes>
void setTimeout(int milliseconds, std::function<void(ParamTypes...)> func, ParamTypes... parames);


class Menu {

public:

private:
	int const WIDTH = 800;
	int const HEIGHT = 800;
	MyShader shader;
	GLuint vbo, vao, ebo;
	Camera camera;
	float deltaTime = 0.0f;
	float lastFrame = 0.0f;
	float lastX = WIDTH / 2.0f;
	float lastY = HEIGHT / 2.0f;
	bool firstMouse = true;
	bool canPan = false;
	bool isWhite = true;
	bool canPress = true;

public:
	Menu(Point topLeft, float w, float h, MyShader& shader, Color color = Color(1, 1, 1)) : shader(shader) {
		camera = Camera(glm::vec3(.0f, .0f, 3.f));

		// 0: 0.x     , 0.y
		// 1: 0.x + 2w, 0.y
		// 2: 0.x + 2w, 0.y - 2h
		// 3: 0.x + 2w, 0.y - 2h
		// 4: 0.x     , 0.y - 2h
		// 5: 0.x     , 0.x
		w *= 2;
		h *= 2;
		/*Point vertices[] = {
			topLeft,
			topLeft + Point(w, 0),
			topLeft + Point(w, -h),
			topLeft + Point(w, -h),
			topLeft + Point(0, -h),
			topLeft
		};*/
		Point vertices[] = {
			Point(-1000, 0, -1000),
			Point(1000, 0, -1000),
			Point(1000, 0, 1000),
			Point(-1000, 0, -1000),
			Point(-1000, 0, 1000),
			Point(1000, 0, 1000)
		};

		/*float vertices[]{
			-1,0,-1,
			1,0,-1,
			1,0,1,
		};*/

		/*float vertices[]{
			-1,1,0,
			1,1,0,
			1,-1,0
		};*/

		int indices[6] = { 0, 1, 3, 1, 2, 3 };
		vao = genVertexArrayObject(1);
		bindVAO();
		vbo = genBufferObject(&vertices[0], sizeof(vertices), GL_ARRAY_BUFFER);
		ebo = genBufferObject(indices, sizeof(indices), GL_ELEMENT_ARRAY_BUFFER);
		interpretVertexData(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
		shader.enableShader();
		setColor(color);
	}

	void setColor(Color color) {
		setColor(color.x, color.y, color.z);
	}

	void setColor(float r, float g, float b) {
		shader.enableShader();
		shader.setVec3("color", glm::vec3(r, g, b));
		shader.disableShader();
	}

	void draw() {
		shader.enableShader();
		bindVAO();
		bindVBO();
		drawInner();
		shader.disableShader();
		unbindVBO();
		unbindVAO();
	}

	void onmousemove(MouseCBList& callbacks) {
		auto mouse_callback = [&](GLFWwindow* window, double xpos, double ypos) {
			if (firstMouse)
			{
				lastX = xpos;
				lastY = ypos;
				firstMouse = false;
			}

			float xoffset = xpos - lastX;
			float yoffset = lastY - ypos; // reversed since y-coordinates go from bottom to top

			lastX = xpos;
			lastY = ypos;

			if (canPan) {
				camera.ProcessMouseMovement(xoffset, yoffset);
			}
		};
		callbacks.push_back(mouse_callback);
	}
	void onmouseclick(MouseButtonCBList& callbacks) {

	}

	void onkeyclick(KeyCBList& callbacks) {
		auto cb = [&](GLFWwindow* window) {
			if (canPress) {
				if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS) {
					canPress = false;
					isWhite = !isWhite;
					setColor(isWhite ? Color(1, 1, 1) : Color(0, 0, 0));
					std::function<void()> callback = [&]() {canPress = true; };
					setTimeout<>(100, callback);
				}
			}
		};
		callbacks.push_back(cb);
	}

private:
	GLuint genBufferObject(void const* vertices, std::size_t size, GLenum target) {
		GLuint BO;
		glGenBuffers(1, &BO);
		glBindBuffer(target, BO);
		glBufferData(target, size, vertices, GL_STATIC_DRAW);
		return BO;
	}
	/*
	 Tells opengl how to treat the vertex buffer
	 @param[in] index: Specifies the index of the vertex attribute
	 @param[in] size: number of components in an attribute
	 @param[in] type: The type of data in the vertex buffer
	 @param[in] shouldNormalise: Wether or not the data should be normalised between 0 and 1
	 @param[in] stride: number of bytes until the start of the next attribute
	 @param[in] offset: how many bytes off the start of the array should you start
	*/
	void interpretVertexData(int index, int size, int type, bool shouldNormalise, int stride, void* offset) {
		glEnableVertexAttribArray(index);
		glVertexAttribPointer(index, size, type, shouldNormalise, stride, offset);
	}

	GLuint genVertexArrayObject(unsigned int const numOfVBOs) {
		GLuint VAO;
		glGenVertexArrays(numOfVBOs, &VAO);
		return VAO;
	}

	void drawInner() {
		glDrawArrays(GL_TRIANGLES, 0, 6); // set the count to 6 since we're drawing 6 vertices now (2 triangles); not 3!
	}

	void bindVAO() {
		glBindVertexArray(vao);
	}

	void bindVBO() {
		glBindBuffer(GL_ARRAY_BUFFER, vbo);
	}
	void unbindVBO() {
		glBindBuffer(GL_ARRAY_BUFFER, 0);
	}

	void unbindVAO() {
		glBindVertexArray(0);
	}
};

template <typename... ParamTypes>
void setTimeout(int milliseconds, std::function<void(ParamTypes...)> func, ParamTypes... params)
{
	std::async(std::launch::async, [=]()
		{
			std::this_thread::sleep_for(std::chrono::milliseconds(milliseconds));
			func(params...);
		});
};

#endif // ! MENU_H
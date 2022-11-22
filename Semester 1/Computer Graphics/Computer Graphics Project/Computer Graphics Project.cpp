#include "libs.h"

void scroll_callback(GLFWwindow* window, double xoffset, double yoffset);
void mouse_callback(GLFWwindow* window, double xposIn, double yposIn);
void mouse_button_callback(GLFWwindow* window, int button, int action, int mode);
void aCallback(GLFWwindow* window, double xposIn, double yposIn);

auto constexpr WIDTH = 800;
auto constexpr HEIGHT = 800;
Camera camera(glm::vec3(0.0f, 0.0f, 3.0f));
// timing
float deltaTime = 0.0f;
float lastFrame = 0.0f;
float lastX = WIDTH / 2.0f;
float lastY = HEIGHT / 2.0f;
bool firstMouse = true;
bool canPan = false;

MouseCBList mouseCallbacks;
MouseButtonCBList mouseButtonCallBacks;
ScrollCBList scrollCallbacks;
KeyCBList keyCallbacks;

int main()
{
	mouseCallbacks.push_back(aCallback);
	stbi_set_flip_vertically_on_load(true);
	glfwInit(); // initialise GLFW
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3); // these 2 lines sets the glfw version to 3.3
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // omits importing the backward compatibilty features used for fixed pipeline (antiquated approach 3d rendering)

	//glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE); 

	auto window = glfwCreateWindow(WIDTH, HEIGHT, "LearnOpenGL", NULL, NULL);
	if (window == NULL)
	{
		std::cout << "Failed to create GLFW window" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);

	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}
	glViewport(0, 0, WIDTH, HEIGHT); // lower left corner = 0,0
	glEnable(GL_DEPTH_TEST);
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	glfwSetCursorPosCallback(window, mouse_callback);
	glfwSetScrollCallback(window, scroll_callback);
	glfwSetMouseButtonCallback(window, mouse_button_callback);
	stbi_set_flip_vertically_on_load(true);

	std::vector<char const*>paths = {
		"./menu.vert",
		"./menu.frag"
	};
	std::vector<GLuint> types = {
		GL_VERTEX_SHADER,
		GL_FRAGMENT_SHADER
	};
	MyShader myShader(paths, types);

	float w = .1;
	float h = .05;
	auto menu = Menu(Point(1 - w * 2, 1), w, h, myShader, Color(0, 0, 0));
	menu.onmousemove(mouseCallbacks);
	menu.onmouseclick(mouseButtonCallBacks);
	menu.onkeyclick(keyCallbacks);

	Shader shader("VertexShader.hlsl", "FragmentShader.hlsl");
	//Model m("C:\\Users\\micha\\Desktop\\Workspace\\4th-year-college\\Semester\ 1\\Computer\ Graphics\\Computer\ Graphics\ Project\\backpack\\backpack.obj");
	Model m("C:\\Users\\micha\\Desktop\\Workspace\\4th-year-college\\Semester 1\\Computer Graphics\\Computer Graphics Project\\snow_man\\snowman.obj");

	while (!glfwWindowShouldClose(window)) {

		float currentFrame = static_cast<float>(glfwGetTime());
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;
		processInput(window);
		clearWindow(.3f, .1f, .5f, 1.f);
		shader.use();
		
		glm::mat4 projection = glm::perspective(glm::radians(camera.Zoom), (float)WIDTH / (float)HEIGHT, .01f, 100.0f);
		glm::mat4 view = camera.GetViewMatrix();

		shader.setMat4("projection", projection);
		shader.setMat4("view", view);
		shader.setVec4("offset", glm::vec4(0, std::sin(glfwGetTime()), 0, 0));
		glm::mat4 model = glm::mat4(1.0f);
		model = glm::translate(model, glm::vec3(0.0f, 0.0f, 0.0f)); // translate it down so it's at the center of the scene
		model = glm::scale(model, glm::vec3(1.0f, 1.0f, 1.0f));	    // it's a bit too big for our scene, so scale it down
		
		shader.setMat4("model", model);

		m.Draw(shader);

		menu.draw();
		myShader.enableShader();
		myShader.setMat4("_projection", projection);
		myShader.setMat4("_view", view);
		myShader.setMat4("_model", model);
		
		glfwPollEvents();
		glfwSwapBuffers(window);

	}
	glfwTerminate();
	return 0;
	// glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	//auto texture0 = genTexture("container.jpg", GL_RGB);
	//auto texture1 = genTexture("awesomeface.png", GL_RGBA);


	//setCurrentShader(shaderProgram);
	//glUniform1i(glGetUniformLocation(shaderProgram, "texture0"), 0);
	//glUniform1i(glGetUniformLocation(shaderProgram, "texture1"), 1);
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
	glViewport(0, 0, width, height);
}

int constexpr keys[6] = { GLFW_KEY_W, GLFW_KEY_S, GLFW_KEY_A, GLFW_KEY_D, GLFW_KEY_SPACE, GLFW_KEY_LEFT_SHIFT };
Camera_Movement constexpr positions[6] = { FORWARD, BACKWARD, LEFT, RIGHT, UP, DOWN };
auto constexpr len = sizeof(keys) / sizeof(int);

void processInput(GLFWwindow* window) {
	if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
		glfwSetWindowShouldClose(window, true);

	for (int i = 0; i < len; i++)
		if (glfwGetKey(window, keys[i]) == GLFW_PRESS)
			camera.ProcessKeyboard(positions[i], deltaTime);

	for (auto callback : keyCallbacks) callback(window);
}

/*
 Sets the window to a specific color
 @param[in] r value between 0 and 1
 @param[in] g value between 0 and 1
 @param[in] b value between 0 and 1
 @param[in] a value between 0 and 1
*/
void clearWindow(float r, float g, float b, float a) {
	glClearColor(r, g, b, a);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
}

void clearWindow(MColor rgb, float a) {
	auto& [r, g, b] = rgb;
	clearWindow(r, g, b, a);
}

MyTexture genTexture(char const* filename, GLenum format) {
	// creating the texture id
	tex_id texture;
	glGenTextures(1, &texture);

	//binding texture
	glBindTexture(GL_TEXTURE_2D, texture);

	// set the texture wrapping/filtering options (on the currently bound texture object)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

	auto data = loadTexture(filename, format);
	auto& [width, height, nrChannels] = data;
	return { texture, width, height, nrChannels };
}

ImageData loadTexture(char const* filename, GLenum format) {
	int width = -1, height = -1, nrChannels;
	auto textureData = stbi_load(filename, &width, &height, &nrChannels, 0);

	if (textureData) {
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, format, GL_UNSIGNED_BYTE, textureData);
		glGenerateMipmap(GL_TEXTURE_2D);
	}
	else {
		std::cout << "Failed to load texture " << filename << std::endl;
	}

	//free image memory
	stbi_image_free(textureData);
	return { width, height, nrChannels };
}

void aCallback(GLFWwindow* window, double xposIn, double yposIn) {
	float xpos = static_cast<float>(xposIn);
	float ypos = static_cast<float>(yposIn);
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
}

void mouse_callback(GLFWwindow* window, double xposIn, double yposIn)
{
	for (auto callback : mouseCallbacks) callback(window, xposIn, yposIn);
}

// glfw: whenever the mouse scroll wheel scrolls, this callback is called
// ----------------------------------------------------------------------
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset)
{
	camera.ProcessMouseScroll(static_cast<float>(yoffset));
	for (auto callback : scrollCallbacks) callback(window, xoffset, yoffset);
}

void mouse_button_callback(GLFWwindow* window, int button, int action, int mode) {

	if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) {
		// set can pan to true
		canPan = true;
	}
	else if (button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_RELEASE)
		canPan = false;
	for (auto callback : mouseButtonCallBacks) callback(window, button, action, mode);
}
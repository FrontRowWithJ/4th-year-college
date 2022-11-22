#ifndef  MY_SHADER_H
#define MY_SHADER_H


// std library
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>

#include <glad/glad.h>
#include <glm.hpp>

class MyShader {

private:
	GLuint shaderID;

public:
	MyShader(std::vector<char const*>paths, std::vector<GLuint> types) {
		std::vector<GLuint> shader_ids; 
		
		for (int i = 0; i < paths.size(); i++) {
			auto shader_id = compileShader(paths[i], types[i]);
			if (!shader_id) { 
				deleteShaders(shader_ids); 
				return; 
			}
			shader_ids.push_back(shader_id);
		}
		auto id = linkShaders(shader_ids);
		if (!id) return;
		this->shaderID = id;
		deleteShaders(shader_ids);
	}

	GLuint getID() {
		return shaderID;
	}

	void enableShader() {
		glUseProgram(shaderID);
	}

	void disableShader() {
		glUseProgram(0);
	}

	// utility uniform functions
	// ------------------------------------------------------------------------
	void setBool(const std::string& name, bool value) const
	{
		glUniform1i(glGetUniformLocation(shaderID, name.c_str()), (int)value);
	}
	// ------------------------------------------------------------------------
	void setInt(const std::string& name, int value) const
	{
		glUniform1i(glGetUniformLocation(shaderID, name.c_str()), value);
	}
	// ------------------------------------------------------------------------
	void setFloat(const std::string& name, float value) const
	{
		glUniform1f(glGetUniformLocation(shaderID, name.c_str()), value);
	}
	// ------------------------------------------------------------------------
	void setVec2(const std::string& name, const glm::vec2& value) const
	{
		glUniform2fv(glGetUniformLocation(shaderID, name.c_str()), 1, &value[0]);
	}
	void setVec2(const std::string& name, float x, float y) const
	{
		glUniform2f(glGetUniformLocation(shaderID, name.c_str()), x, y);
	}
	// ------------------------------------------------------------------------
	void setVec3(const std::string& name, const glm::vec3& value) const
	{
		glUniform3fv(glGetUniformLocation(shaderID, name.c_str()), 1, &value[0]);
	}
	void setVec3(const std::string& name, float x, float y, float z) const
	{
		glUniform3f(glGetUniformLocation(shaderID, name.c_str()), x, y, z);
	}
	// ------------------------------------------------------------------------
	void setVec4(const std::string& name, const glm::vec4& value) const
	{
		glUniform4fv(glGetUniformLocation(shaderID, name.c_str()), 1, &value[0]);
	}
	void setVec4(const std::string& name, float x, float y, float z, float w)
	{
		glUniform4f(glGetUniformLocation(shaderID, name.c_str()), x, y, z, w);
	}
	// ------------------------------------------------------------------------
	void setMat2(const std::string& name, const glm::mat2& mat) const
	{
		glUniformMatrix2fv(glGetUniformLocation(shaderID, name.c_str()), 1, GL_FALSE, &mat[0][0]);
	}
	// ------------------------------------------------------------------------
	void setMat3(const std::string& name, const glm::mat3& mat) const
	{
		glUniformMatrix3fv(glGetUniformLocation(shaderID, name.c_str()), 1, GL_FALSE, &mat[0][0]);
	}
	// ------------------------------------------------------------------------
	void setMat4(const std::string& name, const glm::mat4& mat) const
	{
		glUniformMatrix4fv(glGetUniformLocation(shaderID, name.c_str()), 1, GL_FALSE, &mat[0][0]);
	}

private:
	GLuint linkShaders(std::vector<GLuint> &shaders) {
		auto id = glCreateProgram();
		for (auto shader_id : shaders) glAttachShader(id, shader_id);
		glLinkProgram(id);
		auto result = checkShaderCompilation(id, "PROGRAM");
		return result ? id : 0;
	}
	void deleteShaders(std::vector<GLuint> shaders) {
		for (auto shader_id : shaders)
			glDeleteShader(shader_id);
	}
	GLuint compileShader(char const* filename, unsigned int type) {
		auto shaderCode = loadShaderFile(filename);
		if (shaderCode.length() == 0) return 0;
		auto shaderCodeCString = shaderCode.c_str();
		GLuint shader_id = glCreateShader(type);
		glShaderSource(shader_id, 1, &shaderCodeCString, NULL);
		glCompileShader(shader_id);
		auto errType = type == GL_VERTEX_SHADER ? "VERTEX" : type == GL_FRAGMENT_SHADER ? "FRAGMENT" : "GEOMETRY";
		auto success = checkShaderCompilation(shader_id, errType);
		return success ? shader_id : 0;
	}

	bool checkShaderCompilation(GLuint id, char const* type) {
		int success;
		char log[512];
		glGetShaderiv(id, GL_COMPILE, &success);
		if (!success) {
			glGetShaderInfoLog(id, sizeof(log), NULL, log);
			std::cout << "ERROR::SHADER::" << type << "COMPILATION_FAILED\n" << log << std::endl;
		}
		return success != 0;
	}

	std::string loadShaderFile(char const* filename) {
		std::string shaderCode;
		std::ifstream shaderFile(filename, std::ios::in);

		if (!shaderFile.is_open()) {
			std::cout << "ERROR::SHADER::FILE_NOT_FOUND::" << filename << std::endl;
			return "";
		}
		std::stringstream shaderStream;
		shaderStream << shaderFile.rdbuf();
		shaderFile.close();
		shaderCode = shaderStream.str();
		return shaderCode;
	}
};
#endif // ! MENU_H

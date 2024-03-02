cmake_minimum_required(VERSION 3.22)

macro(MACRO_ENSURE_OUT_OF_SOURCE_BUILD MSG)
    string(COMPARE EQUAL "${CMAKE_SOURCE_DIR}" "${CMAKE_BINARY_DIR}" insource)
    get_filename_component(PARENTDIR ${CMAKE_SOURCE_DIR} PATH)
    string(COMPARE EQUAL "${CMAKE_SOURCE_DIR}" "${PARENTDIR}" insourcesubdir)
    if(insource OR insourcesubdir)
        message(FATAL_ERROR "${MSG}")
    endif(insource OR insourcesubdir)
endmacro(MACRO_ENSURE_OUT_OF_SOURCE_BUILD)

MACRO_ENSURE_OUT_OF_SOURCE_BUILD(
    "${CMAKE_PROJECT_NAME} requires an out-of-source build!\nRun `cmake -B project/build` instead."
)

# Set C++ standard
set(CMAKE_CXX_STANDARD 20)

# Turn on link-time optimization for everything
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION_RELEASE ON)

# Output compile commands to compile_commands.json (for debugging CMake issues)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Build universal lib on macOS
# Note that CMAKE_OSX_ARCHITECTURES must be set before project().
if(APPLE)
    set(CMAKE_OSX_ARCHITECTURES "x86_64;arm64" CACHE STRING "")
endif()

# Set the name of the project
project(MonkeyRun)

# Create our library
add_library(${PROJECT_NAME} SHARED src/main.cpp)

# LIB_ARCH is the architecture being built. It is set to the build system's architecture.
# For macOS, we build a universal library (both arm64 and x86_64).
set(LIB_ARCH ${CMAKE_SYSTEM_PROCESSOR})
if(APPLE)
    set(LIB_ARCH "universal")
endif()

# LIB_DIR is where the actual library ends up. This is used in both the build directory and the
# install directory and needs to be consistent with the paths in the .gdextension file.
#   e.g. linux.release.x86_64 = "Linux-x86_64/libGDExtensionTemplate.so"
set(LIB_DIR "${CMAKE_SYSTEM_NAME}-${LIB_ARCH}")

# BUILD_OUTPUT_DIR is where we put the resulting library (in the project bin directory)
set(BUILD_OUTPUT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/project/build/")

set_target_properties(
    ${PROJECT_NAME} PROPERTIES
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN true
    RUNTIME_OUTPUT_DIRECTORY "${BUILD_OUTPUT_DIR}/${LIB_DIR}"
    LIBRARY_OUTPUT_DIRECTORY "${BUILD_OUTPUT_DIR}/${LIB_DIR}"
)

if(NOT DEFINED CMAKE_DEBUG_POSTFIX)
    set_target_properties(
        ${PROJECT_NAME} PROPERTIES
        DEBUG_POSTFIX ".debug"
    )
endif()

add_subdirectory(src)

# Install the library, extension file, and support files in INSTALL_DIR
set(INSTALL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/project/bin")

install(TARGETS ${PROJECT_NAME} DESTINATION ${INSTALL_DIR}/${LIB_DIR})

# godot-cpp
# From here: https://github.com/godotengine/godot-cpp
if(NOT EXISTS "${CMAKE_CURRENT_LIST_DIR}/extern/godot-cpp/CMakeLists.txt")
    message(
        FATAL_ERROR
        "[${PROJECT_NAME}] The godot-cpp submodule was not downloaded. Please update submodules: git submodule update --init --recursive."
    )
endif()

set(GODOT_CPP_SYSTEM_HEADERS ON CACHE BOOL "" FORCE)

add_subdirectory(extern/godot-cpp)

set_target_properties(
    godot-cpp PROPERTIES
    CXX_VISIBILITY_PRESET hidden # visibility needs to be the same as the main library
)

target_link_libraries(
    ${PROJECT_NAME} PRIVATE
    godot-cpp
)

file(GLOB_RECURSE SRCS src/*.cpp)

target_sources(${PROJECT_NAME} PRIVATE ${SRCS})

target_include_directories(${PROJECT_NAME} PRIVATE "src")

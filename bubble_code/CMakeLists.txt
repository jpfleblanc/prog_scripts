cmake_minimum_required(VERSION 2.8)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

project (BoldDCA)

find_package(ALPSCore REQUIRED COMPONENTS hdf5 accumulators mc params gf)
find_package(HDF5 REQUIRED)

find_package (Boost COMPONENTS program_options filesystem system serialization REQUIRED)

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${ALPSCore_INCLUDES})
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -g -DNDEBUG -DBOOST_DISABLE_ASSERTS")

add_executable(bubble
bubble.cpp
)

target_link_libraries(bubble
${ALPSCore_LIBRARIES}
${Boost_LIBRARIES}
${HDF5_LIBRARIES}
)

# Copyright 2018 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# cmake build file for C++ route_guide example.
# Assumes protobuf and gRPC have been installed using cmake.
# See cmake_externalproject/CMakeLists.txt for all-in-one cmake build
# that automatically builds all the dependencies before building route_guide.

cmake_minimum_required(VERSION 3.16)

project(grpc_x3plus C CXX)

include(../cmake/common.cmake)

# Find absl package
find_package(absl CONFIG REQUIRED)

# Proto file
get_filename_component(x3plus_proto "../../protos/x3plus.proto" ABSOLUTE)
get_filename_component(x3plus_proto_path "${x3plus_proto}" PATH)

# Generated sources
set(x3plus_proto_srcs "${CMAKE_CURRENT_BINARY_DIR}/route_guide.pb.cc")
set(x3plus_proto_hdrs "${CMAKE_CURRENT_BINARY_DIR}/route_guide.pb.h")
set(x3plus_grpc_srcs "${CMAKE_CURRENT_BINARY_DIR}/route_guide.grpc.pb.cc")
set(x3plus_grpc_hdrs "${CMAKE_CURRENT_BINARY_DIR}/route_guide.grpc.pb.h")
add_custom_command(
      OUTPUT "${x3plus_proto_srcs}" "${x3plus_proto_hdrs}" "${x3plus_grpc_srcs}" "${x3plus_grpc_hdrs}"
      COMMAND ${_PROTOBUF_PROTOC}
      ARGS --grpc_out "${CMAKE_CURRENT_BINARY_DIR}"
        --cpp_out "${CMAKE_CURRENT_BINARY_DIR}"
        -I "${x3plus_proto_path}"
        --plugin=protoc-gen-grpc="${_GRPC_CPP_PLUGIN_EXECUTABLE}"
        "${x3plus_proto}"
      DEPENDS "${x3plus_proto}")

# Include generated *.pb.h files
include_directories("${CMAKE_CURRENT_BINARY_DIR}")

# x3plus_grpc_proto
add_library(x3plus_grpc_proto
  ${x3plus_grpc_srcs}
  ${x3plus_grpc_hdrs}
  ${x3plus_proto_srcs}
  ${x3plus_proto_hdrs})
target_link_libraries(x3plus_grpc_proto
  absl::absl_log
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

# route_guide_helper
add_library(route_guide_helper
  "helper.h"
  "helper.cc")
target_link_libraries(route_guide_helper
  x3plus_grpc_proto
  ${_REFLECTION}
  ${_GRPC_GRPCPP}
  ${_PROTOBUF_LIBPROTOBUF})

# Targets route_guide_(client|server)
foreach(_target
  route_guide_client route_guide_server
  route_guide_callback_client route_guide_callback_server)
  add_executable(${_target}
    "${_target}.cc")
  target_link_libraries(${_target}
    x3plus_grpc_proto
    route_guide_helper
    absl::flags_parse
    absl::absl_log
    absl::log_initialize
    absl::log_globals
    ${_REFLECTION}
    ${_GRPC_GRPCPP}
    ${_PROTOBUF_LIBPROTOBUF})
endforeach()

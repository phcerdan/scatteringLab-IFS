cmake_minimum_required (VERSION 2.8.11)
project (Correlator)
add_executable(sample sample.cpp)
add_custom_command(TARGET sample POST_BUILD
                   COMMAND ${CMAKE_COMMAND} -E copy_if_different 
                       ${CMAKE_SOURCE_DIR}/flex02-01dc_win7.dll $<TARGET_FILE_DIR:sample>)


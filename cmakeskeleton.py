#! /usr/bin/env python
import os

# 1) Need a short python script that prompts for input and creates a complete CMake folder stucture and project skeleton
# Input needed:
#    * Project name
#    * External libraries
#    * Desired project library names
#    
# Then
#    * Create root CMakeLists.txt. Set default flags for clang++ and -g and -Wall etc, the whole point of this is a quick project system for c++11 practice
#    * Create $projectname dir and $projectname/main.cpp and CMakeLists.txt 
#    * foreach lib, create $libname and $libname/libname.(h|cpp) and CMakeLists.txt
#    * create build dir
#    * try to generate a .proj file with path to executable in it, for pyclewn debugging
#
#
# 2) need scripts to 
#    * add new h/cpp file to a lib and generate skeleton cpp files


if __name__ == "__main__":
    projectName = raw_input("Project Name: ")	

    externals = []
    while(True):
        result = raw_input("External libs for cmake to find? (blank for none or to stop)")
        if result == '':
            break
        else:
            externals.append(result)


    libs = []
    while(True):
        result = raw_input("libs to create? (blank for none or to stop)")
        if result == '':
            break
        else:
            libs.append(result)


    print "Creating project skeleton..."

    # create project root
    os.mkdir(projectName)

    # create root CMakeLists.txt
    buf = """
# The name of our project is "PROJECTNAME". CMakeLists files in this project can 
# refer to the root source directory of the project as ${PROJECTNAME_SOURCE_DIR} and 
# to the root binary directory of the project as ${PROJECTNAME_BINARY_DIR}. 
cmake_minimum_required (VERSION 2.6) 
project (PROJECTNAME) 

set(CMAKE_CXX_FLAGS "-g -Wall")\n\n""".replace("PROJECTNAME", projectName.upper())

    root_cmkl = os.open(projectName + os.path.sep + "CMakeLists.txt", os.O_RDWR|os.O_CREAT) 
    os.write(root_cmkl, buf)

    # tell cmake to look for external libs
    for ex in externals:
        os.write(root_cmkl, "find_package(" + ex + ")")
        os.write(root_cmkl, "\n")   
    os.write(root_cmkl, "\n")   

    # add the project executable dir
    os.write(root_cmkl, "add_subdirectory(" + projectName + ")" )
    os.write(root_cmkl, "\n")   

    # add our libraries as subdirs
    for lib in libs:
        os.write(root_cmkl, "add_subdirectory(" + lib + ")")
        os.write(root_cmkl, "\n")   
    os.write(root_cmkl, "\n")   


    # create dirs for project and libs
    os.mkdir(projectName + os.path.sep + "build")
    os.mkdir(projectName + os.path.sep + projectName)
    
    for l in libs:
        os.mkdir(projectName + os.path.sep + l)

    # create executable CMakeLists.txt
    buf = """include_directories (${PROJECTNAME_SOURCE_DIR})\n"""
    for l in libs:
        buf += "include_directories (${PROJECTNAME_SOURCE_DIR}/" + l + ")\n"
    buf += "\n\n"
    for l in libs:
        buf += "link_directories (${PROJECTNAME_BINARY_DIR}/" + l +")\n" 
    buf += "\n\n"
    buf += "add_executable (" + projectName + " main.cpp)\n"
    for l in libs:
        buf += "target_link_libraries(" + projectName + " " + l +")\n" 
    buf += "\n\n"
   
    buf = buf.replace("PROJECTNAME", projectName.upper())

    main_cmkl = os.open(projectName + os.path.sep + projectName + os.path.sep + "CMakeLists.txt", os.O_RDWR|os.O_CREAT) 
    os.write(main_cmkl, buf)

    # create main.cpp
    buf = "#include <iostream>\n"
    for l in libs:
        buf += """#include "%s/%s.h" \n""" % (l, l)

    buf += "\nusing namespace std;\n\nint main(void)\n{\n    return 0;\n}\n"

    main_cpp = os.open(projectName + os.path.sep + projectName + os.path.sep + "main.cpp", os.O_RDWR|os.O_CREAT) 
    os.write(main_cpp, buf)

    # create libs CMakeLists.txt and skeleton .h and .cpp
    for l in libs:
        buf = """#ifndef LIB1\n #define LIB1\n\n\n #endif\n""".replace("LIB1", l.upper())
        lib_h = os.open(projectName + os.path.sep + l + os.path.sep + l + ".h", os.O_RDWR|os.O_CREAT) 
        os.write(lib_h, buf)
        
        buf = """#include <iostream>\n#include "lib1.h"\n\nusing namespace std;\n\n""".replace("lib1", l)
        lib_cpp = os.open(projectName + os.path.sep + l + os.path.sep + l + ".cpp", os.O_RDWR|os.O_CREAT) 
        os.write(lib_cpp, buf)

        buf = """add_library (lib1 lib1.h lib1.cpp)""".replace("lib1", l)
        lib_cmkl = os.open(projectName + os.path.sep + l + os.path.sep + "CMakeLists.txt", os.O_RDWR|os.O_CREAT) 
        os.write(lib_cmkl, buf)

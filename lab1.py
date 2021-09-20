# This is the source code for Lab 1.

# Helpful for parsing command line arguments
import sys


# Process the arguments to prepare for the real actions.
if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("Usage: $python3 lab1.py terrain-image elevation-file path-file output-image-filename")
        exit()

    # Determine if there is a proper terrain image
    terrain = sys.argv[1].split(".")
    if terrain[1] != "png":
        print("Error: First argument is not a png file")
        exit()
    try:
        file1 = open(sys.argv[1], "r")
    except FileNotFoundError:
        print("Error: " + sys.argv[1] + " not found")

    # Determine if there is a proper elevation file
    elevation = sys.argv[2].split(".")
    if elevation[1] != "txt":
        print("Error: Second argument is not a text file")
        exit()
    try:
        file2 = open(sys.argv[2], "r")
    except FileNotFoundError:
        print("Error: " + sys.argv[2] + " not found")

    # Determine if there is a proper path file
    path = sys.argv[3].split(".")
    if path[1] != "txt":
        print("Error: Third argument is not a text file")
        exit()
    try:
        file3 = open(sys.argv[3], "r")
    except FileNotFoundError:
        print("Error: " + sys.argv[3] + " not found")

    # Determine if there is a proper output image
    output = sys.argv[4].split(".")
    if output[1] != "png":
        print("Error: Fourth argument is not a png file")
        exit()
    try:
        file4 = open(sys.argv[4], "r")
    except FileNotFoundError:
        print("Error: " + sys.argv[4] + " not found")
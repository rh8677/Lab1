# This is the source code for Lab 1.

# Useful utilities that will be imported
from PIL import Image
import math
import sys

# the list of pixels that will be drawn onto the terrain image
path = []

# speed heuristics for each terrain
speed = {"Open land": 0.9, "Rough meadow": 0.1, "Easy movement forest": 0.8, "Slow run forest": 0.5,
         "Walk forest": 0.4, "Impassible vegetation": 0, "Lake/Swamp/Marsh": 0, "Paved road": 1, "Footpath": 0.9,
         "Out of bounds": 0}

# The rgb combinations that represent each type of terrain
terrainColors = {(248, 148, 18): "Open land", (255, 192, 0): "Rough meadow", (255, 255, 255): "Easy movement forest",
                 (2, 208, 60): "Slow run forest", (2, 136, 40): "Walk forest", (5, 73, 24): "Impassible vegetation",
                 (0, 0, 255): "Lake/Swamp/Marsh", (71, 51, 3): "Paved road", (0, 0, 0): "Footpath",
                 (205, 0, 101): "Out of bounds"}


# Each pixel is represented as such, with coordinates, types of
# terrain, elevation, parents, and cost + heuristic
class Pixel:
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y
        self.type = None
        self.elevation = None
        self.parent = None
        self.penalty = float()


# Combines the pixels from the terrain image and elevations from
# the elevation file into a single array
def buildTerrain(terrArray, elevationInfo):
    terr_combined = []
    for build_row in range(500):
        pixel_row = []
        for build_col in range(395):
            new_pixel = Pixel(build_row, build_col)
            new_pixel.type = terrainColors[terrArray[build_row][build_col][:3]]
            new_pixel.elevation = elevationInfo[build_row][build_col]
            pixel_row.append(new_pixel)
        terr_combined.append(pixel_row)
    return terr_combined


# Calculates the cost from one location to another
def distanceCost(start, end, heading):
    if heading == "X":
        dist = math.sqrt((10.29 ** 2) + (end.elevation - start.elevation) ** 2)
    else:
        dist = math.sqrt((7.55 ** 2) + (end.elevation - start.elevation) ** 2)
    cost = dist / (speed[start.type] + (start.elevation - end.elevation) / 40)
    return cost


# Calculates the heuristic from one location to another
def distanceHeuristic(start, end):
    return math.sqrt((start.x_coord - end.x_coord) ** 2 + (start.y_coord - end.y_coord) ** 2 + (start.elevation -
                                                                                                end.elevation) ** 2) / 2


# Calculates the total penalty (cost + heuristic)
def distanceTotal(current, neighbour, destination):
    if neighbour.x_coord == current.x_coord:
        penalty = distanceCost(current, neighbour, "X") + distanceHeuristic(neighbour, destination)
    else:
        penalty = distanceCost(current, neighbour, "Y") + distanceHeuristic(neighbour, destination)
    return penalty


# Returns all the pixels that are reachable from the starting one
def getNeighbors(start, terrain_map):
    reachable = []
    x = start.x_coord
    y = start.y_coord

    # If the starting x- and y-coordinates are at the border
    if x == 0 and y == 0:
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])

    # If the starting x-coordinate is at the border
    elif x == 0 and (0 < y < 394):
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])

    # If the starting x- and y-coordinates are at the border
    elif x == 0 and y == 394:
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])

    # If the starting x- and y-coordinates are at the border
    elif x == 499 and y == 0:
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])

    # If the starting x-coordinate is at the border
    elif x == 499 and (0 < y < 394):
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])

    # If the starting x- and y-coordinates are at the border
    elif x == 499 and y == 394:
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])

    # If the starting y-coordinate is at the border
    elif y == 0 and (0 < x < 499):
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])

    # If the starting y-coordinate is at the border
    elif y == 394 and (0 < x < 499):
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])

    # If the pixel is not near any borders
    else:
        if speed[terrain_map[x + 1][y].type] != 0:
            reachable.append(terrain_map[x + 1][y])
        if speed[terrain_map[x][y - 1].type] != 0:
            reachable.append(terrain_map[x][y - 1])
        if speed[terrain_map[x - 1][y].type] != 0:
            reachable.append(terrain_map[x - 1][y])
        if speed[terrain_map[x][y + 1].type] != 0:
            reachable.append(terrain_map[x][y + 1])

    # return the list of neighbor pixels
    return reachable


# Return the location that has the lowest cost + heuristic
def getBestNode(toExplore):
    best = None
    minimum = float("inf")
    for node in toExplore:
        if node.penalty < minimum:
            minimum = node.penalty
            best = node
    return best


# A* is performed on the terrain
def starSearch(source, destination, terrain_mapping):
    if (speed[source.type] == 0):
        print("not a valid source")
        return
    if (speed[destination.type] == 0):
        print("not a valid destination")
        return
    visited = []  # pixels that have been visited
    toExplore = []  # pixels that have to be visited (frontier)
    source.penalty = 0
    current = source  # current pixel
    toExplore.append(current)
    while len(toExplore) != 0:
        # as long as the frontier is not empty
        current = getBestNode(toExplore)
        if current == destination:
            # if a path is found
            while current.parent:
                # compute the path
                point = []
                point.append(current.x_coord)
                point.append(current.y_coord)
                path.append(point)
                current = current.parent
            point = []
            point.append(current.x_coord)
            point.append(current.y_coord)
            path.append(point)
            return path
        toExplore.remove(current)
        visited.append(current)
        neighbours = getNeighbors(current, terrain_mapping)
        for neighbour in neighbours:
            # coputing the scores for each neighbour
            if neighbour not in visited:
                if neighbour in toExplore:
                    # if the neighbour has been seen before
                    score = distanceTotal(current, neighbour, destination)
                    if score < neighbour.penalty:
                        neighbour.penalty = score
                        neighbour.parent = current
                else:
                    # if the neighbour has not been seen before
                    neighbour.penalty = distanceTotal(current, neighbour, destination)
                    neighbour.parent = current
                    toExplore.append(neighbour)
    print("no path found")


# Process the arguments to prepare for the real actions.
if __name__ == '__main__':
    # Open the terrain image and retrieve the necessary data
    terrain_image = Image.open(sys.argv[1])
    image_data = list(terrain_image.getdata())
    terrain_array = []
    row = []
    column = 0
    for pixel in image_data:
        row.append(pixel)
        column += 1
        if column == 395:
            column = 0
            terrain_array.append(row)
            row = []

    # Open the elevation file and retrieve the necessary data
    elevations = []
    with open(sys.argv[2]) as elevation_file:
        for line in elevation_file:
            line = line.strip()
            elevate_digit = line.split()
            for i in range(len(elevate_digit)):
                elevate_digit[i] = float(elevate_digit[i])
            elevations.append(elevate_digit)

    # Open the path file and retrieve the necessary data
    path_data = []
    with open(sys.argv[3]) as path_file:
        for line in path_file:
            point = []
            line = line.strip()
            temp = line.split()
            point.append(int(temp[1]))
            point.append(int(temp[0]))
            path_data.append(point)

    # For each pair
    for i in range(len(path_data) - 1):
        terrain = buildTerrain(terrain_array, elevations)
        begin = path_data[i]
        finish = path_data[i + 1]
        starSearch(terrain[begin[0]][begin[1]], terrain[finish[0]][finish[1]], terrain)

    # For each location that the A* returned in the path array,
    # we draw it on the output image
    for path_pixel in path:
        terrain_image.putpixel((path_pixel[1], path_pixel[0]), (255, 0, 127))

    # Output the image with the path drawn
    path_name = sys.argv[3].split(".")
    terrain_image.save(path_name[0] + "Out.png")

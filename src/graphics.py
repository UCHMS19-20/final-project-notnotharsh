import sys, pygame, pygame.gfxdraw, random, math, time

# The following function takes the values of a point in 3D space to be transformed and returns the coordinates on which to blit said point, depending on the screen size, the user's location, and the direction (up, down, forward) the user is looking.
def point_transform(point, size, y_val):
    global coords, theta
    # The following block of code returns the translated coordinates of the point with respect to the user's location.
    x_dist = point[0] - coords[0]
    y_dist = point[1] - coords[1]
    z_dist = point[2] - coords[2]
    # These cases process the rotations of the points depending on whether the user is looking up, down, or forward
    if y_val == 1:
        new_x = x_dist * math.cos(math.pi / 2 - theta) - y_dist * math.sin(math.pi / 2 - theta)
        new_y = y_dist * math.cos(math.pi / 2 - theta) + x_dist * math.sin(math.pi / 2 - theta)
        new_z = z_dist
    elif y_val == 2:
        new_y = z_dist * -1
        new_x = x_dist * math.cos(math.pi / 2 - theta) - y_dist * math.sin(math.pi / 2 - theta)
        new_z = y_dist * math.cos(math.pi / 2 - theta) + x_dist * math.sin(math.pi / 2 - theta)
    else:
        new_y = z_dist
        new_x = x_dist * math.cos(math.pi / 2 - theta) - y_dist * math.sin(math.pi / 2 - theta)
        new_z = -1 * y_dist * math.cos(math.pi / 2 - theta) - x_dist * math.sin(math.pi / 2 - theta)
    # These final lines of code yield the angles of the points as an array by processing them and returning coordinates based on where to blit said point.
    x_angle = math.atan2(new_x, new_y)
    z_angle = math.atan2(new_z, new_y)
    # The last element in this array yields if the point is in front of or behind the user. It is useful later in drawing lines where some points are offscreen.
    display_angles = [(size[0] / 2) * (1 + 2 * x_angle), (size[0] / 2) * (1 - 2 * z_angle), new_y > 0]
    return display_angles

# The following function takes the point given from point_transform and draws it on the screen. If not, it just passes it through for all three views for any other method to call it.
def draw_point(point, draw, color):
    global mid_size, side_size, top_screen, mid_screen, bottom_screen
    top_display_coords = point_transform(point, side_size, 0)
    mid_display_coords = point_transform(point, mid_size, 1)
    bottom_display_coords = point_transform(point, side_size, 2)
    if draw: # if user chooses to draw this point, do the pygame draw
        pygame.draw.circle(top_screen, color, (int(top_display_coords[0]), int(top_display_coords[1])), 4)
        pygame.draw.circle(mid_screen, color, (int(mid_display_coords[0]), int(mid_display_coords[1])), 4)
        pygame.draw.circle(bottom_screen, color, (int(bottom_display_coords[0]), int(bottom_display_coords[1])), 4)
    return [top_display_coords, mid_display_coords, bottom_display_coords]

# The following function gets the coordinates of two points to draw (optionally) draws them, and draws the line between them.
def draw_line(p1, p2, draw_points, color):
    global top_screen, mid_screen, bottom_screen
    coords_set_1 = draw_point(p1, draw_points, color)
    coords_set_2 = draw_point(p2, draw_points, color)
    # These variables are defined based on whether either point is in front or behind the user. It is just an analysis on the variable introduced at the end of point_transform.
    top_forward = coords_set_1[0][2] or coords_set_2[0][2]
    mid_forward = coords_set_1[1][2] or coords_set_2[1][2]
    bottom_forward = coords_set_1[2][2] or coords_set_2[2][2]
    # If in each view, not a single point of the line is in front of the user, don't draw the line. It makes the code more efficient and prevents edge cases of lines being on screen when they shouldn't be.
    if top_forward:
        pygame.draw.line(top_screen, color, (int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), 4)
    if mid_forward:
        pygame.draw.line(mid_screen, color, (int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), 4)
    if bottom_forward:
        pygame.draw.line(bottom_screen, color, (int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), 4)
    return [coords_set_1, coords_set_2]

# This function just outputs the square of the distance from the user. It is used for the purposes of ranking which surfaces to draw and how to color each surface.
def get_dist_squared(surface, pos):
    center_x = (min(surface[0][0], surface[1][0], surface[2][0], surface[3][0]) + max(surface[0][0], surface[1][0], surface[2][0], surface[3][0])) / 2
    center_y = (min(surface[0][1], surface[1][1], surface[2][1], surface[3][1]) + max(surface[0][1], surface[1][1], surface[2][1], surface[3][1])) / 2
    center_z = (min(surface[0][2], surface[1][2], surface[2][2], surface[3][2]) + max(surface[0][2], surface[1][2], surface[2][2], surface[3][2])) / 2
    return (math.pow(center_x - pos[0], 2) + math.pow(center_y - pos[1], 2) + math.pow(center_z - pos[2], 2))

# This is a function to return a color based on two distances: one from the user and one from a certain coordinate where a light is.
# The minimum function in the RGB values is to cap the values to keep them valid. Blue is computed slightly darker to give the color its tan/sandstone appearance.``
def return_color(dist_squared, from_outside):
    return (min(250, 300 / dist_squared + 650 / from_outside), min(250, 300 / dist_squared + 650 / from_outside), min(225, 250 / dist_squared + 600 / from_outside)) # blue is a bit less

# This function draws a surface given by three sets of coordinates, boolean values for whether or not to draw the lines, and what color/transparency to color the surface.
def draw_surface(plist, draw_points, draw_lines, color, transparent):
    global top_screen, mid_screen, bottom_screen
    coords_set_1 = draw_point(plist[0], draw_points, color)
    coords_set_2 = draw_point(plist[1], draw_points, color)
    coords_set_3 = draw_point(plist[2], draw_points, color)
    coords_set_4 = draw_point(plist[3], draw_points, color)
    # These boolean values are defined based on, for each view, whether there exists a single point in front of the user.
    top_forward = (coords_set_1[0][2] or coords_set_2[0][2]) or (coords_set_3[0][2] or coords_set_4[0][2])
    mid_forward = (coords_set_1[1][2] or coords_set_2[1][2]) or (coords_set_3[1][2] or coords_set_4[1][2])
    bottom_forward = (coords_set_1[2][2] or coords_set_2[2][2]) or (coords_set_3[2][2] or coords_set_4[2][2])
    if draw_lines: # if yes, draw the lines
        draw_line(plist[0], plist[1], draw_points, color)
        draw_line(plist[1], plist[2], draw_points, color)
        draw_line(plist[2], plist[3], draw_points, color)
        draw_line(plist[3], plist[0], draw_points, color)
    if transparent == 2:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 63)
    elif transparent == 1:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 127)
    else:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 255)
    # These if cases control if the surface is drawn, based on the boolean values for whether it is in front for each view.
    if top_forward:
        pygame.gfxdraw.filled_polygon(top_screen, [(int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), (int(coords_set_3[0][0]), int(coords_set_3[0][1])), (int(coords_set_4[0][0]), int(coords_set_4[0][1]))], color_obj)
    if mid_forward:
        pygame.gfxdraw.filled_polygon(mid_screen, [(int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), (int(coords_set_3[1][0]), int(coords_set_3[1][1])), (int(coords_set_4[1][0]), int(coords_set_4[1][1]))], color_obj)
    if bottom_forward:
        pygame.gfxdraw.filled_polygon(bottom_screen, [(int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), (int(coords_set_3[2][0]), int(coords_set_3[2][1])), (int(coords_set_4[2][0]), int(coords_set_4[2][1]))], color_obj)

# This method adds, depending on the quality of the rendering, either the 6 or 24 surfaces that define a cube (24 implies four on each face) to the surfaces array. Every surface in this array is drawn.
def add_cube(corner):
    global surfaces, high_quality
    transparent = [-1, -1, -1]
    if len(corner) != 3: # just lets the color data through into the surfaces list if transparent, that's handled in draw_surface
        transparent = [corner[3], corner[4], corner[5]]
    x = corner[0]
    y = corner[1]
    z = corner[2]
    if high_quality: # draw 24
        if [[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z], transparent]) # bottom left front
        if [[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z], transparent] not in surfaces:
            surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z], transparent]) # bottom right front
        if [[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z], transparent]) # bottom left back
        if [[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z], transparent]) # bottom right back
        if [[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2], transparent]) # top left front
        if [[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2], transparent] not in surfaces:
            surfaces.append([[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2], transparent]) # top right front
        if [[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent]) # top left back
        if [[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent]) # top right back
        if [[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1], transparent]) # front bottom left
        if [[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1], transparent] not in surfaces:
            surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1], transparent]) # front bottom right
        if [[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2], transparent]) # front top left
        if [[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2], transparent] not in surfaces:
            surfaces.append([[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2], transparent]) # front top right
        if [[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1], transparent] not in surfaces:
            surfaces.append([[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1], transparent]) # back bottom left
        if [[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1], transparent] not in surfaces:
            surfaces.append([[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1], transparent]) # back bottom right
        if [[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent]) # back top left
        if [[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent]) # back top right
        if [[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z], transparent]) # left front bottom
        if [[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1], transparent] not in surfaces:
            surfaces.append([[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1], transparent]) # left front top
        if [[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z], transparent]) # left back bottom
        if [[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1], transparent] not in surfaces:
            surfaces.append([[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1], transparent]) # left back top
        if [[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z], transparent] not in surfaces:
            surfaces.append([[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z], transparent]) # right front bottom
        if [[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1], transparent] not in surfaces:
            surfaces.append([[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1], transparent]) # right front top
        if [[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z], transparent]) # right back bottom
        if [[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1], transparent] not in surfaces:
            surfaces.append([[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1], transparent]) # right back top
    else: # draw 6
        if [[x, y, z], [x + 2, y, z], [x + 2, y + 2, z], [x, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x + 2, y, z], [x + 2, y + 2, z], [x, y + 2, z], transparent]) # bottom
        if [[x, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 2, z + 2], [x, y + 2, z + 2], transparent]) # top
        if [[x, y, z], [x + 2, y, z], [x + 2, y, z + 2], [x, y, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x + 2, y, z], [x + 2, y, z + 2], [x, y, z + 2], transparent]) # front
        if [[x, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
            surfaces.append([[x, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 2], [x, y + 2, z + 2], transparent]) # back
        if [[x, y, z], [x, y, z + 2], [x, y + 2, z + 2], [x, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x, y, z], [x, y, z + 2], [x, y + 2, z + 2], [x, y + 2, z], transparent]) # left
        if [[x + 2, y, z], [x + 2, y, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z], transparent] not in surfaces:
            surfaces.append([[x + 2, y, z], [x + 2, y, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z], transparent]) # right

# This function takes a set of coordinates and determines if the user is inside a normal block.
def free(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2))]
    return local_cube not in cubes

# This function takes a set of coordinates and determines if the user is inside a death zone.
def alive(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 127, 0, 0]
    return local_cube not in cubes

# This function takes a set of coordinates and determines if the user is inside a victory zone.
def playing(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 0, 127, 0]
    return local_cube not in cubes

# This function takes a set of coordinates and determines if the user is inside a starting zone.
def outside(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 0, 0, 127]
    return local_cube not in cubes

size_coefficient = 50 # change this to set size

# These next few statements declare each array in terms of the size coefficient. They are useful for forming surfaces of that size.
side_size = (5 * size_coefficient, 5 * size_coefficient)
mid_size = (8 * size_coefficient, 8 * size_coefficient)
items_size = (mid_size[0], side_size[1] * 2 - mid_size[1])

# These give the starting coordinates and angle for the user.
coords = [1, -5, 1]
theta = math.pi / 2

# These give the translational and rotational speed (that determine how fast the user can move and rotate).
trans_speed = .1
rot_speed = math.pi / 50

cubes = [] # cubes list initialized to keep track of all cubes
surfaces = [] # surfaces list initialized to keep track for all surfaces - is always defined by performing add_cube() of the bottom left corner of every cube

# These lines of code set up pygame, the window title, and the screens on which everything will be displayed.
pygame.init()
pygame.display.set_caption("Maze Minecraft")
total_screen = pygame.display.set_mode((side_size[0] + mid_size[0], 2 * side_size[1]))
top_screen = pygame.Surface(side_size)
mid_screen = pygame.Surface(mid_size)
bottom_screen = pygame.Surface(side_size)
items_screen = pygame.Surface(items_size)

# These next few lines of code set up the text to be displayed throughout the game.
font = pygame.font.SysFont("Courier", 50)
little_font = pygame.font.SysFont("Courier", 20, bold = True)
top_text = little_font.render("top", True, (127, 127, 127))
bottom_text = little_font.render("bottom", True, (127, 127, 127))
front_text = little_font.render("forward", True, (127, 127, 127))
won_text = font.render("you won!", True, (255, 255, 255))
lost_text = font.render("you lost!", True, (255, 255, 255))
build_text = font.render("build", True, (255, 255, 255))
play_text = font.render("play", True, (255, 255, 255))
high_text = font.render("quality: high", True, (255, 255, 255))
low_text = font.render("quality: low", True, (255, 255, 255))

# These lines of code set up the rectangles containing the text boxes to be displayed.
won_text_rect = won_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1]))
lost_text_rect = lost_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1]))
build_text_rect = build_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1] / 2))
play_text_rect = play_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1]))
high_text_rect = high_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, 3 * side_size[1] / 2))
low_text_rect = low_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, 3 * side_size[1] / 2))

# These lines of code set up the images that show the pickaxe, green, red, and opaque cubes.
pickaxe = pygame.transform.scale(pygame.image.load("img/pickaxe.png"), (items_size[1], items_size[1]))
normal_cube = pygame.transform.scale(pygame.image.load("img/normalcube.png"), (items_size[1], items_size[1]))
green_cube = pygame.transform.scale(pygame.image.load("img/greencube.png"), (items_size[1], items_size[1]))
red_cube = pygame.transform.scale(pygame.image.load("img/redcube.png"), (items_size[1], items_size[1]))

# These lines of code set up the rectangles containing the above images.
pickaxe_rect = pickaxe.get_rect(topleft = (0, 0))
normal_cube_rect = normal_cube.get_rect(topleft = (items_size[1], 0))
green_cube_rect = green_cube.get_rect(topleft = (2 * items_size[1], 0))
red_cube_rect = red_cube.get_rect(topleft = (3 * items_size[1], 0))

high_quality = True # sets the default setting for the quality of the graphics to be high and can be changed in the main menu

# These lines of code read the file cubes.txt to form the cubes array. Since the entire cubes (and therefore surfaces) array is formed from this file, it can be copied to any other instance of this game.
f = open("cubes.txt", "r")
cube_strings = f.readlines()
for i in cube_strings:
    text = i.split()
    if len(text) == 3:
        cubes.append([int(text[0]), int(text[1]), int(text[2])])
    else:
        cubes.append([int(text[0]), int(text[1]), int(text[2]), int(text[3]), int(text[4]), int(text[5])])

for i in cubes:
    add_cube(i) # adds every surface of every cube to the surfaces list

# Each of these boolean values represents if something is happening in the game - any single one of them being true triggers an inner loop in the main game loop below, which triggers another set of events.
main_menu = True
build_loop = False
game_loop = False
won = False
saving = False

# This stamp is used to rebuild the surfaces array every every 10 iterations of the game loop.
buildstamp = 0

# This main loop is the game loop - it has a lot of inner loops inside.
while True:

    # This inner loop controls the main menu screen, blits setting for high/low quality and options to play or build
    while main_menu:
        coords = [1, -5, 1]
        theta = math.pi / 2
        total_screen.fill([0, 0, 0])
        total_screen.blit(build_text, build_text_rect)
        total_screen.blit(play_text, play_text_rect)
        if high_quality:
            total_screen.blit(high_text, high_text_rect)
        else:
            total_screen.blit(low_text, low_text_rect)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # onclick trigger
                if play_text_rect.collidepoint(pos): # start play loop
                    main_menu = False
                    game_loop = True
                elif build_text_rect.collidepoint(pos): # start build loop
                    main_menu = False
                    build_loop = True
                elif high_text_rect.collidepoint(pos) and high_quality: # set quality to low
                    high_quality = False
                elif low_text_rect.collidepoint(pos) and not high_quality: # set quality to high
                    high_quality = True
        pygame.display.flip()

    # This inner loop controls the gameplay when the mode is to solve the maze (opaque cubes, deaths and victories are real).
    while game_loop:
        # This if case resets the surface list to rebuild / update surfaces every 10 iterations.
        if buildstamp % 10 == 0:
            del surfaces[:]
            for i in cubes:
                add_cube(i)
        buildstamp += 1 # increments loop count
        won = False
        # These next few lines end the game loop if the player is in a red or green block.
        if not alive(coords):
            game_loop = False
        if not playing(coords):
            game_loop = False
            won = True
        # The next lines of code just set the entire screen black.
        total_screen.fill([0, 0, 0])
        top_screen.fill([0, 0, 0])
        mid_screen.fill([0, 0, 0])
        bottom_screen.fill([0, 0, 0])
        items_screen.fill([0, 0, 0])
        surfaces.sort(key = lambda surface: get_dist_squared(surface, coords), reverse = True)
        for i in surfaces:
            if i[4] == [-1, -1, -1]:
                draw_surface(i, False, False, return_color(get_dist_squared(i, coords), get_dist_squared(i, [1, -5, 1])), 0)
            else:
                draw_surface(i, False, False, i[4], 2)
        keystate = pygame.key.get_pressed() # gets list of booleans for all keys based on whether they are currently pressed
        if keystate[pygame.K_z]: # moves forward relative to direction
            if free([coords[0] + 10 * trans_speed * math.cos(theta), coords[1] + 10 * trans_speed * math.sin(theta), coords[2]]): # checks if next move is allowed (if it collides)
                coords[0] += trans_speed * math.cos(theta)
                coords[1] += trans_speed * math.sin(theta)
        if keystate[pygame.K_x]: # moves back relative to direction
            if free([coords[0] - 10 * trans_speed * math.cos(theta), coords[1] - 10 * trans_speed * math.sin(theta), coords[2]]): # checks if next move is allowed (if it collides)
                coords[0] -= trans_speed * math.cos(theta)
                coords[1] -= trans_speed * math.sin(theta)
        if keystate[pygame.K_a]: # moves left relative to direction
            if free([coords[0] - 10 * trans_speed * math.sin(theta), coords[1] + 10 * trans_speed * math.cos(theta), coords[2]]): # checks if next move is allowed (if it collides)
                coords[0] -= trans_speed * math.sin(theta)
                coords[1] += trans_speed * math.cos(theta)
        if keystate[pygame.K_d]: # moves right relative to direction
            if free([coords[0] + 10 * trans_speed * math.sin(theta), coords[1] - 10 * trans_speed * math.cos(theta), coords[2]]): # checks if next move is allowed (if it collides)
                coords[0] += trans_speed * math.sin(theta)
                coords[1] -= trans_speed * math.cos(theta)
        if keystate[pygame.K_w]: # moves up
            if free([coords[0], coords[1], coords[2] + 10 * trans_speed]): # checks if next move is allowed (if it collides)
                coords[2] += trans_speed
        if keystate[pygame.K_s]: # moves down
            if free([coords[0], coords[1], coords[2] - 10 * trans_speed]): # checks if next move is allowed (if it collides)
                coords[2] -= trans_speed
        if keystate[pygame.K_LEFT]: # rotates left
            theta += rot_speed
        if keystate[pygame.K_RIGHT]: # rotates right
            theta -= rot_speed
        if keystate[pygame.K_SPACE]:
            game_loop = False
            main_menu = True
        # These next few lines blit text onto the screens and the screens onto the main screen.
        top_screen.blit(top_text, (10, 10))
        bottom_screen.blit(bottom_text, (10, 10))
        mid_screen.blit(front_text, (10, 10))
        total_screen.blit(top_screen, (0, 0))
        total_screen.blit(bottom_screen, (0, side_size[1]))
        total_screen.blit(mid_screen, (side_size[0], 0))
        total_screen.blit(items_screen, (side_size[0], mid_size[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()

    # This inner loop controls the gameplay when the mode is to build the maze (translucent cubes, deaths and victories are not real).
    while build_loop:
        # This if case resets the surface list to rebuild / update surfaces every 10 iterations.
        if buildstamp % 10 == 0:
            del surfaces[:]
            for i in cubes:
                add_cube(i)
        buildstamp += 1 # increments loop count
        # The next lines of code just set the entire screen black.
        total_screen.fill([0, 0, 0])
        top_screen.fill([0, 0, 0])
        bottom_screen.fill([0, 0, 0])
        mid_screen.fill([0, 0, 0])
        items_screen.fill([0, 0, 0])
        surfaces.sort(key = lambda surface: get_dist_squared(surface, coords), reverse = True)
        for i in surfaces:
            if i[4] == [-1, -1, -1]:
                draw_surface(i, False, False, return_color(get_dist_squared(i, coords), get_dist_squared(i, [1, -5, 1])), 1)
            else:
                draw_surface(i, False, False, i[4], 2)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_z]: # moves forward relative to direction
            coords[0] += trans_speed * math.cos(theta)
            coords[1] += trans_speed * math.sin(theta)
        if keystate[pygame.K_x]: # moves back relative to direction
            coords[0] -= trans_speed * math.cos(theta)
            coords[1] -= trans_speed * math.sin(theta)
        if keystate[pygame.K_a]: # moves left relative to direction
            coords[0] -= trans_speed * math.sin(theta)
            coords[1] += trans_speed * math.cos(theta)
        if keystate[pygame.K_d]: # moves right relative to direction
            coords[0] += trans_speed * math.sin(theta)
            coords[1] -= trans_speed * math.cos(theta)
        if keystate[pygame.K_w]: # moves up
            coords[2] += trans_speed
        if keystate[pygame.K_s]: # moves down
            coords[2] -= trans_speed
        if keystate[pygame.K_LEFT]: # rotates left
            theta += rot_speed
        if keystate[pygame.K_RIGHT]: # rotates right
            theta -= rot_speed
        if keystate[pygame.K_SPACE]: # go back to main menu
            build_loop = False
            main_menu = True
            if not saving: # write cubes array to cubes.txt file
                saving = True
                w = open("cubes.txt", "w")
                cubestr = "" # initialize cube string to contain every cube
                for i in cubes:
                    if len(i) == 3:
                        cubestr += str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n"
                    else:
                        cubestr += str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]) + " " + str(i[4]) + " " + str(i[5]) + "\n"
                w.write(cubestr) # write cube string to file
                w.close() # close file writer
        # These next few lines blit text onto the different screens, the images onto the items screen, and the screens onto the main screen.
        top_screen.blit(top_text, (10, 10))
        bottom_screen.blit(bottom_text, (10, 10))
        mid_screen.blit(front_text, (10, 10))
        items_screen.blit(pickaxe, pickaxe_rect)
        items_screen.blit(normal_cube, normal_cube_rect)
        items_screen.blit(green_cube, green_cube_rect)
        items_screen.blit(red_cube, red_cube_rect)
        total_screen.blit(top_screen, (0, 0))
        total_screen.blit(bottom_screen, (0, side_size[1]))
        total_screen.blit(mid_screen, (side_size[0], 0))
        total_screen.blit(items_screen, (side_size[0], mid_size[1]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # The following case handles if the user clicked inside the build loop.
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                actual = (pos[0] - side_size[0], pos[1] - mid_size[1]) # get coordinates of mouse relative to top left of image screen
                if pickaxe_rect.collidepoint(actual): # handles if the user hits the pickaxe button (if the user wants to remove the block in which they currently are)
                    if not free(coords): # inside a normal block
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))]) # removes cube from list
                    if not alive(coords): # inside a death zone
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0]) # removes cube from list
                    if not playing(coords): # inside a victory zone
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0]) # removes cube from list
                elif green_cube_rect.collidepoint(actual) and (playing(coords) and outside(coords)): # handles if the user hits the green cube button (if the user wants to add a victory zone in the location in which they currently are)
                    if (free(coords) and alive(coords)) and playing(coords):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0]) # adds cube to list if not in already
                elif red_cube_rect.collidepoint(actual) and (playing(coords) and outside(coords)): # handles if the user hits the red cube button (if the user wants to add a death zone in the location in which they currently are)
                    if (free(coords) and alive(coords)) and playing(coords):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0]) # adds cube to list if not in already
                elif normal_cube_rect.collidepoint(actual) and (playing(coords) and outside(coords)): # case handles if the user hits the regular block button (if the user wants to add a regular block in the location in which they currently are)
                    if (free(coords) and alive(coords)) and playing(coords):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))]) # adds cube to list if not in already
        pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_SPACE]: # go back to main menu
        main_menu = True
        game_loop = False
    else:
        if won:
            total_screen.blit(won_text, won_text_rect) # show screen, you won!
        else:
            total_screen.blit(lost_text, lost_text_rect) # show screen, you lost!
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

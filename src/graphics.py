import sys, pygame, random, math, time

def point_transform(point, size, y_val):
    global coords, theta
    x_dist = point[0] - coords[0]
    y_dist = point[1] - coords[1]
    z_dist = point[2] - coords[2]
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
    x_angle = math.atan2(new_x, new_y)
    z_angle = math.atan2(new_z, new_y)
    display_angles = [(size[0] / 2) * (1 + 2 * x_angle), (size[0] / 2) * (1 - 2 * z_angle), new_y > 0]
    return display_angles

def draw_point(point, draw, color):
    global mid_size, side_size, top_screen, mid_screen, bottom_screen
    top_display_coords = point_transform(point, side_size, 0)
    mid_display_coords = point_transform(point, mid_size, 1)
    bottom_display_coords = point_transform(point, side_size, 2)
    if draw:
        pygame.draw.circle(top_screen, color, (int(top_display_coords[0]), int(top_display_coords[1])), 4)
        pygame.draw.circle(mid_screen, color, (int(mid_display_coords[0]), int(mid_display_coords[1])), 4)
        pygame.draw.circle(bottom_screen, color, (int(bottom_display_coords[0]), int(bottom_display_coords[1])), 4)
    return [top_display_coords, mid_display_coords, bottom_display_coords]

def draw_line(p1, p2, draw_points, color):
    global top_screen, mid_screen, bottom_screen
    coords_set_1 = draw_point(p1, draw_points, color)
    coords_set_2 = draw_point(p2, draw_points, color)
    top_forward = coords_set_1[0][2] or coords_set_2[0][2]
    mid_forward = coords_set_1[1][2] or coords_set_2[1][2]
    bottom_forward = coords_set_1[2][2] or coords_set_2[2][2]
    if top_forward:
        pygame.draw.line(top_screen, color, (int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), 4)
    if mid_forward:
        pygame.draw.line(mid_screen, color, (int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), 4)
    if bottom_forward:
        pygame.draw.line(bottom_screen, color, (int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), 4)
    return [coords_set_1, coords_set_2]

def get_dist_squared(surface, pos):
    center_x = (min(surface[0][0], surface[1][0], surface[2][0], surface[3][0]) + max(surface[0][0], surface[1][0], surface[2][0], surface[3][0])) / 2
    center_y = (min(surface[0][1], surface[1][1], surface[2][1], surface[3][1]) + max(surface[0][1], surface[1][1], surface[2][1], surface[3][1])) / 2
    center_z = (min(surface[0][2], surface[1][2], surface[2][2], surface[3][2]) + max(surface[0][2], surface[1][2], surface[2][2], surface[3][2])) / 2
    return (math.pow(center_x - pos[0], 2) + math.pow(center_y - pos[1], 2) + math.pow(center_z - pos[2], 2))

def return_color(dist_squared, from_outside):
    return (min(250, 300 / dist_squared + 10000 / from_outside), min(250, 300 / dist_squared + 10000 / from_outside), min(250, 300 / dist_squared + 10000 / from_outside))

def draw_surface(plist, draw_points, draw_lines, color):
    global top_screen, mid_screen, bottom_screen
    coords_set_1 = draw_point(plist[0], draw_points, color)
    coords_set_2 = draw_point(plist[1], draw_points, color)
    coords_set_3 = draw_point(plist[2], draw_points, color)
    coords_set_4 = draw_point(plist[3], draw_points, color)
    top_forward = (coords_set_1[0][2] or coords_set_2[0][2]) or (coords_set_3[0][2] or coords_set_4[0][2])
    mid_forward = (coords_set_1[1][2] or coords_set_2[1][2]) or (coords_set_3[1][2] or coords_set_4[1][2])
    bottom_forward = (coords_set_1[2][2] or coords_set_2[2][2]) or (coords_set_3[2][2] or coords_set_4[2][2])
    if draw_lines:
        draw_line(plist[0], plist[1], draw_points, color)
        draw_line(plist[1], plist[2], draw_points, color)
        draw_line(plist[2], plist[3], draw_points, color)
        draw_line(plist[3], plist[0], draw_points, color)
    if top_forward:
        pygame.draw.polygon(top_screen, color, [(int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), (int(coords_set_3[0][0]), int(coords_set_3[0][1])), (int(coords_set_4[0][0]), int(coords_set_4[0][1]))])
    if mid_forward:
        pygame.draw.polygon(mid_screen, color, [(int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), (int(coords_set_3[1][0]), int(coords_set_3[1][1])), (int(coords_set_4[1][0]), int(coords_set_4[1][1]))])
    if bottom_forward:
        pygame.draw.polygon(bottom_screen, color, [(int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), (int(coords_set_3[2][0]), int(coords_set_3[2][1])), (int(coords_set_4[2][0]), int(coords_set_4[2][1]))])

def add_cube(corner):
    global surfaces
    x = corner[0]
    y = corner[1]
    z = corner[2]
    if [[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z]] not in surfaces:
        surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z]])
    if [[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z]] not in surfaces:
        surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z]])
    if [[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z]] not in surfaces:
        surfaces.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z]])
    if [[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z]] not in surfaces:
        surfaces.append([[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z]])
    if [[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2]] not in surfaces:
        surfaces.append([[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2]])
    if [[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2]] not in surfaces:
        surfaces.append([[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2]])
    if [[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2]] not in surfaces:
        surfaces.append([[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2]])
    if [[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2]] not in surfaces:
        surfaces.append([[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2]])
    if [[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]] not in surfaces:
        surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1]])
    if [[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1]] not in surfaces:
        surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1]])
    if [[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2]] not in surfaces:
        surfaces.append([[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2]])
    if [[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2]] not in surfaces:
        surfaces.append([[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2]])
    if [[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1]] not in surfaces:
        surfaces.append([[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1]])
    if [[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1]] not in surfaces:
        surfaces.append([[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1]])
    if [[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2]] not in surfaces:
        surfaces.append([[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2]])
    if [[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2]] not in surfaces:
        surfaces.append([[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2]])
    if [[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z]] not in surfaces:
        surfaces.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z]])
    if [[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1]] not in surfaces:
        surfaces.append([[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1]])
    if [[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z]] not in surfaces:
        surfaces.append([[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z]])
    if [[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1]] not in surfaces:
        surfaces.append([[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1]])
    if [[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z]] not in surfaces:
        surfaces.append([[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z]])
    if [[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1]] not in surfaces:
        surfaces.append([[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1]])
    if [[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z]] not in surfaces:
        surfaces.append([[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z]])
    if [[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1]] not in surfaces:
        surfaces.append([[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1]])

def free(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2))]
    return local_cube not in cubes

side_size = (600, 450)
mid_size = (900, 900)

coords = [0, -12, 0]
theta = math.pi / 2
y_val = 1

trans_speed = .1
rot_speed = math.pi / 50

cubes = []
surfaces = []

pygame.init()
total_screen = pygame.display.set_mode((side_size[0] + mid_size[0], 2 * side_size[1]))
top_screen = pygame.Surface(side_size)
mid_screen = pygame.Surface(mid_size)
bottom_screen = pygame.Surface(side_size)

f = open("cubes.txt", "r")
cube_strings = f.readlines()
for i in cube_strings:
    text = i.split()
    cubes.append([int(text[0]), int(text[1]), int(text[2])])

for i in cubes:
    add_cube(i)

while True:
    total_screen.fill([0, 0, 0])
    top_screen.fill([0, 0, 0])
    mid_screen.fill([0, 0, 0])
    bottom_screen.fill([0, 0, 0])
    surfaces.sort(key = lambda surface: get_dist_squared(surface, coords), reverse = True)
    for i in surfaces:
        draw_surface(i, False, False, return_color(get_dist_squared(i, coords), get_dist_squared(i, [0, -12, 0])))
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_z]:
        if free([coords[0] + 10 * trans_speed * math.cos(theta), coords[1] + 10 * trans_speed * math.sin(theta), coords[2]]):
            coords[0] += trans_speed * math.cos(theta)
            coords[1] += trans_speed * math.sin(theta)
    if keystate[pygame.K_x]:
        if free([coords[0] - 10 * trans_speed * math.cos(theta), coords[1] - 10 * trans_speed * math.sin(theta), coords[2]]):
            coords[0] -= trans_speed * math.cos(theta)
            coords[1] -= trans_speed * math.sin(theta)
    if keystate[pygame.K_a]:
        if free([coords[0] - 10 * trans_speed * math.sin(theta), coords[1] + 10 * trans_speed * math.cos(theta), coords[2]]):
            coords[0] -= trans_speed * math.sin(theta)
            coords[1] += trans_speed * math.cos(theta)
    if keystate[pygame.K_d]:
        if free([coords[0] + 10 * trans_speed * math.sin(theta), coords[1] - 10 * trans_speed * math.cos(theta), coords[2]]):
            coords[0] += trans_speed * math.sin(theta)
            coords[1] -= trans_speed * math.cos(theta)
    if keystate[pygame.K_w]:
        if free([coords[0], coords[1], coords[2] + 10 * trans_speed]):
            coords[2] += trans_speed
    if keystate[pygame.K_s]:
        if free([coords[0], coords[1], coords[2] - 10 * trans_speed]):
            coords[2] -= trans_speed
    if keystate[pygame.K_LEFT]:
        theta += rot_speed
    if keystate[pygame.K_RIGHT]:
        theta -= rot_speed
    total_screen.blit(top_screen, (0, 0))
    total_screen.blit(bottom_screen, (0, side_size[1]))
    total_screen.blit(mid_screen, (side_size[0], 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()

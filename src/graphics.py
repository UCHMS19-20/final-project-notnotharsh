import sys, pygame, pygame.gfxdraw, random, math, time

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
    return (min(250, 300 / dist_squared + 10000 / from_outside), min(250, 300 / dist_squared + 10000 / from_outside), min(225, 250 / dist_squared + 9000 / from_outside))

def draw_surface(plist, draw_points, draw_lines, color, transparent):
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
    if transparent == 2:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 63)
    elif transparent == 1:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 127)
    else:
        color_obj = pygame.Color(int(color[0]), int(color[1]), int(color[2]), 255)
    if top_forward:
        pygame.gfxdraw.filled_polygon(top_screen, [(int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), (int(coords_set_3[0][0]), int(coords_set_3[0][1])), (int(coords_set_4[0][0]), int(coords_set_4[0][1]))], color_obj)
    if mid_forward:
        pygame.gfxdraw.filled_polygon(mid_screen, [(int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), (int(coords_set_3[1][0]), int(coords_set_3[1][1])), (int(coords_set_4[1][0]), int(coords_set_4[1][1]))], color_obj)
    if bottom_forward:
        pygame.gfxdraw.filled_polygon(bottom_screen, [(int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), (int(coords_set_3[2][0]), int(coords_set_3[2][1])), (int(coords_set_4[2][0]), int(coords_set_4[2][1]))], color_obj)

def add_cube(corner):
    global surfaces
    transparent = [-1, -1, -1]
    if len(corner) != 3:
        transparent = [corner[3], corner[4], corner[5]]
    x = corner[0]
    y = corner[1]
    z = corner[2]
    if [[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z], transparent] not in surfaces:
        surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y + 1, z], [x, y + 1, z], transparent])
    if [[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z], transparent] not in surfaces:
        surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y + 1, z], [x + 1, y + 1, z], transparent])
    if [[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z], transparent] not in surfaces:
        surfaces.append([[x, y + 1, z], [x + 1, y + 1, z], [x + 1, y + 2, z], [x, y + 2, z], transparent])
    if [[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z], transparent] not in surfaces:
        surfaces.append([[x + 1, y + 1, z], [x + 2, y + 1, z], [x + 2, y + 2, z], [x + 1, y + 2, z], transparent])
    if [[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2], transparent] not in surfaces:
        surfaces.append([[x, y, z + 2], [x + 1, y, z + 2], [x + 1, y + 1, z + 2], [x, y + 1, z + 2], transparent])
    if [[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2], transparent] not in surfaces:
        surfaces.append([[x + 1, y, z + 2], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 1, y + 1, z + 2], transparent])
    if [[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
        surfaces.append([[x, y + 1, z + 2], [x + 1, y + 1, z + 2], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent])
    if [[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent] not in surfaces:
        surfaces.append([[x + 1, y + 1, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent])
    if [[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1], transparent] not in surfaces:
        surfaces.append([[x, y, z], [x + 1, y, z], [x + 1, y, z + 1], [x, y, z + 1], transparent])
    if [[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1], transparent] not in surfaces:
        surfaces.append([[x + 1, y, z], [x + 2, y, z], [x + 2, y, z + 1], [x + 1, y, z + 1], transparent])
    if [[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2], transparent] not in surfaces:
        surfaces.append([[x, y, z + 1], [x + 1, y, z + 1], [x + 1, y, z + 2], [x, y, z + 2], transparent])
    if [[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2], transparent] not in surfaces:
        surfaces.append([[x + 1, y, z + 1], [x + 2, y, z + 1], [x + 2, y, z + 2], [x + 1, y, z + 2], transparent])
    if [[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1], transparent] not in surfaces:
        surfaces.append([[x, y + 2, z], [x + 1, y + 2, z], [x + 1, y + 2, z + 1], [x, y + 2, z + 1], transparent])
    if [[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1], transparent] not in surfaces:
        surfaces.append([[x + 1, y + 2, z], [x + 2, y + 2, z], [x + 2, y + 2, z + 1], [x + 1, y + 2, z + 1], transparent])
    if [[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent] not in surfaces:
        surfaces.append([[x, y + 2, z + 1], [x + 1, y + 2, z + 1], [x + 1, y + 2, z + 2], [x, y + 2, z + 2], transparent])
    if [[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent] not in surfaces:
        surfaces.append([[x + 1, y + 2, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z + 2], [x + 1, y + 2, z + 2], transparent])
    if [[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z], transparent] not in surfaces:
        surfaces.append([[x, y, z], [x, y, z + 1], [x, y + 1, z + 1], [x, y + 1, z], transparent])
    if [[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1], transparent] not in surfaces:
        surfaces.append([[x, y, z + 1], [x, y, z + 2], [x, y + 1, z + 2], [x, y + 1, z + 1], transparent])
    if [[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z], transparent] not in surfaces:
        surfaces.append([[x, y + 1, z], [x, y + 1, z + 1], [x, y + 2, z + 1], [x, y + 2, z], transparent])
    if [[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1], transparent] not in surfaces:
        surfaces.append([[x, y + 1, z + 1], [x, y + 1, z + 2], [x, y + 2, z + 2], [x, y + 2, z + 1], transparent])
    if [[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z], transparent] not in surfaces:
        surfaces.append([[x + 2, y, z], [x + 2, y, z + 1], [x + 2, y + 1, z + 1], [x + 2, y + 1, z], transparent])
    if [[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1], transparent] not in surfaces:
        surfaces.append([[x + 2, y, z + 1], [x + 2, y, z + 2], [x + 2, y + 1, z + 2], [x + 2, y + 1, z + 1], transparent])
    if [[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z], transparent] not in surfaces:
        surfaces.append([[x + 2, y + 1, z], [x + 2, y + 1, z + 1], [x + 2, y + 2, z + 1], [x + 2, y + 2, z], transparent])
    if [[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1], transparent] not in surfaces:
        surfaces.append([[x + 2, y + 1, z + 1], [x + 2, y + 1, z + 2], [x + 2, y + 2, z + 2], [x + 2, y + 2, z + 1], transparent])

def free(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2))]
    return local_cube not in cubes

def alive(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 127, 0, 0]
    return local_cube not in cubes

def playing(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 0, 127, 0]
    return local_cube not in cubes

def outside(pos):
    global cubes
    local_cube = [int(2 * math.floor(pos[0] / 2)), int(2 * math.floor(pos[1] / 2)), int(2 * math.floor(pos[2] / 2)), 0, 0, 127]
    return local_cube not in cubes

side_size = (300, 300)
mid_size = (480, 480)
items_size = (mid_size[0], side_size[1] * 2 - mid_size[1])

coords = [1, -5, 1]
theta = math.pi / 2

trans_speed = .1
rot_speed = math.pi / 50

cubes = []
surfaces = []

pygame.init()
total_screen = pygame.display.set_mode((side_size[0] + mid_size[0], 2 * side_size[1]))
top_screen = pygame.Surface(side_size)
mid_screen = pygame.Surface(mid_size)
bottom_screen = pygame.Surface(side_size)
items_screen = pygame.Surface(items_size)

font = pygame.font.SysFont("Courier", 50)
little_font = pygame.font.SysFont("Courier", 20, bold = True)
top_text = little_font.render("top", True, (127, 127, 127))
bottom_text = little_font.render("bottom", True, (127, 127, 127))
front_text = little_font.render("forward", True, (127, 127, 127))
won_text = font.render("you won!", True, (255, 255, 255))
lost_text = font.render("you lost!", True, (255, 255, 255))
build_text = font.render("Build", True, (255, 255, 255))
play_text = font.render("Play", True, (255, 255, 255))

won_text_rect = won_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1]))
lost_text_rect = lost_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1]))
build_text_rect = build_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1] * 2 / 3))
play_text_rect = play_text.get_rect(center = ((side_size[0] + mid_size[0]) / 2, side_size[1] * 4 / 3))

pickaxe = pygame.transform.scale(pygame.image.load("img/pickaxe.png"), (items_size[1], items_size[1]))
normal_cube = pygame.transform.scale(pygame.image.load("img/normalcube.png"), (items_size[1], items_size[1]))
green_cube = pygame.transform.scale(pygame.image.load("img/greencube.png"), (items_size[1], items_size[1]))
red_cube = pygame.transform.scale(pygame.image.load("img/redcube.png"), (items_size[1], items_size[1]))

pickaxe_rect = pickaxe.get_rect(topleft = (0, 0))
normal_cube_rect = normal_cube.get_rect(topleft = (items_size[1], 0))
green_cube_rect = green_cube.get_rect(topleft = (2 * items_size[1], 0))
red_cube_rect = red_cube.get_rect(topleft = (3 * items_size[1], 0))

f = open("cubes.txt", "r")
cube_strings = f.readlines()
for i in cube_strings:
    text = i.split()
    if len(text) == 3:
        cubes.append([int(text[0]), int(text[1]), int(text[2])])
    else:
        cubes.append([int(text[0]), int(text[1]), int(text[2]), int(text[3]), int(text[4]), int(text[5])])

for i in cubes:
    add_cube(i)

main_menu = True
build_loop = False
game_loop = False
won = False
saving = False

buildstamp = 0

while True:
    while main_menu:
        coords = [1, -5, 1]
        theta = math.pi / 2
        total_screen.fill([0, 0, 0])
        total_screen.blit(build_text, build_text_rect)
        total_screen.blit(play_text, play_text_rect)
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_text_rect.collidepoint(pos):
                    main_menu = False
                    game_loop = True
                elif build_text_rect.collidepoint(pos):
                    main_menu = False
                    build_loop = True
        pygame.display.flip()
    while game_loop:
        won = False
        if not alive(coords):
            game_loop = False
        if not playing(coords):
            game_loop = False
            won = True
        total_screen.fill([0, 0, 0])
        top_screen.fill([0, 0, 0])
        mid_screen.fill([0, 0, 0])
        bottom_screen.fill([0, 0, 0])
        items_screen.fill([0, 0, 0])
        surfaces.sort(key = lambda surface: get_dist_squared(surface, coords), reverse = True)
        for i in surfaces:
            if i[4] == [-1, -1, -1]:
                draw_surface(i, False, False, return_color(get_dist_squared(i, coords), get_dist_squared(i, [10, 10, 10])), 0)
            else:
                draw_surface(i, False, False, i[4], 2)
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
        if keystate[pygame.K_SPACE]:
            game_loop = False
            main_menu = True
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
    while build_loop:
        if buildstamp % 10 == 0:
            del surfaces[:]
            for i in cubes:
                add_cube(i)
        buildstamp += 1
        total_screen.fill([0, 0, 0])
        top_screen.fill([0, 0, 0])
        bottom_screen.fill([0, 0, 0])
        mid_screen.fill([0, 0, 0])
        items_screen.fill([0, 0, 0])
        surfaces.sort(key = lambda surface: get_dist_squared(surface, coords), reverse = True)
        for i in surfaces:
            if i[4] == [-1, -1, -1]:
                draw_surface(i, False, False, return_color(get_dist_squared(i, coords), get_dist_squared(i, [0, -12, 0])), 1)
            else:
                draw_surface(i, False, False, i[4], 2)
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_z]:
            coords[0] += trans_speed * math.cos(theta)
            coords[1] += trans_speed * math.sin(theta)
        if keystate[pygame.K_x]:
            coords[0] -= trans_speed * math.cos(theta)
            coords[1] -= trans_speed * math.sin(theta)
        if keystate[pygame.K_a]:
            coords[0] -= trans_speed * math.sin(theta)
            coords[1] += trans_speed * math.cos(theta)
        if keystate[pygame.K_d]:
            coords[0] += trans_speed * math.sin(theta)
            coords[1] -= trans_speed * math.cos(theta)
        if keystate[pygame.K_w]:
            coords[2] += trans_speed
        if keystate[pygame.K_s]:
            coords[2] -= trans_speed
        if keystate[pygame.K_LEFT]:
            theta += rot_speed
        if keystate[pygame.K_RIGHT]:
            theta -= rot_speed
        if keystate[pygame.K_SPACE]:
            build_loop = False
            main_menu = True
            if not saving:
                saving = True
                w = open("cubes.txt", "w")
                cubestr = ""
                for i in cubes:
                    if len(i) == 3:
                        cubestr += str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + "\n"
                    else:
                        cubestr += str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]) + " " + str(i[4]) + " " + str(i[5]) + "\n"
                w.write(cubestr)
                w.close()
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                actual = (pos[0] - side_size[0], pos[1] - mid_size[1])
                if pickaxe_rect.collidepoint(actual):
                    if not free(coords):
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))])
                    if not alive(coords):
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0])
                    if not playing(coords):
                        cubes.remove([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0])
                elif green_cube_rect.collidepoint(actual):
                    if (free(coords) and alive(coords)) and (playing(coords) and outside(coords)):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 0, 127, 0])
                elif red_cube_rect.collidepoint(actual) and (playing(coords) and outside(coords)):
                    if (free(coords) and alive(coords)) and playing(coords):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2)), 127, 0, 0])
                elif normal_cube_rect.collidepoint(actual) and (playing(coords) and outside(coords)):
                    if (free(coords) and alive(coords)) and playing(coords):
                        if [int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))] not in cubes:
                            cubes.append([int(2 * math.floor(coords[0] / 2)), int(2 * math.floor(coords[1] / 2)), int(2 * math.floor(coords[2] / 2))])
        pygame.display.flip()
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        main_menu = True
        game_loop = False
    else:
        if won:
            total_screen.blit(won_text, won_text_rect)
        else:
            total_screen.blit(lost_text, lost_text_rect)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

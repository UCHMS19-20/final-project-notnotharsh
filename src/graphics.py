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
coords = [0, 0, 0]
theta = math.pi / 2
y_val = 1
side_size = (300, 300)
mid_size = (400, 400)

def draw_point(point, draw):
    global mid_size, side_size, top_screen, mid_screen, bottom_screen
    top_display_coords = point_transform(point, side_size, 0)
    mid_display_coords = point_transform(point, mid_size, 1)
    bottom_display_coords = point_transform(point, side_size, 2)
    if draw:
        pygame.draw.circle(top_screen, [255, 255, 255], (int(top_display_coords[0]), int(top_display_coords[1])), 4)
        pygame.draw.circle(mid_screen, [255, 255, 255], (int(mid_display_coords[0]), int(mid_display_coords[1])), 4)
        pygame.draw.circle(bottom_screen, [255, 255, 255], (int(bottom_display_coords[0]), int(bottom_display_coords[1])), 4)
    return [top_display_coords, mid_display_coords, bottom_display_coords]

def draw_line(p1, p2, draw_points):
    global mid_size, side_size, top_screen, mid_screen, bottom_screen
    coords_set_1 = draw_point(p1, draw_points)
    coords_set_2 = draw_point(p2, draw_points)
    top_forward = coords_set_1[0][2] or coords_set_2[0][2]
    mid_forward = coords_set_1[1][2] or coords_set_2[1][2]
    bottom_forward = coords_set_1[2][2] or coords_set_2[2][2]
    if top_forward:
        pygame.draw.line(top_screen, [255, 255, 255], (int(coords_set_1[0][0]), int(coords_set_1[0][1])), (int(coords_set_2[0][0]), int(coords_set_2[0][1])), 4)
    if mid_forward:
        pygame.draw.line(mid_screen, [255, 255, 255], (int(coords_set_1[1][0]), int(coords_set_1[1][1])), (int(coords_set_2[1][0]), int(coords_set_2[1][1])), 4)
    if bottom_forward:
        pygame.draw.line(bottom_screen, [255, 255, 255], (int(coords_set_1[2][0]), int(coords_set_1[2][1])), (int(coords_set_2[2][0]), int(coords_set_2[2][1])), 4)
    return [coords_set_1, coords_set_2]

pygame.init()
total_screen = pygame.display.set_mode((side_size[0] + mid_size[0], 2 * side_size[1]))
top_screen = pygame.Surface(side_size)
mid_screen = pygame.Surface(mid_size)
bottom_screen = pygame.Surface(side_size)

while True:
    # print(round(coords[0], 3), round(coords[1], 3), round(coords[2], 3), round(theta, 3))
    total_screen.fill([0, 0, 0])
    top_screen.fill([0, 0, 0])
    mid_screen.fill([0, 0, 0])
    bottom_screen.fill([0, 0, 0])
    phi = math.pi / 2 * y_val
    draw_line([-3, -3, -3], [-3, -3, 3], True)
    draw_line([-3, -3, -3], [-3, 3, -3], True)
    draw_line([-3, -3, -3], [3, -3, -3], True)
    draw_line([3, -3, 3], [-3, -3, 3], True)
    draw_line([-3, 3, 3], [-3, 3, -3], True)
    draw_line([3, 3, -3], [3, -3, -3], True)
    draw_line([-3, 3, 3], [-3, -3, 3], True)
    draw_line([3, 3, -3], [-3, 3, -3], True)
    draw_line([3, -3, 3], [3, -3, -3], True)
    draw_line([-3, 3, 3], [3, 3, 3], True)
    draw_line([3, 3, -3], [3, 3, 3], True)
    draw_line([3, -3, 3], [3, 3, 3], True)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_z]:
        coords[0] += .03 * math.cos(theta)
        coords[1] += .03 * math.sin(theta)
    if keystate[pygame.K_x]:
        coords[0] -= .03 * math.cos(theta)
        coords[1] -= .03 * math.sin(theta)
    if keystate[pygame.K_a]:
        coords[0] -= .03 * math.sin(theta)
        coords[1] += .03 * math.cos(theta)
    if keystate[pygame.K_d]:
        coords[0] += .03 * math.sin(theta)
        coords[1] -= .03 * math.cos(theta)
    if keystate[pygame.K_w]:
        coords[2] += .03
    if keystate[pygame.K_s]:
        coords[2] -= .03
    if keystate[pygame.K_j]:
        theta += .003
    if keystate[pygame.K_l]:
        theta -= .003
    total_screen.blit(top_screen, (0, 0))
    total_screen.blit(bottom_screen, (0, side_size[1]))
    total_screen.blit(mid_screen, (side_size[0], 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()

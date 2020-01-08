import sys, pygame, random, math

def point_transform(point):
    global coords, angles, size
    x_dist = point[0] - coords[0]
    y_dist = point[1] - coords[1]
    z_dist = point[2] - coords[2]
    rho = math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2) + math.pow(z_dist, 2))
    old_theta = math.atan2(y_dist, x_dist)
    old_phi = math.atan2(math.sqrt(math.pow(x_dist, 2) + math.pow(y_dist, 2)), z_dist)
    new_theta = old_theta + math.pi / 2 - angles[0]
    new_phi = old_phi + math.pi / 2 - angles[1]
    x_angle = 1 / (math.tan(new_theta))
    y_angle = 1 / (math.tan(new_phi) * math.sin(new_theta))
    # print(round(new_theta, 3), round(new_phi, 3), round(new_x, 3), round(new_y, 3), round(new_z, 3), round(x_angle, 3), round(y_angle, 3))
    x_display = (size[0] / 2) * (x_angle * 2)
    y_display = (size[1] / 2) * (y_angle * -2)
    display_angles = [size[0] / 2 + x_display, size[1] / 2 + y_display]
    return display_angles

coords = [0, -.001, 0]
angles = [math.pi / 2, math.pi / 2]
size = [1000, 1000]

pygame.init()
screen = pygame.display.set_mode((size[0], size[1]))

while True:
    # print(str(round(angles[0], 3)) + " " + str(round(angles[1], 3)) + " " + str(round(coords[0], 3)) + " " + str(round(coords[1], 3)) + " " + str(round(coords[2], 3)))
    screen.fill([0, -.001, 0])
    for i in range(-5, 6):
        for j in range(10, 21):
            for k in range(-5, 6):
                point = [i, j, k]
                display_coords = point_transform(point)
                pygame.draw.circle(screen, [255, 255, 255], (int(display_coords[0]), int(display_coords[1])), 4)
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_z]:
        coords[0] += .05 * math.sin(angles[1]) * math.cos(angles[0])
        coords[1] += .05 * math.sin(angles[1]) * math.sin(angles[0])
        coords[2] += .05 * math.cos(angles[1])
    if keystate[pygame.K_x]:
        coords[0] -= .05 * math.sin(angles[1]) * math.cos(angles[0])
        coords[1] -= .05 * math.sin(angles[1]) * math.sin(angles[0])
        coords[2] -= .05 * math.cos(angles[1])
    if keystate[pygame.K_a]:
        coords[0] -= .05 * math.sin(angles[1]) * math.sin(angles[0])
        coords[1] -= .05 * math.sin(angles[1]) * math.cos(angles[0]) * -1
        coords[2] -= .05 * math.cos(angles[1])
    if keystate[pygame.K_d]:
        coords[0] += .05 * math.sin(angles[1]) * math.sin(angles[0])
        coords[1] += .05 * math.sin(angles[1]) * math.cos(angles[0]) * -1
        coords[2] += .05 * math.cos(angles[1])
    if keystate[pygame.K_w]:
        coords[0] += .05 * math.cos(angles[1]) * math.cos(angles[0]) * -1
        coords[1] += .05 * math.cos(angles[1]) * math.sin(angles[0]) * -1
        coords[2] += .05 * math.sin(angles[1])
    if keystate[pygame.K_s]:
        coords[0] -= .05 * math.cos(angles[1]) * math.cos(angles[0]) * -1
        coords[1] -= .05 * math.cos(angles[1]) * math.sin(angles[0]) * -1
        coords[2] -= .05 * math.sin(angles[1])
    if keystate[pygame.K_v]:
        coords[1] += .05
    if keystate[pygame.K_b]:
        coords[1] -= .05
    if keystate[pygame.K_f]:
        coords[0] -= .05
    if keystate[pygame.K_h]:
        coords[0] += .05
    if keystate[pygame.K_t]:
        coords[2] += .05
    if keystate[pygame.K_g]:
        coords[2] -= .05
    if keystate[pygame.K_i]:
        if angles[1] > 0 and angles[1] < math.pi:
            angles[1] -= .003
    if keystate[pygame.K_k]:
        if angles[1] > 0 and angles[1] < math.pi:
            angles[1] += .003
    if keystate[pygame.K_j]:
        angles[0] += .003
    if keystate[pygame.K_l]:
        angles[0] -= .003
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()
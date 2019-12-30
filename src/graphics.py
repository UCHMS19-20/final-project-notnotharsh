import sys, pygame, random, math

def point_transform(point):
    global coords, angles, size
    x_dist = point[0] - coords[0]
    y_dist = point[1] - coords[1]
    z_dist = point[2] - coords[2]
    not_new_z = z_dist * math.cos(angles[0] + y_dist * math.sin(angles[0]))
    new_x = x_dist * math.cos(angles[1]) + not_new_z * math.sin(angles[1])
    new_y = y_dist * math.cos(angles[0]) - z_dist * math.sin(angles[0])
    new_z = not_new_z * math.cos(angles[1]) - x_dist * math.sin(angles[1])
    x_denom = math.sqrt(math.pow(new_x, 2) + math.pow(new_z, 2))
    y_denom = math.sqrt(math.pow(new_y, 2) + math.pow(new_z, 2))
    x_angle = math.asin(new_x / x_denom)
    y_angle = math.asin(new_y / y_denom)
    if (new_z <= 0):
        if (new_x > 0):
            x_angle = math.pi - x_angle
        if (new_x < 0):
            x_angle = -1 * math.pi - x_angle
        if (new_y > 0):
            y_angle = math.pi - y_angle
        if (new_y < 0):
            y_angle = -1 * math.pi - y_angle
    display_angles = [(size[0] / 2) * (1 + x_angle * 2), (size[0] / 2) * (1 + y_angle * 2)]
    return display_angles

coords = [0, 0, 0.01]
angles = [0, 0]
size = [600, 600]

pygame.init()
screen = pygame.display.set_mode((size[0], size[1]))

while True:
    screen.fill([0, 0, 0])
    for i in range(-5, 5):
        for j in range(-5, 5):
            for k in range(10, 20):
                point = [i, j, k]
                display_coords = point_transform(point)
                screen.set_at((int(display_coords[0]), int(display_coords[1])), [255, 255, 255])
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_d]:
        coords[0] += .1
    if keystate[pygame.K_a]:
        coords[0] -= .1
    if keystate[pygame.K_w]:
        coords[1] -= .1
    if keystate[pygame.K_s]:
        coords[1] += .1
    if keystate[pygame.K_z]:
        coords[2] += .1
    if keystate[pygame.K_x]:
        coords[2] -= .1
    pygame.event.pump()
    pygame.display.flip()

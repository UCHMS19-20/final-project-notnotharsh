def pointTransform(point, coords, angles, screen):
    x_dist = point[0] - coords[0]
    y_dist = point[1] - coords[1]
    z_dist = point[2] - coords[2]
    not_new_z = z_dist * math.cos(angles[0] + y_dist * math.sin(angles[0])
    new_x = x_dist * math.cos(angles[1]) + not_new_z * math.sin(angles[1])
    new_y = y_dist * math.cos(angles[0]) - z_dist * math.sin(angles[0])
    new_z = not_new_z * math.cos(angles[1]) - x_dist * math.sin(angles[1])
import numpy as np
import matplotlib.pyplot as plt


# set up the rectangular frame
frame_width = 10
frame_height = 10

# set up the circular object
object_radius = 0.3
object_center = np.array([frame_width/2, frame_height/2])
object_direction = np.array([1, 0])  # start moving to the right

# set up the time parameters
num_steps = 100000
time_step = 0.1

# create a plot to show the object's motion
fig, ax = plt.subplots()
ax.set_xlim(0, frame_width)
ax.set_ylim(0, frame_height)
ax.set_aspect('equal')
object_patch = plt.Circle(object_center, object_radius, color='g', alpha=0.5)
ax.add_patch(object_patch)

# simulate the motion and update the object's position
for i in range(num_steps):
    # calculate the new position based on the current direction
    new_position = object_center + object_direction * time_step
    
    # check if the new position is inside the frame
    if (new_position[0] > object_radius and new_position[0] < frame_width - object_radius and
        new_position[1] > object_radius and new_position[1] < frame_height - object_radius):
        # if the new position is inside the frame, update the position of the object
        object_center = new_position
    else:
        # if the new position is outside the frame, calculate a random duration of rotation
        rotation_duration = np.random.uniform(0.1, 1.0)
        # rotate the object by a random angle and update its direction
        rotation_angle = np.random.uniform(0, 2 * np.pi)
        rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
                                    [np.sin(rotation_angle), np.cos(rotation_angle)]])
        object_direction = np.dot(rotation_matrix, object_direction)
        # update the position of the object based on the rotated direction
        object_center = object_center + object_direction * rotation_duration

        # keep moving in the new direction until the next collision
        while (object_center[0] < object_radius or object_center[0] > frame_width - object_radius or
               object_center[1] < object_radius or object_center[1] > frame_height - object_radius):
            object_center = object_center + object_direction * time_step

    # update the position of the object on the plot
    object_patch.center = object_center
    plt.pause(0.01)

plt.show()


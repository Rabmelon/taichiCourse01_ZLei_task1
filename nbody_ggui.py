import taichi as ti
from CelestialObject import CelestialObject

ti.init(arch=ti.gpu)
print("Hallo, Taichi")

## def parameters
bodies = CelestialObject(3, 1000, 1)

title_str = "N-Body" + ("-2D" if bodies.dim == 2 else "-3D" if bodies.dim == 3 else "-Error")
my_ggui = ti.ui.Window(title_str, (1000, 600))
my_canvas = my_ggui.get_canvas()
my_scene = ti.ui.Scene()
my_camera = ti.ui.make_camera()
pos_camera_x = 1
pos_camera_y = 1
pos_camera_z = 1
lookat_camera_x = 0
lookat_camera_y = 0
lookat_camera_z = 0
fov_camera = 100
flag_RMB = False

flag_pause = True

off_size = 0.3
init_speed = 1
radius_body = 0.01

h = 1e-4
id_frame = 0

if bodies.dim == 2:
    pos_c = ti.Vector([0.0, 0.0])
elif bodies.dim == 3:
    # pos_c = ti.Vector([0.6, 0.5, 0.2])
    pos_c = ti.Vector([0.0, 0.0, 0.0])

bodies.initialize_range(pos_c, off_size, init_speed)

## main roop
while my_ggui.running:
    # Create options
    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.2)
    radius_body = my_ggui.GUI.slider_float("radius", radius_body, 1e-3, 1e-1)
    bodies.G[None] = ti.exp(my_ggui.GUI.slider_float("log(G)", ti.log(bodies.G[None]), -10, 0))
    my_ggui.GUI.text("G = {:.5e}".format(bodies.G[None]))
    my_ggui.GUI.text("Frame: " + str(id_frame))
    my_ggui.GUI.end()
    my_ggui.GUI.begin("Property need restart", 0.03, 0.3, 0.2, 0.2)
    off_size = my_ggui.GUI.slider_float("off size", off_size, 0, 1)
    init_speed = my_ggui.GUI.slider_float("velocity 0", init_speed, 0, 10) # 初速度对模拟没有什么影响？
    my_ggui.GUI.end()
    if bodies.dim == 3:
        my_ggui.GUI.begin("Camera options", 0.03, 0.55, 0.3, 0.35)
        pos_camera_x = my_ggui.GUI.slider_float("pos x of camera", pos_camera_x, -2.5, 2.5)
        pos_camera_y = my_ggui.GUI.slider_float("pos y of camera", pos_camera_y, -2.5, 2.5)
        pos_camera_z = my_ggui.GUI.slider_float("pos z of camera", pos_camera_z, -2.5, 2.5)
        lookat_camera_x = my_ggui.GUI.slider_float("lookat x of camera", lookat_camera_x, -2.5, 2.5)
        lookat_camera_y = my_ggui.GUI.slider_float("lookat y of camera", lookat_camera_y, -2.5, 2.5)
        lookat_camera_z = my_ggui.GUI.slider_float("lookat z of camera", lookat_camera_z, -2.5, 2.5)
        fov_camera = my_ggui.GUI.slider_float("fov of camera", fov_camera, 10, 200)
        if flag_RMB:
            if my_ggui.GUI.button("RMB rotation off"):
                flag_RMB = False
        else:
            if my_ggui.GUI.button("RMB rotation on"):
                flag_RMB = True
        my_ggui.GUI.end()

    # Create actions
    for e in my_ggui.get_events(ti.ui.PRESS):
        if e.key == ti.ui.ESCAPE:
            exit()
        elif e.key == ti.ui.SPACE:
            flag_pause = not flag_pause
        elif e.key == 'r':
            id_frame = 0
            bodies.initialize_range(pos_c, off_size, init_speed)
        elif e.key == ti.ui.LMB:
            pos = my_ggui.get_cursor_pos()
            print(pos)

    # Main loop
    if not flag_pause:
        bodies.computeForce()
        bodies.update(h)
        id_frame += 1

    # Render the scene
    if bodies.dim == 3:
        if flag_RMB:
            my_camera.track_user_inputs(my_ggui, movement_speed=0.05, hold_key=ti.ui.RMB)
        else:
            my_camera.position(pos_camera_x, pos_camera_y, pos_camera_z)
            my_camera.lookat(lookat_camera_x, lookat_camera_y, lookat_camera_z)
            my_camera.fov(fov_camera)
    bodies.display(my_canvas, my_scene, my_camera, radius_body)
    my_ggui.show()

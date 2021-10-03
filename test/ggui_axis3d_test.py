import taichi as ti
ti.init()

# use a cube to understand how ggui scene and canvas work

# create gui parameters
my_ggui = ti.ui.Window("test-3D", (1000, 600))
my_canvas = my_ggui.get_canvas()
my_scene = ti.ui.Scene()
my_camera = ti.ui.make_camera()
flag_RMB = False

# cube parameters
pos_axis = ti.Vector.field(3, ti.f32, shape=8)
c_axis = ti.Vector.field(3, ti.f32, shape=8)
pos_axis[0] = ti.Vector([0.0, 0.0, 0.0])
pos_axis[1] = ti.Vector([0.5, 0.0, 0.0])
pos_axis[2] = ti.Vector([0.0, 0.5, 0.0])
pos_axis[3] = ti.Vector([0.0, 0.0, 0.5])
pos_axis[4] = ti.Vector([0.5, 0.5, 0.5])
pos_axis[5] = ti.Vector([0.5, 0.5, 0.0])
pos_axis[6] = ti.Vector([0.5, 0.0, 0.5])
pos_axis[7] = ti.Vector([0.0, 0.5, 0.5])
c_axis[0] = ti.Vector([1, 1, 0])
c_axis[1] = ti.Vector([1, 0, 0])
c_axis[2] = ti.Vector([0, 1, 0])
c_axis[3] = ti.Vector([0, 0, 1])
c_axis[4] = ti.Vector([0, 0, 0])
c_axis[5] = ti.Vector([1, 1, 1])
c_axis[6] = ti.Vector([1, 1, 1])
c_axis[7] = ti.Vector([1, 1, 1])

# assist parameters
r = 0.05
pos_pl1 = (0.5, 1.5, 0.5)
pos_pl2 = (0.5, 1.5, 1.5)
c_pl = (0.5, 0.5, 0.5)
pos_cam = (1, 1, 1)
la_cam = (0, 0, 0)
fov_cam = 90

while my_ggui.running:
    # option window
    my_ggui.GUI.begin("Camera options", 0.03, 0.05, 0.3, 0.35)
    [pos_cam_x, pos_cam_y, pos_cam_z] = pos_cam
    pos_cam_x = my_ggui.GUI.slider_float("pos x of camera", pos_cam_x, -2.5, 2.5)
    pos_cam_y = my_ggui.GUI.slider_float("pos y of camera", pos_cam_y, -2.5, 2.5)
    pos_cam_z = my_ggui.GUI.slider_float("pos z of camera", pos_cam_z, -2.5, 2.5)
    pos_cam = [pos_cam_x, pos_cam_y, pos_cam_z]
    [la_cam_x, la_cam_y, la_cam_z] = la_cam
    la_cam_x = my_ggui.GUI.slider_float("lookat x of camera", la_cam_x, -2.5, 2.5)
    la_cam_y = my_ggui.GUI.slider_float("lookat y of camera", la_cam_y, -2.5, 2.5)
    la_cam_z = my_ggui.GUI.slider_float("lookat z of camera", la_cam_z, -2.5, 2.5)
    la_cam = [la_cam_x, la_cam_y, la_cam_z]
    fov_cam = my_ggui.GUI.slider_float("fov of camera", fov_cam, 10, 200)
    if flag_RMB:
        if my_ggui.GUI.button("RMB rotation off"):
            flag_RMB = False
    else:
        if my_ggui.GUI.button("RMB rotation on"):
            flag_RMB = True
    my_ggui.GUI.end()
    my_ggui.GUI.begin('Property', 0.05, 0.45, 0.3, 0.2)
    r = my_ggui.GUI.slider_float('radius', r, 0.01, 1)
    my_ggui.GUI.end()


    # actions
    for e in my_ggui.get_events(ti.ui.PRESS):
        if e.key == ti.ui.ESCAPE:
            exit()
        elif e.key == 'r':
            pos_cam = (1, 1, 1)
            la_cam = (0, 0, 0)
            fov_cam = 90
            r = 0.05

    # render
    my_canvas.set_background_color((17 / 255, 47 / 255, 65 / 255))
    if flag_RMB:
        my_camera.track_user_inputs(my_ggui, movement_speed=0.05, hold_key=ti.ui.RMB)
    else:
        my_camera.position(pos_cam[0], pos_cam[1], pos_cam[2])
        my_camera.lookat(la_cam[0], la_cam[1], la_cam[2])
        my_camera.fov(fov_cam)

    my_scene.set_camera(my_camera)
    my_scene.particles(pos_axis, radius=r, per_vertex_color=c_axis)
    my_scene.point_light(pos=pos_pl1, color=c_pl)

    my_canvas.scene(my_scene)
    my_ggui.show()

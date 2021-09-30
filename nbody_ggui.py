import taichi as ti
from CelestialObject import CelestialObject

ti.init(arch=ti.gpu)
print("Hallo, Taichi")

## def parameters
my_ggui = ti.ui.Window("N-Body", (1000, 600))
my_canvas = my_ggui.get_canvas()
my_scene = ti.ui.Scene()
my_camera = ti.ui.make_camera()
my_camera.position(0.5, 1.0, 1.5)
my_camera.lookat(0.5, 0.3, 0.5)
my_camera.fov(55)

flag_pause = True

off_size = 0.3
init_speed = 1
radius_body = 0.005

h = 1e-4
id_frame = 0

# pos_c = ti.Vector([0.6, 0.5])
pos_c = ti.Vector([0.6, 0.5, 0.2])

bodies = CelestialObject(3, 2000, 1)
bodies.initialize_range(pos_c, off_size, init_speed)

## main roop
while my_ggui.running:
    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.2)
    radius_body = my_ggui.GUI.slider_float("radius", radius_body, 1e-3, 1e-2)
    bodies.G[None] = ti.exp(my_ggui.GUI.slider_float("log(G)", ti.log(bodies.G[None]), -25, 0))
    my_ggui.GUI.text("G = {:.5e}".format(bodies.G[None]))
    my_ggui.GUI.text("Frame: " + str(id_frame))
    my_ggui.GUI.end()
    my_ggui.GUI.begin("Property need restart", 0.03, 0.3, 0.2, 0.2)
    off_size = my_ggui.GUI.slider_float("off size", off_size, 0, 1)
    init_speed = my_ggui.GUI.slider_float("velocity 0", init_speed, 0, 10) # 初速度对模拟没有什么影响？
    my_ggui.GUI.end()

    for e in my_ggui.get_events(ti.ui.PRESS):
        if e.key == ti.ui.ESCAPE:
            exit()
        elif e.key == ti.ui.SPACE:
            flag_pause = not flag_pause
        elif e.key == 'r':
            id_frame = 0
            bodies.initialize_range(pos_c, off_size, init_speed)

    if not flag_pause:
        bodies.computeForce()
        bodies.update(h)
        id_frame += 1

    my_camera.track_user_inputs(my_ggui, movement_speed=0.05, hold_key=ti.ui.RMB)
    bodies.display(my_canvas, my_scene, my_camera, radius_body)
    my_ggui.show()

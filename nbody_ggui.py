import taichi as ti
from CelestialObject import CelestialObject

ti.init(arch=ti.gpu)
print("Hallo, Taichi")

my_ggui = ti.ui.Window("N-Body", (1000, 600))
myconvas = my_ggui.get_canvas()
flag_pause = False
off_size = 0.3
init_speed = 1
h = 1e-4
id_frame = 0

bodies = CelestialObject(2, 200, 1)
bodies.initialize_range(0.6, 0.5, off_size, init_speed)

while my_ggui.running:
    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.2)
    radius_body = my_ggui.GUI.slider_float("radius", 0.005, 1e-3, 1e-2)
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
            bodies.initialize_range(0.6, 0.5, off_size, init_speed)

    if not flag_pause:
        bodies.computeForce()
        bodies.update(h)
        id_frame += 1

    bodies.display_2d(myconvas, radius_body)
    my_ggui.show()

import taichi as ti

ti.init()

# define variables
flag_exit = False
flag_pause = False
id_frame = 0

steps = 1e3

n_particles = 100
dim = 2
G = 1

x = ti.Vector.field(dim, ti.f32, shape=n_particles)


res = (1200, 800)
my_ggui = ti.ui.Window("Hallo Taichi GGUI", res, vsync=True)
particles_radius = 0.1
canvas = my_ggui.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.make_camera()
camera.position(0.5, 1.0, 1.95)
camera.lookat(0.5, 0.3, 0.5)
camera.fov(55)

# def classes



# def functions
@ti.kernel
def init_x():
    for i in range(n_particles):
        x[i] = ti.Vector([ti.random() for j in range(dim)])


# def GGUI windows
def show_options():
    global flag_exit
    global flag_pause
    global id_frame
    global G
    global particles_radius

    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.2)
    G = my_ggui.GUI.slider_float("G", G, 1e-3, 1)
    particles_radius = my_ggui.GUI.slider_float("radius of particles", particles_radius, 0.001, 0.1)
    my_ggui.GUI.end()

    my_ggui.GUI.begin("Options", 0.03, 0.3, 0.2, 0.4)
    if my_ggui.GUI.button("Restart"):
        id_frame = 0
    if flag_pause:
        if my_ggui.GUI.button("Continue"):
            flag_pause = False
    else:
        if my_ggui.GUI.button("Pause"):
            flag_pause = True
    if my_ggui.GUI.button("Bye"):
        flag_exit = True
    my_ggui.GUI.end()

def render():
    camera.track_user_inputs(my_ggui, movement_speed=0.03, hold_key=ti.ui.RMB)

    scene.set_camera(camera)
    scene.ambient_light((0, 0, 0))
    scene.point_light(pos=(0.5, 1.5, 0.5), color=(0.5, 0.5, 0.5))
    scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))
    scene.particles(x, radius=particles_radius)

    canvas.scene(scene)




def show_frame_id():
    global id_frame
    global G

    my_ggui.GUI.begin("Command Window", 0.03, 0.75, 0.2, 0.2)
    tmp_str = "Thank you " + str(id_frame)
    my_ggui.GUI.text(tmp_str)
    my_ggui.GUI.text(str(G))
    my_ggui.GUI.end()

# main
while my_ggui.running:
    if not flag_pause:
        id_frame += 1
    if flag_exit:
        my_ggui.running = False

    render()
    show_frame_id()
    show_options()

    my_ggui.show()

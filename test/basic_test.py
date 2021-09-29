import taichi as ti

ti.init(ti.cuda)

# 目的1：创建一个维度无关的pos和pos_center，在中心点周围随机生成所有的pos坐标值 √
# 目的2：创建一个2d的N-body系统，实现2d的计算和GGUI显示 √
# 目的3：创建一个2d系统，加入鼠标点击后创建一团新星团的功能

## def parameters
dim = 2
N = 200
m = 1
G = 1

dt = 1e-5
substepping = 20

init_vel = 20
off_scale = 0.2
p_radius = 0.005
res = (1000, 600)

pos = ti.Vector.field(dim, ti.f32, N)
vel = ti.Vector.field(dim, ti.f32, N)
force = ti.Vector.field(dim, ti.f32, N)
pos_c = ti.Vector([0.5, 0.4])
# pos_c = ti.Vector([0.5, 0.2, 0.4])

flag_exit = False
flag_pause = False
id_frame = 0

my_ggui = ti.ui.Window("My N-Body GGUI", res)
canvas = my_ggui.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.make_camera()

## def taichi funcs

## def taichi kernels
@ti.kernel
def initialize(pos_center: ti.template()):
    for i in range(N):
        offset = ti.Vector([ti.random() for j in range(dim)]) * off_scale - ti.Vector([off_scale for j in range(dim)]) * 0.5
        pos[i] = pos_center + offset
        # print("offset[", i, "] = ", offset)

        vel[i] = [-offset.y, offset.x] # 如何计算三维速度方向？
        vel[i] *= init_vel
        # print("vel[", i, "] = ", vel[i])

@ti.kernel
def cal_force():
    # clear cur force
    for i in range(N):
        force[i] = ti.Vector([0.0 for j in range(dim)])

    # compute gravitational force
    for i in range(N):
        p = pos[i]
        for j in range(N):
            if i != j:
                diff = p-pos[j]
                r = diff.norm(1e-5)
                f = -G * m * m * (1.0 / r)**3 * diff
                force[i] += f

@ti.kernel
def update():
    ddt = dt / substepping
    for i in range(N):
        vel[i] += ddt * force[i] / m
        pos[i] += ddt * vel[i]

## def common funcs
def show_options():
    global flag_exit, flag_pause, id_frame
    global G, off_scale, p_radius, substepping, dt, m

    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.2)
    # G = my_ggui.GUI.slider_float("G", G, 1e-11, 1)
    # off_scale = my_ggui.GUI.slider_float("off scale", off_scale, 0, 1)
    p_radius = my_ggui.GUI.slider_float("radius", p_radius, 1e-3, 1e-2)
    # substepping = my_ggui.GUI.slider_float("substepping", substepping, 1, 1e2)
    my_ggui.GUI.end()

    my_ggui.GUI.begin("Options", 0.03, 0.3, 0.2, 0.4)
    if my_ggui.GUI.button("Restart"):
        initialize(pos_c)
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
    if dim == 3:
        # The code is still wrong
        camera.position(0.5, 1.0, 1.95)
        camera.lookat(0.5, 0.3, 0.5)
        camera.fov(55)

        camera.track_user_inputs(my_ggui, movement_speed=0.05, hold_key=ti.ui.LMB)
        scene.set_camera(camera)
        scene.ambient_light((0, 0, 0))
        scene.particles(pos, per_vertex_color=0xffffff, radius=p_radius)
        scene.point_light(pos=(0.5, 1.5, 0.5), color=(0.5, 0.5, 0.5))
        scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))
        canvas.scene(scene)
    elif dim == 2:
        backgroundcolor = (17 / 255, 47 / 255, 65 / 255) # 0x112F41
        canvas.set_background_color(backgroundcolor)
        canvas.circles(pos, radius=p_radius, color=(1, 1, 1))



## main
print("Hallo, N-Body")

initialize(pos_c)

while my_ggui.running:
    if not flag_pause:
        for i in range(substepping):
            cal_force()
            update()
    if flag_exit:
        my_ggui.running = False
    render()
    show_options()
    my_ggui.show()

"""
my_gui = ti.GUI("My N-Body GUI", res)
while my_gui.running:
    for i in range(substepping):
        cal_force()
        update()
    my_gui.clear(0x112F41)
    my_gui.circles(pos.to_numpy(), color=0xffffff, radius=p_radius)
    my_gui.show()
"""

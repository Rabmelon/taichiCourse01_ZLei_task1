import taichi as ti

ti.init(ti.cuda)

## def parameters
dim = 2
N = 500
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
        # 如何在矩形的视窗内创建方形的星团？
        pos[i] = pos_center + offset

        vel[i] = [-offset.y, offset.x] # 如何计算三维速度方向？
        vel[i] *= init_vel

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

    my_ggui.GUI.begin("Property", 0.03, 0.05, 0.2, 0.15)
    p_radius = my_ggui.GUI.slider_float("radius", p_radius, 1e-3, 1e-2)
    # 下面的变量暂时无法传参
    # G = my_ggui.GUI.slider_float("G", G, 1e-11, 1)
    # off_scale = my_ggui.GUI.slider_float("off scale", off_scale, 0, 1)
    # substepping = my_ggui.GUI.slider_float("substepping", substepping, 1, 1e2)
    my_ggui.GUI.end()

    my_ggui.GUI.begin("Options", 0.03, 0.25, 0.2, 0.25)
    str_frame = "Frame: " + str(id_frame)
    my_ggui.GUI.text(str_frame)
    if my_ggui.GUI.button("Restart"):
        id_frame = 0
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
        print("3D Renderer Designing...")
    elif dim == 2:
        backgroundcolor = (17 / 255, 47 / 255, 65 / 255) # 0x112F41
        canvas.set_background_color(backgroundcolor)
        canvas.circles(pos, radius=p_radius, color=(1, 1, 1))

## main
print("Hallo, N-Body")
initialize(pos_c)

while my_ggui.running:
    for e in my_ggui.get_events(ti.ui.PRESS):
        if e.key in [ti.ui.ESCAPE]:
            exit()
        elif e.key == ti.ui.SPACE:
            flag_pause = not flag_pause
        elif (e.key == ti.ui.LMB) & (dim == 0):
            # Wrong of pos????? What's the difference between this "pos" and the "pos_c" defined already?
            pos_tmp = my_ggui.get_cursor_pos()
            pos = ti.Vector([pos_tmp[0], pos_tmp[1]])
            initialize(pos)

    if not flag_pause:
        id_frame += 1
        for i in range(substepping):
            cal_force()
            update()
    if flag_exit:
        my_ggui.running = False
    render()
    show_options()
    my_ggui.show()

"""
# 注意gui和ggui的尺寸计算方式似乎不同
my_gui = ti.GUI("My N-Body GUI", res)
while my_gui.running:
    for i in range(substepping):
        cal_force()
        update()
    my_gui.clear(0x112F41)
    my_gui.circles(pos.to_numpy(), color=0xffffff, radius=p_radius)
    my_gui.show()
"""

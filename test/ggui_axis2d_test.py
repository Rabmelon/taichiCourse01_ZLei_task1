import taichi as ti
ti.init()

my_ggui = ti.ui.Window("test-2D", (1000, 600))
my_canvas = my_ggui.get_canvas()

pos_axis = ti.Vector.field(2, ti.f32, shape=4)
c_axis = ti.Vector.field(3, ti.f32, shape=4)
pos_axis[0] = ti.Vector([0.0, 0.0])
pos_axis[1] = ti.Vector([0.5, 0.0])
pos_axis[2] = ti.Vector([0.0, 0.5])
pos_axis[3] = ti.Vector([0.5, 0.5])
c_axis[0] = ti.Vector([1.0, 1.0, 0.0])
c_axis[1] = ti.Vector([1.0, 0.0, 0.0])
c_axis[2] = ti.Vector([0.0, 1.0, 0.0])
c_axis[3] = ti.Vector([0.0, 0.0, 1.0])

while my_ggui.running:
    my_canvas.set_background_color((17 / 255, 47 / 255, 65 / 255))
    my_canvas.circles(pos_axis, radius=0.1, per_vertex_color=c_axis)
    my_ggui.show()

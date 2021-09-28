import taichi as ti

ti.init()

# define variables
flag_exit = False
flag_pause = False
id_frame = 0

steps = 1e3

res = (800, 600)
my_ggui = ti.ui.Window("Hallo Taichi GGUI", res, vsync=True)

# def functions



# def GGUI windows
def show_options():
    global flag_exit
    global flag_pause
    global id_frame

    my_ggui.GUI.begin("Options", 0.1, 0.5, 0.2, 0.4)
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

def show_frame_id():
    global id_frame

    tmp_str = "Thank you " + str(id_frame)
    my_ggui.GUI.text(tmp_str)


# main
while my_ggui.running:
    if not flag_pause:
        id_frame += 1
    if flag_exit:
        my_ggui.running = False

    show_frame_id()
    show_options()

    my_ggui.show()

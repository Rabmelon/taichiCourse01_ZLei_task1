import taichi as ti
from celestial_objects import Star, Planet


if __name__ == "__main__":

    ti.init(arch=ti.cuda)

    # control
    paused = False
    export_images = False

    # stars and planets
    stars = Star(N=3, mass=10000)
    stars.initialize(0.5, 0.5, 0.2, 10)
    planets = Planet(N=10000, mass=1)
    planets.initialize(0.5, 0.5, 0.4, 10)

    # GGUI
    my_ggui = ti.ui.Window("Galaxy GGUI", (900, 800))
    scene = ti.ui.Scene()

    # GUI
    # my_gui = ti.GUI("Galaxy", (800, 800))

    h = 5e-5 # time-step size
    i = 0
    while my_ggui.running:

        for e in my_ggui.get_events(ti.ui.PRESS):
            if e.key == ti.ui.ESCAPE:
                exit()
            elif e.key == ti.ui.SPACE:
                paused = not paused
                print("paused =", paused)
            elif e.key == 'r':
                stars.initialize(0.5, 0.5, 0.2, 10)
                planets.initialize(0.5, 0.5, 0.4, 10)
                i = 0
            elif e.key == 'i':
                export_images = not export_images

        if not paused:
            stars.computeForce()
            planets.computeForce(stars)
            for celestial_obj in (stars, planets):
                celestial_obj.update(h)
            scene.particles(stars.Pos(), radius=5, per_vertex_color=0xffd500)
            i += 1

        # stars.display(my_ggui, radius=10, color=0xffd500)
        planets.display(my_ggui)
        if export_images:
            my_ggui.show(f"images\output_{i:05}.png")
        else:
            my_ggui.show()

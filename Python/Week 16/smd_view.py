import json, pathlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons, Button
from smd_model import simulate, regime

CONFIG_PATH = "config.json"
FORCES = ("free", "step", "sin")


def run():
    fig, (ax_t, ax_ph) = plt.subplots(1, 2, figsize=(12, 6))
    fig.subplots_adjust(bottom=0.42)
    ax_t.set_xlabel("t (s)"); ax_t.set_ylabel("x (m)"); ax_t.grid(alpha=0.3)
    ax_ph.set_xlabel("x (m)"); ax_ph.set_ylabel("v (m/s)"); ax_ph.grid(alpha=0.3)

    line_t,  = ax_t.plot([],  [], color="#1E88E5")
    line_ph, = ax_ph.plot([], [], color="#D63E3E")

    s_m  = Slider(fig.add_axes([0.1, 0.30, 0.6, 0.02]), "m",    0.1, 10.0, valinit=1.0)
    s_k  = Slider(fig.add_axes([0.1, 0.26, 0.6, 0.02]), "k",    0.1, 50.0, valinit=10.0)
    s_c  = Slider(fig.add_axes([0.1, 0.22, 0.6, 0.02]), "c",    0.0, 10.0, valinit=0.5)
    s_x0 = Slider(fig.add_axes([0.1, 0.18, 0.6, 0.02]), "x₀", -5.0,  5.0, valinit=1.0)
    s_v0 = Slider(fig.add_axes([0.1, 0.14, 0.6, 0.02]), "v₀", -5.0,  5.0, valinit=0.0)
    s_A  = Slider(fig.add_axes([0.1, 0.10, 0.6, 0.02]), "A",    0.0, 10.0, valinit=1.0)
    s_om = Slider(fig.add_axes([0.1, 0.06, 0.6, 0.02]), "ω_f",  0.1, 20.0, valinit=3.0)

    radio    = RadioButtons(fig.add_axes([0.78, 0.15, 0.12, 0.15]), FORCES)
    btn_save = Button(fig.add_axes([0.78, 0.08, 0.05, 0.04]), "save")
    btn_load = Button(fig.add_axes([0.85, 0.08, 0.05, 0.04]), "load")

    def force_fn():
        lbl = radio.value_selected
        if lbl == "free": return lambda t: 0.0
        if lbl == "step": return lambda t: 1.0 if t > 1.0 else 0.0
        return lambda t: s_A.val * np.sin(s_om.val * t)

    def update(_=None):
        m, k, c = s_m.val, s_k.val, s_c.val
        t_arr, X = simulate(m, c, k, s_x0.val, s_v0.val, force_fn())
        line_t.set_data(t_arr, X[:, 0])
        line_ph.set_data(X[:, 0], X[:, 1])
        ax_t.relim();  ax_t.autoscale_view()
        ax_ph.relim(); ax_ph.autoscale_view()
        fig.suptitle(f"{regime(m, c, k)}   ζ = {c/(2*(m*k)**0.5):.3f}")
        fig.canvas.draw_idle()

    def save(_):
        cfg = {"m": s_m.val, "k": s_k.val, "c": s_c.val,
               "x0": s_x0.val, "v0": s_v0.val,
               "A": s_A.val, "omega_f": s_om.val,
               "force": radio.value_selected}
        pathlib.Path(CONFIG_PATH).write_text(json.dumps(cfg, indent=2))
        print(f"saved → {CONFIG_PATH}")

    def load(_):
        try:
            cfg = json.loads(pathlib.Path(CONFIG_PATH).read_text())
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"load failed: {e}"); return
        s_m.set_val(cfg["m"]); s_k.set_val(cfg["k"]); s_c.set_val(cfg["c"])
        s_x0.set_val(cfg["x0"]); s_v0.set_val(cfg["v0"])
        s_A.set_val(cfg["A"]); s_om.set_val(cfg["omega_f"])
        radio.set_active(FORCES.index(cfg["force"]))

    for s in (s_m, s_k, s_c, s_x0, s_v0, s_A, s_om):
        s.on_changed(update)
    radio.on_clicked(update)
    btn_save.on_clicked(save)
    btn_load.on_clicked(load)

    update()
    plt.show()
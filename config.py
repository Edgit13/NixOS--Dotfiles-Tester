import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import libqtile.resources

mod = "mod4"
terminal = guess_terminal()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    if os.path.isfile(home):
        # Popen не блокує запуск самого Qtile
        subprocess.Popen([home])

keys = [
    # Запуск програм
    Key([mod], "b", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod], "e", lazy.spawn("nautilus"), desc="Launch Nautilus"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch Rofi"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Керування гучністю (Pipewire / PulseAudio)
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    
    # Стрілки для гучності (якщо немає спец. клавіш)
    Key([mod], "Up", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([mod], "Down", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),

    # Навігація між вікнами (Vim style)
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "space", lazy.layout.next()),

    # Переміщення вікон
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Зміна розміру вікон
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),

    # Керування вікнами та системою
    Key([mod], "q", lazy.window.kill(), desc="Kill window"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "t", lazy.window.toggle_floating()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

# Робочі столи
groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
    ])

layout_theme = {
    "border_width": 3,
    "margin": 15,
    "border_focus": "FFFFFF",
    "border_normal": "CCCCCC",
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(highlight_method='line'),
                widget.Prompt(),
                widget.WindowName(),
                widget.Systray(),
                # Додав віджет гучності, щоб бачити відсотки
                widget.Volume(
                    fmt='Vol: {}',
                    padding=10,
                    # Ця команда витягує чистий відсоток гучності через pactl
                    get_volume_command="pactl get-sink-volume @DEFAULT_SINK@ | awk '{print $5}' | head -n1",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('pavucontrol')},
                ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.QuickExit(),
            ],
            24,
            background="#000000",
        ),
    ),
]

# Налаштування миші та плаваючих вікон
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wmname = "LG3D"



# Qtile Conf
from libqtile.config import Key, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout

# Custom Conf
from custom.bindings import mod_key, init_keys
from custom.theme import colors
from custom.screens import init_screens
from custom.groups import init_groups
from custom.widgets import defaults


# Basic Config

mod = mod_key
keys = init_keys()
widget_defaults = defaults
extension_defaults = widget_defaults.copy()

# Workspaces

groups = init_groups(keys)

# Layouts

layouts = [
    layout.Max(),
    layout.MonadTall(
        border_focus=colors["primary"][0],
        border_width=1,
        margin=4
    )
]

# Screens

screens = init_screens()

# Drag floating layouts

mouse = [
    Drag(
        [mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        {'wmclass': 'confirm'},
        {'wmclass': 'dialog'},
        {'wmclass': 'download'},
        {'wmclass': 'error'},
        {'wmclass': 'file_progress'},
        {'wmclass': 'notification'},
        {'wmclass': 'splash'},
        {'wmclass': 'toolbar'},
        {'wmclass': 'confirmreset'},  # gitk
        {'wmclass': 'makebranch'},  # gitk
        {'wmclass': 'maketag'},  # gitk
        {'wname': 'branchdialog'},  # gitk
        {'wname': 'pinentry'},  # GPG key password entry
        {'wmclass': 'ssh-askpass'},  # ssh-askpass
    ],
    border_focus=colors["secondary"][0]
)
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's lightlist.
wmname = "LG3D"

from libqtile.config import Key
from libqtile.command import lazy

mod_key = "mod4"

def init_keys():
    return [
        # ------------ WINDOW CONFIGS ------------

        # Switch between windows in current stack pane
        Key([mod_key], "j", lazy.layout.down()),
        Key([mod_key], "k", lazy.layout.up()),
        Key([mod_key], "h", lazy.layout.left()),
        Key([mod_key], "l", lazy.layout.right()),

        # Change window sizes (MonadTall)
        Key([mod_key, "shift"], "l", lazy.layout.grow()),
        Key([mod_key, "shift"], "h", lazy.layout.shrink()),

        # Toggle floating
        Key([mod_key, "shift"], "f", lazy.window.toggle_floating()),

        # Move windows up or down in current stack
        Key([mod_key, "shift"], "j", lazy.layout.shuffle_down()),
        Key([mod_key, "shift"], "k", lazy.layout.shuffle_up()),

        # Toggle between different layouts as defined below
        Key([mod_key], "Tab", lazy.next_layout()),

        # Kill window
        Key([mod_key], "w", lazy.window.kill()),

        # Restart Qtile
        Key([mod_key, "control"], "r", lazy.restart()),

        Key([mod_key, "control"], "q", lazy.shutdown()),
        Key([mod_key], "r", lazy.spawncmd()),

        # Switch window focus to other pane(s) of stack
        Key([mod_key], "space", lazy.layout.next()),

        # Swap panes of split stack
        Key([mod_key, "shift"], "space", lazy.layout.rotate()),

        # ------------ APPS CONFIG ------------

        # Menu
        Key([mod_key], "m", lazy.spawn("rofi -show run")),

        # Window Nav
        Key([mod_key, "shift"], "m", lazy.spawn("rofi -show")),

        # Browser
        Key([mod_key], "b", lazy.spawn("firefox")),

        # File Manager
        Key([mod_key], "f", lazy.spawn("thunar")),

        # Terminal
        Key([mod_key], "Return", lazy.spawn("alacritty")),

        # Redshift
        Key([mod_key], "r", lazy.spawn("redshift -O 2400")),
        Key([mod_key, "shift"], "r", lazy.spawn("redshift -x")),

        # ------------ HARDWARE CONFIG ------------

        # Volume
        Key([], "XF86AudioLowerVolume", lazy.spawn(
            "pactl set-sink-volume @DEFAULT_SINK@ -5%"
        )),
        Key([], "XF86AudioRaiseVolume", lazy.spawn(
            "pactl set-sink-volume @DEFAULT_SINK@ +5%"
        )),
        Key([], "XF86AudioMute", lazy.spawn(
            "pactl set-sink-mute @DEFAULT_SINK@ toggle"
        )),

        #Brightness
        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
    ]
    
    from libqtile.config import Key, Group
from libqtile.command import lazy

from custom.bindings import mod_key

def init_groups(keys):
    groups = [Group(i) for i in ["NET", "DEV", "TERM", "FS", "MEDIA", "MISC"]]

    for i in range(len(groups)):
        # Each workspace is identified by a number starting at 1
        actual_key = i + 1
        keys.extend([
            # Switch to workspace N (actual_key)
            Key([mod_key], str(actual_key), lazy.group[groups[i].name].toscreen()),
            # Send window to workspace N (actual_key)
            Key([mod_key, "shift"], str(actual_key), lazy.window.togroup(groups[i].name)),
        ])

    return groups
    
    rom libqtile.config import Screen
from libqtile import bar

from custom.widgets import init_laptop_widgets, init_monitor_widgets
import subprocess


def init_screens():
    screens = [
        Screen(
            top=bar.Bar(
                init_laptop_widgets(),
                24,
                opacity=0.95
            )
        )
    ]

    # Check if HMDI is plugged in, if so initialize another screen
    check_hdmi = "xrandr | grep ' connected' | grep 'HDMI' | awk '{print $1}'"
    if (subprocess.getoutput(check_hdmi) == "HDMI-1"):
        screens.append(
            Screen(
                top=bar.Bar(
                    init_monitor_widgets(),
                    24,
                    opacity=0.95
                )
            )
        )

    return screens
    
    from os import listdir
from os import path
import json


# color scheme available in ~/.config/qtile/themes
theme = "material-darker"

theme_path = path.join(
    path.expanduser("~"), ".config", "qtile", "themes", theme
)

# map color name to hex values
with open(path.join(theme_path, "colors.json")) as f:
    colors = json.load(f)

img = {}

# map img name to its path
img_path = path.join(theme_path, "img")
for i in listdir(img_path):
    img[i.split(".")[0]] = path.join(img_path, i)
    
    from libqtile import widget
from custom.theme import colors, img


def sep(p):
    return widget.Sep(
        linewidth=0,
        padding=p,
        foreground=colors["light"],
        background=colors["dark"]
    )


def group_box():
    return widget.GroupBox(
        font="Ubuntu Bold",
        fontsize=10,
        margin_y=5,
        margin_x=0,
        padding_y=8,
        padding_x=5,
        borderwidth=1,
        active=colors["light"],
        inactive=colors["light"],
        rounded=False,
        highlight_method="block",
        this_current_screen_border=colors["primary"],
        this_screen_border=colors["grey"],
        other_current_screen_border=colors["dark"],
        other_screen_border=colors["dark"],
        foreground=colors["light"],
        background=colors["dark"]
    )


def window_name():
    return widget.WindowName(
        font="Ubuntu Bold",
        fontsize=11,
        foreground=colors["primary"],
        background=colors["dark"],
        padding=5
    )


def systray():
    return widget.Systray(
        background=colors["dark"],
        padding=5
    )


def image(image):
    return widget.Image(
        scale=True,
        filename=img[image],
        background=colors["dark"]
    )


def text_box(s, bgcolor):
    return widget.TextBox(
        font="Ubuntu Bold",
        text=s,
        padding=5,
        foreground=colors["light"],
        background=colors[bgcolor],
        fontsize=15
    )


def pacman(bgcolor):
    return widget.Pacman(
        execute="alacritty",
        update_interval=1800,
        foreground=colors["light"],
        background=colors[bgcolor]
    )


def net(bgcolor):
    return widget.Net(
        interface="wlp2s0",
        foreground=colors["light"],
        background=colors[bgcolor],
    )


def current_layout_icon(bgcolor):
    return widget.CurrentLayoutIcon(
        scale=0.65,
        foreground=colors["light"],
        background=colors[bgcolor],
    )


def current_layout(bgcolor):
    return widget.CurrentLayout(
        foreground=colors["light"],
        background=colors[bgcolor],
        padding=5
    )


def clock(bgcolor):
    return widget.Clock(
        foreground=colors["light"],
        background=colors[bgcolor],
        format="%d / %m / %Y - %H:%M "
    )


def init_laptop_widgets():
    return [
        sep(5),
        group_box(),
        sep(5),
        window_name(),
        sep(5),
        systray(),
        sep(5),
        image("bg-to-secondary"),
        text_box(" ⟳", "secondary"),
        pacman("secondary"),
        image("primary"),
        text_box(" ↯", "primary"),
        net("primary"),
        image("secondary"),
        current_layout_icon("secondary"),
        current_layout("secondary"),
        image("primary"),
        text_box(" 🕒", "primary"),
        clock("primary")
     ]


def init_monitor_widgets():
    return [
        sep(5),
        group_box(),
        sep(5),
        window_name(),
        image("bg-to-secondary"),
        current_layout_icon("secondary"),
        current_layout("secondary"),
        image("primary"),
        text_box(" 🕒", "primary"),
        clock("primary")
    ]


defaults = dict(
    font='Ubuntu Mono',
    fontsize=13,
    padding=2,
)

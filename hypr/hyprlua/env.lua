mainMod = "SUPER"
terminal = "kitty"
-- filemanager = "thunar"
filemanager = "dolphin"
code_editor = "code"
browser = "firefox"


hl.env("HYPRSHOT_DIR","/home/aashiqed/Pictures/hyprshot/")


-- Set the current desktop environment to KDE to ensure compatibility with certain applications(like dolphin) and features that rely on this environment variable.
hl.env("XDG_CURRENT_DESKTOP","KDE")
local mat = require("colors")
hl.window_rule({

    match = {
        class = "waypaper"
    },
    float = true,
    persistent_size = true
})
hl.window_rule({

    match = {
        class = "kitty|code|firefox|thunar|yazi|discord"
    },
    opacity=0.85
})

hl.window_rule({
    match = {
        class = "thunar"
    },
    float = true,
    size = { 800, 550 },
    center = true
})

hl.window_rule({
    match = {
        class = "kitty",
        title = "btop"
    },
    float = true,
    size = { 1000, 700 },
    center = true
})
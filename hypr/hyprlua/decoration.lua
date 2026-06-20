local mat = require("colors")
hl.config (
    {
        decoration = {
            rounding = 7,
            shadow = {
                color = mat.outline,
                color_inactive = mat.outline_variant,
                range = 1
            },
            blur = {
                enabled = true,
                size = 8,
                passes = 1,
                ignore_opacity = true,
                new_optimizations = true,
                xray = false,
                noise = 0.0177,
                contrast = 0.8916,
                brightness = 0.8172,
                vibrancy = 0.1696,
                vibrancy_darkness = 0.0000
            }
        },
    }
)

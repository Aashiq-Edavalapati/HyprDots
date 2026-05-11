local mat = require("colors")
hl.config (
    {
        decoration = {
            rounding = 7,
            -- dim_special = 0.5,

            blur = {
                -- enabled = false
            -- special = trues
          },
          shadow = {
            -- enabled = false
            color = mat.outline,
            color_inactive = mat.outline_variant
            -- color = "rgb(AC128C)",
          }
        },
    }
)
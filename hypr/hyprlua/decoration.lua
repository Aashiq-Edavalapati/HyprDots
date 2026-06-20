local mat = require("colors")
hl.config (
    {
        decoration = {
            rounding = 7,
          shadow = {

            color = mat.outline,
            color_inactive = mat.outline_variant,
            range = 1
          }
        },
    }
)
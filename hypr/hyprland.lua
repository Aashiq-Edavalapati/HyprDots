-- require("hyprlua.binds")

require("monitors")
require("hyprlua.binds")
require("hyprlua.general")
require("hyprlua.decoration")
require("hyprlua.exec")
require("hyprlua.workspace")
require("hyprlua.windowrule")
require("colors")


hl.gesture({
    fingers = 4,
    direction = "horizontal",
    action = "workspace"
})


hl.config({

	input =  {
		touchpad = {
			natural_scroll = true
		}
	},

    misc = {
        disable_hyprland_logo = true,
        vrr = true,
        disable_autoreload = false,
    },
    dwindle = {
        special_scale_factor = 0.9,
        
    },
    scrolling = {
        direction = "down"
    }
  }
  )


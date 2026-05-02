-- require("hyprlua.binds")

require("monitors")
require("hyprlua.binds")
require("hyprlua.general")
require("hyprlua.decoration")
require("hyprlua.exec")
require("hyprlua.workspace")


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
    },
    dwindle = {
        special_scale_factor = 0.9,
        
    }
  }
  )


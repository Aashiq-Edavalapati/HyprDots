-- require("hyprlua.binds")

require("monitors")
require("hyprlua.binds")
require("hyprlua.general")
require("hyprlua.decoration")


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
	}
  }
  )


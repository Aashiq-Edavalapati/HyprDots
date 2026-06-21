local mat = require("colors")

hl.window_rule({

    match = {

        class = "waypaper"

    },

    float = true
 

})

hl.window_rule{
    match = {
        class = "org.kde.dolphin"
    },
    float = true,
    center = true,
    persistent_size = true

}

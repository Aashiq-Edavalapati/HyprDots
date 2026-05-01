require("hyprlua.env")

-- hl.bind(keys, dispatcher, { flag1 = true, flag2 = true })

hl.bind(mainMod .. " + RETURN", hl.dsp.exec_cmd(terminal))

local closeWindowBind = hl.bind(mainMod .. " + Q", hl.dsp.window.close())

-- Move focus with "SUPER" + arrow keys
hl.bind(mainMod .. " + left",  hl.dsp.focus({ direction = "left" }))
hl.bind(mainMod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mainMod .. " + up",    hl.dsp.focus({ direction = "up" }))
hl.bind(mainMod .. " + down",  hl.dsp.focus({ direction = "down" }))


-- Laptop multimedia keys for volume and LCD brightness
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),      { locked = true, repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),     { locked = true, repeating = true })
hl.bind("XF86AudioMicMute",     hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),   { locked = true, repeating = true })
hl.bind("XF86MonBrightnessUp",  hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),                  { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),                  { locked = true, repeating = true })



hl.bind(mainMod .. "+ Z", hl.dsp.window.drag(), { mouse = true })
hl.bind(mainMod .. "+ X",hl.dsp.window.resize(), {mouse = true})


-- change focused workspace
hl.bind(mainMod .. "+ 1",hl.dsp.focus({workspace = 1}))
hl.bind(mainMod .. "+ 2",hl.dsp.focus({workspace = 2}))
hl.bind(mainMod .. "+ 3",hl.dsp.focus({workspace = 3}))
hl.bind(mainMod .. "+ 4",hl.dsp.focus({workspace = 4}))
hl.bind(mainMod .. "+ 5",hl.dsp.focus({workspace = 5}))
hl.bind(mainMod .. "+ 6",hl.dsp.focus({workspace = 6}))
hl.bind(mainMod .. "+ 7",hl.dsp.focus({workspace = 7}))
hl.bind(mainMod .. "+ 8",hl.dsp.focus({workspace = 8}))
hl.bind(mainMod .. "+ 9",hl.dsp.focus({workspace = 9}))

--move window to a specific tab
hl.bind(mainMod .. " + ALT + 1",hl.dsp.window.move({workspace = 1  }) )
hl.bind(mainMod .. " + ALT + 2",hl.dsp.window.move({workspace = 2  }) )
hl.bind(mainMod .. " + ALT + 3",hl.dsp.window.move({workspace = 3  }) )
hl.bind(mainMod .. " + ALT + 4",hl.dsp.window.move({workspace = 4  }) )
hl.bind(mainMod .. " + ALT + 5",hl.dsp.window.move({workspace = 5  }) )
hl.bind(mainMod .. " + ALT + 6",hl.dsp.window.move({workspace = 6  }) )
hl.bind(mainMod .. " + ALT + 7",hl.dsp.window.move({workspace = 7  }) )
hl.bind(mainMod .. " + ALT + 8",hl.dsp.window.move({workspace = 8  }) )
hl.bind(mainMod .. " + ALT + 9",hl.dsp.window.move({workspace = 9  }) )

--toggle floating state
hl.bind(mainMod .. "+ ALT + SPACE", hl.dsp.window.float())

--move window within a workspace
hl.bind(mainMod .. "+SHIFT + up",hl.dsp.window.move({direction = "up"}))
hl.bind(mainMod .. "+SHIFT + down",hl.dsp.window.move({direction = "down"}))
hl.bind(mainMod .. "+SHIFT + left",hl.dsp.window.move({direction = "left"}))
hl.bind(mainMod .. "+SHIFT + right",hl.dsp.window.move({direction = "right"}))


--fullscreen a window
hl.bind(mainMod .. "+SHIFT+F",hl.dsp.window.fullscreen({mode = "fullscreen"}))
hl.bind(mainMod .. "+SHIFT+D",hl.dsp.window.fullscreen({mode = "maximized"}))
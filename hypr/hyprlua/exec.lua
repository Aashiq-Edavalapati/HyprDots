hl.on("hyprland.start", function () 
  hl.exec_cmd("waypaper --restore")
  hl.exec_cmd("syncthing --no-browser")
  hl.exec_cmd("quickshell -p ~/.local/src/HyprDots/tide-island/")

end)
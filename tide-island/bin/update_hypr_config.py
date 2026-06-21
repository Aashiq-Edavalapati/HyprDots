#!/usr/bin/env python3
import sys
import argparse
import os
import re
import json

def parse_window_rules(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, 'r') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading gui.lua: {e}", file=sys.stderr)
        return []
        
    rules = []
    idx = 0
    while True:
        pos = content.find("hl.window_rule", idx)
        if pos == -1:
            break
        brace_pos = content.find("{", pos)
        if brace_pos == -1:
            break
        brace_count = 1
        i = brace_pos + 1
        while i < len(content) and brace_count > 0:
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
            i += 1
        block = content[brace_pos:i]
        idx = i
        
        rule = {}
        match_block_m = re.search(r'match\s*=\s*\{([^}]+)\}', block)
        if match_block_m:
            match_body = match_block_m.group(1)
            class_m = re.search(r'class\s*=\s*"([^"]+)"', match_body)
            if class_m:
                rule['class'] = class_m.group(1)
            title_m = re.search(r'title\s*=\s*"([^"]+)"', match_body)
            if title_m:
                rule['title'] = title_m.group(1)
                
        block_clean = re.sub(r'match\s*=\s*\{[^}]+\}', '', block)
        
        def parse_bool(k):
            m = re.search(rf'{k}\s*=\s*(true|false)', block_clean)
            return m.group(1) == 'true' if m else None
            
        def parse_float(k):
            m = re.search(rf'{k}\s*=\s*([0-9.]+)', block_clean)
            return float(m.group(1)) if m else None
            
        def parse_int(k):
            m = re.search(rf'{k}\s*=\s*(\d+)', block_clean)
            return int(m.group(1)) if m else None

        for k in ['float', 'opaque', 'no_blur', 'stay_focused', 'persistent_size']:
            val = parse_bool(k)
            if val is not None:
                rule[k] = val
        val_opacity = parse_float('opacity')
        if val_opacity is not None:
            rule['opacity'] = val_opacity
        val_rounding = parse_int('rounding')
        if val_rounding is not None:
            rule['rounding'] = val_rounding
            
        if 'class' in rule or 'title' in rule:
            rules.append(rule)
            
    return rules

def parse_gui_lua(path):
    vals = {
        'gaps_in': 5,
        'gaps_out': 15,
        'border_size': 2,
        'rounding': 12,
        'blur_enabled': 'true',
        'blur_size': 8,
        'blur_passes': 1,
        'blur_ignore_opacity': 'true',
        'blur_new_optimizations': 'true',
        'blur_xray': 'false',
        'blur_noise': 0.0117,
        'blur_contrast': 0.8916,
        'blur_brightness': 0.8172,
        'blur_vibrancy': 0.1696,
        'blur_vibrancy_darkness': 0.0,
        'rules': []
    }
    if not os.path.exists(path):
        return vals
        
    try:
        with open(path, 'r') as f:
            content = f.read()
            
        m = re.search(r'gaps_in\s*=\s*(\d+)', content)
        if m:
            vals['gaps_in'] = int(m.group(1))
            
        m = re.search(r'gaps_out\s*=\s*(\d+)', content)
        if m:
            vals['gaps_out'] = int(m.group(1))
            
        m = re.search(r'border_size\s*=\s*(\d+)', content)
        if m:
            vals['border_size'] = int(m.group(1))
            
        m = re.search(r'rounding\s*=\s*(\d+)', content)
        if m:
            vals['rounding'] = int(m.group(1))
            
        # extract blur block
        blur_match = re.search(r'blur\s*=\s*\{([^}]+)\}', content)
        if blur_match:
            blur_body = blur_match.group(1)
            
            def parse_bool(k, default):
                m = re.search(rf'{k}\s*=\s*(true|false)', blur_body)
                return m.group(1) if m else default
                
            def parse_int(k, default):
                m = re.search(rf'{k}\s*=\s*(\d+)', blur_body)
                return int(m.group(1)) if m else default
                
            def parse_float(k, default):
                m = re.search(rf'{k}\s*=\s*([0-9.]+)', blur_body)
                return float(m.group(1)) if m else default
                
            vals['blur_enabled'] = parse_bool('enabled', vals['blur_enabled'])
            vals['blur_size'] = parse_int('size', vals['blur_size'])
            vals['blur_passes'] = parse_int('passes', vals['blur_passes'])
            vals['blur_ignore_opacity'] = parse_bool('ignore_opacity', vals['blur_ignore_opacity'])
            vals['blur_new_optimizations'] = parse_bool('new_optimizations', vals['blur_new_optimizations'])
            vals['blur_xray'] = parse_bool('xray', vals['blur_xray'])
            vals['blur_noise'] = parse_float('noise', vals['blur_noise'])
            vals['blur_contrast'] = parse_float('contrast', vals['blur_contrast'])
            vals['blur_brightness'] = parse_float('brightness', vals['blur_brightness'])
            vals['blur_vibrancy'] = parse_float('vibrancy', vals['blur_vibrancy'])
            vals['blur_vibrancy_darkness'] = parse_float('vibrancy_darkness', vals['blur_vibrancy_darkness'])
    except Exception as e:
        print(f"Error parsing gui.lua: {e}", file=sys.stderr)
        
    vals['rules'] = parse_window_rules(path)
    return vals

def write_gui_lua(path, vals):
    content = f"""local mat = require("colors")

hl.config (
{{
    general = {{
        gaps_out = {vals['gaps_out']},
        gaps_in = {vals['gaps_in']},
        border_size = {vals['border_size']},
        col = {{
            active_border = mat.primary,
            inactive_border = mat.surface
        }}
    }},
    decoration = {{
        rounding = {vals['rounding']},
        shadow = {{
            color = mat.outline,
            color_inactive = mat.outline_variant,
            range = 1
        }},
        blur = {{
            enabled = {vals['blur_enabled']},
            size = {vals['blur_size']},
            passes = {vals['blur_passes']},
            ignore_opacity = {vals['blur_ignore_opacity']},
            new_optimizations = {vals['blur_new_optimizations']},
            xray = {vals['blur_xray']},
            noise = {vals['blur_noise']:.4f},
            contrast = {vals['blur_contrast']:.4f},
            brightness = {vals['blur_brightness']:.4f},
            vibrancy = {vals['blur_vibrancy']:.4f},
            vibrancy_darkness = {vals['blur_vibrancy_darkness']:.4f}
        }}
    }}
}}
)
"""

    lua_rules = []
    for r in vals['rules']:
        rule_lines = ["hl.window_rule({", "    match = {"]
        match_fields = []
        if 'class' in r and r['class']:
            match_fields.append(f'        class = "{r["class"]}"')
        if 'title' in r and r['title']:
            match_fields.append(f'        title = "{r["title"]}"')
        rule_lines.append(",\n".join(match_fields))
        rule_lines.append("    },")
        
        effects = []
        for k in ['float', 'opaque', 'no_blur', 'stay_focused', 'persistent_size']:
            if k in r and r[k] is not None:
                effects.append(f'    {k} = {"true" if r[k] else "false"}')
        if 'opacity' in r and r['opacity'] is not None:
            try:
                effects.append(f'    opacity = {float(r["opacity"])}')
            except:
                pass
        if 'rounding' in r and r['rounding'] is not None:
            try:
                effects.append(f'    rounding = {int(r["rounding"])}')
            except:
                pass
        rule_lines.append(",\n".join(effects))
        rule_lines.append("})")
        lua_rules.append("\n".join(rule_lines))
        
    if lua_rules:
        content += "\n\n" + "\n\n".join(lua_rules) + "\n"
    else:
        content += "\n"
        
    try:
        with open(path, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing gui.lua: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Update Hyprland Lua settings in gui.lua")
    parser.add_argument("--gaps-in", type=int)
    parser.add_argument("--gaps-out", type=int)
    parser.add_argument("--border", type=int)
    parser.add_argument("--rounding", type=int)
    
    # blur parameters
    parser.add_argument("--blur-enabled", choices=['true', 'false'])
    parser.add_argument("--blur-size", type=int)
    parser.add_argument("--blur-passes", type=int)
    parser.add_argument("--blur-ignore-opacity", choices=['true', 'false'])
    parser.add_argument("--blur-new-optimizations", choices=['true', 'false'])
    parser.add_argument("--blur-xray", choices=['true', 'false'])
    parser.add_argument("--blur-noise", type=float)
    parser.add_argument("--blur-contrast", type=float)
    parser.add_argument("--blur-brightness", type=float)
    parser.add_argument("--blur-vibrancy", type=float)
    parser.add_argument("--blur-vibrancy-darkness", type=float)
    
    # window rules
    parser.add_argument("--get-window-rules", action="store_true")
    parser.add_argument("--window-rules", type=str)
    
    args = parser.parse_args()
    
    hyprlua_dir = os.path.expanduser("~/.config/hypr/hyprlua")
    if not os.path.exists(hyprlua_dir):
        hyprlua_dir = os.path.expanduser("~/.local/src/HyprDots/hypr/hyprlua")
        
    gui_path = os.path.join(hyprlua_dir, "gui.lua")
    
    # Read the current values from gui.lua
    vals = parse_gui_lua(gui_path)
    
    if args.get_window_rules:
        print(json.dumps(vals['rules']))
        return
        
    should_write = False
    
    if args.window_rules is not None:
        try:
            vals['rules'] = json.loads(args.window_rules)
            should_write = True
        except Exception as e:
            print(f"Error parsing window rules parameter: {e}", file=sys.stderr)
            
    if args.gaps_in is not None and args.gaps_out is not None and args.border is not None:
        vals['gaps_in'] = args.gaps_in
        vals['gaps_out'] = args.gaps_out
        vals['border_size'] = args.border
        should_write = True
        
    # Update blur/decoration parameters if provided
    if args.rounding is not None:
        vals['rounding'] = args.rounding
        should_write = True
    if args.blur_enabled is not None:
        vals['blur_enabled'] = args.blur_enabled
        should_write = True
    if args.blur_size is not None:
        vals['blur_size'] = args.blur_size
        should_write = True
    if args.blur_passes is not None:
        vals['blur_passes'] = args.blur_passes
        should_write = True
    if args.blur_ignore_opacity is not None:
        vals['blur_ignore_opacity'] = args.blur_ignore_opacity
        should_write = True
    if args.blur_new_optimizations is not None:
        vals['blur_new_optimizations'] = args.blur_new_optimizations
        should_write = True
    if args.blur_xray is not None:
        vals['blur_xray'] = args.blur_xray
        should_write = True
    if args.blur_noise is not None:
        vals['blur_noise'] = args.blur_noise
        should_write = True
    if args.blur_contrast is not None:
        vals['blur_contrast'] = args.blur_contrast
        should_write = True
    if args.blur_brightness is not None:
        vals['blur_brightness'] = args.blur_brightness
        should_write = True
    if args.blur_vibrancy is not None:
        vals['blur_vibrancy'] = args.blur_vibrancy
        should_write = True
    if args.blur_vibrancy_darkness is not None:
        vals['blur_vibrancy_darkness'] = args.blur_vibrancy_darkness
        should_write = True
        
    if should_write:
        write_gui_lua(gui_path, vals)
        os.system("hyprctl reload")

if __name__ == "__main__":
    main()

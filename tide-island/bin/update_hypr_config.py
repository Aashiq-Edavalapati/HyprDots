#!/usr/bin/env python3
import sys
import argparse
import os
import re
import json

def parse_decoration_lua(path):
    vals = {
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
        'blur_vibrancy_darkness': 0.0
    }
    if not os.path.exists(path):
        return vals
        
    try:
        with open(path, 'r') as f:
            content = f.read()
            
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
        print(f"Error parsing decoration.lua: {e}", file=sys.stderr)
        
    return vals

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

def main():
    parser = argparse.ArgumentParser(description="Update Hyprland Lua settings")
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
        # Fallback to local source path if symlink doesn't exist
        hyprlua_dir = os.path.expanduser("~/.local/src/HyprDots/hypr/hyprlua")
        
    general_path = os.path.join(hyprlua_dir, "general.lua")
    decoration_path = os.path.join(hyprlua_dir, "decoration.lua")
    windowrule_path = os.path.join(hyprlua_dir, "gui.lua")
    
    if args.get_window_rules:
        rules = parse_window_rules(windowrule_path)
        print(json.dumps(rules))
        return
        
    if args.window_rules is not None:
        try:
            rules = json.loads(args.window_rules)
            lua_lines = ['local mat = require("colors")']
            for r in rules:
                lua_lines.append("hl.window_rule({")
                lua_lines.append("    match = {")
                match_fields = []
                if 'class' in r and r['class']:
                    match_fields.append(f'        class = "{r["class"]}"')
                if 'title' in r and r['title']:
                    match_fields.append(f'        title = "{r["title"]}"')
                lua_lines.append(",\n".join(match_fields))
                lua_lines.append("    },")
                
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
                lua_lines.append(",\n".join(effects))
                lua_lines.append("})")
            
            with open(windowrule_path, "w") as f:
                f.write("\n\n".join(lua_lines) + "\n")
                
            os.system("hyprctl reload")
        except Exception as e:
            print(f"Error updating window rules: {e}", file=sys.stderr)
            
    if args.gaps_in is not None and args.gaps_out is not None and args.border is not None:
        general_content = f"""local mat = require("colors")
hl.config (

{{
    general = {{
        gaps_out = {args.gaps_out},
        gaps_in = {args.gaps_in},
        border_size = {args.border},
        col = {{
            active_border = mat.primary,
            inactive_border = mat.surface
        }}
    }}
}}

)
"""
        with open(general_path, "w") as f:
            f.write(general_content)
            
    # Check if we need to update decoration.lua
    update_dec = (args.rounding is not None or
                  args.blur_enabled is not None or
                  args.blur_size is not None or
                  args.blur_passes is not None or
                  args.blur_ignore_opacity is not None or
                  args.blur_new_optimizations is not None or
                  args.blur_xray is not None or
                  args.blur_noise is not None or
                  args.blur_contrast is not None or
                  args.blur_brightness is not None or
                  args.blur_vibrancy is not None or
                  args.blur_vibrancy_darkness is not None)
                  
    if update_dec:
        vals = parse_decoration_lua(decoration_path)
        
        if args.rounding is not None:
            vals['rounding'] = args.rounding
        if args.blur_enabled is not None:
            vals['blur_enabled'] = args.blur_enabled
        if args.blur_size is not None:
            vals['blur_size'] = args.blur_size
        if args.blur_passes is not None:
            vals['blur_passes'] = args.blur_passes
        if args.blur_ignore_opacity is not None:
            vals['blur_ignore_opacity'] = args.blur_ignore_opacity
        if args.blur_new_optimizations is not None:
            vals['blur_new_optimizations'] = args.blur_new_optimizations
        if args.blur_xray is not None:
            vals['blur_xray'] = args.blur_xray
        if args.blur_noise is not None:
            vals['blur_noise'] = args.blur_noise
        if args.blur_contrast is not None:
            vals['blur_contrast'] = args.blur_contrast
        if args.blur_brightness is not None:
            vals['blur_brightness'] = args.blur_brightness
        if args.blur_vibrancy is not None:
            vals['blur_vibrancy'] = args.blur_vibrancy
        if args.blur_vibrancy_darkness is not None:
            vals['blur_vibrancy_darkness'] = args.blur_vibrancy_darkness
            
        decoration_content = f"""local mat = require("colors")
hl.config (
    {{
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
        }},
    }}
)
"""
        with open(decoration_path, "w") as f:
            f.write(decoration_content)

if __name__ == "__main__":
    main()

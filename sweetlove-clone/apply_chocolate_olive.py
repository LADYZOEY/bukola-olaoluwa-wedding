#!/usr/bin/env python3
"""
Updates Sweet Love Theme to Chocolate & Olive Palette:
- Chocolate: Deep rich warm chocolate (#4A2E18 / HSL 25 45% 32%), Cocoa Text (#38200F)
- Olive: Elegant Olive Green (#606C38 / HSL 85 28% 62%), Olive Mist (#EEF2E6 / HSL 85 24% 92%)
- Accents: Warm Linen Cream (#FAF7F2), Champagne Gold accents
- Wax Seal: Embossed Chocolate Wax Seal with Gold Monogram
- Confetti: Chocolate & Olive celebration palette
"""

import os
import re

CLONE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(CLONE_DIR, "assets", "index-CMJN1tNq.css")
JS_FILE = os.path.join(CLONE_DIR, "assets", "index-qUp0T8yC.js")

def update_css():
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # Current root token string from previous update:
    old_root_tokens = "--primary: 354 44% 64%;--primary-foreground: 0 0% 100%;--secondary: 265 32% 76%;--secondary-foreground: 265 25% 15%;--muted: 265 25% 96%;--muted-foreground: 265 15% 42%;--accent: 354 44% 64%;--accent-foreground: 0 0% 100%;--destructive: 0 84% 60%;--destructive-foreground: 0 0% 98%;--border: 265 20% 90%;--input: 265 20% 90%;--ring: 354 44% 64%;--radius: .5rem;--sidebar-background: 0 0% 98%;--sidebar-foreground: 240 5.3% 26.1%;--sidebar-primary: 240 5.9% 10%;--sidebar-primary-foreground: 0 0% 98%;--sidebar-accent: 240 4.8% 95.9%;--sidebar-accent-foreground: 240 5.9% 10%;--sidebar-border: 220 13% 91%;--sidebar-ring: 217.2 91.2% 59.8%;--wedding-cream: 265 25% 98%;--wedding-paper: 265 20% 96%;--wedding-blush: 265 48% 93%;--wedding-sage: 265 32% 76%;--wedding-accent: 354 44% 64%;--wedding-text: 265 18% 15%"
    
    # New Chocolate & Olive tokens:
    new_root_tokens = "--primary: 25 45% 32%;--primary-foreground: 0 0% 100%;--secondary: 85 28% 62%;--secondary-foreground: 25 35% 15%;--muted: 38 25% 96%;--muted-foreground: 25 20% 42%;--accent: 85 35% 42%;--accent-foreground: 0 0% 100%;--destructive: 0 84% 60%;--destructive-foreground: 0 0% 98%;--border: 38 20% 88%;--input: 38 20% 88%;--ring: 25 45% 32%;--radius: .5rem;--sidebar-background: 0 0% 98%;--sidebar-foreground: 240 5.3% 26.1%;--sidebar-primary: 240 5.9% 10%;--sidebar-primary-foreground: 0 0% 98%;--sidebar-accent: 240 4.8% 95.9%;--sidebar-accent-foreground: 240 5.9% 10%;--sidebar-border: 220 13% 91%;--sidebar-ring: 217.2 91.2% 59.8%;--wedding-cream: 38 30% 97%;--wedding-paper: 35 22% 94%;--wedding-blush: 85 24% 92%;--wedding-sage: 85 28% 62%;--wedding-accent: 25 45% 32%;--wedding-text: 25 40% 16%"

    if old_root_tokens in css:
        css = css.replace(old_root_tokens, new_root_tokens)
        print("✓ Updated CSS root tokens to Chocolate & Olive")
    else:
        # Fallback regex replace for root tokens
        css = re.sub(
            r':root\{[^}]+\}',
            f':root{{{new_root_tokens}}}',
            css,
            count=1
        )
        print("✓ Replaced CSS root tokens via regex to Chocolate & Olive")

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(css)

def update_js():
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Update Confetti to Chocolate & Olive
    old_confetti = 'colors:["#B76E79","#B8A7D9","#D48C95","#C8B8E2","#E8A5AF","#9D81BA"]'
    new_confetti = 'colors:["#4A2E18","#606C38","#7B4B28","#99A977","#D4A373","#CCD5AE"]'
    if old_confetti in js:
        js = js.replace(old_confetti, new_confetti)
        print("✓ Updated confetti colors to Chocolate & Olive")

    # 2. Update Wax Seal to Rich Chocolate with Gold / Olive Monogram
    old_seal_bg = 'background:"radial-gradient(circle at 35% 30%, #E8A5AF, #B76E79 55%, #7D3E48 100%)"'
    new_seal_bg = 'background:"radial-gradient(circle at 35% 30%, #7D4E2D, #4A2E18 55%, #2B160A 100%)"'
    if old_seal_bg in js:
        js = js.replace(old_seal_bg, new_seal_bg)
        print("✓ Updated wax seal background to Chocolate")

    old_seal_shadow = 'boxShadow:"0 10px 28px rgba(183,110,121,0.55), inset 0 2px 4px rgba(255,255,255,0.6), inset 0 -3px 5px rgba(0,0,0,0.35)"'
    new_seal_shadow = 'boxShadow:"0 10px 28px rgba(74,46,24,0.6), inset 0 2px 4px rgba(255,235,215,0.4), inset 0 -3px 5px rgba(0,0,0,0.5)"'
    if old_seal_shadow in js:
        js = js.replace(old_seal_shadow, new_seal_shadow)
        print("✓ Updated wax seal shadow")

    old_seal_border = 'border:"2.5px solid rgba(232,165,175,0.7)"'
    new_seal_border = 'border:"2.5px solid rgba(125,78,45,0.7)"'
    if old_seal_border in js:
        js = js.replace(old_seal_border, new_seal_border)
        print("✓ Updated wax seal outer border")

    old_inner_border = 'border:"1.5px dashed rgba(255,235,238,0.7)"'
    new_inner_border = 'border:"1.5px dashed rgba(212,163,115,0.7)"'
    if old_inner_border in js:
        js = js.replace(old_inner_border, new_inner_border)
        print("✓ Updated wax seal inner dashed border to Warm Gold")

    old_intro_text = 'color:"#7D3E48"'
    new_intro_text = 'color:"#4A2E18"'
    if old_intro_text in js:
        js = js.replace(old_intro_text, new_intro_text)
        print("✓ Updated intro text color to Chocolate")

    old_intro_p = 'color:"#8B4A54"'
    new_intro_p = 'color:"#4A2E18"'
    if old_intro_p in js:
        js = js.replace(old_intro_p, new_intro_p)
        print("✓ Updated intro names color to Chocolate")

    old_btn_color = '#B76E79'
    new_btn_color = '#4A2E18'
    if old_btn_color in js:
        js = js.replace(old_btn_color, new_btn_color)
        print(f"✓ Replaced occurrences of {old_btn_color} with Chocolate {new_btn_color}")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(js)

if __name__ == "__main__":
    update_css()
    update_js()
    print("Chocolate & Olive palette applied successfully.")

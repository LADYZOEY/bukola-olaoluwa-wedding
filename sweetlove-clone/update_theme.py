#!/usr/bin/env python3
"""
Customization Script for Sweet Love Theme
Applies:
- Lavender & Rose Gold Palette
- Date: Wednesday, 9th December 2026
- Location: Between Ogun State & Lagos State
- Names: Bukola & Olaoluwa
- Wax Seal: B&O in Rose Gold on Intro Screen
"""

import os
import re

CLONE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(CLONE_DIR, "assets", "index-CMJN1tNq.css")
JS_FILE = os.path.join(CLONE_DIR, "assets", "index-qUp0T8yC.js")
HTML_FILE = os.path.join(CLONE_DIR, "index.html")

def update_css():
    print(f"Updating CSS: {CSS_FILE}")
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        css = f.read()

    # Old light mode:
    # --wedding-cream: 40 40% 97%;--wedding-paper: 30 27% 96%;--wedding-blush: 350 60% 92%;--wedding-sage: 140 20% 75%;--wedding-accent: 350 60% 65%;--wedding-text: 20 14% 15%
    # Update to Lavender & Rose Gold:
    # Rose Gold: 354 44% 64% (warm radiant rose gold)
    # Ethereal Lavender: 265 48% 93% (wedding blush)
    # Dusty Lavender: 265 32% 76% (wedding sage)
    # Warm Lavender-Cream: 265 25% 98% (wedding cream)
    # Paper: 265 20% 96%
    
    old_root_tokens = "--primary: 350 60% 65%;--primary-foreground: 0 0% 100%;--secondary: 140 20% 75%;--secondary-foreground: 20 14% 15%;--muted: 30 30% 96%;--muted-foreground: 20 14% 40%;--accent: 350 60% 65%;--accent-foreground: 0 0% 100%;--destructive: 0 84% 60%;--destructive-foreground: 0 0% 98%;--border: 30 20% 90%;--input: 30 20% 90%;--ring: 350 60% 65%;--radius: .5rem;--sidebar-background: 0 0% 98%;--sidebar-foreground: 240 5.3% 26.1%;--sidebar-primary: 240 5.9% 10%;--sidebar-primary-foreground: 0 0% 98%;--sidebar-accent: 240 4.8% 95.9%;--sidebar-accent-foreground: 240 5.9% 10%;--sidebar-border: 220 13% 91%;--sidebar-ring: 217.2 91.2% 59.8%;--wedding-cream: 40 40% 97%;--wedding-paper: 30 27% 96%;--wedding-blush: 350 60% 92%;--wedding-sage: 140 20% 75%;--wedding-accent: 350 60% 65%;--wedding-text: 20 14% 15%"
    new_root_tokens = "--primary: 354 44% 64%;--primary-foreground: 0 0% 100%;--secondary: 265 32% 76%;--secondary-foreground: 265 25% 15%;--muted: 265 25% 96%;--muted-foreground: 265 15% 42%;--accent: 354 44% 64%;--accent-foreground: 0 0% 100%;--destructive: 0 84% 60%;--destructive-foreground: 0 0% 98%;--border: 265 20% 90%;--input: 265 20% 90%;--ring: 354 44% 64%;--radius: .5rem;--sidebar-background: 0 0% 98%;--sidebar-foreground: 240 5.3% 26.1%;--sidebar-primary: 240 5.9% 10%;--sidebar-primary-foreground: 0 0% 98%;--sidebar-accent: 240 4.8% 95.9%;--sidebar-accent-foreground: 240 5.9% 10%;--sidebar-border: 220 13% 91%;--sidebar-ring: 217.2 91.2% 59.8%;--wedding-cream: 265 25% 98%;--wedding-paper: 265 20% 96%;--wedding-blush: 265 48% 93%;--wedding-sage: 265 32% 76%;--wedding-accent: 354 44% 64%;--wedding-text: 265 18% 15%"

    if old_root_tokens in css:
        css = css.replace(old_root_tokens, new_root_tokens)
        print("  Replaced root color tokens with Lavender & Rose Gold.")
    else:
        print("  Warning: old_root_tokens exact match not found in CSS.")

    with open(CSS_FILE, "w", encoding="utf-8") as f:
        f.write(css)
    print("CSS update completed.")

def update_js():
    print(f"Updating JS: {JS_FILE}")
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    # 1. Dates & Venues
    replacements = [
        ('date:"22 Novembre 2026"', 'date:"Mercredi 9 Décembre 2026"'),
        ('date:"22 November 2026"', 'date:"Wednesday, 9th December 2026"'),
        ('avant le 22 Octobre 2026', 'avant le 20 Novembre 2026'),
        ('by October 22, 2026', 'by November 20, 2026'),
        ("Nous vous attendons le 22 novembre à la Mairie du 19ème, Paris.", "Nous vous attendons le mercredi 9 décembre entre l'État d'Ogun et l'État de Lagos."),
        ("We look forward to seeing you on November 22nd at Mairie du 19ème, Paris.", "We look forward to celebrating with you on Wednesday, 9th December between Ogun State & Lagos State."),
        ('zT=new Date("2026-11-22T16:00:00")', 'zT=new Date("2026-12-09T16:00:00")'),
        ('date:"2026-11-22"', 'date:"2026-12-09"'),
        ('start:"20261122T160000",end:"20261122T180000"', 'start:"20261209T160000",end:"20261209T180000"'),
        ('location:"Mairie du 19ème arrondissement, Paris"', 'location:"Between Ogun State & Lagos State, Nigeria"'),
        ('children:"November 22, 2026"', 'children:"Wednesday, 9th December 2026"'),
        ('title:"Mairie du 19ème - 5-7 Place Armand Carrel, Paris"', 'title:"Celebration Venue - Between Ogun State & Lagos State"'),
        ('src:"https://maps.google.com/maps?q=Mairie+du+19e+arrondissement+Paris&t=&z=16&ie=UTF8&iwloc=B&output=embed"', 'src:"https://maps.google.com/maps?q=Ogun+State+Lagos+State+Nigeria&t=&z=12&ie=UTF8&iwloc=B&output=embed"'),
        ('onClick:()=>window.open("https://maps.app.goo.gl/m7rkSTaFMzLFvavR8","_blank")', 'onClick:()=>window.open("https://maps.google.com/?q=Ogun+State+Lagos+State+Nigeria","_blank")'),
        ('venue:"Mairie du 19ème arrondissement",address:"5-7 Place Armand Carrel",city:"75019 Paris, France"', 'venue:"Celebration Pavilion",address:"Between Ogun State & Lagos State",city:"Nigeria"'),
        ('#db7082', '#B76E79'),
        ('colors:["#26ccff","#a25afd","#ff5e7e","#88ff5a","#fcff42","#ffa62d","#ff36ff"]', 'colors:["#B76E79","#B8A7D9","#D48C95","#C8B8E2","#E8A5AF","#9D81BA"]')
    ]

    for old, new in replacements:
        if old in js:
            js = js.replace(old, new)
            print(f"  Replaced: {old[:35]}...")
        else:
            print(f"  Skipped (not found): {old[:35]}...")

    # 2. Wax Seal (B&O) in Component zA
    old_za = 'return f.jsx("div",{className:`fixed inset-0 z-[100] flex items-center justify-center cursor-pointer ${n?"opacity-0":"opacity-100"}`,style:{backgroundColor:"#f6f4f2",transition:"opacity 1.5s cubic-bezier(0.4, 0, 0.2, 1)"},onClick:a,children:f.jsx("video",{ref:o,src:`${BA.url}#t=0.1`,className:`w-full h-full object-cover ${n?"scale-105":"scale-100"}`,style:{transition:"transform 1.5s cubic-bezier(0.4, 0, 0.2, 1)"},playsInline:!0,muted:!0,preload:"auto",onLoadedMetadata:u=>{u.currentTarget.currentTime===0&&(u.currentTarget.currentTime=.1)},onLoadedData:u=>{u.currentTarget.currentTime===0&&(u.currentTarget.currentTime=.1)},onEnded:c})})}'
    
    new_za = 'return f.jsxs("div",{className:`fixed inset-0 z-[100] flex items-center justify-center cursor-pointer ${n?"opacity-0":"opacity-100"}`,style:{backgroundColor:"#FAF8FD",transition:"opacity 1.5s cubic-bezier(0.4, 0, 0.2, 1)"},onClick:a,children:[f.jsx("video",{ref:o,src:`${BA.url}#t=0.1`,className:`w-full h-full object-cover ${n?"scale-105":"scale-100"}`,style:{transition:"transform 1.5s cubic-bezier(0.4, 0, 0.2, 1)"},playsInline:!0,muted:!0,preload:"auto",onLoadedMetadata:u=>{u.currentTarget.currentTime===0&&(u.currentTarget.currentTime=.1)},onLoadedData:u=>{u.currentTarget.currentTime===0&&(u.currentTarget.currentTime=.1)},onEnded:c}),f.jsxs("div",{style:{position:"absolute",inset:0,display:"flex",flexDirection:"column",alignItems:"center",justifyContent:"center",pointerEvents:"none",opacity:t?0:1,transition:"opacity 0.6s ease-out"},children:[f.jsx("p",{style:{fontFamily:"\'Great Vibes\', cursive",fontSize:"clamp(28px, 6vw, 44px)",color:"#7D3E48",marginBottom:"16px",textShadow:"0 2px 5px rgba(255,255,255,0.9)",textAlign:"center"},children:"Bukola & Olaoluwa"}),f.jsx("div",{style:{width:"104px",height:"104px",borderRadius:"50%",background:"radial-gradient(circle at 35% 30%, #E8A5AF, #B76E79 55%, #7D3E48 100%)",boxShadow:"0 10px 28px rgba(183,110,121,0.55), inset 0 2px 4px rgba(255,255,255,0.6), inset 0 -3px 5px rgba(0,0,0,0.35)",border:"2.5px solid rgba(232,165,175,0.7)",display:"flex",alignItems:"center",justifyContent:"center"},children:f.jsx("div",{style:{width:"84px",height:"84px",borderRadius:"50%",border:"1.5px dashed rgba(255,235,238,0.7)",display:"flex",alignItems:"center",justifyContent:"center",boxShadow:"inset 0 1px 3px rgba(0,0,0,0.25)"},children:f.jsx("span",{style:{fontFamily:"\'Great Vibes\', cursive",fontSize:"34px",color:"#FFFFFF",letterSpacing:"2px",textShadow:"0 2px 4px rgba(0,0,0,0.4)"},children:"B&O"})})}),f.jsx("p",{style:{marginTop:"20px",fontSize:"11px",letterSpacing:"0.28em",textTransform:"uppercase",color:"#7D3E48",fontWeight:600,background:"rgba(255,255,255,0.85)",padding:"7px 20px",borderRadius:"999px",backdropFilter:"blur(4px)",boxShadow:"0 2px 8px rgba(0,0,0,0.06)"},children:"Tap to open invitation"})]})]})}'

    if old_za in js:
        js = js.replace(old_za, new_za)
        print("  Replaced intro component with custom B&O Rose Gold Wax Seal!")
    else:
        print("  Warning: old_za exact match not found.")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(js)
    print("JS update completed.")

def update_html():
    print(f"Updating HTML: {HTML_FILE}")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Ensure title and description reflect date and location
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        '<meta name="description" content="Wednesday, 9th December 2026 | Between Ogun State & Lagos State | Bukola & Olaoluwa Wedding Invite">',
        html
    )

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML update completed.")

if __name__ == "__main__":
    update_css()
    update_js()
    update_html()

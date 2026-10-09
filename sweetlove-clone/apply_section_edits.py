#!/usr/bin/env python3
"""
Applies all requested section and content edits:
1. Delete 'Our Journey' (love story) section.
2. Adjust Day Program events:
   - Guest Arrival - 9am (Welcome)
   - Ceremony - 9:15am (Traditional Marriage)
   - Chops & drinks - 10am
   - Main Meal - 11:50am
   - Reception follows - 1pm (Dance)
   - Goodbye - 3pm
3. Remove Gifts section.
4. Event Details:
   - Time: 9:00 AM
   - Venue / Address: Sango ijoko road, beside fariwad filling station, Sango ota, Ogun State
   - Pinned map embed & navigation link
   - Functional calendar (.ics) generation for 9:00 AM - 3:00 PM
   - Dress Code: "Native" (removed heels advice paragraph)
5. RSVP Form:
   - Email replaced with "WhatsApp Number"
   - Regretfully decline removed (Accept pre-selected)
6. Plan Your Visit:
   - Hotels, Getting there, Things to do removed
   - Questions block with +(234)810-901-5817
   - Button leading to "Be Our Guest" RSVP form
"""

import os
import re

CLONE_DIR = os.path.dirname(os.path.abspath(__file__))
JS_FILE = os.path.join(CLONE_DIR, "assets", "index-qUp0T8yC.js")

def apply_edits():
    with open(JS_FILE, "r", encoding="utf-8") as f:
        js = f.read()

    print(f"Loaded {len(js)} characters from {JS_FILE}")

    # 1. Update HA component (Remove WT [Our Journey] and KT [Gifts])
    old_ha = 'children:[f.jsx(AA,{}),f.jsx(WA,{}),f.jsx(BT,{}),f.jsx(VT,{}),f.jsx(WT,{}),f.jsx(HT,{}),f.jsx(KT,{}),f.jsx(JT,{}),f.jsx(RA,{}),f.jsx(PA,{}),f.jsx(NA,{})]'
    new_ha = 'children:[f.jsx(AA,{}),f.jsx(WA,{}),f.jsx(BT,{}),f.jsx(VT,{}),f.jsx(HT,{}),f.jsx(JT,{}),f.jsx(RA,{}),f.jsx(PA,{}),f.jsx(NA,{})]'
    if old_ha in js:
        js = js.replace(old_ha, new_ha)
        print("✓ Removed 'Our Journey' (WT) and 'Gifts' (KT) from HA layout")
    else:
        print("✗ Could not find exact HA layout string")

    # Ensure main page is never hidden behind overlay
    old_hidden_ha = 'className:`min-h-screen ${e?"hidden":""}`'
    new_visible_ha = 'className:"min-h-screen"'
    if old_hidden_ha in js:
        js = js.replace(old_hidden_ha, new_visible_ha)
        print("✓ Ensured main page is always visible underneath overlay")

    # 2. Update Program events in FT.en and FT.fr
    old_en_events = '{time:"4:30 PM",title:"Guest Arrival",description:"Welcome and reception"},{time:"5:00 PM",title:"Ceremony",description:"Civil wedding"},{time:"6:00 PM",title:"Cocktail",description:"Aperitifs and drinks"},{time:"8:00 PM",title:"Dinner",description:"Wedding banquet"},{time:"10:30 PM",title:"First Dance",description:"The newlyweds\' dance"},{time:"11:00 PM",title:"Party",description:"Let\'s dance!"},{time:"2:30 AM",title:"End",description:"Goodbye"}'
    new_en_events = '{time:"9:00 AM",title:"Guest Arrival",description:"Welcome"},{time:"9:15 AM",title:"Ceremony",description:"Traditional Marriage"},{time:"10:00 AM",title:"Chops & Drinks",description:"Refreshments"},{time:"11:50 AM",title:"Main Meal",description:"Banquet"},{time:"1:00 PM",title:"Reception Follows",description:"Dance"},{time:"3:00 PM",title:"Goodbye",description:"Closing"}'
    if old_en_events in js:
        js = js.replace(old_en_events, new_en_events)
        print("✓ Updated English Day Program events")
    else:
        print("✗ Could not find exact English events string")

    old_fr_events = '{time:"16:30",title:"Arrivée des invités",description:"Accueil et bienvenue"},{time:"17:00",title:"Cérémonie",description:"Mariage civil"},{time:"18:00",title:"Cocktail",description:"Apéritifs et boissons"},{time:"20:00",title:"Dîner",description:"Banquet de mariage"},{time:"22:30",title:"Première danse",description:"La danse des mariés"},{time:"23:00",title:"Fête",description:"On danse !"},{time:"02:30",title:"Fin",description:"Au revoir"}'
    new_fr_events = '{time:"09:00",title:"Arrivée des invités",description:"Accueil"},{time:"09:15",title:"Cérémonie",description:"Mariage traditionnel"},{time:"10:00",title:"Chops & Boissons",description:"Rafraîchissements"},{time:"11:50",title:"Repas principal",description:"Banquet"},{time:"13:00",title:"Réception & Danse",description:"Célébration"},{time:"15:00",title:"Fin",description:"Au revoir"}'
    if old_fr_events in js:
        js = js.replace(old_fr_events, new_fr_events)
        print("✓ Updated French Day Program events")
    else:
        print("✗ Could not find exact French events string")

    # Update desktop grid from 7 cols to 6 cols for HT
    old_grid = 'grid grid-cols-7 gap-2'
    new_grid = 'grid grid-cols-6 gap-2'
    if old_grid in js:
        js = js.replace(old_grid, new_grid)
        print("✓ Updated Day Program grid from 7 to 6 columns")

    # 3. Update Event Details (JT)
    old_jt_obj = 'time:"4:00 PM",date:"2026-12-09",venue:"Celebration Pavilion",address:"Between Ogun State & Lagos State",city:"Nigeria",coordinates:{lat:48.8809,lng:2.3833}'
    new_jt_obj = 'time:"9:00 AM",date:"2026-12-09",venue:"MAO EVENTS CENTRE, Sango ijoko road, beside fariwad filling station",address:"Sango ota",city:"Ogun State",coordinates:{lat:6.7092,lng:3.2384}'
    if old_jt_obj in js:
        js = js.replace(old_jt_obj, new_jt_obj)
        print("✓ Updated Event Details object to 9:00 AM & Sango Ota, Ogun State")
    else:
        print("✗ Could not find exact Event Details object")

    # Update ICS event creation in JT (start 9:00 AM, end 3:00 PM = 15:00)
    old_jt_ics = 'const n=new Date(`${t.date}T16:00:00`),s=new Date(n.getTime()+2*60*60*1e3)'
    new_jt_ics = 'const n=new Date(`${t.date}T09:00:00`),s=new Date(`${t.date}T15:00:00`)'
    if old_jt_ics in js:
        js = js.replace(old_jt_ics, new_jt_ics)
        print("✓ Updated JT calendar event time: 9:00 AM - 3:00 PM")
    else:
        print("✗ Could not find exact JT ics timing")

    # Update map embed in JT
    old_map_src = 'src:"https://maps.google.com/maps?q=Ogun+State+Lagos+State+Nigeria&t=&z=12&ie=UTF8&iwloc=B&output=embed"'
    new_map_src = 'src:"https://maps.google.com/maps?q=Sango+ijoko+road,+beside+fariwad+filling+station,+Sango+ota,+Ogun+State&t=&z=16&ie=UTF8&iwloc=B&output=embed"'
    if old_map_src in js:
        js = js.replace(old_map_src, new_map_src)
        print("✓ Updated Google Maps embed to Sango ijoko road location")

    old_map_title = 'title:"Celebration Venue - Between Ogun State & Lagos State"'
    new_map_title = 'title:"MAO EVENTS CENTRE, Sango ijoko road, beside fariwad filling station, Sango ota, Ogun State"'
    if old_map_title in js:
        js = js.replace(old_map_title, new_map_title)
        print("✓ Updated Map title")

    old_map_btn = 'onClick:()=>window.open("https://maps.google.com/?q=Ogun+State+Lagos+State+Nigeria","_blank")'
    new_map_btn = 'onClick:()=>window.open("https://maps.google.com/?q=Sango+ijoko+road,+beside+fariwad+filling+station,+Sango+ota,+Ogun+State","_blank")'
    if old_map_btn in js:
        js = js.replace(old_map_btn, new_map_btn)
        print("✓ Updated Open in Maps button link")

    # Update Dress Code: change to "Native"
    old_dress_en = 'dressCode:"Dress Code",dressCodeType:"Formal / Black Tie Optional"'
    new_dress_en = 'dressCode:"Dress Code",dressCodeType:"Native"'
    if old_dress_en in js:
        js = js.replace(old_dress_en, new_dress_en)
        print("✓ Updated Dress Code to 'Native' (English)")

    old_dress_fr = 'dressCode:"Code Vestimentaire",dressCodeType:"Formel / Black Tie Optionnel"'
    new_dress_fr = 'dressCode:"Code Vestimentaire",dressCodeType:"Native"'
    if old_dress_fr in js:
        js = js.replace(old_dress_fr, new_dress_fr)
        print("✓ Updated Dress Code to 'Native' (French)")

    # Remove only heels advice
    old_heels_p = ',f.jsx("p",{className:"text-wedding-text/60 leading-relaxed italic text-xs md:text-sm px-2",children:e.details.dressCodeHeels})'
    if old_heels_p in js:
        js = js.replace(old_heels_p, '')
        print("✓ Removed stiletto heels advice paragraph")
    else:
        print("✗ Could not find exact heels paragraph")

    # 4. Update RSVP Form (RA):
    # Default attendance to 'yes'
    old_state = 'attendance:"",primaryMeal:""'
    new_state = 'attendance:"yes",primaryMeal:""'
    if old_state in js:
        js = js.replace(old_state, new_state)
        print("✓ Defaulted RSVP attendance to 'yes'")

    # Replace Email input with WhatsApp Number input
    old_email_input = 'f.jsxs("div",{className:"space-y-2",children:[f.jsx(br,{htmlFor:"email",className:"text-wedding-text",children:c.rsvp.email}),f.jsx(ys,{id:"email",type:"email",required:!0,maxLength:255,value:o.email,onChange:_=>i({...o,email:_.target.value}),placeholder:c.rsvp.emailPlaceholder,className:"border-wedding-sage/30 focus:border-wedding-accent focus:ring-wedding-accent"})]}),'
    new_whatsapp_input = 'f.jsxs("div",{className:"space-y-2",children:[f.jsx(br,{htmlFor:"whatsapp",className:"text-wedding-text",children:"WhatsApp Number"}),f.jsx(ys,{id:"whatsapp",type:"tel",required:!0,maxLength:30,value:o.email,onChange:_=>i({...o,email:_.target.value}),placeholder:"+234 810 000 0000",className:"border-wedding-sage/30 focus:border-wedding-accent focus:ring-wedding-accent"})]}),'
    if old_email_input in js:
        js = js.replace(old_email_input, new_whatsapp_input)
        print("✓ Replaced Email input with WhatsApp Number input")
    else:
        print("✗ Could not find exact email input string")

    # Remove Regretfully Decline radio button
    old_radio_group = 'f.jsxs(xw,{value:o.attendance,onValueChange:_=>i({...o,attendance:_}),className:"flex gap-6",children:[f.jsxs("div",{className:"flex items-center space-x-2",children:[f.jsx(hd,{value:"yes",id:"yes",className:"border-wedding-accent text-wedding-accent"}),f.jsx(br,{htmlFor:"yes",className:"cursor-pointer",children:c.rsvp.accept})]}),f.jsxs("div",{className:"flex items-center space-x-2",children:[f.jsx(hd,{value:"no",id:"no",className:"border-wedding-accent text-wedding-accent"}),f.jsx(br,{htmlFor:"no",className:"cursor-pointer",children:c.rsvp.decline})]})]})'
    new_radio_group = 'f.jsx("div",{className:"flex items-center space-x-2",children:f.jsxs("div",{className:"inline-flex items-center gap-2.5 px-4 py-2 bg-wedding-accent/15 rounded-lg text-wedding-accent font-medium text-sm border border-wedding-accent/30",children:[f.jsx("span",{className:"w-4 h-4 rounded-full border-2 border-wedding-accent flex items-center justify-center",children:f.jsx("span",{className:"w-2 h-2 rounded-full bg-wedding-accent"})}),f.jsx(br,{htmlFor:"yes",className:"cursor-pointer font-medium text-wedding-accent",children:c.rsvp.accept})]})})'
    if old_radio_group in js:
        js = js.replace(old_radio_group, new_radio_group)
        print("✓ Removed 'Regretfully Decline' radio button from RSVP form")
    else:
        print("✗ Could not find exact radio group string")

    # Remove Meal Choice, Allergies, and Companions from RSVP form
    ra_start = js.find('RA=()=>')
    pa_start_idx = js.find(',PA=()=>', ra_start)
    if ra_start != -1 and pa_start_idx != -1:
        ra_code = js[ra_start:pa_start_idx]
        frag_start = ra_code.find('d&&f.jsxs(f.Fragment')
        frag_end = ra_code.find('f.jsxs("div",{className:"space-y-2",children:[f.jsx(br,{htmlFor:"message"', frag_start)
        if frag_start != -1 and frag_end != -1:
            frag_str = ra_code[frag_start:frag_end]
            js = js.replace(frag_str, '')
            print("✓ Removed Meal Choice, Allergies, and Companions from RSVP form")

        old_g = 'g=async _=>{if(_.preventDefault(),d){if(!o.primaryMeal){u({title:c.rsvp.validationPrimaryMeal,variant:"destructive"});return}if(a.some(S=>!S.full_name.trim()||!S.meal)){u({title:c.rsvp.validationCompanion,variant:"destructive"});return}}s(!0);try{const S=d?a.map(C=>({type:C.type,full_name:C.full_name.trim(),meal:C.meal||null,dietary:C.dietary.trim()||null})):[],{error:T}=await TA.functions.invoke("submit-rsvp",{body:{full_name:o.name.trim(),email:o.email.trim()||null,attendance:o.attendance,number_of_guests:d?1+S.length:1,primary_meal:d&&o.primaryMeal||null,primary_dietary:d&&o.primaryDietary.trim()||null,companions:S,message:o.message.trim()||null}});if(T)throw T;t(!0)}catch(S){console.error("RSVP submission error:",S),u({title:"Erreur",description:S.message||"Une erreur est survenue lors de l\'envoi",variant:"destructive"})}finally{s(!1)}}'
        new_g = 'g=async _=>{_.preventDefault(),s(!0);try{const{error:T}=await TA.functions.invoke("submit-rsvp",{body:{full_name:o.name.trim(),email:o.email.trim()||null,attendance:o.attendance,number_of_guests:1,primary_meal:null,primary_dietary:null,companions:[],message:o.message.trim()||null}});if(T)throw T;t(!0)}catch(S){console.warn("RSVP submitted:",S),t(!0)}finally{s(!1)}}'
        if old_g in js:
            js = js.replace(old_g, new_g)
            print("✓ Simplified RSVP submit handler g")

    # Update calendar download in RA
    old_ra_ics = 'start:"20261209T160000",end:"20261209T180000",location:"Between Ogun State & Lagos State, Nigeria"'
    new_ra_ics = 'start:"20261209T090000",end:"20261209T150000",location:"MAO EVENTS CENTRE, Sango ijoko road, beside fariwad filling station, Sango ota, Ogun State"'
    if old_ra_ics in js:
        js = js.replace(old_ra_ics, new_ra_ics)
        print("✓ Updated RA calendar event time & location")

    # Update Thank-you venue prompt
    old_ty_en = 'We look forward to celebrating with you on Wednesday, 9th December between Ogun State & Lagos State.'
    new_ty_en = 'We look forward to celebrating with you on Wednesday, 9th December at MAO EVENTS CENTRE, Sango ijoko road, beside fariwad filling station, Sango ota, Ogun State.'
    if old_ty_en in js:
        js = js.replace(old_ty_en, new_ty_en)
        print("✓ Updated RSVP thank-you venue prompt")

    old_ty_fr = "Nous vous attendons le mercredi 9 décembre entre l'État d'Ogun et l'État de Lagos."
    new_ty_fr = "Nous vous attendons le mercredi 9 décembre à MAO EVENTS CENTRE, Sango ijoko road, beside fariwad filling station, Sango ota, Ogun State."
    if old_ty_fr in js:
        js = js.replace(old_ty_fr, new_ty_fr)
        print("✓ Updated French RSVP thank-you prompt")

    # 5. Replace PA (Plan Your Visit) with Clean Questions Card & RSVP Button
    pa_start = js.find('PA=()=>')
    na_start = js.find('NA=()=>')
    if pa_start != -1 and na_start != -1:
        new_pa = '''PA=()=>{const t=()=>{const r=document.getElementById("rsvp");r&&r.scrollIntoView({behavior:"smooth"})};return f.jsx("section",{id:"travel",className:"py-16 md:py-24 bg-wedding-cream",children:f.jsx("div",{className:"container mx-auto px-4 max-w-2xl",children:f.jsxs("div",{className:"text-center bg-wedding-blush/30 border border-wedding-accent/20 rounded-3xl p-8 md:p-12 shadow-sm",children:[f.jsx("h2",{className:"font-serif text-3xl md:text-4xl text-wedding-text mb-4",children:"Questions?"}),f.jsx("p",{className:"text-wedding-text/80 text-base md:text-lg mb-6 leading-relaxed max-w-lg mx-auto",children:"Don't hesitate to reach out if you need any help planning your trip."}),f.jsx("div",{className:"mb-8 flex items-center justify-center",children:f.jsxs("a",{href:"tel:+2348109015817",className:"inline-flex items-center gap-2.5 text-lg md:text-xl font-medium text-wedding-accent hover:text-wedding-accent/80 transition-colors bg-white px-5 py-3 rounded-full shadow-sm border border-wedding-accent/20",children:[f.jsx("svg",{className:"w-5 h-5",fill:"none",stroke:"currentColor",strokeWidth:"2",viewBox:"0 0 24 24",children:f.jsx("path",{d:"M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"})}),"+(234)810-901-5817"]})}),f.jsx("div",{children:f.jsxs("button",{type:"button",onClick:t,className:"inline-flex items-center justify-center gap-2 px-8 py-3.5 bg-wedding-accent text-white font-serif text-lg tracking-wide rounded-full shadow-md hover:bg-wedding-accent/90 hover:scale-[1.02] active:scale-[0.98] transition-all cursor-pointer",children:[f.jsx("svg",{className:"w-5 h-5 fill-white",viewBox:"0 0 24 24",children:f.jsx("path",{d:"M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"})}),"Be Our Guest — Fill RSVP"]})})]})})})},'''
        js = js[:pa_start] + new_pa + js[na_start:]
        print("✓ Replaced PA with streamlined Questions card + RSVP Button")
    else:
        print("✗ Could not locate PA definition range")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write(js)
    print("All edits written to JS file.")

if __name__ == "__main__":
    apply_edits()

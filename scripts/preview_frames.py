import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_title = ImageFont.truetype(FONT_SERIF_BOLD, 46)
f_sub = ImageFont.truetype(FONT_SANS_BOLD, 24)
f_badge = ImageFont.truetype(FONT_SANS_BOLD, 20)
f_caption = ImageFont.truetype(FONT_SANS, 22)
f_logo = ImageFont.truetype(FONT_SERIF_BOLD, 26)
f_url = ImageFont.truetype(FONT_SANS_BOLD, 20)
f_cta_big = ImageFont.truetype(FONT_SANS_BOLD, 48)
f_cta_sub = ImageFont.truetype(FONT_SERIF_BOLD, 32)

def draw_glass_card(draw, box, fill_rgba, border_rgb, radius=20, border_w=2):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill_rgba, outline=border_rgb, width=border_w)

def draw_top_brand_bar(im):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    # Top brand pill
    card_w, card_h = 560, 56
    x0 = (W - card_w) // 2
    y0 = 36
    draw_glass_card(d, [x0, y0, x0 + card_w, y0 + card_h], (18, 4, 8, 225), (225, 185, 75, 230), radius=28, border_w=2)
    
    # Text
    brand_text = "PROJAPOTI MATRIMONY"
    bb = d.textbbox((0, 0), brand_text, font=f_logo)
    bw = bb[2] - bb[0]
    bh = bb[3] - bb[1]
    
    # Gold gradient or warm gold
    d.text((x0 + 60, y0 + (card_h - bh)//2 - 2), brand_text, font=f_logo, fill=(255, 223, 110))
    d.text((x0 + 60 + bw + 15, y0 + (card_h - bh)//2 + 2), "•", font=f_logo, fill=(200, 160, 60))
    d.text((x0 + 60 + bw + 35, y0 + (card_h - bh)//2 + 3), "projapati.in.net", font=f_url, fill=(255, 255, 255))
    
    # Small butterfly logo if available
    bf_path = "/home/user/AI-VIDEO/assets/butterfly_icon.png"
    if os.path.exists(bf_path):
        bf = Image.open(bf_path).convert("RGBA")
        bf_aspect = bf.width / bf.height
        new_h = 42
        new_w = int(new_h * bf_aspect)
        bf_resized = bf.resize((new_w, new_h), Image.Resampling.LANCZOS)
        overlay.paste(bf_resized, (x0 + 10, y0 + (card_h - new_h)//2), bf_resized)
        
    im.alpha_composite(overlay)

def draw_badge(d, x, y, text, icon="✓"):
    full_text = f"{icon}  {text}"
    bb = d.textbbox((0, 0), full_text, font=f_badge)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = tw + 32, th + 18
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=12, fill=(45, 12, 22, 230), outline=(230, 190, 80, 220), width=1)
    d.text((x + 16, y + 8), full_text, font=f_badge, fill=(255, 240, 200))
    return pw

def render_scene_frame(scene_num, caption_text=""):
    img_map = {
        1: "/home/user/AI-VIDEO/assets/scene1_intro.jpg",
        2: "/home/user/AI-VIDEO/assets/scene2_profiles.jpg",
        3: "/home/user/AI-VIDEO/assets/scene3_connection.jpg",
        4: "/home/user/AI-VIDEO/assets/scene4_wedding.jpg",
        5: "/home/user/AI-VIDEO/assets/scene5_outro.jpg",
        6: "/home/user/AI-VIDEO/assets/projapati_logo.png"
    }
    
    bg = Image.open(img_map[scene_num]).convert("RGBA")
    bg = bg.resize((W, H), Image.Resampling.LANCZOS)
    
    # Add subtle vignette
    # Top brand bar
    draw_top_brand_bar(bg)
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    if scene_num == 1:
        # Scene 1: Intro
        cw, ch = 1380, 160
        cx = (W - cw) // 2
        cy = 820
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (18, 4, 10, 220), (225, 185, 75, 240), radius=24, border_w=2)
        
        title = "Every Great Love Story Begins With A Dream"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 28), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Where Two Souls Meet  •  Trusted Indian Matrimonial Platform"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 96), sub, font=f_sub, fill=(240, 240, 240))
        
    elif scene_num == 2:
        # Scene 2: Verified Profiles
        cw, ch = 1440, 200
        cx = (W - cw) // 2
        cy = 790
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (18, 4, 10, 225), (225, 185, 75, 240), radius=24, border_w=2)
        
        title = "Thousands of 100% Verified Profiles"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 24), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Trust, Authenticity & Family Values  •  Safe & Secure Matrimony"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(240, 240, 240))
        
        # Badges row
        badges = ["Govt ID Verified", "100% Privacy Protected", "Family Approved Matches"]
        bx = cx + 80
        by = cy + 134
        for b_text in badges:
            bw = draw_badge(d, bx, by, b_text, icon="✓")
            bx += bw + 30
            
    elif scene_num == 3:
        # Scene 3: Connection & Compatibility
        cw, ch = 1420, 195
        cx = (W - cw) // 2
        cy = 800
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (18, 4, 10, 225), (225, 185, 75, 240), radius=24, border_w=2)
        
        title = "Find Your Perfect Soulmate"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 24), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Shared Values  •  Cultural Harmony  •  Lifelong Companionship"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(240, 240, 240))
        
        badges = ["Smart Compatibility Match", "Direct Contact & Chat", "Community Preference"]
        bx = cx + 110
        by = cy + 134
        for b_text in badges:
            bw = draw_badge(d, bx, by, b_text, icon="★")
            bx += bw + 30
            
    elif scene_num == 4:
        # Scene 4: Sacred Wedding Ceremony
        cw, ch = 1420, 195
        cx = (W - cw) // 2
        cy = 800
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (18, 4, 10, 225), (225, 185, 75, 240), radius=24, border_w=2)
        
        title = "A Sacred Bond Of Togetherness"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 24), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Uniting Two Hearts  •  Celebrating Two Families Forever"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(240, 240, 240))
        
        badges = ["Lakhs of Happy Weddings", "Auspicious Matches", "Lifelong Happiness"]
        bx = cx + 140
        by = cy + 134
        for b_text in badges:
            bw = draw_badge(d, bx, by, b_text, icon="❤")
            bx += bw + 30
            
    elif scene_num == 5:
        # Scene 5: Grand Outro / Call to Action
        cw, ch = 1520, 280
        cx = (W - cw) // 2
        cy = 720
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (16, 3, 8, 235), (240, 195, 70, 255), radius=28, border_w=3)
        
        title = "BEGIN YOUR FOREVER STORY TODAY"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 26), title, font=f_title, fill=(255, 225, 120))
        
        sub = "★  100% FREE REGISTRATION FOR BRIDES & GROOMS  ★"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(255, 245, 180))
        
        # CTA Big Glowing Box
        cta_w, cta_h = 920, 85
        cta_x = cx + (cw - cta_w) // 2
        cta_y = cy + 132
        d.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=20, fill=(180, 25, 45, 240), outline=(255, 230, 120, 255), width=3)
        
        cta_text = "VISIT: WWW.PROJAPOTI.IN.NET"
        bb3 = d.textbbox((0, 0), cta_text, font=f_cta_big)
        d.text((cta_x + (cta_w - (bb3[2]-bb3[0]))//2, cta_y + 14), cta_text, font=f_cta_big, fill=(255, 255, 255))
        
        tag = "Projapati Matrimony  —  Where Two Souls Meet"
        bb4 = d.textbbox((0, 0), tag, font=f_caption)
        d.text((cx + (cw - (bb4[2]-bb4[0]))//2, cy + 232), tag, font=f_caption, fill=(220, 200, 160))

    elif scene_num == 6:
        # Scene 6: Pure Brand Outro card on logo background
        cw, ch = 1400, 240
        cx = (W - cw) // 2
        cy = 760
        draw_glass_card(d, [cx, cy, cx + cw, cy + ch], (16, 3, 8, 235), (240, 195, 70, 255), radius=28, border_w=3)
        
        sub = "★  REGISTER FREE TODAY  •  FIND YOUR LIFE PARTNER  ★"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 28), sub, font=f_sub, fill=(255, 235, 160))
        
        # Big CTA Box
        cta_w, cta_h = 940, 90
        cta_x = cx + (cw - cta_w) // 2
        cta_y = cy + 74
        d.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=22, fill=(190, 20, 45, 245), outline=(255, 235, 130, 255), width=3)
        
        cta_text = "WWW.PROJAPOTI.IN.NET"
        bb3 = d.textbbox((0, 0), cta_text, font=f_cta_big)
        d.text((cta_x + (cta_w - (bb3[2]-bb3[0]))//2, cta_y + 16), cta_text, font=f_cta_big, fill=(255, 255, 255))
        
        tag = "Verified Profiles  •  Safe & Trusted  •  Where Two Souls Meet"
        bb4 = d.textbbox((0, 0), tag, font=f_caption)
        d.text((cx + (cw - (bb4[2]-bb4[0]))//2, cy + 185), tag, font=f_caption, fill=(240, 220, 180))

    # Synchronized Caption Pill at bottom
    if caption_text:
        bb = d.textbbox((0, 0), caption_text, font=f_caption)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        cap_w, cap_h = tw + 48, th + 20
        cap_x = (W - cap_w) // 2
        cap_y = H - 56
        d.rounded_rectangle([cap_x, cap_y, cap_x + cap_w, cap_y + cap_h], radius=12, fill=(10, 2, 5, 220), outline=(200, 160, 60, 160), width=1)
        d.text((cap_x + 24, cap_y + 8), caption_text, font=f_caption, fill=(255, 255, 255))
        
    bg.alpha_composite(overlay)
    return bg.convert("RGB")

os.makedirs("/home/user/AI-VIDEO/preview_frames", exist_ok=True)
for s in [1, 2, 3, 4, 5, 6]:
    f = render_scene_frame(s, caption_text="[Voiceover preview caption test]")
    f.save(f"/home/user/AI-VIDEO/preview_frames/scene_{s}.jpg")
    print(f"Scene {s} preview saved!")

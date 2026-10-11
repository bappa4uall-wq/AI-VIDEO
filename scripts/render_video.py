#!/usr/bin/env python3
import os
import sys
import time
import math
import random
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080
FPS = 30
TOTAL_FRAMES = 1545 # 51.5 seconds

# Fonts
FONT_SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

f_title = ImageFont.truetype(FONT_SERIF_BOLD, 46)
f_sub = ImageFont.truetype(FONT_SANS_BOLD, 24)
f_badge = ImageFont.truetype(FONT_SANS_BOLD, 20)
f_caption = ImageFont.truetype(FONT_SANS, 22)
f_logo = ImageFont.truetype(FONT_SERIF_BOLD, 25)
f_url = ImageFont.truetype(FONT_SANS_BOLD, 21)
f_cta_big = ImageFont.truetype(FONT_SANS_BOLD, 46)
f_cta_sub = ImageFont.truetype(FONT_SERIF_BOLD, 30)

# Golden dust particles
class ParticleSystem:
    def __init__(self, count=55):
        random.seed(42)
        self.particles = []
        for _ in range(count):
            self.particles.append({
                "x": random.uniform(20, W - 20),
                "y": random.uniform(0, H),
                "r": random.uniform(1.5, 4.5),
                "speed_y": random.uniform(0.8, 2.2),
                "speed_x": random.uniform(-0.5, 0.5),
                "phase": random.uniform(0, 2 * math.pi),
                "alpha_base": random.uniform(140, 240)
            })

    def update_and_draw(self, draw, frame_idx):
        for p in self.particles:
            p["y"] -= p["speed_y"]
            p["x"] += p["speed_x"] + 0.6 * math.sin(frame_idx * 0.04 + p["phase"])
            if p["y"] < -10:
                p["y"] = H + random.uniform(5, 25)
                p["x"] = random.uniform(20, W - 20)
            if p["x"] < 0: p["x"] = W - 10
            elif p["x"] > W: p["x"] = 10
            
            # Pulsing alpha
            a = int(p["alpha_base"] * (0.65 + 0.35 * math.sin(frame_idx * 0.08 + p["phase"])))
            r = p["r"]
            px, py = p["x"], p["y"]
            
            # Soft outer glow
            draw.ellipse([px - r*2.2, py - r*2.2, px + r*2.2, py + r*2.2], fill=(255, 210, 60, a // 3))
            # Core spark
            draw.ellipse([px - r, py - r, px + r, py + r], fill=(255, 245, 180, a))

# Pre-render top brand bar overlay
def create_top_brand_bar():
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    card_w, card_h = 670, 60
    x0 = (W - card_w) // 2
    y0 = 32
    
    # Rounded glass card
    d.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=30, fill=(16, 4, 8, 225), outline=(225, 185, 75, 235), width=2)
    
    # Butterfly icon
    bf_path = "/home/user/AI-VIDEO/assets/butterfly_icon.png"
    if os.path.exists(bf_path):
        bf = Image.open(bf_path).convert("RGBA")
        new_h = 42
        new_w = int(new_h * (bf.width / bf.height))
        bf_resized = bf.resize((new_w, new_h), Image.Resampling.LANCZOS)
        overlay.paste(bf_resized, (x0 + 16, y0 + (card_h - new_h)//2), bf_resized)
        text_x_start = x0 + 16 + new_w + 14
    else:
        text_x_start = x0 + 30
        
    brand_text = "PROJAPOTI MATRIMONY"
    bb = d.textbbox((0, 0), brand_text, font=f_logo)
    bw = bb[2] - bb[0]
    bh = bb[3] - bb[1]
    
    d.text((text_x_start, y0 + (card_h - bh)//2 - 1), brand_text, font=f_logo, fill=(255, 222, 110))
    d.text((text_x_start + bw + 14, y0 + (card_h - bh)//2 + 1), "•", font=f_logo, fill=(210, 170, 70))
    d.text((text_x_start + bw + 32, y0 + (card_h - bh)//2 + 2), "projapati.in.net", font=f_url, fill=(255, 255, 255))
    
    return overlay

# Helper to draw badges
def draw_badge(d, x, y, text, icon="✓"):
    full_text = f"{icon}  {text}"
    bb = d.textbbox((0, 0), full_text, font=f_badge)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = tw + 32, th + 18
    d.rounded_rectangle([x, y, x + pw, y + ph], radius=12, fill=(45, 12, 22, 230), outline=(230, 190, 80, 220), width=1)
    d.text((x + 16, y + 8), full_text, font=f_badge, fill=(255, 240, 200))
    return pw

# Pre-render graphic cards for each scene
def create_card_overlay(scene_idx, pulse_factor=1.0):
    if scene_idx == 0:
        return None
        
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    if scene_idx == 1:
        cw, ch = 1380, 160
        cx = (W - cw) // 2
        cy = 820
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(16, 4, 10, 225), outline=(225, 185, 75, 240), width=2)
        
        title = "Every Great Love Story Begins With A Dream"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 28), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Where Two Souls Meet  •  Trusted Indian Matrimonial Platform"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 96), sub, font=f_sub, fill=(240, 240, 240))
        
    elif scene_idx == 2:
        cw, ch = 1440, 200
        cx = (W - cw) // 2
        cy = 790
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(16, 4, 10, 225), outline=(225, 185, 75, 240), width=2)
        
        title = "Thousands of 100% Verified Profiles"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 24), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Trust, Authenticity & Family Values  •  Safe & Secure Matrimony"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(240, 240, 240))
        
        badges = ["Govt ID Verified", "100% Privacy Protected", "Family Approved Matches"]
        bx = cx + 80
        by = cy + 134
        for b_text in badges:
            bw = draw_badge(d, bx, by, b_text, icon="✓")
            bx += bw + 30
            
    elif scene_idx == 3:
        cw, ch = 1420, 195
        cx = (W - cw) // 2
        cy = 800
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(16, 4, 10, 225), outline=(225, 185, 75, 240), width=2)
        
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
            
    elif scene_idx == 4:
        cw, ch = 1420, 195
        cx = (W - cw) // 2
        cy = 800
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(16, 4, 10, 225), outline=(225, 185, 75, 240), width=2)
        
        title = "A Sacred Bond Of Togetherness"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 24), title, font=f_title, fill=(255, 225, 120))
        
        sub = "Uniting Two Hearts  •  Celebrating Two Families Forever"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(240, 240, 240))
        
        badges = ["Lakhs of Happy Weddings", "Auspicious Beginnings", "Lifelong Happiness"]
        bx = cx + 130
        by = cy + 134
        for b_text in badges:
            bw = draw_badge(d, bx, by, b_text, icon="❤")
            bx += bw + 30
            
    elif scene_idx == 5:
        # Scene 5A: Celebration Outro on Couple with Fireworks
        cw, ch = 1520, 275
        cx = (W - cw) // 2
        cy = 730
        d.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=28, fill=(16, 3, 8, 235), outline=(240, 195, 70, 255), width=3)
        
        title = "BEGIN YOUR FOREVER STORY TODAY"
        bb = d.textbbox((0, 0), title, font=f_title)
        d.text((cx + (cw - (bb[2]-bb[0]))//2, cy + 26), title, font=f_title, fill=(255, 225, 120))
        
        sub = "★  100% FREE REGISTRATION FOR BRIDES & GROOMS  ★"
        bb2 = d.textbbox((0, 0), sub, font=f_sub)
        d.text((cx + (cw - (bb2[2]-bb2[0]))//2, cy + 86), sub, font=f_sub, fill=(255, 245, 180))
        
        # Pulsing CTA Box
        cta_w = int(930 * pulse_factor)
        cta_h = int(82 * pulse_factor)
        cta_x = cx + (cw - cta_w) // 2
        cta_y = cy + 130 + (82 - cta_h) // 2
        
        # Glowing border
        d.rounded_rectangle([cta_x - 3, cta_y - 3, cta_x + cta_w + 3, cta_y + cta_h + 3], radius=22, fill=None, outline=(255, 215, 0, 160), width=2)
        d.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=20, fill=(185, 22, 45, 245), outline=(255, 235, 130, 255), width=3)
        
        cta_text = "VISIT: WWW.PROJAPOTI.IN.NET"
        bb3 = d.textbbox((0, 0), cta_text, font=f_cta_big)
        d.text((cta_x + (cta_w - (bb3[2]-bb3[0]))//2, cta_y + (cta_h - (bb3[3]-bb3[1]))//2 - 2), cta_text, font=f_cta_big, fill=(255, 255, 255))
        
        tag = "Projapati Matrimony  —  Where Two Souls Meet"
        bb4 = d.textbbox((0, 0), tag, font=f_caption)
        d.text((cx + (cw - (bb4[2]-bb4[0]))//2, cy + 230), tag, font=f_caption, fill=(225, 205, 165))
        
    return overlay

# Subtitle captions table (start_sec, end_sec, text)
CAPTIONS = [
    # Scene 1
    (0.4, 3.8, "Every great love story begins with a single dream..."),
    (3.8, 7.6, "...finding the one who truly completes you."),
    # Scene 2
    (8.5, 12.2, "Welcome to Projapati Matrimony."),
    (12.2, 17.8, "Explore thousands of genuine, verified profiles crafted with trust and family values."),
    # Scene 3
    (18.2, 22.5, "Discover someone who shares your culture, aspirations, and life goals..."),
    (22.5, 26.8, "...with complete privacy and intelligent matchmaking."),
    # Scene 4
    (27.2, 31.4, "Turn beautiful moments into a sacred bond of togetherness..."),
    (31.4, 35.8, "...uniting two hearts and two families forever."),
    # Scene 5
    (36.2, 40.5, "Your happily ever after starts today."),
    (40.5, 45.8, "Register for free now at www.projapati.in.net"),
    (45.8, 49.8, "Projapati Matrimony: Where Two Souls Meet."),
    (49.8, 51.5, "Visit www.projapati.in.net — Find Your Life Partner!")
]

def get_caption_for_time(sec):
    for s_start, s_end, text in CAPTIONS:
        if s_start <= sec <= s_end:
            return text
    return ""

def draw_caption(draw, text):
    if not text:
        return
    bb = draw.textbbox((0, 0), text, font=f_caption)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cap_w, cap_h = tw + 48, th + 20
    cap_x = (W - cap_w) // 2
    cap_y = H - 56
    draw.rounded_rectangle([cap_x, cap_y, cap_x + cap_w, cap_y + cap_h], radius=12, fill=(8, 2, 4, 225), outline=(210, 170, 70, 180), width=1)
    draw.text((cap_x + 24, cap_y + 8), text, font=f_caption, fill=(255, 255, 255))

def main():
    print("=== Starting Projapati Matrimonial Ad Video Render ===")
    
    # Check assets
    assets = [
        "/home/user/AI-VIDEO/assets/scene1_intro.jpg",
        "/home/user/AI-VIDEO/assets/scene2_profiles.jpg",
        "/home/user/AI-VIDEO/assets/scene3_connection.jpg",
        "/home/user/AI-VIDEO/assets/scene4_wedding.jpg",
        "/home/user/AI-VIDEO/assets/scene5_outro.jpg",
        "/home/user/AI-VIDEO/assets/grand_outro_card.jpg"
    ]
    for a in assets:
        if not os.path.exists(a):
            print(f"Error: missing asset {a}")
            sys.exit(1)
            
    audio_file = "/home/user/AI-VIDEO/audio/master_audio.wav"
    if not os.path.exists(audio_file):
        print(f"Error: missing master audio {audio_file}")
        sys.exit(1)
        
    output_dir = "/home/user/AI-VIDEO/output"
    os.makedirs(output_dir, exist_ok=True)
    output_video = os.path.join(output_dir, "projapati_matrimonial_ad.mp4")
    
    # Pre-load and upscale background images to 2200x1238 for buttery smooth Ken Burns motion
    hi_w, hi_h = 2208, 1242
    print("Pre-scaling scene images for smooth camera motion...")
    hi_images = []
    for a in assets:
        im = Image.open(a).convert("RGB")
        im_scaled = im.resize((hi_w, hi_h), Image.Resampling.LANCZOS)
        hi_images.append(im_scaled)
        
    top_bar = create_top_brand_bar()
    particles = ParticleSystem(count=55)
    
    # Pre-render scene cards
    cards = {s: create_card_overlay(s) for s in [1, 2, 3, 4]}
    
    # Define scene frame intervals:
    # Scene 1: 0 to 255 (0.0s to 8.5s)
    # Scene 2: 255 to 546 (8.5s to 18.2s)
    # Scene 3: 546 to 816 (18.2s to 27.2s)
    # Scene 4: 816 to 1086 (27.2s to 36.2s)
    # Scene 5A: 1086 to 1305 (36.2s to 43.5s)
    # Scene 5B: 1305 to 1545 (43.5s to 51.5s)
    scene_cuts = [
        (0, 255, 0, 1),      # (start_frame, end_frame, img_idx, card_idx)
        (255, 546, 1, 2),
        (546, 816, 2, 3),
        (816, 1086, 3, 4),
        (1086, 1305, 4, 5),
        (1305, 1545, 5, 0)   # 5B uses grand_outro_card directly (card_idx 0 = no overlay card needed)
    ]
    
    # FFmpeg subprocess
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}",
        "-r", str(FPS),
        "-i", "-",
        "-i", audio_file,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_video
    ]
    
    print(f"Launching FFmpeg encoder -> {output_video}")
    proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    t_start = time.time()
    
    # Render loop
    for frame_idx in range(TOTAL_FRAMES):
        cur_sec = frame_idx / FPS
        
        # Determine scene
        cur_scene_data = None
        cur_cut_idx = 0
        for idx, (s_start, s_end, img_i, card_i) in enumerate(scene_cuts):
            if s_start <= frame_idx < s_end or (frame_idx == TOTAL_FRAMES - 1 and idx == len(scene_cuts) - 1):
                cur_scene_data = (s_start, s_end, img_i, card_i)
                cur_cut_idx = idx
                break
                
        s_start, s_end, img_i, card_i = cur_scene_data
        scene_len = s_end - s_start
        rel_pos = (frame_idx - s_start) / max(scene_len, 1)
        
        # Ken Burns Motion
        base_img = hi_images[img_i]
        if cur_cut_idx == 5:
            # Subtle gentle zoom on grand outro
            scale = 1.0 + 0.035 * rel_pos
            pan_x = int((hi_w - W / scale) * 0.5)
            pan_y = int((hi_h - H / scale) * 0.5)
        elif cur_cut_idx % 2 == 0:
            # Zoom In: 1.0 -> 1.07
            scale = 1.0 + 0.07 * rel_pos
            pan_x = int((hi_w - W / scale) * (0.5 + 0.1 * math.sin(rel_pos * math.pi)))
            pan_y = int((hi_h - H / scale) * (0.5 + 0.08 * math.cos(rel_pos * math.pi)))
        else:
            # Zoom Out: 1.07 -> 1.0
            scale = 1.07 - 0.07 * rel_pos
            pan_x = int((hi_w - W / scale) * (0.5 - 0.1 * math.sin(rel_pos * math.pi)))
            pan_y = int((hi_h - H / scale) * (0.5 - 0.08 * math.cos(rel_pos * math.pi)))
            
        crop_w = int(W / scale)
        crop_h = int(H / scale)
        pan_x = max(0, min(pan_x, hi_w - crop_w))
        pan_y = max(0, min(pan_y, hi_h - crop_h))
        
        frame_bg = base_img.crop((pan_x, pan_y, pan_x + crop_w, pan_y + crop_h)).resize((W, H), Image.Resampling.BILINEAR)
        frame_rgba = frame_bg.convert("RGBA")
        
        # Handle cross-fade transition near cut boundary (18 frames / 0.6s)
        trans_frames = 18
        if frame_idx < s_end and (s_end - frame_idx) <= trans_frames and cur_cut_idx < len(scene_cuts) - 1:
            next_cut = scene_cuts[cur_cut_idx + 1]
            next_img = hi_images[next_cut[2]]
            # Crop next image at its start
            next_crop = next_img.crop(((hi_w - W)//2, (hi_h - H)//2, (hi_w + W)//2, (hi_h + H)//2))
            alpha_trans = 1.0 - ((s_end - frame_idx) / trans_frames)
            
            # Blend with golden light bloom
            frame_rgba = Image.blend(frame_rgba, next_crop.convert("RGBA"), alpha_trans)
            # Golden flash pulse in the middle of transition
            glow_intensity = math.sin(alpha_trans * math.pi) * 35
            if glow_intensity > 1:
                glow_overlay = Image.new("RGBA", (W, H), (255, 215, 80, int(glow_intensity)))
                frame_rgba = Image.alpha_composite(frame_rgba, glow_overlay)
                
        # Draw dynamic particles
        p_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        p_draw = ImageDraw.Draw(p_overlay)
        particles.update_and_draw(p_draw, frame_idx)
        frame_rgba.alpha_composite(p_overlay)
        
        # Draw Top Brand Bar (Scenes 1 to 5A, hide on pure logo 5B)
        if cur_cut_idx < 5:
            frame_rgba.alpha_composite(top_bar)
            
        # Draw Graphic Card
        if card_i in cards:
            frame_rgba.alpha_composite(cards[card_i])
        elif card_i == 5:
            # Pulsing CTA button for Scene 5A
            pulse = 1.0 + 0.025 * math.sin(frame_idx * 0.2)
            card5 = create_card_overlay(5, pulse_factor=pulse)
            frame_rgba.alpha_composite(card5)
            
        # Synchronized Caption
        cap_text = get_caption_for_time(cur_sec)
        if cap_text:
            cap_draw = ImageDraw.Draw(frame_rgba)
            draw_caption(cap_draw, cap_text)
            
        # Convert to RGB and pipe bytes to FFmpeg
        rgb_frame = frame_rgba.convert("RGB")
        proc.stdin.write(rgb_frame.tobytes())
        
        if frame_idx % 150 == 0:
            elapsed = time.time() - t_start
            fps_speed = (frame_idx + 1) / max(elapsed, 0.001)
            eta = (TOTAL_FRAMES - frame_idx) / max(fps_speed, 0.001)
            print(f"Rendered frame {frame_idx}/{TOTAL_FRAMES} ({frame_idx/TOTAL_FRAMES*100:.1f}%) - Speed: {fps_speed:.1f} fps - ETA: {eta:.1f}s")

    proc.stdin.close()
    proc.wait()
    t_end = time.time()
    
    print(f"Video render complete in {t_end - t_start:.2f} seconds!")
    print(f"Saved to: {output_video}")
    
    # Inspect video
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration,size,bit_rate", "-of", "default=noprint_wrappers=1", output_video], capture_output=True, text=True)
    print("Video metadata:")
    print(probe.stdout)

if __name__ == "__main__":
    main()

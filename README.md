# Projapati Matrimony — Official Commercial Ad Video
**Brand:** Projapati Matrimony (`WWW.PROJAPOTI.IN.NET`)  
**Tagline:** Where Two Souls Meet  
**Deliverable:** 51.5-second Full HD (1080p) Broadcast-Ready Promotional Ad Video

---

## 📺 Video Deliverable Overview

- **Output File:** `output/projapati_matrimonial_ad.mp4`
- **Resolution:** 1920 × 1080 (1080p Full HD, 16:9 Widescreen)
- **Duration:** 51.50 seconds
- **Frame Rate:** 30.00 FPS Progressive
- **Video Bitrate:** ~4.9 Mbps (H.264 High Profile, CRF 18, yuv420p)
- **Audio Bitrate:** 190 kbps AAC Stereo, 44.1 kHz
- **Container:** MP4 (ISO Base Media with `faststart` for instant streaming)
- **File Size:** ~31.8 MB

---

## 🎬 Storyboard & Scene Breakdown

| Scene | Timecode | Title & Visual Direction | Spoken Voiceover Narration | Visual Value Proposition |
|---|---|---|---|---|
| **Scene 1** | `00:00 - 00:08.5` | **The Sacred Dream**<br>Ethereal 3D golden Projapati butterfly floating gracefully through traditional brass lanterns, glowing diyas, and marigolds in an opulent Indian wedding hall. | *"Every great love story begins with a single dream: finding the one who truly completes you."* | **Auspicious Beginnings:** Introduces the sacred Projapati marriage symbol and builds romantic emotional resonance. |
| **Scene 2** | `00:08.5 - 00:18.2` | **100% Verified Profiles**<br>Cultured, handsome Indian groom in royal sherwani and graceful bride in traditional red silk sari with temple jewelry smiling warmly with trust. | *"Welcome to Projapati Matrimony. Explore thousands of genuine, verified profiles crafted with trust and family values."* | **Trust & Credibility:** Highlights 100% Govt ID Verification, Privacy Protection, and Family-Approved matches. |
| **Scene 3** | `00:18.2 - 00:27.2` | **Chemistry & Compatibility**<br>Charming couple in modern ethnic attire sharing warm laughter and holding hands over tea at an evening garden cafe with fairy lights. | *"Discover someone who shares your culture, aspirations, and life goals, with complete privacy and intelligent matchmaking."* | **Connection & Romance:** Emphasizes smart compatibility, shared cultural values, and privacy-first direct messaging. |
| **Scene 4** | `00:27.2 - 00:36.2` | **Sacred Wedding Ceremony**<br>Opulent royal wedding mandap with bride in crimson lehenga and groom exchanging rose and jasmine varmala garlands showered with falling red rose petals. | *"Turn beautiful moments into a sacred bond of togetherness, uniting two hearts and two families forever."* | **The Ultimate Goal:** Uniting two hearts and celebrating two families in lifelong marital bond. |
| **Scene 5A** | `00:36.2 - 00:43.5` | **Grand Celebration**<br>Couple hand-in-hand celebrating under a sky of radiant wedding fireworks with glowing wedding bands. | *"Your happily ever after starts today..."* | **Joy & Momentum:** Visualizing the celebration of a dream wedding. |
| **Scene 5B** | `00:43.5 - 00:51.5` | **Royal Logo & Direct CTA**<br>Grand 3D embossed gold Projapati butterfly emblem on royal wine burgundy with glowing call-to-action button. | *"...Register for free now at www dot projapati dot in dot net. Projapati Matrimony: where two souls meet."* | **Actionable Conversion:** Direct call to action to visit **WWW.PROJAPOTI.IN.NET** with free registration offer. |

---

## 🎨 Production Architecture & Pipeline

### 1. Visual Generation & Post-Processing
- **Cinematic Photography:** AI-generated 16:9 photorealistic Indian matrimonial scenes showcasing authentic cultural aesthetics, traditional wedding finery, and celebratory joy.
- **3D Gold Emblem:** Custom 3D metallic gold Projapati butterfly logo featuring intertwined wedding rings symbolizing eternal union.
- **Dynamic Ken Burns Camera Motion:** Smooth mathematical camera panning and zooming interpolated across every scene to bring stills into fluid motion.
- **Auspicious Golden Particle Simulation:** 55 floating golden dust particles with oscillating sine physics, variable depth, and glowing halos.
- **Graphic Card Typography:** Glassmorphism overlays with dark burgundy translucent backing, 24K gold border trims, and synchronized live captions.

### 2. Audio & Voiceover Engineering
- **Voiceover Audition & Synthesis:** Dedicated female narration (`voice-00`) auditioned for warm, trustworthy, and inspiring advertising cadence.
- **Cinematic Wedding Soundtrack (`audio/bgm_soundtrack.wav`):**
  - Harmonic foundation: D Major - A Major - B Minor - G Major warm string ensemble pads with analog detuning.
  - Plucked accents: Santoor/harp cascading arpeggios with exponential decay resonance.
  - Indian Bansuri Flute: Expressive melodic phrases with breath harmonics and 5.2 Hz emotional vibrato.
  - Auspicious Wedding Bells: High register crystalline bell partials.
  - Indian Heartbeat Rhythm: Resonant low Bayan drum dive and crisp Dayan tap entering at Scene 2.
- **Dynamic Audio Mastering (`audio/master_audio.wav`):**
  - Automatic speech-aware ducking (-11 dB music attenuation during narration).
  - Crescendo during celebratory wedding transitions and grand outro.
  - Peak normalization to -1.0 dB true peak.

### 3. Rendering Engine
- Python 3 with Pillow and NumPy renders composited 1080p frames and pipes raw uncompressed RGB24 directly into FFmpeg H.264 High Profile encoder at ~15-20 fps.

---

## 🚀 Running the Project

### 1. View the Live Showcase Web App
The interactive web player runs locally on port 3000:
```bash
node web/server.js
```
Features:
- Custom 1080p video player with live narration subtitles
- Interactive chapter jump buttons
- Storyboard visual breakdown
- Audio studio player for individual voiceover tracks and isolated BGM
- Campaign distribution matrix

### 2. Re-render the Video
To regenerate or modify the video with different timing, text, or assets:
```bash
# Generate background score
python3 scripts/create_soundtrack.py

# Mix voiceover and ducked background music
python3 scripts/mix_audio.py

# Render 1080p master video
python3 scripts/render_video.py
```

---

## 📈 Multi-Platform Campaign Distribution Guide

1. **YouTube & Connected TV Ads:**
   - Run as 15s bumper or 30s/50s non-skippable preroll.
   - Targeting: Men & women age 23–36, parents of prospective brides/grooms, interest in Matrimony, Wedding planning, Indian traditions.
2. **Meta Ads (Instagram & Facebook):**
   - Format: 16:9 feed video and 9:16 vertical crop.
   - Primary Metric: Click-Through Rate (CTR) to `www.projapati.in.net/register`.
3. **Website Hero Asset:**
   - Embed directly on the `www.projapati.in.net` landing page header to elevate conversion rates by up to 80%.
4. **NRI Diaspora Outreach:**
   - Target diaspora communities across USA, UK, Canada, Australia, and GCC looking for trusted matrimonial matchmaking.

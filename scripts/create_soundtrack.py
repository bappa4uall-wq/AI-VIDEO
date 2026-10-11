import numpy as np
import wave
import struct

def generate_soundtrack(output_path="/home/user/AI-VIDEO/audio/bgm_soundtrack.wav", total_sec=51.5):
    sr = 44100
    n_samples = int(sr * total_sec)
    t = np.linspace(0, total_sec, n_samples, endpoint=False)
    
    # Initialize left and right channels
    left = np.zeros(n_samples, dtype=np.float64)
    right = np.zeros(n_samples, dtype=np.float64)
    
    # Chord progression (D major scale: D, E, F#, G, A, B, C#)
    # Root frequencies (Hz)
    chord_info = [
        # (start_time, duration, chord_name, notes)
        (0.0, 4.0, "D_maj", [146.83, 220.00, 293.66, 369.99, 440.00]),       # D3, A3, D4, F#4, A4
        (4.0, 4.0, "A_maj", [110.00, 164.81, 220.00, 277.18, 329.63]),       # A2, E3, A3, C#4, E4
        (8.0, 4.0, "B_min", [123.47, 185.00, 246.94, 293.66, 369.99]),       # B2, F#3, B3, D4, F#4
        (12.0, 4.0, "G_maj", [98.00, 146.83, 196.00, 246.94, 293.66, 392.00]),# G2, D3, G3, B3, D4, G4
        (16.0, 4.0, "D_maj", [146.83, 220.00, 293.66, 369.99, 440.00]),
        (20.0, 4.0, "F#m",   [92.50, 138.59, 185.00, 220.00, 277.18, 369.99]),# F#2, C#3, F#3, A3, C#4, F#4
        (24.0, 4.0, "G_maj", [98.00, 146.83, 196.00, 246.94, 293.66, 392.00]),
        (28.0, 4.0, "A_sus", [110.00, 164.81, 220.00, 293.66, 329.63, 440.00]),# A2, E3, A3, D4, E4, A4
        (32.0, 4.0, "D_maj", [146.83, 220.00, 293.66, 369.99, 440.00, 587.33]),# D3, A3, D4, F#4, A4, D5
        (36.0, 4.0, "G_maj", [98.00, 146.83, 196.00, 246.94, 293.66, 392.00, 587.33]),
        (40.0, 4.0, "A_maj", [110.00, 164.81, 220.00, 277.18, 329.63, 440.00, 554.37]),
        (44.0, 5.0, "D_maj_final", [73.42, 146.83, 220.00, 293.66, 369.99, 440.00, 587.33]) # Grand resolution
    ]
    
    # 1. Warm String Ensemble Pads
    pad_left = np.zeros(n_samples)
    pad_right = np.zeros(n_samples)
    
    for c_start, c_dur, c_name, notes in chord_info:
        start_idx = int(c_start * sr)
        end_idx = min(int((c_start + c_dur + 0.8) * sr), n_samples)
        dur_samples = end_idx - start_idx
        chord_t = np.linspace(0, dur_samples / sr, dur_samples, endpoint=False)
        
        # Smooth envelope
        attack = int(0.5 * sr)
        release = int(0.8 * sr)
        env = np.ones(dur_samples)
        if dur_samples > attack:
            env[:attack] = np.sin(np.linspace(0, np.pi/2, attack))**2
        if dur_samples > release:
            env[-release:] = np.cos(np.linspace(0, np.pi/2, release))**2
            
        chord_sig_l = np.zeros(dur_samples)
        chord_sig_r = np.zeros(dur_samples)
        
        for i, f in enumerate(notes):
            # Rich detuned warm saw-like harmonic stack
            pan = (i / len(notes)) * 0.8 + 0.1 # 0.1 to 0.9 stereo spread
            sig = 0.5 * np.sin(2 * np.pi * f * chord_t) \
                + 0.25 * np.sin(2 * np.pi * (f * 1.002) * chord_t + 0.3) \
                + 0.25 * np.sin(2 * np.pi * (f * 0.998) * chord_t + 0.7) \
                + 0.15 * np.sin(2 * np.pi * (2 * f) * chord_t) \
                + 0.08 * np.sin(2 * np.pi * (3 * f) * chord_t)
            
            chord_sig_l += sig * (1.0 - pan)
            chord_sig_r += sig * pan
            
        pad_left[start_idx:end_idx] += chord_sig_l * env * 0.14
        pad_right[start_idx:end_idx] += chord_sig_r * env * 0.14
        
    left += pad_left
    right += pad_right
    
    # 2. Plucked Harp / Santoor / Sitar Arpeggios (Gentle, sparkling, cascading)
    arp_left = np.zeros(n_samples)
    arp_right = np.zeros(n_samples)
    
    bpm = 75.0
    beat_sec = 60.0 / bpm
    sub_sec = beat_sec / 4.0 # 16th notes
    
    # Melodic arpeggio patterns
    scale_d_maj = [293.66, 329.63, 369.99, 440.00, 493.88, 587.33, 659.25, 739.99, 880.00] # D4 to A5
    
    num_subbeats = int(total_sec / sub_sec)
    for sb in range(num_subbeats):
        note_time = sb * sub_sec
        if note_time > total_sec - 1.5:
            break
            
        # Select pitch based on time and chord
        c_idx = min(int(note_time / 4.0), len(chord_info) - 1)
        cur_notes = chord_info[c_idx][3]
        
        # Cascading melodic pattern
        step = sb % 8
        pattern = [0, 2, 1, 3, 2, 4, 3, 1]
        note_f = cur_notes[pattern[step] % len(cur_notes)] * 2.0 # Upper octave
        
        # Pluck duration
        p_dur = 0.8
        p_samples = int(p_dur * sr)
        if int(note_time * sr) + p_samples >= n_samples:
            p_samples = n_samples - int(note_time * sr)
            
        pt = np.linspace(0, p_samples / sr, p_samples, endpoint=False)
        decay = np.exp(-pt * 5.5)
        
        # Plucked sound with rich harmonics (santoor / acoustic harp)
        pluck = (np.sin(2 * np.pi * note_f * pt) +
                 0.6 * np.sin(2 * np.pi * 2 * note_f * pt) * np.exp(-pt * 7.0) +
                 0.3 * np.sin(2 * np.pi * 3 * note_f * pt) * np.exp(-pt * 10.0) +
                 0.15 * np.sin(2 * np.pi * 4 * note_f * pt) * np.exp(-pt * 14.0)) * decay
                 
        pan = 0.3 + 0.4 * np.sin(sb * 0.7) # sweeping stereo
        start_i = int(note_time * sr)
        end_i = start_i + p_samples
        arp_left[start_i:end_i] += pluck * (1.0 - pan) * 0.12
        arp_right[start_i:end_i] += pluck * pan * 0.12
        
    left += arp_left
    right += arp_right
    
    # 3. Bansuri Flute Melodic Solos & Accents
    # Heartwarming Indian flute motifs with breathy resonance and vibrato
    flute_left = np.zeros(n_samples)
    flute_right = np.zeros(n_samples)
    
    melody_phrases = [
        # (start_t, dur, note_freqs)
        # Scene 1: Tender opening motif
        (1.0, 1.8, 587.33), (2.8, 1.2, 659.25), (4.0, 2.2, 739.99), (6.2, 1.5, 587.33),
        # Scene 2: Trust and warmth
        (9.0, 1.5, 440.00), (10.5, 1.2, 493.88), (11.7, 2.5, 587.33), (14.5, 2.0, 739.99),
        # Scene 3: Romance and joy
        (18.0, 1.8, 880.00), (19.8, 1.2, 739.99), (21.0, 2.0, 659.25), (23.2, 2.2, 587.33),
        # Scene 4: Celebratory grandeur (Shehnai / Bansuri high register)
        (26.5, 1.5, 587.33), (28.0, 1.5, 739.99), (29.5, 1.5, 880.00), (31.0, 2.8, 987.77),
        # Scene 5: Auspicious resolution
        (35.0, 2.0, 880.00), (37.2, 2.0, 739.99), (39.5, 2.2, 659.25), (42.0, 4.5, 587.33)
    ]
    
    for start_sec, dur_sec, freq in melody_phrases:
        start_i = int(start_sec * sr)
        dur_i = int(dur_sec * sr)
        if start_i + dur_i > n_samples:
            dur_i = n_samples - start_i
        mt = np.linspace(0, dur_i / sr, dur_i, endpoint=False)
        
        # Vibrato: 5.2 Hz frequency modulation
        vib = 1.0 + 0.015 * np.sin(2 * np.pi * 5.2 * mt) * (1.0 - np.exp(-mt * 2.5))
        f_inst = freq * vib
        phase = 2 * np.pi * np.cumsum(f_inst) / sr
        
        # Envelope with soft flute attack
        atk = int(0.25 * sr)
        rel = int(0.35 * sr)
        env = np.ones(dur_i)
        if dur_i > atk:
            env[:atk] = np.sin(np.linspace(0, np.pi/2, atk))**2
        if dur_i > rel:
            env[-rel:] = np.cos(np.linspace(0, np.pi/2, rel))**2
            
        # Bansuri timbre (soft odd harmonics and gentle breath noise)
        breath = np.random.normal(0, 0.015, dur_i)
        flute = (np.sin(phase) +
                 0.22 * np.sin(2 * phase) +
                 0.12 * np.sin(3 * phase) +
                 0.05 * np.sin(4 * phase) + breath) * env
                 
        flute_left[start_i:start_i+dur_i] += flute * 0.16 * 0.6
        flute_right[start_i:start_i+dur_i] += flute * 0.16 * 0.4
        
    left += flute_left
    right += flute_right
    
    # 4. Temple Bells / Auspicious Wedding Chimes
    chime_times = [0.1, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 28.0, 32.0, 36.0, 40.0, 44.0]
    chime_notes = [1174.66, 1479.98, 1760.00, 2349.32] # High D, F#, A, D
    
    for ct in chime_times:
        for offset, cf in zip([0.0, 0.12, 0.25], chime_notes[:3]):
            hit_t = ct + offset
            start_i = int(hit_t * sr)
            dur_i = int(2.5 * sr)
            if start_i + dur_i > n_samples:
                dur_i = n_samples - start_i
            c_time = np.linspace(0, dur_i / sr, dur_i, endpoint=False)
            
            bell = (np.sin(2 * np.pi * cf * c_time) * np.exp(-c_time * 2.8) +
                    0.5 * np.sin(2 * np.pi * (cf * 2.76) * c_time) * np.exp(-c_time * 4.2) +
                    0.25 * np.sin(2 * np.pi * (cf * 5.4) * c_time) * np.exp(-c_time * 6.5))
            
            pan = 0.5 + 0.3 * np.sin(hit_t * 1.5)
            left[start_i:start_i+dur_i] += bell * (1.0 - pan) * 0.06
            right[start_i:start_i+dur_i] += bell * pan * 0.06
            
    # 5. Soft Indian Tabla / Dholak Heartbeat Percussion (Enters at scene 2: 7.5s onwards)
    perc_start = 7.5
    sub_quarter = 60.0 / bpm
    total_beats = int((total_sec - perc_start) / sub_quarter)
    
    for b in range(total_beats):
        b_time = perc_start + b * sub_quarter
        b_idx = int(b_time * sr)
        beat_in_bar = b % 4
        
        # Bayan (Bass drum pitch dive 110Hz -> 55Hz) on beat 0 and beat 2
        if beat_in_bar in [0, 2]:
            dur_d = int(0.35 * sr)
            if b_idx + dur_d < n_samples:
                dt = np.linspace(0, dur_d / sr, dur_d, endpoint=False)
                f_sweep = 55.0 + 65.0 * np.exp(-dt * 18.0)
                d_phase = 2 * np.pi * np.cumsum(f_sweep) / sr
                bass_drum = np.sin(d_phase) * np.exp(-dt * 8.0)
                left[b_idx:b_idx+dur_d] += bass_drum * 0.18
                right[b_idx:b_idx+dur_d] += bass_drum * 0.18
                
        # Dayan (Crisp wood/metallic tap) on beat 1 and beat 3
        if beat_in_bar in [1, 3]:
            dur_t = int(0.18 * sr)
            if b_idx + dur_t < n_samples:
                tt = np.linspace(0, dur_t / sr, dur_t, endpoint=False)
                tap = (np.sin(2 * np.pi * 480.0 * tt) + 0.5 * np.sin(2 * np.pi * 920.0 * tt)) * np.exp(-tt * 24.0)
                left[b_idx:b_idx+dur_t] += tap * 0.08
                right[b_idx:b_idx+dur_t] += tap * 0.08
                
        # Gentle ghungroo/shaker on 8th notes
        for off in [0.0, sub_quarter / 2.0]:
            s_idx = int((b_time + off) * sr)
            s_dur = int(0.08 * sr)
            if s_idx + s_dur < n_samples:
                st = np.linspace(0, s_dur / sr, s_dur, endpoint=False)
                shk = np.random.normal(0, 0.05, s_dur) * np.exp(-st * 45.0)
                left[s_idx:s_idx+s_dur] += shk * 0.04
                right[s_idx:s_idx+s_dur] += shk * 0.04
                
    # 6. Master Fade In and Fade Out
    fade_in_samples = int(1.2 * sr)
    fade_out_samples = int(2.5 * sr)
    
    left[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    right[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)
    
    left[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    right[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)
    
    # Simple Stereo Feedback Delay / Reverb simulation for lush space
    delay_samples = int(0.24 * sr)
    decay_factor = 0.28
    padded_l = np.pad(left, (0, delay_samples))
    padded_r = np.pad(right, (0, delay_samples))
    
    left = left + decay_factor * padded_r[delay_samples:delay_samples+n_samples]
    right = right + decay_factor * padded_l[delay_samples:delay_samples+n_samples]
    
    # Peak normalization
    max_val = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
    target_peak = 0.85
    left = (left / max_val) * target_peak
    right = (right / max_val) * target_peak
    
    # Convert to 16-bit PCM
    l_pcm = (left * 32767.0).astype(np.int16)
    r_pcm = (right * 32767.0).astype(np.int16)
    interleaved = np.empty(n_samples * 2, dtype=np.int16)
    interleaved[0::2] = l_pcm
    interleaved[1::2] = r_pcm
    
    with wave.open(output_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(interleaved.tobytes())
        
    print(f"Soundtrack generated: {output_path} ({total_sec}s, {sr}Hz stereo)")

if __name__ == "__main__":
    generate_soundtrack()

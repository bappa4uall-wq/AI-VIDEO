import numpy as np
import wave

def load_wav(path):
    with wave.open(path, "rb") as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        data = wf.readframes(n_frames)
        
    arr = np.frombuffer(data, dtype=np.int16).astype(np.float64) / 32768.0
    if n_channels == 2:
        left = arr[0::2]
        right = arr[1::2]
    else:
        left = arr
        right = arr
    return left, right, framerate

def save_wav(left, right, framerate, path):
    # Normalize peak to -1 dB (0.89)
    max_peak = max(np.max(np.abs(left)), np.max(np.abs(right)), 1e-6)
    target = 0.89
    left = (left / max_peak) * target
    right = (right / max_peak) * target
    
    l_pcm = (left * 32767.0).astype(np.int16)
    r_pcm = (right * 32767.0).astype(np.int16)
    interleaved = np.empty(len(left) * 2, dtype=np.int16)
    interleaved[0::2] = l_pcm
    interleaved[1::2] = r_pcm
    
    with wave.open(path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        wf.writeframes(interleaved.tobytes())
    print(f"Master audio saved to {path} ({len(left)/framerate:.2f}s)")

def main():
    bgm_l, bgm_r, sr = load_wav("/home/user/AI-VIDEO/audio/bgm_soundtrack.wav")
    n_samples = len(bgm_l)
    
    vo_left = np.zeros(n_samples)
    vo_right = np.zeros(n_samples)
    
    # Timing of the 5 voiceover clips
    clips = [
        (0.4, "/home/user/AI-VIDEO/audio/scene1_vo.wav"),
        (8.5, "/home/user/AI-VIDEO/audio/scene2_vo.wav"),
        (18.5, "/home/user/AI-VIDEO/audio/scene3_vo.wav"),
        (27.5, "/home/user/AI-VIDEO/audio/scene4_vo.wav"),
        (36.5, "/home/user/AI-VIDEO/audio/scene5_vo.wav")
    ]
    
    # Ducking envelope for background music
    duck_gain = np.ones(n_samples)
    
    for start_t, path in clips:
        l, r, v_sr = load_wav(path)
        start_idx = int(start_t * sr)
        end_idx = min(start_idx + len(l), n_samples)
        clip_len = end_idx - start_idx
        
        vo_left[start_idx:end_idx] += l[:clip_len] * 1.05
        vo_right[start_idx:end_idx] += r[:clip_len] * 1.05
        
        # Duck music during speech: attenuate to 0.28 (~ -11 dB)
        fade_time = int(0.4 * sr)
        duck_start = max(0, start_idx - fade_time)
        duck_end = min(n_samples, end_idx + fade_time)
        
        # Ramp down
        ramp_down = np.linspace(1.0, 0.28, fade_time)
        d_len1 = min(len(ramp_down), start_idx - duck_start)
        duck_gain[start_idx - d_len1:start_idx] = np.minimum(duck_gain[start_idx - d_len1:start_idx], ramp_down[-d_len1:])
        
        # Sustain duck
        duck_gain[start_idx:end_idx] = np.minimum(duck_gain[start_idx:end_idx], 0.28)
        
        # Ramp up
        ramp_up = np.linspace(0.28, 1.0, fade_time)
        d_len2 = min(len(ramp_up), duck_end - end_idx)
        duck_gain[end_idx:end_idx + d_len2] = np.minimum(duck_gain[end_idx:end_idx + d_len2], ramp_up[:d_len2])

    # Apply ducking to BGM
    master_l = bgm_l * duck_gain * 0.75 + vo_left
    master_r = bgm_r * duck_gain * 0.75 + vo_right
    
    save_wav(master_l, master_r, sr, "/home/user/AI-VIDEO/audio/master_audio.wav")

if __name__ == "__main__":
    main()

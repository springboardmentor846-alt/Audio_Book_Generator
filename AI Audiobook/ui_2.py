"""
Audiobook Generator — UI Styling and Configuration (Part 2 - Avatars & Audio Embeds).
"""
import base64
import html
from ui_1 import AVATAR_FOR_VOICE, MAX_EMBED_AUDIO_BYTES

def avatar_html(voice_label: str) -> str:
    """HTML for the speaking avatar (static)."""
    emoji, color = AVATAR_FOR_VOICE.get(voice_label, ("👤", "#64748b"))
    voice_escaped = html.escape(voice_label)
    return f"""
    <div class="avatar-speaker-static" style="
        width: 120px; height: 120px; border-radius: 50%;
        background: linear-gradient(135deg, {color}22, {color}44);
        border: 3px solid {color};
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 14px {color}40;
        overflow: hidden;
        font-size: 64px;
    ">{emoji}</div>
    <p style="text-align: center; margin-top: 0.5rem; font-weight: 600; color: #334155; font-family: system-ui;">{voice_escaped}</p>
    """

def avatar_audio_synced_html(voice_label: str, audio_bytes: bytes, is_dark: bool = True) -> str | None:
    """Build HTML with avatar + audio; avatar animates when audio plays with a professional UI."""
    if len(audio_bytes) > MAX_EMBED_AUDIO_BYTES:
        return None
    b64 = base64.b64encode(audio_bytes).decode("ascii")
    emoji, color = AVATAR_FOR_VOICE.get(voice_label, ("👤", "#64748b"))
    voice_escaped = html.escape(voice_label)
    
    bg_color = "rgba(15, 23, 42, 0.4)" if is_dark else "rgba(255, 255, 255, 0.7)"
    border_color = "rgba(148, 163, 184, 0.2)" if is_dark else "rgba(148, 163, 184, 0.4)"
    text_color = "#f8fafc" if is_dark else "#1e293b"
    audio_bg = "rgba(0, 0, 0, 0.3)" if is_dark else "rgba(241, 245, 249, 0.8)"
    audio_shadow = "inset 0 2px 6px rgba(0,0,0,0.4)" if is_dark else "inset 0 2px 6px rgba(0,0,0,0.05), 0 2px 10px rgba(0,0,0,0.05)"
    container_shadow = "0 20px 40px -10px rgba(0,0,0,0.4)" if is_dark else "0 10px 30px -5px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.02)"

    return f"""
    <style>
    .avatar-audio-container {{ 
        display: flex; align-items: center; gap: 2.5rem; flex-wrap: wrap; 
        padding: 2rem 3rem; background: {bg_color}; 
        border-radius: 28px; border: 1px solid {border_color};
        box-shadow: {container_shadow};
        backdrop-filter: blur(20px);
        margin: 1.5rem 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .avatar-audio-container:hover {{
        transform: translateY(-2px);
        box-shadow: {container_shadow}, 0 0 0 1px rgba(56,189,248,0.3);
    }}
    .avatar-speaker-box {{ 
        flex-shrink: 0; display: flex; flex-direction: column; 
        align-items: center; justify-content: center;
    }}
    .avatar-speaker {{
        width: 140px; height: 140px; border-radius: 50%;
        background: linear-gradient(135deg, {color}15, {color}40);
        border: 4px solid {color};
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 8px 24px {color}30, inset 0 4px 12px rgba(255,255,255,0.1);
        overflow: hidden;
        font-size: 72px;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    }}
    .avatar-speaker.speaking {{
        border-color: {color};
        animation: avatar-pulse 1.5s cubic-bezier(0.4, 0, 0.2, 1) infinite alternate;
    }}
    @keyframes avatar-pulse {{
        0% {{ transform: scale(1); box-shadow: 0 8px 24px {color}40, 0 0 0 0 {color}50; }}
        100% {{ transform: scale(1.06); box-shadow: 0 16px 32px {color}60, 0 0 0 20px rgba(0,0,0,0); }}
    }}
    .avatar-label {{ 
        text-align: center; margin-top: 1.2rem; font-weight: 800; font-size: 1.15rem;
        color: {text_color}; letter-spacing: 0.06em; text-transform: uppercase;
        font-family: system-ui, -apple-system, sans-serif;
    }}
    .audio-box {{ 
        flex: 1; min-width: 300px;
        background: {audio_bg};
        padding: 0.8rem 1.5rem; border-radius: 999px;
        box-shadow: {audio_shadow};
        display: flex; align-items: center; justify-content: center;
    }}
    audio {{ 
        width: 100%; height: 50px; outline: none; border-radius: 999px; 
        color-scheme: { 'dark' if is_dark else 'light' };
    }}
    /* Webkit custom controls base styling to blend nicely */
    audio::-webkit-media-controls-enclosure {{
        border-radius: 999px;
        background-color: transparent;
    }}
    audio::-webkit-media-controls-panel {{
        background-color: transparent;
    }}
    </style>
    <div class="avatar-audio-container">
        <div class="avatar-speaker-box">
            <div class="avatar-speaker" id="speaker-avatar">
                <div class="avatar-emoji">{emoji}</div>
            </div>
            <p class="avatar-label">{voice_escaped}</p>
        </div>
        <div class="audio-box">
            <audio id="synced-audio" controls controlsList="nodownload">
                <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            </audio>
        </div>
    </div>
    <script>
    (function() {{
        var audio = document.getElementById('synced-audio');
        var avatar = document.getElementById('speaker-avatar');
        if (!audio || !avatar) return;
        audio.addEventListener('play', function() {{ avatar.classList.add('speaking'); }});
        audio.addEventListener('pause', function() {{ avatar.classList.remove('speaking'); }});
        audio.addEventListener('ended', function() {{ avatar.classList.remove('speaking'); }});
    }})();
    </script>
    """

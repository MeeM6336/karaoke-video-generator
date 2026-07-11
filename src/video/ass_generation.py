import json

def format_time(secs):
    h = int(secs // 3600)
    m = int((secs % 3600) // 60)
    s = int(secs % 60)
    cs = int(round((secs - int(secs)) * 100))
    if cs == 100:
        s += 1
        cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def segment_to_ass(segment):
    ass_text = ""
    words = segment.get("words", [])

    for i, w in enumerate(words):
        # Fallback to segment start/end if Whisper misses a word-level timestamp
        start = w.get("start", segment["start"])
        
        # Extend the word's duration until the start of the NEXT word to consume gaps
        if i < len(words) - 1:
            end = words[i + 1].get("start", w.get("end", segment["end"]))
        else:
            end = segment["end"]
            
        duration_cs = int(round((end - start) * 100))
        word_str = w["word"].strip()
        
        # Ensure spacing is natural outside the \k tags
        if i < len(words) - 1:
            ass_text += f"{{\\k{duration_cs}}}{word_str} "
        else:
            ass_text += f"{{\\k{duration_cs}}}{word_str}"

    return ass_text

def rgb_to_ass(hex_color, alpha = 0):
    hex_color = hex_color.lstrip("#")
    r = hex_color[0:2]
    g = hex_color[2:4]
    b = hex_color[4:6]

    aa = f"{alpha:02X}"

    return f"&H{aa}{b}{g}{r}&"

def aligned_segments_to_ass(json_path, output_path, track_name, font_color):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Fetch the main segments list from the JSON
    segments = data.get("segments", [])

    # Standard header matching the example file exactly
    header = f"""[Script Info]
Title: {track_name}
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 0
PlayResY: 0
Original Timing: Generated

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,32,{rgb_to_ass(font_color)},&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,1.5,0,8,2,2,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Comment: 0,0:00:00.00,0:00:00.00,Default,,0,0,0,template pre-line all keeptags,!retime("line",$start < 900 and -$start or -900,200)!{{!$start < 900 and "\\k" .. ($start/10) or "\\k90"!\\fad(!$start < 900 and $start or 300!,200)}}
"""

    comments = []
    dialogues = []

    for segment in segments:
        c_start_sec = segment["start"]
        c_end_sec = segment["end"]
        
        lead_out = 0.2 
        
        if c_start_sec < 0.9:
            d_start_sec = 0.0
            k_lead = int(round(c_start_sec * 100))
            fade_in_ms = int(round(c_start_sec * 1000))
        else:
            d_start_sec = c_start_sec - 0.9
            k_lead = 90
            fade_in_ms = 300

        d_end_sec = c_end_sec + lead_out
        
        c_start_fmt = format_time(c_start_sec)
        c_end_fmt = format_time(c_end_sec)
        d_start_fmt = format_time(d_start_sec)
        d_end_fmt = format_time(d_end_sec)
        
        text = segment_to_ass(segment)
        
        comments.append(
            f"Comment: 0,{c_start_fmt},{c_end_fmt},Default,,0,0,0,karaoke,{text}"
        )
        
        d_text = f"{{\\k{k_lead}\\fad({fade_in_ms},200)}}{text}"
        dialogues.append(
            f"Dialogue: 0,{d_start_fmt},{d_end_fmt},Default,,0,0,0,fx,{d_text}"
        )

    ass_content = header + "\n".join(comments) + "\n" + "\n".join(dialogues) + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_content)
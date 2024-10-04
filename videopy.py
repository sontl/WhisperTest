from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import VideoClip
import textwrap

def add_captions_word_by_word(video_path, captions):
    # Load the video
    video = VideoFileClip(video_path)
    
    # Parse the captions
    subtitle_clips = []
    for line in captions.split('\n'):
        if line.strip():
            time_range, text = line.split(']')
            start, end = map(lambda x: float(x.strip('s ')), time_range[1:-1].split('->'))
            subtitle_clips.append(((start, end), text.strip()))
    
    # Create text clips for each word
    text_clips = []
    colors = ['blue', 'green', 'red', 'yellow']
    color_index = 0
    
    for (start, end), text in subtitle_clips:
        text_clip = (TextClip(text, fontsize=70, color=colors[color_index], font='Arial-Bold', stroke_color='black', stroke_width=2)
                     .set_position('center')
                     .set_start(start)
                     .set_end(end))
        text_clips.append(text_clip)
        color_index = (color_index + 1) % len(colors)
    
    # Combine the original video with the text clips
    final_video = CompositeVideoClip([video] + text_clips)
    
    return final_video




def wrap_text(text, max_width, font_size):
    # Estimate characters per line based on font size and video width
    chars_per_line = int(max_width / (font_size * 0.6))  # Adjust this factor as needed
    return textwrap.fill(text, width=chars_per_line)

from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
import textwrap

def wrap_text(text, max_width, font_size):
    chars_per_line = int(max_width / (font_size * 0.6))
    return textwrap.fill(text, width=chars_per_line)

def add_caption_karaoke_style(video_path, parsed_captions):
    video = VideoFileClip(video_path)
    
    text_clips = []
    font_size = 24  # Reduced font size
    max_text_width = video.w * 0.9
    
    for caption in parsed_captions:
        wrapped_text = wrap_text(caption['text'], max_text_width, font_size)
        lines = wrapped_text.split('\n')
        
        for line_num, line in enumerate(lines):
            words = []
            line_words = line.split()
            word_index = 0
            for word in caption['words']:
                if word_index < len(line_words) and word['word'] == line_words[word_index]:
                    words.append(word)
                    word_index += 1
            
            for i, word_info in enumerate(words):
                word = word_info['word']
                start = word_info['start']
                end = word_info['end']
                
                # Create a clip for the highlighted word
                highlighted = (TextClip(word, fontsize=font_size, font='Arial', color='yellow', method='label')
                               .set_start(start)
                               .set_end(end))
                
                # Create a clip for the non-highlighted word
                normal = (TextClip(word, fontsize=font_size, font='Arial', color='white', method='label')
                          .set_start(caption['start'])
                          .set_end(caption['end']))
                
                # Combine the two clips
                word_clip = CompositeVideoClip([normal, highlighted])
                
                # Position the word
                word_width = TextClip(word, fontsize=font_size, font='Arial').w
                space_width = font_size * 0.3  # Adjust this value for desired spacing
                
                if i == 0:
                    line_width = sum(TextClip(w['word'], fontsize=font_size, font='Arial').w for w in words) + (len(words) - 1) * space_width
                    x_position = video.w/2 - line_width/2
                else:
                    prev_word = words[i-1]['word']
                    prev_word_width = TextClip(prev_word, fontsize=font_size, font='Arial').w
                    x_position += prev_word_width + space_width
                y_position = video.h - (len(lines) - line_num) * font_size * 1.5 - font_size
                
                word_clip = word_clip.set_position((x_position, y_position))
                
                text_clips.append(word_clip)
    
    final_video = CompositeVideoClip([video] + text_clips)
    return final_video

def parse_captions(captions):
    parsed_captions = []
    lines = captions.split('\n')
    current_segment = None

    for line in lines:
        if line.startswith('[') and '] [Segment]' in line:
            if current_segment:
                parsed_captions.append(current_segment)
            time_range, text = line.split('] [Segment]')
            start, end = map(lambda x: float(x.strip().rstrip('s')), time_range.strip('[]').split('->'))
            current_segment = {
                'start': start,
                'end': end,
                'text': text.strip(),
                'words': []
            }
        elif line.startswith('[') and '] [Word]' in line:
            if current_segment is None:
                continue  # Skip word if no current segment
            time_range, word = line.split('] [Word]')
            word_start, word_end = map(lambda x: float(x.strip().rstrip('s')), time_range.strip('[]').split('->'))
            current_segment['words'].append({
                'start': word_start,
                'end': word_end,
                'word': word.strip()
            })

    if current_segment:
        parsed_captions.append(current_segment)

    return parsed_captions

def get_text_at_time(t, parsed_captions):
    for caption in parsed_captions:
        if caption['start'] <= t < caption['end']:
            return caption['text']
    return ""

# Usage example:
video_path = "input/happy.mp4"
# Read captions from caption.txt file
with open('caption.txt', 'r') as file:
    content = file.read()

captions = content

# Before calling add_caption_karaoke_style, add:
parsed_captions = parse_captions(captions)
print(f"Type of parsed_captions: {type(parsed_captions)}")
print(f"First item in parsed_captions: {parsed_captions[0] if parsed_captions else 'Empty list'}")
# final_video = add_captions_word_by_word(video_path, captions)
# final_video.write_videofile("output_video_word_by_word.mp4")
final_video_karaoke = add_caption_karaoke_style(video_path, parsed_captions)
final_video_karaoke.write_videofile("output_video_karaoke.mp4")

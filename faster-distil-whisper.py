from faster_whisper import WhisperModel

model_size = "distil-large-v3"

model = WhisperModel(model_size, device="cuda", compute_type="float16")
segments, info = model.transcribe("input/l.mp3", beam_size=5, language="vi", condition_on_previous_text=False, word_timestamps=True)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    # print("[%.2fs -> %.2fs] [Segment] %s" % (segment.start, segment.end, segment.text))
    #for word in segment.words:
    #    print("[%.2fs -> %.2fs] [Word] %s" % (word.start, word.end, word.word))
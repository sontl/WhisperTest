from faster_whisper import WhisperModel

model_size = "large-v3"

# Run on GPU with FP16
model = WhisperModel(model_size, device="cuda", compute_type="float16")
# batched_model = BatchedInferencePipeline(model=model)
# or run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")
# or run on GPU with INT
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")
segments, info = model.transcribe("input/ba.mp3", beam_size=5, word_timestamps=True)
# segments, info = batched_model.transcribe("input/ruvo.mp3", batch_size=16, word_timestamps=True)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[Sentence][%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    for word in segment.words:
       print("[Word][%.2fs -> %.2fs] %s" % (word.start, word.end, word.word))
    


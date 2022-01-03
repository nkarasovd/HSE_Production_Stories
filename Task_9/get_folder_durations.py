import librosa
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

wavs = sorted(
    list(Path("/shared/green/ssd2/libritts-22k/audios/train-clean-100/").rglob("**/**/*.wav")),
    key=lambda x: x.stem,
)

results = defaultdict(int)

for wav in tqdm(wavs):
    wav_dur = librosa.get_duration(filename=str(wav))
    results[wav.parents[1]] += wav_dur

for k, v in sorted(results.items(), key=lambda p: p[1]):
    print(k, v)

from pathlib import Path


def val_to_class(val):
    if val < 1:
        return 1
    if 1 < val < 2:
        return 2
    return 3

wavs = Path("libri_training_data").glob("*.prom")

with open("libri_transcripts.txt", "w") as f:
    for wav in wavs:
        text_grid_path = wav
        with open(text_grid_path) as f1:
            words = []
            proms = []
            boundaries = []
            for line in f1.read().splitlines():
                _, _, _, word, prom, boundary = line.split('\t')
                words.append(word)
                proms.append(str(val_to_class(float(prom))))
                boundaries.append(str(val_to_class(float(boundary))))

        cur_sent = " ".join(words)
        cur_prom = " ".join(proms)
        cur_bound = " ".join(boundaries)
        f.write(f"{wav.with_suffix('.pt')}|{cur_sent}|{cur_prom}|{cur_bound}\n")
"""Compress portfolio images.

Dry-run by default: reports the size every file *would* become without touching
anything. Pass --apply to actually rewrite them.

Rules:
  - CMYK JPEG -> sRGB (browsers render CMYK JPEG with wrong colors)
  - longest side capped at MAX_SIDE
  - opaque source -> JPEG q85 (alpha channel carries no information)
  - genuinely transparent source -> stays PNG
  - animated GIF -> resized, animation preserved
"""
import io
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageSequence

MAX_SIDE = 1600
# The GIF is only ever shown at height:120px in .exp-media and is not a
# lightbox trigger, so it never needs to be larger than this.
MAX_SIDE_GIF = 400
JPEG_Q = 85
APPLY = '--apply' in sys.argv


def has_real_alpha(im):
    if im.mode not in ('RGBA', 'LA', 'P') and 'transparency' not in im.info:
        return False
    a = im.convert('RGBA').getchannel('A')
    return a.getextrema()[0] < 255


def quantized_ok(original, quant):
    """Reject palette reduction that visibly posterises the image.

    Flat-colour logos and UI screenshots survive a 255-colour palette with
    almost no error. Photographs and smooth gradients band badly, which is
    obvious to the eye, so measure the error and refuse those.
    """
    a = original.convert('RGB')
    b = quant.convert('RGB')
    diff = ImageChops.difference(a, b)
    hist = diff.convert('L').histogram()
    total = sum(hist)
    mean = sum(v * c for v, c in enumerate(hist)) / total
    # 99.5th percentile of per-pixel error
    run, p995 = 0, 0
    for v, c in enumerate(hist):
        run += c
        if run >= total * 0.995:
            p995 = v
            break
    return mean < 1.5 and p995 < 12


def fit(im, cap=MAX_SIDE):
    w, h = im.size
    if max(w, h) <= cap:
        return im
    s = cap / max(w, h)
    return im.resize((round(w * s), round(h * s)), Image.LANCZOS)


def encode(path):
    """Return (new_suffix, bytes, note) for the compressed version."""
    im = Image.open(path)

    # Animated GIF: resize every frame, keep the animation.
    if getattr(im, 'n_frames', 1) > 1:
        orig = im.size
        frames = [fit(f.convert('RGBA'), MAX_SIDE_GIF)
                  for f in ImageSequence.Iterator(im)]
        buf = io.BytesIO()
        frames[0].convert('P', palette=Image.ADAPTIVE).save(
            buf, 'GIF', save_all=True, optimize=True,
            append_images=[f.convert('P', palette=Image.ADAPTIVE) for f in frames[1:]],
            loop=im.info.get('loop', 0), duration=im.info.get('duration', 100),
            disposal=2)
        note = f"{im.n_frames} frames"
        if frames[0].size != orig:
            note += f" {orig[0]}x{orig[1]}->{frames[0].size[0]}x{frames[0].size[1]}"
        return '.gif', buf.getvalue(), note

    note = []
    if im.mode == 'CMYK':
        note.append('CMYK->sRGB')

    alpha = has_real_alpha(im)
    orig_size = im.size
    im = fit(im.convert('RGBA') if alpha else im.convert('RGB'))
    if im.size != orig_size:
        note.append(f"{orig_size[0]}x{orig_size[1]}->{im.size[0]}x{im.size[1]}")

    buf = io.BytesIO()
    if alpha:
        # Photographic content with an alpha channel is the worst case for PNG
        # and there is no pngquant on this machine. Candidates, smallest wins:
        #   full-colour PNG  - always correct, often huge
        #   palette PNG      - tiny, but bands on gradients (gated)
        #   lossy WebP       - keeps alpha, ~87% smaller, universally supported
        im.save(buf, 'PNG', optimize=True)
        cands = [(len(buf.getvalue()), '.png', buf.getvalue(), 'full-colour png')]

        qim = im.quantize(colors=255, method=Image.FASTOCTREE)
        q = io.BytesIO()
        qim.save(q, 'PNG', optimize=True)
        if quantized_ok(im, qim):
            cands.append((len(q.getvalue()), '.png', q.getvalue(), 'quantized png'))

        w = io.BytesIO()
        im.save(w, 'WEBP', quality=82, method=6)
        cands.append((len(w.getvalue()), '.webp', w.getvalue(), 'webp (alpha)'))

        _, suffix, data, why = min(cands, key=lambda c: c[0])
        note.append(why)
        if suffix != path.suffix.lower():
            note.append(f"{path.suffix}->{suffix}")
        return suffix, data, ' '.join(note)

    # Flat-colour UI screenshots often compress better as PNG than as JPEG,
    # and PNG avoids ringing artefacts around text. Try both, keep the smaller.
    im.save(buf, 'JPEG', quality=JPEG_Q, optimize=True, progressive=True)
    as_jpeg = buf.getvalue()
    qim = im.quantize(colors=255, method=Image.FASTOCTREE)
    png = io.BytesIO()
    qim.save(png, 'PNG', optimize=True)
    as_png = png.getvalue() if quantized_ok(im, qim) else None

    if as_png is not None and len(as_png) < len(as_jpeg):
        note.append('png (smaller than jpeg)')
        return '.png', as_png, ' '.join(note)
    if path.suffix.lower() not in ('.jpg', '.jpeg'):
        note.append(f"{path.suffix}->.jpg")
    return '.jpg', as_jpeg, ' '.join(note)


rows = []
for p in sorted(Path('images').rglob('*')):
    if not p.is_file():
        continue
    old = p.stat().st_size
    try:
        suffix, data, note = encode(p)
    except Exception as e:
        rows.append((p, old, old, p.name, f"SKIPPED: {e}"))
        continue
    new_path = p.with_suffix(suffix)
    # Never grow a file. This has to be checked even when the extension would
    # change, otherwise a "conversion" that loses gets applied anyway.
    if len(data) >= old:
        rows.append((p, old, old, p.name, 'kept (already optimal)'))
        continue
    rows.append((p, old, len(data), new_path.name, note))
    if APPLY:
        new_path.write_bytes(data)
        if new_path != p:
            p.unlink()

print(f"{'KB now':>7} {'KB new':>7} {'save':>6}  {'file':<44} note")
print('-' * 104)
for p, old, new, newname, note in sorted(rows, key=lambda r: -r[1]):
    pct = f"{(1 - new / old) * 100:.0f}%" if old else '-'
    print(f"{old/1024:7.0f} {new/1024:7.0f} {pct:>6}  {p.as_posix():<44} {note}")
to = sum(r[1] for r in rows)
tn = sum(r[2] for r in rows)
print('-' * 104)
print(f"{to/1048576:7.1f} {tn/1048576:7.1f} MB   {(1-tn/to)*100:.0f}% smaller overall")
print()
print('APPLIED - files rewritten' if APPLY else 'DRY RUN - nothing written (pass --apply)')

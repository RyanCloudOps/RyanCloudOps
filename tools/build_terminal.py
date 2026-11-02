# Builds assets/terminal.svg: an animated terminal (whoami + kubectl get pods) that loops, in the portfolio's black & white style.
import sys
out = sys.argv[1]
W, H = 720, 360
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"
CW = 9.6; FS = 16; LOOP = 17.0
o = []; a = o.append
def tag(s): a(s)
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami → gary · systems engineer → cloud architect; kubectl get pods -n career → systems-engineer Running, cloud-engineer ContainerCreating, cloud-architect Pending">')
a('<defs>')
clips = []
def typed(idx, text, x, y, t0, per=0.055):
    """Types `text` at (x,y) starting at t0 (s after the loop start). Returns the end time."""
    n = len(text); dur = n * per
    a(f'<clipPath id="c{idx}"><rect x="{x}" y="{y-FS-2}" height="{FS+10}" width="0">'
      f'<animate attributeName="width" calcMode="discrete" begin="m.begin+{t0:.2f}s" dur="{dur:.2f}s" keyTimes="{";".join(f"{i/n:.4f}" for i in range(n))}" values="{";".join(f"{i*CW:.1f}" for i in range(n))}"/>'
      f'<set attributeName="width" to="{n*CW+6:.0f}" begin="m.begin+{t0+dur:.2f}s" end="m.end"/></rect></clipPath>')
    return dur
body = []
def text_typed(idx, text, x, y, t0, fill="#c8c8c8", per=0.055):
    dur = typed(idx, text, x, y, t0, per)
    n = len(text)
    body.append(f'<text x="{x}" y="{y}" clip-path="url(#c{idx})" font-family="{MONO}" font-size="{FS}" textLength="{n*CW:.0f}" lengthAdjust="spacing" fill="{fill}" opacity="0"><set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.end"/>{text}</text>')
    # caret following the typing
    body.append(f'<rect x="{x}" y="{y-FS+1}" width="9" height="19" fill="#f2f2f2" opacity="0"><set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.begin+{t0+dur+0.35:.2f}s"/>'
                f'<animate attributeName="x" calcMode="discrete" begin="m.begin+{t0:.2f}s" dur="{dur:.2f}s" keyTimes="{";".join(f"{i/n:.4f}" for i in range(n))}" values="{";".join(f"{x+i*CW:.1f}" for i in range(n))}"/>'
                f'<set attributeName="x" to="{x+n*CW+2:.1f}" begin="m.begin+{t0+dur:.2f}s" end="m.end"/></rect>')
    return dur
def line(text_markup, x, y, t0, fill="#9a9a9a", weight=400, blink=False):
    inner = f'<set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.end"/>'
    body.append(f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{FS}" font-weight="{weight}" fill="{fill}" opacity="0" xml:space="preserve">{text_markup}{inner}</text>')

P = "$ "
# --- command 1
y1, y2 = 82, 112
body.append(f'<text x="44" y="{y1}" font-family="{MONO}" font-size="{FS}" fill="#f2f2f2" font-weight="700" opacity="0">$<set attributeName="opacity" to="1" begin="m.begin+0.2s" end="m.end"/></text>')
d1 = text_typed(1, "whoami", 44 + 2 * CW, y1, 0.5)
line("gary · systems engineer -&gt; cloud architect", 44, y2, 0.5 + d1 + 0.35, "#f2f2f2", 600)
# --- command 2
y3 = 160
t2 = 2.9
body.append(f'<text x="44" y="{y3}" font-family="{MONO}" font-size="{FS}" fill="#f2f2f2" font-weight="700" opacity="0">$<set attributeName="opacity" to="1" begin="m.begin+{t2-0.2}s" end="m.end"/></text>')
d2 = text_typed(2, "kubectl get pods -n career", 44 + 2 * CW, y3, t2)
t = t2 + d2 + 0.5
cols = (44, 300, 392)
yh = 198
line("NAME", cols[0], yh, t, "#9a9a9a", 700); line("READY", cols[1], yh, t, "#9a9a9a", 700); line("STATUS", cols[2], yh, t, "#9a9a9a", 700)
rows = [("systems-engineer", "1/1", "Running", "#f2f2f2", 700), ("cloud-engineer", "0/1", "ContainerCreating", "#c8c8c8", 400), ("cloud-architect", "0/1", "Pending", "#6a6a6a", 400)]
for i, (n_, r_, s_, c_, w_) in enumerate(rows):
    y = yh + 28 * (i + 1); tt = t + 0.45 * (i + 1)
    line(n_, cols[0], y, tt, "#c8c8c8"); line(r_, cols[1], y, tt, "#c8c8c8")
    if s_ == "ContainerCreating":
        # status with a blinking "…" to show it is still in progress
        body.append(f'<text x="{cols[2]}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{c_}" opacity="0">{s_}<set attributeName="opacity" to="1" begin="m.begin+{tt:.2f}s" end="m.end"/></text>')
        body.append(f'<text x="{cols[2]+len(s_)*CW+4:.1f}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="#c8c8c8" opacity="0">…<animate attributeName="opacity" values="0;1;0" dur="1.4s" begin="m.begin+{tt+0.4:.2f}s" repeatCount="indefinite" end="m.end"/></text>')
    else:
        line(s_, cols[2], y, tt, c_, w_)
# --- idle prompt with a blinking caret
yp = yh + 28 * 4 + 6
tp = t + 0.45 * 3 + 0.7
body.append(f'<text x="44" y="{yp}" font-family="{MONO}" font-size="{FS}" fill="#f2f2f2" font-weight="700" opacity="0">$<set attributeName="opacity" to="1" begin="m.begin+{tp:.2f}s" end="m.end"/></text>')
body.append(f'<rect x="{44+2*CW}" y="{yp-FS+1}" width="9" height="19" fill="#f2f2f2" opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="m.begin+{tp:.2f}s" repeatCount="indefinite" end="m.end"/></rect>')
a('</defs>')
# window
a(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#000" stroke="#272727" stroke-width="2"/>')
a(f'<rect x="1" y="1" width="{W-2}" height="40" rx="14" fill="#0a0a0a"/><rect x="1" y="26" width="{W-2}" height="15" fill="#0a0a0a"/><line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#272727"/>')
for i in range(3): a(f'<circle cx="{28+i*22}" cy="21" r="6" fill="#272727"/>')
a(f'<text x="{W/2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="1" fill="#6a6a6a">gary@prod: ~/career</text>')
a(f'<rect width="0" height="0"><animate id="m" attributeName="x" from="0" to="0" dur="{LOOP}s" begin="0s;m.end+1.2s"/></rect>')
a('<g>'); o.extend(body); a('</g>')
a('</svg>')
open(out, "w", encoding="utf-8").write("\n".join(o))
print(out, len("\n".join(o)) // 1024, "KB")

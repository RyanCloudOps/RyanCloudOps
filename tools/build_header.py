# Builds assets/header.svg: terminal intro (typing + BUILD/TEST/DEPLOY/RELEASE), constellations and the hero character.
import base64, random, sys
random.seed(7)
W, H = 1200, 520
poster = sys.argv[1]   # transparent poster of the character (webp)
out = sys.argv[2]
img = base64.b64encode(open(poster, "rb").read()).decode()
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Gary Flores — Systems Engineer, futuro Cloud Architect">')
a('<defs><radialGradient id="glow" cx="38%" cy="42%" r="55%"><stop offset="0" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
CMD = "gary@prod :~$ deploy --env production --portfolio"
N = len(CMD); CW = 10.2; TX = 60
a(f'<clipPath id="tc"><rect x="{TX}" y="40" height="34" width="0"><animate attributeName="width" calcMode="discrete" begin="0.5s" dur="{N*0.045:.2f}s" fill="freeze" keyTimes="{";".join(f"{i/N:.4f}" for i in range(N))}" values="{";".join(f"{i*CW:.1f}" for i in range(N))}"/>'
  f'<set attributeName="width" to="{N*CW+8:.0f}" begin="{0.5+N*0.045:.2f}s" fill="freeze"/></rect></clipPath></defs>')
a(f'<rect width="{W}" height="{H}" fill="#000"/><rect width="{W}" height="{H}" fill="url(#glow)"/>')
a(f'<text x="600" y="330" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="380" letter-spacing="14" fill="#f2f2f2" fill-opacity="0.05">GARY</text>')
# dust
for i in range(90):
    x, y, r = random.uniform(10, W-10), random.uniform(10, H-10), random.uniform(.5, 1.4)
    a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="#fff" opacity=".3"><animate attributeName="opacity" values=".1;.7;.1" dur="{random.uniform(2.5,6):.1f}s" begin="-{random.uniform(0,5):.1f}s" repeatCount="indefinite"/></circle>')
# constellations
def con(name, pts, edges, lx, ly):
    for i, j in edges:
        a(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="#fff" stroke-opacity=".14"/>')
    for k, (x, y) in enumerate(pts):
        a(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#fff"><animate attributeName="opacity" values=".35;1;.35" dur="{3+k*.7:.1f}s" begin="-{k}s" repeatCount="indefinite"/></circle>')
    a(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="2" fill="#fff" fill-opacity=".22">{name}</text>')
con("CLOUD", [(1050,70),(1100,45),(1150,85),(1118,140),(1062,125)], [(0,1),(1,2),(2,3),(3,4),(4,0)], 1100, 30)
con("DEVOPS", [(1052,425),(1090,402),(1140,430),(1118,486),(1070,478)], [(0,1),(1,2),(2,3),(3,4),(4,0),(1,3)], 1096, 392)
# terminal prompt (typed)
a(f'<text x="{TX}" y="64" clip-path="url(#tc)" font-family="{MONO}" font-size="17" textLength="{N*CW:.0f}" lengthAdjust="spacing"><tspan fill="#f2f2f2" font-weight="700">gary@prod</tspan><tspan fill="#9a9a9a"> :~$ </tspan><tspan fill="#c8c8c8">deploy --env production --portfolio</tspan></text>')
caret_t = ";".join(f"{i/N:.4f}" for i in range(N))
a(f'<rect x="{TX}" y="48" width="9" height="19" fill="#f2f2f2"><animate attributeName="x" calcMode="discrete" begin="0.5s" dur="{N*0.045:.2f}s" fill="freeze" keyTimes="{caret_t}" values="{";".join(f"{TX+i*CW:.1f}" for i in range(N))}"/><set attributeName="x" to="{TX+N*CW+2:.1f}" begin="{0.5+N*0.045:.2f}s" fill="freeze"/><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="{0.5+N*0.045:.2f}s" repeatCount="indefinite"/></rect>')
# pipeline
START = 3.0; STEP = 1.5
xs = [90, 250, 410, 570]; Y = 140; L = ["BUILD", "TEST", "DEPLOY", "RELEASE"]
a(f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[-1]}" y2="{Y}" stroke="#272727" stroke-width="3" stroke-linecap="round"/>')
a(f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[0]}" y2="{Y}" stroke="#f2f2f2" stroke-width="3" stroke-linecap="round"><animate attributeName="x2" values="{xs[0]};{xs[-1]}" dur="{STEP*3}s" begin="{START}s" fill="freeze"/></line>')
for k, x in enumerate(xs):
    t = START + k * STEP
    a(f'<circle cx="{x}" cy="{Y}" r="17" fill="#0a0a0a" stroke="#272727" stroke-width="2"/>')
    a(f'<circle cx="{x}" cy="{Y}" r="0" fill="#f2f2f2"><animate attributeName="r" values="0;19;17" keyTimes="0;.6;1" dur=".45s" begin="{t:.2f}s" fill="freeze"/></circle>')
    a(f'<path d="M{x-6} {Y+1}l4.5 4.5L{x+7} {Y-5}" fill="none" stroke="#000" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0"><set attributeName="opacity" to="1" begin="{t+.15:.2f}s" fill="freeze"/></path>')
    a(f'<text x="{x}" y="{Y+46}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2.5" fill="#4a4a4a">{L[k]}<set attributeName="fill" to="#f2f2f2" begin="{t:.2f}s" fill="freeze"/></text>')
# status line + percentage
MSG = ["› initializing build environment…", "› running test suite…", "› deploying to production…", "› verifying health checks…"]
T = [START - .2 + k * STEP for k in range(4)] + [START + 3 * STEP + .9]
for k, m in enumerate(MSG):
    a(f'<text x="{TX}" y="232" font-family="{MONO}" font-size="13" font-weight="600" fill="#c8c8c8" opacity="0">{m}<set attributeName="opacity" to="1" begin="{T[k]:.2f}s" fill="freeze"/><set attributeName="opacity" to="0" begin="{T[k+1]:.2f}s" fill="freeze"/></text>')
a(f'<text x="{TX}" y="232" font-family="{MONO}" font-size="13" font-weight="600" fill="#f2f2f2" opacity="0">› ready — welcome<set attributeName="opacity" to="1" begin="{T[4]:.2f}s" fill="freeze"/></text>')
PCT = [0, 25, 50, 75, 100]; PT = [START - .2, START + .6, START + STEP + .6, START + 2 * STEP + .6, START + 3 * STEP + .5, 999]
for k, p in enumerate(PCT):
    a(f'<text x="640" y="236" text-anchor="end" font-family="{MONO}" font-size="22" font-weight="700" fill="#f2f2f2" opacity="0">{p}<tspan fill="#9a9a9a" font-size="16">%</tspan><set attributeName="opacity" to="1" begin="{PT[k]:.2f}s" fill="freeze"/>' + (f'<set attributeName="opacity" to="0" begin="{PT[k+1]:.2f}s" fill="freeze"/>' if k < 4 else '') + '</text>')
# title
a(f'<text x="{TX}" y="296" font-family="{MONO}" font-size="14" letter-spacing="3" fill="#9a9a9a">BARCELONA · SOTHIS · PLM</text>')
a(f'<text x="56" y="388" font-family="{SANS}" font-weight="800" font-size="104" letter-spacing="-4" fill="#f2f2f2">Systems</text>')
a(f'<text x="56" y="480" font-family="{SANS}" font-weight="800" font-size="104" letter-spacing="-4" fill="#f2f2f2">Engineer<tspan fill="#9a9a9a">.</tspan></text>')
# character + roles
a(f'<image x="700" y="20" width="296" height="500" preserveAspectRatio="xMidYMax meet" xlink:href="data:image/webp;base64,{img}"/>')
for k, (t, c, w) in enumerate([("[x] systems engineer", "#9a9a9a", 400), ("[>] cloud engineer", "#f2f2f2", 700), ("[ ] cloud architect", "#9a9a9a", 400)]):
    a(f'<text x="1010" y="{300+k*26}" font-family="{MONO}" font-size="13" font-weight="{w}" fill="{c}">{t}</text>')
a('</svg>')
open(out, "w", encoding="utf-8").write("\n".join(o))
print(out, len("\n".join(o)) // 1024, "KB")

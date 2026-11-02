# Builds the profile README graphics: git graph (experience + education), certifications, roadmap pipeline and the starry terminals.
# usage: python build_sections.py <out_dir>
import random, textwrap, sys
OUT = sys.argv[1]
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def save(name, parts): s = "\n".join(parts); open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(s); print(name, len(s) // 1024, "KB")

# ---------- starry background helpers ----------
def dust(W, H, n, seed, x0=0, y0=0):
    r = random.Random(seed); o = []
    for _ in range(n):
        x, y, rad = r.uniform(x0 + 6, W - 6), r.uniform(y0 + 4, H - 6), r.uniform(.5, 1.3)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rad:.1f}" fill="#fff" opacity=".3"><animate attributeName="opacity" values=".08;.65;.08" dur="{r.uniform(2.5,6):.1f}s" begin="-{r.uniform(0,5):.1f}s" repeatCount="indefinite"/></circle>')
    return o
def con(name, pts, edges, lx, ly, op=.14):
    o = []
    for i, j in edges: o.append(f'<line x1="{pts[i][0]}" y1="{pts[i][1]}" x2="{pts[j][0]}" y2="{pts[j][1]}" stroke="#fff" stroke-opacity="{op}"/>')
    for k, (x, y) in enumerate(pts): o.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#fff"><animate attributeName="opacity" values=".3;.95;.3" dur="{3+k*.7:.1f}s" begin="-{k}s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="2" fill="#fff" fill-opacity=".2">{name}</text>')
    return o
CLOUD = lambda dx, dy: con("CLOUD", [(dx+0,dy+30),(dx+45,dy+5),(dx+95,dy+42),(dx+68,dy+92),(dx+14,dy+80)], [(0,1),(1,2),(2,3),(3,4),(4,0)], dx+48, dy-6)
DEVOPS = lambda dx, dy: con("DEVOPS", [(dx+0,dy+22),(dx+40,dy),(dx+90,dy+28),(dx+66,dy+84),(dx+16,dy+76)], [(0,1),(1,2),(2,3),(3,4),(4,0),(1,3)], dx+44, dy-8)
def frame(W, H, title, fillbg="#000"):
    o = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{fillbg}" stroke="#272727" stroke-width="2"/>']
    return o
def titlebar(W, title):
    o = [f'<rect x="1" y="1" width="{W-2}" height="40" rx="14" fill="#0a0a0a"/><rect x="1" y="26" width="{W-2}" height="15" fill="#0a0a0a"/><line x1="1" y1="41" x2="{W-1}" y2="41" stroke="#272727"/>']
    for i in range(3): o.append(f'<circle cx="{28+i*22}" cy="21" r="6" fill="#272727"/>')
    o.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="1" fill="#6a6a6a">{title}</text>')
    return o

# ---------- generic animated terminal (loops) ----------
def term(W, H, title, items, label, constellations=()):
    CW, FS, LOOP = 9.6, 16, 18.0
    defs, body, idx = [], [], 0
    for it in items:
        k = it["k"]
        if k == "cmd":
            idx += 1; text, y, t0 = it["text"], it["y"], it["t"]; n = len(text); per = .06; dur = n * per; x = 44 + 2 * CW
            kt = ";".join(f"{i/n:.4f}" for i in range(n))
            defs.append(f'<clipPath id="c{idx}"><rect x="{x}" y="{y-FS-2}" height="{FS+10}" width="0"><animate attributeName="width" calcMode="discrete" begin="m.begin+{t0:.2f}s" dur="{dur:.2f}s" keyTimes="{kt}" values="{";".join(f"{i*CW:.1f}" for i in range(n))}"/><set attributeName="width" to="{n*CW+6:.0f}" begin="m.begin+{t0+dur:.2f}s" end="m.end"/></rect></clipPath>')
            body.append(f'<text x="44" y="{y}" font-family="{MONO}" font-size="{FS}" fill="#f2f2f2" font-weight="700" opacity="0">$<set attributeName="opacity" to="1" begin="m.begin+{t0-.2:.2f}s" end="m.end"/></text>')
            body.append(f'<text x="{x}" y="{y}" clip-path="url(#c{idx})" font-family="{MONO}" font-size="{FS}" textLength="{n*CW:.0f}" lengthAdjust="spacing" fill="#c8c8c8" opacity="0"><set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.end"/>{esc(text)}</text>')
            body.append(f'<rect x="{x}" y="{y-FS+1}" width="9" height="19" fill="#f2f2f2" opacity="0"><set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.begin+{t0+dur+.35:.2f}s"/><animate attributeName="x" calcMode="discrete" begin="m.begin+{t0:.2f}s" dur="{dur:.2f}s" keyTimes="{kt}" values="{";".join(f"{x+i*CW:.1f}" for i in range(n))}"/><set attributeName="x" to="{x+n*CW+2:.1f}" begin="m.begin+{t0+dur:.2f}s" end="m.end"/></rect>')
            it["_end"] = t0 + dur
        elif k == "line":
            spans = "".join(f'<tspan fill="{f}" font-weight="{w}"' + (f' x="{x}"' if x is not None else '') + f'>{esc(t)}</tspan>' for (t, f, w, x) in it["parts"])
            body.append(f'<text x="{it.get("x",44)}" y="{it["y"]}" font-family="{MONO}" font-size="{FS}" xml:space="preserve" opacity="0">{spans}<set attributeName="opacity" to="1" begin="m.begin+{it["t"]:.2f}s" end="m.end"/></text>')
        elif k == "idle":
            y, t0 = it["y"], it["t"]
            body.append(f'<text x="44" y="{y}" font-family="{MONO}" font-size="{FS}" fill="#f2f2f2" font-weight="700" opacity="0">$<set attributeName="opacity" to="1" begin="m.begin+{t0:.2f}s" end="m.end"/></text><rect x="{44+2*CW}" y="{y-FS+1}" width="9" height="19" fill="#f2f2f2" opacity="0"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="m.begin+{t0:.2f}s" repeatCount="indefinite" end="m.end"/></rect>')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">', '<defs>' + "".join(defs) + f'<clipPath id="win"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14"/></clipPath></defs>']
    o += frame(W, H, title)
    o.append('<g clip-path="url(#win)">')
    o += dust(W, H, int(W * H / 5200), 11, 0, 42)
    for c in constellations: o += c
    o += titlebar(W, title)
    o.append(f'<rect width="0" height="0"><animate id="m" attributeName="x" from="0" to="0" dur="{LOOP}s" begin="0s;m.end+1.2s"/></rect>')
    o += body
    o.append('</g></svg>')
    return o

W_ = lambda t, f="#c8c8c8", w=400, x=None: (t, f, w, x)
# whoami / kubectl terminal, now with stars
cols = (44, 300, 392)
it = [{"k": "cmd", "text": "whoami", "y": 82, "t": .5},
      {"k": "line", "y": 112, "t": 1.55, "parts": [W_("gary · systems engineer -> cloud architect", "#f2f2f2", 600)]},
      {"k": "cmd", "text": "kubectl get pods -n career", "y": 160, "t": 2.9}]
t = 2.9 + 26 * .06 + .5
it.append({"k": "line", "y": 198, "t": t, "parts": [W_("NAME", "#9a9a9a", 700), W_("READY", "#9a9a9a", 700, cols[1]), W_("STATUS", "#9a9a9a", 700, cols[2])]})
for i, (n_, r_, s_, c_, w_) in enumerate([("systems-engineer", "1/1", "Running", "#f2f2f2", 700), ("cloud-engineer", "0/1", "ContainerCreating …", "#c8c8c8", 400), ("cloud-architect", "0/1", "Pending", "#6a6a6a", 400)]):
    it.append({"k": "line", "y": 198 + 28 * (i + 1), "t": t + .45 * (i + 1), "parts": [W_(n_), W_(r_, "#c8c8c8", 400, cols[1]), W_(s_, c_, w_, cols[2])]})
it.append({"k": "idle", "y": 198 + 28 * 4 + 6, "t": t + 2.1})
save("terminal", term(720, 360, "gary@prod: ~/career", it, "Terminal: whoami → gary · systems engineer → cloud architect; kubectl get pods -n career → systems-engineer Running, cloud-engineer ContainerCreating, cloud-architect Pending", [CLOUD(600, 70), DEVOPS(590, 230)]))

# contact terminal
it = [{"k": "cmd", "text": "./contact.sh", "y": 82, "t": .5},
      {"k": "line", "y": 116, "t": 1.7, "parts": [W_("¿Buscas a alguien para tu equipo de sistemas o cloud?", "#f2f2f2", 600)]},
      {"k": "line", "y": 144, "t": 2.3, "parts": [W_("→ Escríbeme y lo hablamos.", "#9a9a9a", 400)]},
      {"k": "idle", "y": 184, "t": 3.1}]
save("contact-terminal", term(720, 214, "gary@prod: ~/contacto", it, "Terminal: ./contact.sh — ¿Buscas a alguien para tu equipo de sistemas o cloud? Escríbeme y lo hablamos.", [CLOUD(612, 66)]))

# ---------- git graph: experience + education ----------
def gitgraph():
    W, H = 820, 760
    X = 250; L1 = 540; L2 = 660
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Historial en forma de ramas de git: v1.0 Clicc (Jun–Nov 2021), v2.0 Alten Spain (Abr 2022–Abr 2023), v3.0 Sothis (Jul 2023 → hoy); ramas de formación: CFGS ASIR 2020–2022, CFGS DAM 2021–2023 y Grado en Ingeniería Informática UOC 2024 → en curso">']
    o += frame(W, H, "")
    o.append('<g>')
    o += dust(W, H, 130, 5)
    o += CLOUD(690, 40) + DEVOPS(40, 640)
    o.append('</g>')
    seq = [0]
    def when(): seq[0] += 1; return .3 + seq[0] * .17
    def draw(d, dash=False, delay=None, op=1):
        delay = when() if delay is None else delay
        extra = ' stroke-dasharray="1"' if not dash else ''
        if dash:
            o.append(f'<path d="{d}" fill="none" stroke="#f2f2f2" stroke-opacity=".55" stroke-width="2.2" stroke-dasharray="5 6" stroke-linecap="round" opacity="0"><set attributeName="opacity" to="1" begin="{delay:.2f}s" fill="freeze"/></path>')
        else:
            o.append(f'<path d="{d}" pathLength="1" fill="none" stroke="#f2f2f2" stroke-opacity="{op}" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur=".7s" begin="{delay:.2f}s" fill="freeze"/></path>')
    def node(x, y, hollow=False, big=False, delay=None):
        delay = when() if delay is None else delay
        r = 9 if big else 7
        fill = "#000" if hollow else "#f2f2f2"
        o.append(f'<circle cx="{x}" cy="{y}" r="0" fill="{fill}" stroke="#f2f2f2" stroke-width="2.2"><animate attributeName="r" values="0;{r+3};{r}" keyTimes="0;.6;1" dur=".4s" begin="{delay:.2f}s" fill="freeze"/></circle>')
    def label(x, y, t, size=13, fill="#c8c8c8", weight=400, anchor="start", mono=True, delay=None, ls=0):
        delay = when() if delay is None else delay
        fam = MONO if mono else SANS
        o.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" font-size="{size}" font-weight="{weight}" letter-spacing="{ls}" fill="{fill}" opacity="0">{esc(t)}<set attributeName="opacity" to="1" begin="{delay:.2f}s" fill="freeze"/></text>')
    main = [50, 560]
    draw(f"M{X} {main[0]} L{X} {main[1]}", delay=.3)
    # main start
    node(X, 50, hollow=True, delay=.3); label(X - 18, 54, "main", 12, "#6a6a6a", anchor="end", delay=.4)
    # --- ASIR branch (2020-2022)
    draw(f"M{X} 90 C{X} 130 {L1} 130 {L1} 170"); draw(f"M{L1} 170 L{L1} 330")
    node(L1, 170, hollow=True); label(L1 + 18, 168, "edu/asir", 13, "#f2f2f2", 700); label(L1 + 18, 187, "CFGS ASIR · 2020 – 2022", 11, "#6a6a6a")
    # --- v1.0 Clicc
    node(X, 240, big=True); label(X - 20, 236, "v1.0 · init", 12, "#9a9a9a", anchor="end"); label(X - 20, 258, "Clicc", 20, "#f2f2f2", 800, anchor="end", mono=False)
    label(X - 20, 278, "Technical Support Help Desk", 12, "#c8c8c8", anchor="end"); label(X - 20, 296, "Jun 2021 – Nov 2021", 11, "#6a6a6a", anchor="end")
    label(X + 20, 262, "Microsoft 365 · Active Directory", 11, "#6a6a6a"); label(X + 20, 279, "Windows y Linux", 11, "#6a6a6a")
    # --- DAM branch (2021-2023)
    draw(f"M{X} 290 C{X} 330 {L2} 330 {L2} 370"); draw(f"M{L2} 370 L{L2} 490")
    node(L2, 370, hollow=True); label(L2 + 18, 368, "edu/dam", 13, "#f2f2f2", 700); label(L2 + 18, 387, "CFGS DAM · 2021 – 2023", 11, "#6a6a6a")
    # --- ASIR merge + v2.0 Alten
    draw(f"M{L1} 330 C{L1} 370 {X} 360 {X} 400")
    node(X, 400, big=True); label(X - 20, 396, "v2.0", 12, "#9a9a9a", anchor="end"); label(X - 20, 418, "Alten Spain", 20, "#f2f2f2", 800, anchor="end", mono=False)
    label(X - 20, 438, "Desarrollador de software", 12, "#c8c8c8", anchor="end"); label(X - 20, 456, "Abr 2022 – Abr 2023", 11, "#6a6a6a", anchor="end")
    label(X + 20, 422, "SQL Server · Report Builder", 11, "#6a6a6a"); label(X + 20, 439, ".NET · Bootstrap · Git", 11, "#6a6a6a")
    # --- DAM merge + v3.0 Sothis (HEAD)
    draw(f"M{L2} 490 C{L2} 540 {X} 520 {X} 560")
    node(X, 560, big=True); label(X - 20, 556, "v3.0 · HEAD → main", 12, "#f2f2f2", 700, anchor="end"); label(X - 20, 578, "Sothis", 20, "#f2f2f2", 800, anchor="end", mono=False)
    label(X - 20, 598, "Systems Engineer · PLM", 12, "#c8c8c8", anchor="end"); label(X - 20, 616, "Jul 2023 → hoy", 11, "#6a6a6a", anchor="end")
    label(X + 20, 582, "Teamcenter · Tecnomatix · Azure DevOps", 11, "#6a6a6a"); label(X + 20, 599, "Tomcat · SQL Server · Windows Server / AD", 11, "#6a6a6a")
    # --- UOC (open branch, in progress)
    draw(f"M{X} 600 C{X} 640 {L1} 640 {L1} 680"); draw(f"M{L1} 680 L{L1} 735", dash=True)
    node(L1, 680, hollow=True); label(L1 + 18, 678, "edu/uoc", 13, "#f2f2f2", 700); label(L1 + 18, 697, "Grado en Ingeniería Informática", 11, "#6a6a6a"); label(L1 + 18, 714, "2024 → en curso", 11, "#9a9a9a")
    o.append(f'<circle cx="{L1}" cy="735" r="5" fill="none" stroke="#f2f2f2" stroke-width="2"><animate attributeName="r" values="4;10;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.2;1" dur="2s" repeatCount="indefinite"/></circle>')
    o.append('</svg>')
    return o
save("gitgraph", gitgraph())

# ---------- certifications ----------
def certs():
    done = ["Technical Support Associate", "Technical Support Manager", "Experto en Virtualización VMware", "Servidor Web Apache 2.4", "Planificación de copias de seguridad"]
    nxt = ["AWS Cloud Practitioner", "Azure AZ-104", "HashiCorp Terraform Associate"]
    W = 820; CW = 8.1
    o = []; y = 100; x = 28
    def chip(t, solid, delay):
        nonlocal x, y
        w = len(t) * CW + 52
        if x + w > W - 28: x, y = 28, y + 46
        if solid:
            o.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{delay:.2f}s" fill="freeze"/><rect x="{x}" y="{y-20}" width="{w:.0f}" height="34" rx="17" fill="#f2f2f2" fill-opacity=".08" stroke="#f2f2f2" stroke-opacity=".7"/><path d="M{x+14} {y-3}l4.5 4.5L{x+27} {y-12}" fill="none" stroke="#f2f2f2" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><text x="{x+36}" y="{y}" font-family="{MONO}" font-size="13" fill="#f2f2f2">{esc(t)}</text></g>')
        else:
            o.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{delay:.2f}s" fill="freeze"/><rect x="{x}" y="{y-20}" width="{w:.0f}" height="34" rx="17" fill="none" stroke="#6a6a6a" stroke-dasharray="4 4"/><circle cx="{x+20}" cy="{y-3}" r="5" fill="none" stroke="#6a6a6a" stroke-width="1.8"/><text x="{x+36}" y="{y}" font-family="{MONO}" font-size="13" fill="#9a9a9a">{esc(t)}</text></g>')
        x += w + 10
    for i, t in enumerate(done): chip(t, True, .5 + i * .2)
    y += 76; x = 28; ny = y
    for i, t in enumerate(nxt): chip(t, False, 1.8 + i * .2)
    H = y + 34
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Certificaciones: 5 de 8. Hechas: Technical Support Associate, Technical Support Manager, Experto en Virtualización VMware, Servidor Web Apache 2.4, Planificación de copias de seguridad. Próximas: AWS Cloud Practitioner, Azure AZ-104, HashiCorp Terraform Associate">']
    head += frame(W, H, "") + dust(W, H, 70, 9)
    head.append(f'<text x="28" y="44" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#9a9a9a">CERTIFICACIONES DESBLOQUEADAS</text><text x="{W-28}" y="46" text-anchor="end" font-family="{SANS}" font-weight="800" font-size="26" fill="#f2f2f2">5<tspan fill="#6a6a6a" font-size="18">/8</tspan></text>')
    head.append(f'<rect x="28" y="58" width="{W-56}" height="6" rx="3" fill="#1a1a1a"/><rect x="28" y="58" width="0" height="6" rx="3" fill="#f2f2f2"><animate attributeName="width" from="0" to="{(W-56)*5/8:.0f}" dur="1.4s" begin=".3s" fill="freeze"/></rect>')
    head.append(f'<text x="28" y="{ny-30}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#6a6a6a">PRÓXIMAS</text>')
    return head + o + ['</svg>']
save("certs", certs())

# ---------- roadmap pipeline ----------
def roadmap():
    W, H = 820, 300
    S = [("01", "Fundamentos", "Linux, redes, Windows Server, AD, virtualización, Git", "COMPLETADO", "done"),
         ("02", "Nube e IaC", "AWS / Azure, Docker, Terraform, CI/CD", "EN CURSO", "now"),
         ("03", "Plataforma y operación", "Kubernetes, Helm, observabilidad, costes, alta disponibilidad", "SIGUIENTE", "next"),
         ("04", "Cloud Architect", "Landing zones, redes híbridas, Well-Architected", "OBJETIVO", "goal")]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Roadmap: 01 Fundamentos (completado), 02 Nube e IaC (en curso), 03 Plataforma y operación (siguiente), 04 Cloud Architect (objetivo)">']
    o += frame(W, H, "") + dust(W, H, 80, 3) + CLOUD(700, 150)[:0]
    cw = (W - 56) / 4; Y = 56
    xs = [28 + cw * i + cw / 2 for i in range(4)]
    o.append(f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[3]}" y2="{Y}" stroke="#272727" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<line x1="{xs[0]}" y1="{Y}" x2="{xs[0]}" y2="{Y}" stroke="#f2f2f2" stroke-width="3" stroke-linecap="round"><animate attributeName="x2" values="{xs[0]};{xs[1]}" dur="1.2s" begin=".4s" fill="freeze"/></line>')
    o.append(f'<line x1="{xs[1]}" y1="{Y}" x2="{xs[1]}" y2="{Y}" stroke="#f2f2f2" stroke-opacity=".5" stroke-width="3" stroke-linecap="round" stroke-dasharray="2 8"><animate attributeName="x2" values="{xs[1]};{xs[1]+70}" dur="1s" begin="1.7s" fill="freeze"/></line>')
    for i, (n, t, f, st, kind) in enumerate(S):
        x = xs[i]; cx0 = 28 + cw * i + 6
        # node
        if kind == "done":
            o.append(f'<circle cx="{x}" cy="{Y}" r="18" fill="#0a0a0a" stroke="#272727" stroke-width="2"/><circle cx="{x}" cy="{Y}" r="0" fill="#f2f2f2"><animate attributeName="r" values="0;20;18" keyTimes="0;.6;1" dur=".45s" begin=".3s" fill="freeze"/></circle><path d="M{x-7} {Y+1}l5 5L{x+8} {Y-6}" fill="none" stroke="#000" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" opacity="0"><set attributeName="opacity" to="1" begin=".5s" fill="freeze"/></path>')
        elif kind == "now":
            o.append(f'<circle cx="{x}" cy="{Y}" r="18" fill="#0a0a0a" stroke="#272727" stroke-width="2"/><g transform="translate({x} {Y})" opacity="0"><set attributeName="opacity" to="1" begin="1.6s" fill="freeze"/><circle r="18" fill="none" stroke="#f2f2f2" stroke-width="3" stroke-linecap="round" stroke-dasharray="28 90"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="1.1s" repeatCount="indefinite"/></circle></g>')
        else:
            o.append(f'<circle cx="{x}" cy="{Y}" r="18" fill="#0a0a0a" stroke="#4a4a4a" stroke-width="2" stroke-dasharray="4 4"/>')
        # card
        d = "" if kind in ("done", "now") else ' stroke-dasharray="4 4"'
        sc = {"done": "#f2f2f2", "now": "#f2f2f2", "next": "#6a6a6a", "goal": "#6a6a6a"}[kind]
        o.append(f'<rect x="{cx0}" y="100" width="{cw-12:.0f}" height="170" rx="12" fill="#050505" stroke="{sc}" stroke-opacity="{ .5 if kind in ("done","now") else .6}"{d}/>')
        o.append(f'<text x="{cx0+14}" y="128" font-family="{MONO}" font-size="12" letter-spacing="2" fill="#6a6a6a">{n}</text>')
        o.append(f'<text x="{cx0+14}" y="152" font-family="{SANS}" font-weight="800" font-size="{13 if len(t) > 18 else 16}" fill="{"#f2f2f2" if kind in ("done","now") else "#9a9a9a"}">{esc(t)}</text>')
        for j, ln in enumerate(textwrap.wrap(f, 24)[:4]): o.append(f'<text x="{cx0+14}" y="{176+j*17}" font-family="{MONO}" font-size="11" fill="#6a6a6a">{esc(ln)}</text>')
        o.append(f'<text x="{cx0+14}" y="256" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="2" fill="{"#f2f2f2" if kind in ("done","now") else "#6a6a6a"}">{st}</text>')
    o.append('</svg>')
    return o
save("roadmap", roadmap())

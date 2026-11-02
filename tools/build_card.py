# Builds assets/card.svg (ID card that flips) and assets/stats.svg (counters) for the profile README.
# usage: python build_card.py <portrait.webp> <out_dir>
import base64, sys
MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
portrait = base64.b64encode(open(sys.argv[1], "rb").read()).decode()
OUT = sys.argv[2]

# ---------------- 1. ID card that flips ----------------
def card():
    W, H = 360, 500
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tarjeta ID de Gary Flores: Systems Engineer en Sothis (PLM), Barcelona">']
    o.append('<defs><clipPath id="ph"><rect x="30" y="86" width="300" height="270" rx="12"/></clipPath></defs>')
    flip = 'dur="11s" repeatCount="indefinite"'
    o.append(f'<g transform="translate({W/2} 0)"><g><animateTransform attributeName="transform" type="scale" calcMode="linear" {flip} keyTimes="0;.36;.405;.45;.86;.905;.95;1" values="1 1;1 1;0 1;1 1;1 1;0 1;1 1;1 1"/>')
    o.append(f'<g transform="translate({-W/2} 0)">')
    # ---- front
    o.append('<g><animate attributeName="opacity" '+flip+' keyTimes="0;.40;.401;.90;.901;1" values="1;1;0;0;1;1"/>')
    o.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="#050505" stroke="#272727" stroke-width="3"/>')
    o.append(f'<rect x="{W/2-34}" y="14" width="68" height="14" rx="7" fill="#1a1a1a" stroke="#272727"/>')
    o.append(f'<image x="30" y="86" width="300" height="270" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)" xlink:href="data:image/webp;base64,{portrait}"/>')
    o.append(f'<text x="30" y="394" font-family="{SANS}" font-weight="800" font-size="34" letter-spacing="-1" fill="#f2f2f2">Gary Flores</text>')
    o.append(f'<text x="30" y="418" font-family="{MONO}" font-size="12" letter-spacing="2.5" fill="#9a9a9a">SYSTEMS ENGINEER</text>')
    o.append(f'<text x="30" y="446" font-family="{MONO}" font-size="12" fill="#6a6a6a">Sothis · PLM · Barcelona</text>')
    for i in range(34):
        w = 2 if i % 3 else 4
        o.append(f'<rect x="{30+i*8.8:.1f}" y="462" width="{w}" height="20" fill="#f2f2f2" opacity=".8"/>')
    o.append('</g>')
    # ---- back
    o.append('<g opacity="0"><animate attributeName="opacity" '+flip+' keyTimes="0;.40;.401;.90;.901;1" values="0;0;1;1;0;0"/>')
    o.append(f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="22" fill="#050505" stroke="#f2f2f2" stroke-opacity=".5" stroke-width="3"/>')
    o.append(f'<text x="30" y="64" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#9a9a9a">STACK EN USO</text>')
    chips = ["Teamcenter", "Tecnomatix", "Azure DevOps", "Tomcat", "SQL Server", "Windows Server", "Active Directory"]
    x, y = 30, 96
    for c in chips:
        w = len(c) * 8.4 + 22
        if x + w > W - 30: x, y = 30, y + 38
        o.append(f'<rect x="{x}" y="{y-18}" width="{w:.0f}" height="28" rx="14" fill="none" stroke="#f2f2f2" stroke-opacity=".6"/><text x="{x+11}" y="{y}" font-family="{MONO}" font-size="13" fill="#f2f2f2">{c}</text>')
        x += w + 8
    y += 64
    o.append(f'<text x="30" y="{y}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="#9a9a9a">APRENDIENDO</text>')
    y += 32; x = 30
    for c in ["Azure", "AWS", "Terraform", "Kubernetes"]:
        w = len(c) * 8.4 + 22
        if x + w > W - 30: x, y = 30, y + 38
        o.append(f'<rect x="{x}" y="{y-18}" width="{w:.0f}" height="28" rx="14" fill="none" stroke="#6a6a6a" stroke-dasharray="3 3"/><text x="{x+11}" y="{y}" font-family="{MONO}" font-size="13" fill="#9a9a9a">{c}</text>')
        x += w + 8
    o.append(f'<text x="30" y="{H-48}" font-family="{MONO}" font-size="12" fill="#6a6a6a">es · ca · en</text>')
    o.append(f'<text x="30" y="{H-28}" font-family="{SANS}" font-weight="700" font-size="16" fill="#f2f2f2">Next: Cloud Architect →</text>')
    o.append('</g></g></g></g></svg>')
    return "\n".join(o)

# ---------------- 3. stats counting up ----------------
def stats():
    W, H = 720, 150
    S = [(3, "+", "AÑOS EN PRODUCCIÓN"), (20, "+", "TECNOLOGÍAS"), (3, "", "IDIOMAS")]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Más de 3 años en producción, más de 20 tecnologías y 3 idiomas">']
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#000" stroke="#272727" stroke-width="2"/>')
    N = 16; col = (W - 40) / 3
    for k, (v, suf, lab) in enumerate(S):
        cx = 20 + col * k + col / 2
        if k: o.append(f'<line x1="{20+col*k}" y1="30" x2="{20+col*k}" y2="{H-30}" stroke="#272727"/>')
        t0 = .4 + k * .25
        for i in range(N + 1):
            e = 1 - (1 - i / N) ** 3
            val = round(v * e) if v < 100 else round(2000 + (v - 2000) * e)
            begin = t0 + i * .07; last = i == N
            end = '' if last else f' end="{t0+(i+1)*.07:.2f}s"'
            o.append(f'<text x="{cx:.0f}" y="82" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="52" letter-spacing="-2" fill="#f2f2f2" opacity="0">{val}<tspan fill="#9a9a9a">{suf}</tspan><set attributeName="opacity" to="1" begin="{begin:.2f}s"{end} fill="{"freeze" if last else "remove"}"/></text>')
        o.append(f'<text x="{cx:.0f}" y="116" text-anchor="middle" font-family="{MONO}" font-size="11" letter-spacing="2" fill="#9a9a9a">{lab}</text>')
    o.append('</svg>')
    return "\n".join(o)


for name, fn in (("card", card), ("stats", stats)):
    s = fn(); open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(s); print(name, len(s) // 1024, "KB")

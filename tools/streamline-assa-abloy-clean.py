with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 优化注意力体系为 ASSA ABLOY 工业克制风：
# 1. 彻底移除花哨的渐变蓝阴影和放大缩放动画
# 2. 采用纯正 ASSA ABLOY 极简工业线条：白底、深灰文字、清晰细边框
old_attention = """.gallery-portal-card--core {
  border: 1.5px solid #2563eb !important;
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.12) !important;
  opacity: 1 !important;
  transform: scale(1.01);
}
.gallery-portal-card--core:hover {
  border-color: #1d4ed8 !important;
  box-shadow: 0 16px 32px rgba(37, 99, 235, 0.22) !important;
  transform: translateY(-6px) scale(1.02) !important;
}

/* Tier 2 Secondary Divisions: Subdued, De-emphasised, Muted Neutral Tone */
.gallery-portal-card--secondary {
  border: 1px solid #e2e8f0 !important;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
  opacity: 0.88;
  background: #f8fafc !important;
}
.gallery-portal-card--secondary .gallery-portal-card__img {
  filter: grayscale(18%) contrast(95%);
  transition: filter .3s ease, transform .3s ease;
}
.gallery-portal-card--secondary:hover {
  opacity: 1;
  border-color: #94a3b8 !important;
  box-shadow: 0 8px 18px rgba(15, 23, 42, 0.08) !important;
  transform: translateY(-4px) !important;
}
.gallery-portal-card--secondary:hover .gallery-portal-card__img {
  filter: grayscale(0%) contrast(100%);
}

/* Core Baseline Floating Badge */
.portal-tier-pill {
  position: absolute;
  top: 10px;
  left: 10px;
  z-index: 10;
  font-size: 0.68rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  padding: 3px 8px;
  border-radius: 4px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.18);
}
.portal-tier-pill--core {
  background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
  color: #ffffff;
  border: 1px solid rgba(255,255,255,0.3);
}"""

new_attention = """/* ASSA ABLOY Minimalist Industrial Aesthetics (克制、严谨、少即是多) */
.gallery-portal-card--core {
  border: 1.5px solid #0f172a !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06) !important;
  opacity: 1 !important;
}
.gallery-portal-card--core:hover {
  border-color: #2563eb !important;
  box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1) !important;
  transform: translateY(-3px) !important;
}

/* Tier 2 Secondary: Muted Industrial Gray, Clean Neutral */
.gallery-portal-card--secondary {
  border: 1px solid #e2e8f0 !important;
  box-shadow: none !important;
  opacity: 0.92;
  background: #ffffff !important;
}
.gallery-portal-card--secondary .gallery-portal-card__img {
  filter: grayscale(12%);
  transition: filter .2s ease;
}
.gallery-portal-card--secondary:hover {
  opacity: 1;
  border-color: #cbd5e1 !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06) !important;
  transform: translateY(-2px) !important;
}
.gallery-portal-card--secondary:hover .gallery-portal-card__img {
  filter: none;
}

/* Core Baseline: Minimalist Monospaced Tag */
.portal-tier-pill {
  position: absolute;
  top: 8px;
  left: 8px;
  z-index: 10;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 2px 6px;
  border-radius: 3px;
}
.portal-tier-pill--core {
  background: #0f172a;
  color: #ffffff;
  border: none;
}"""

if old_attention in css:
    css = css.replace(old_attention, new_attention)
    with open('assets/css/site.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Streamlined attention CSS to ASSA ABLOY minimalist industrial aesthetic!")


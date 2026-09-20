import re

css_addition = """
/* ==========================================================================
   ASSA ABLOY Industrial Specification Cards & Patent Layout
   ========================================================================== */
.spec-hero-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  padding: 10px 16px;
  background: #f8fafc;
  border-left: 3px solid #0B1D47;
  border-radius: 4px;
  margin: 14px 0 24px;
  font-size: 0.82rem;
  color: #334155;
}
.spec-hero-meta span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.spec-topic-nav {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin: 0 0 28px;
}
@media (max-width: 860px) {
  .spec-topic-nav {
    grid-template-columns: repeat(2, 1fr);
  }
}
.spec-topic-pill {
  display: block;
  padding: 8px 10px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  text-decoration: none;
  color: #0f172a;
  transition: all 0.2s ease;
  text-align: center;
}
.spec-topic-pill:hover {
  border-color: #0B1D47;
  background: #f8fafc;
  transform: translateY(-1px);
}
.spec-topic-pill__num {
  display: block;
  font-size: 0.68rem;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 2px;
}
.spec-topic-pill__title {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  color: #0f172a;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.spec-card {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  margin: 20px 0 32px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}
.spec-card__header {
  padding: 12px 18px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.spec-card__title {
  margin: 0;
  font-size: 0.96rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.01em;
}
.spec-card__badge {
  font-size: 0.70rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 3px;
  white-space: nowrap;
}
.spec-card__badge--red {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}
.spec-card__badge--green {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}
.spec-card__badge--blue {
  background: #e0f2fe;
  color: #0369a1;
  border: 1px solid #bae6fd;
}
.spec-card__body {
  padding: 18px;
}

.spec-grid-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 16px;
}
@media (max-width: 720px) {
  .spec-grid-2col {
    grid-template-columns: 1fr;
  }
}
.spec-box-risk {
  background: #fff5f5;
  border: 1px solid #fed7d7;
  border-radius: 4px;
  padding: 12px 14px;
}
.spec-box-solution {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 4px;
  padding: 12px 14px;
}
.spec-box__label {
  font-size: 0.74rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.spec-box-risk .spec-box__label {
  color: #991b1b;
}
.spec-box-solution .spec-box__label {
  color: #166534;
}
.spec-box__text {
  font-size: 0.82rem;
  line-height: 1.5;
  color: #334155;
  margin: 0;
}
.spec-box__text b {
  color: #0f172a;
}
"""

with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    css = f.read()

if 'spec-topic-nav' not in css:
    css += '\n' + css_addition
    with open('assets/css/site.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print('Updated assets/css/site.css with spec components.')
else:
    print('assets/css/site.css already contains spec components.')

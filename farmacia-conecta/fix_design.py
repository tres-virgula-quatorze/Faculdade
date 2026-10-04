import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Blur filter to all elements that have opacity mapped to getOp
def add_blur(m):
    op_call = m.group(1) # e.g. "t, 0.15"
    return f'opacity: {{getOp({op_call})}}; filter: blur({{getBlur({op_call})}}px);'

content = re.sub(r'opacity:\s*\{getOp\((.*?)\)\};', add_blur, content)

# 2. Inject decorative SVGs after <div class="slide-inner">
deco_html = '''
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxRight(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, 1)}deg);" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="3"><circle cx="12" cy="12" r="9"/></svg>
      <svg class="deco deco-3" style="opacity: {getOp(t, 0.45)}; transform: translate({getTxRight(t, 0.45)}px, {getTy(t, 0.45)}px) rotate({getRotate(t, 0.45, 1)}deg);" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
'''
content = re.sub(r'<div class="slide-inner">', f'<div class="slide-inner">\n{deco_html}', content)

# 3. Add CSS classes for .deco
css_inject = '''
  .deco { position: absolute; pointer-events: none; z-index: -1; }
  .deco-1 { top: -2rem; right: -3rem; }
  .deco-2 { bottom: 2rem; left: -4rem; }
  .deco-3 { top: 40%; right: -5rem; }
'''
content = content.replace('/* ===== Slide base ===== */', css_inject + '\n  /* ===== Slide base ===== */')

# 4. Tweak padding, gap and fonts for minimalism
content = re.sub(
    r'padding: clamp\(3rem, 6vh, 4rem\) clamp\(1rem, 4vw, 3rem\);',
    r'padding: clamp(2.5rem, 5vh, 3.5rem) clamp(1rem, 3vw, 2.5rem);',
    content
)
content = re.sub(
    r'gap: clamp\(1rem, 2vh, 1\.8rem\);',
    r'gap: clamp(0.9rem, 1.8vh, 1.5rem);',
    content
)
content = re.sub(
    r'font-size: clamp\(1\.4rem, 2\.8vw, 2\.2rem\);',
    r'font-size: clamp(1.25rem, 2.2vw, 1.8rem);',
    content
)
content = re.sub(
    r'font-size: clamp\(0\.85rem, 1vw, 1rem\);',
    r'font-size: clamp(0.8rem, 0.9vw, 0.95rem);',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

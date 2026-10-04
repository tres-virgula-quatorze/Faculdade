import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

script_inject = '''
  function getT(phaseIndex) {
    const start = phaseIndex / 10;
    const end = (phaseIndex + 1) / 10;
    const center = (start + end) / 2;
    return (currentRatio - center) / 0.05; 
  }

  function getOp(t, delay = 0) {
    const adjustedT = t > 0 ? t - delay * 2 : t + delay * 2;
    const absT = Math.abs(adjustedT);
    if (absT >= 1) return 0;
    if (absT <= 0.4) return 1;
    return (1 - absT) / 0.6;
  }

  function getTy(t, delay = 0) {
    const adjustedT = t > 0 ? t - delay * 2 : t + delay * 2;
    if (adjustedT < -0.4) return Math.pow(Math.abs(adjustedT + 0.4), 1.5) * 150;
    if (adjustedT > 0.4) return -Math.pow(Math.abs(adjustedT - 0.4), 1.5) * 150;
    return 0;
  }

  function getTxLeft(t, delay = 0) {
    const adjustedT = t > 0 ? t - delay * 2 : t + delay * 2;
    if (adjustedT < -0.4) return -Math.pow(Math.abs(adjustedT + 0.4), 1.5) * 200;
    if (adjustedT > 0.4) return Math.pow(Math.abs(adjustedT - 0.4), 1.5) * 200;
    return 0;
  }

  function getTxRight(t, delay = 0) {
    const adjustedT = t > 0 ? t - delay * 2 : t + delay * 2;
    if (adjustedT < -0.4) return Math.pow(Math.abs(adjustedT + 0.4), 1.5) * 200;
    if (adjustedT > 0.4) return -Math.pow(Math.abs(adjustedT - 0.4), 1.5) * 200;
    return 0;
  }

  function getScale(t, delay = 0) {
    const adjustedT = t > 0 ? t - delay * 2 : t + delay * 2;
    if (adjustedT < -0.4) return 1 - Math.abs(adjustedT + 0.4) * 0.3;
    if (adjustedT > 0.4) return 1 - Math.abs(adjustedT - 0.4) * 0.3;
    return 1;
  }
'''
content = content.replace('const slideIds =', script_inject + '\n  const slideIds =')

def replace_section(m):
    classes = m.group(1)
    phase = m.group(2)
    return f'{{@const t = getT({phase})}}\n<section id="slide-{int(phase)+1}" {classes} style="opacity: {{getOp(t)}}; pointer-events: {{Math.abs(t) < 0.9 ? \'auto\' : \'none\'}}; z-index: {{Math.abs(t) < 1 ? 2 : 1}};">'

content = re.sub(r'<section id="slide-\d+" (class="[^"]*") class:vis=\{activePhase === (\d+)\}>', replace_section, content)

def process_rv_tags():
    global content
    pattern = r'<([a-zA-Z0-9]+)([^>]*)class="([^"]*rv[^"]*)"([^>]*)>'
    
    def replacer(m):
        tag = m.group(1)
        pre = m.group(2)
        classes = m.group(3)
        post = m.group(4)
        
        delay = 0
        style_match = re.search(r'style="[^"]*--d:\s*([\d\.]+)s[^"]*"', pre + post)
        if style_match:
            delay = float(style_match.group(1))
            
        anim = 'getTy'
        if 'rv-l' in classes: anim = 'getTxLeft'
        elif 'rv-r' in classes: anim = 'getTxRight'
        elif 'rv-up' in classes: anim = 'getTy'
        elif 'rv-zoom' in classes: anim = 'getScale'
        
        classes = re.sub(r'\s*\brv(-[a-z]+)?\b\s*', ' ', classes).strip()
        classes = ' '.join(classes.split())
        
        if anim == 'getScale':
            new_style = f'opacity: {{getOp(t, {delay})}}; transform: scale({{getScale(t, {delay})}}) translateY({{getTy(t, {delay})}}px);'
        elif anim in ['getTxLeft', 'getTxRight']:
            new_style = f'opacity: {{getOp(t, {delay})}}; transform: translateX({{{anim}(t, {delay})}}px);'
        else:
            new_style = f'opacity: {{getOp(t, {delay})}}; transform: translateY({{{anim}(t, {delay})}}px);'
            
        pre = re.sub(r'\s*style="[^"]*"\s*', ' ', pre)
        post = re.sub(r'\s*style="[^"]*"\s*', ' ', post)
        pre = re.sub(r'\s*class:(pulse|glow)=\{[^\}]+\}\s*', ' ', pre)
        post = re.sub(r'\s*class:(pulse|glow)=\{[^\}]+\}\s*', ' ', post)
        
        return f'<{tag}{pre}class="{classes}" style="{new_style}"{post}>'
        
    content = re.sub(pattern, replacer, content)

process_rv_tags()

# Clean up leftover transition properties in style section
content = re.sub(r'\.slide \{[^}]*?transition:[^}]*?\}', lambda m: m.group(0).replace('transition: opacity 0.6s ease, visibility 0.6s ease;', ''), content)

# Remove the rv classes definitions
content = re.sub(r'/\* ===== Reveal on scroll ===== \*/.*?(?=\/\* ===== Cards ===== \*\/)', '', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

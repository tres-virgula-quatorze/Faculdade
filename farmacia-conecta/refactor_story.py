import re

# --- 1. Modify About.svelte ---
about_file = 'src/lib/components/About.svelte'
with open(about_file, 'r', encoding='utf-8') as f:
    about_content = f.read()

# Replace the corner-element logic
old_corner_logic = """    // Apply class to corner elements for CSS effects
    [434, 595, 590, 567, 562, 545, 304, 435, 668, 842].forEach(ind => {
      if (layers[ind]) {
        layers[ind].cl = "corner-element";
      }
    });"""

new_corner_logic = """    // Classify elements for CSS scroll animations
    if (layers[842]) layers[842].cl = "lottie-title";
    if (layers[756]) layers[756].cl = "lottie-seminario";
    if (layers[4]) layers[4].cl = "lottie-seminario";
    if (layers[13]) layers[13].cl = "lottie-integrantes";

    [434, 595, 590, 567, 562, 545, 304, 435, 668].forEach(ind => {
      if (layers[ind]) {
        layers[ind].cl = "corner-element";
      }
    });"""

about_content = about_content.replace(old_corner_logic, new_corner_logic)

# Replace the div.lottie-fullscreen styles
old_div = """      <div 
        bind:this={lottieContainer} 
        class="lottie-fullscreen"
        class:is-ready={!isLoading && !hasError}
        style="opacity: {activePhase === 0 ? 1 : 0}; pointer-events: {activePhase === 0 ? 'auto' : 'none'}; transition: opacity 0.5s ease; --corner-blur: {transitionProgress * 6}px; --corner-opacity: {1 - (transitionProgress * 0.7)};"
      ></div>"""

new_div = """      <div 
        bind:this={lottieContainer} 
        class="lottie-fullscreen"
        class:is-ready={!isLoading && !hasError}
        style="
          opacity: 1; pointer-events: {activePhase === 0 ? 'auto' : 'none'};
          --title-op: {currentScrollRatio < 0.05 ? 1 : Math.max(0, 1 - (currentScrollRatio - 0.05) * 20)};
          --title-ty: {currentScrollRatio < 0.05 ? 0 : -(currentScrollRatio - 0.05) * 1500}px;
          --seminario-op: {currentScrollRatio < 0.12 ? 1 : Math.max(0, 1 - (currentScrollRatio - 0.12) * 20)};
          --seminario-ty: {currentScrollRatio < 0.12 ? 0 : -(currentScrollRatio - 0.12) * 1500}px;
          --integrantes-op: {currentScrollRatio < 0.18 ? 1 : Math.max(0, 1 - (currentScrollRatio - 0.18) * 20)};
          --integrantes-tx: {currentScrollRatio < 0.18 ? 0 : (currentScrollRatio - 0.18) * 1000}px;
          --corner-opacity: {currentScrollRatio > 0.95 ? Math.max(0, 1 - (currentScrollRatio - 0.95) * 20) : 1};
        "
      ></div>"""

about_content = about_content.replace(old_div, new_div)

# Add CSS rules to the style section
css_addition = """
  .lottie-fullscreen :global(.lottie-title) {
    opacity: var(--title-op);
    transform: translateY(var(--title-ty));
  }
  .lottie-fullscreen :global(.lottie-seminario) {
    opacity: var(--seminario-op);
    transform: translateY(var(--seminario-ty));
  }
  .lottie-fullscreen :global(.lottie-integrantes) {
    opacity: var(--integrantes-op);
    transform: translateX(var(--integrantes-tx));
  }
  .lottie-fullscreen :global(.corner-element) {
    opacity: var(--corner-opacity);
  }
"""
# Remove old corner-element styles
about_content = re.sub(r'\.lottie-fullscreen :global\(\.corner-element\) \{.*?\}', '', about_content, flags=re.DOTALL)
about_content = about_content.replace('</style>', css_addition + '</style>')

with open(about_file, 'w', encoding='utf-8') as f:
    f.write(about_content)


# --- 2. Modify Slides.svelte ---
slides_file = 'src/lib/components/Slides.svelte'
with open(slides_file, 'r', encoding='utf-8') as f:
    slides_content = f.read()

# Replace <section class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); ...">
# with <section class="slide" style="pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
# across all slides!

slides_content = re.sub(
    r'<section id="slide-(\d+)" class="(slide.*?)" style="opacity: \{getOp\(t\)\}; filter: blur\(\{getBlur\(t\)\}px\); pointer-events: \{Math\.abs\(t\) < 0\.9 \? \'auto\' : \'none\'\}; z-index: \{Math\.abs\(t\) < 1 \? 2 : 1\};">',
    r'<section id="slide-\1" class="\2" style="pointer-events: {Math.abs(t) < 0.9 ? \'auto\' : \'none\'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">',
    slides_content
)

# For Slide 2, we can make the corner frames only appear smoothly
slide2_frames = """      <!-- ELEMENTOS DE MOLDURA (Frame) -->
      <div class="abs top-left" style="top: 4vh; left: 4vw; opacity: {getOp(t, 0.05)}; transform: translateY({Math.abs(t)*-20}px);">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">02 / Conceitos Fundamentais</p>
      </div>
      <div class="abs top-right" style="top: 4vh; right: 4vw; opacity: {getOp(t, 0.05)}; transform: translateY({Math.abs(t)*-20}px); text-align: right;">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">Telefarmácia no Brasil</p>
      </div>
      <div class="abs bottom-left" style="bottom: 4vh; left: 4vw; opacity: {getOp(t, 0.1)}; transform: translateY({Math.abs(t)*20}px);">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">+ Resoluções CFF</p>
      </div>
      <div class="abs bottom-right" style="bottom: 4vh; right: 4vw; opacity: {getOp(t, 0.1)}; transform: translateY({Math.abs(t)*20}px); text-align: right;">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">Legislação</p>
      </div>"""

slides_content = re.sub(
    r'<!-- ELEMENTOS DE MOLDURA \(Frame\) IDÊNTICOS AO SLIDE 1 -->.*?</div>.*?</div>.*?</div>.*?</div>',
    slide2_frames,
    slides_content,
    flags=re.DOTALL
)

with open(slides_file, 'w', encoding='utf-8') as f:
    f.write(slides_content)

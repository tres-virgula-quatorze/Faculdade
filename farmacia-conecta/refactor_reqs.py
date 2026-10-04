import re

# 1. Update About.svelte to move the names down
about_file = 'src/lib/components/About.svelte'
with open(about_file, 'r', encoding='utf-8') as f:
    about_content = f.read()

about_content = about_content.replace(
    'const intY = Math.max(midY + 20 * scale, Math.min(targetH * 0.65, targetH - marginBot - intHeight - 15));',
    'const intY = targetH - marginBot - intHeight - (20 * (scale / 0.38));'
)

with open(about_file, 'w', encoding='utf-8') as f:
    f.write(about_content)


# 2. Update Slides.svelte
slides_file = 'src/lib/components/Slides.svelte'
with open(slides_file, 'r', encoding='utf-8') as f:
    slides_content = f.read()

# Delete slide-nav
slides_content = re.sub(r'<nav class="slide-nav" aria-label="Navegação dos slides">.*?</nav>', '', slides_content, flags=re.DOTALL)

# Completely rewrite Slide 2
slide_2_new = """  <!-- SLIDE 2 -->
  {#if true}
  {@const t = getT(1)}
  <section id="slide-2" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout" style="perspective: 1200px;">
      
      <!-- BACKGROUND: Formas geométricas lúdicas gigantes (Flat Design) -->
      <!-- Círculo que expande -->
      <div class="abs center" style="width: 120vh; height: 120vh; border-radius: 50%; background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 70%); transform: translate(-50%, -50%) scale({getScale(t, 0.4)}); opacity: {getOp(t, 0)}; pointer-events: none;"></div>
      
      <!-- Arco que rotaciona e entra do lado -->
      <svg class="abs" style="top: 10%; right: -10%; transform: translateX({getTxRight(t, 0.3)}px) rotate({getRotate(t, 0.3, 2)}deg); opacity: {getOp(t, 0.1)};" width="500" height="500" viewBox="0 0 100 100" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="2">
        <path d="M 10 50 A 40 40 0 0 1 90 50" />
        <circle cx="90" cy="50" r="3" fill="rgba(255,255,255,0.04)" />
      </svg>
      
      <!-- Cruzeta que entra pela esquerda -->
      <svg class="abs" style="bottom: 20%; left: 5%; transform: translateX({getTxLeft(t, 0.2)}px) rotate({getRotate(t, 0.2, -1.5)}deg); opacity: {getOp(t, 0.15)};" width="200" height="200" viewBox="0 0 100 100" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1.5">
        <line x1="50" y1="20" x2="50" y2="80" />
        <line x1="20" y1="50" x2="80" y2="50" />
      </svg>
      
      <!-- ELEMENTOS DE MOLDURA (Frame) IDÊNTICOS AO SLIDE 1 -->
      <div class="abs top-left" style="top: 4vh; left: 4vw; opacity: {getOp(t, 0.05)}; transform: translateX({getTxLeft(t, 0.05)}px);">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">02 / Conceitos Fundamentais</p>
      </div>
      <div class="abs top-right" style="top: 4vh; right: 4vw; opacity: {getOp(t, 0.05)}; transform: translateX({getTxRight(t, 0.05)}px); text-align: right;">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">Telefarmácia no Brasil</p>
      </div>
      <div class="abs bottom-left" style="bottom: 4vh; left: 4vw; opacity: {getOp(t, 0.1)}; transform: translateY({getTy(t, 0.1)}px);">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">+ Resoluções CFF</p>
      </div>
      <div class="abs bottom-right" style="bottom: 4vh; right: 4vw; opacity: {getOp(t, 0.1)}; transform: translateY({getTy(t, 0.1)}px); text-align: right;">
        <p style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.15em; color: rgba(255,255,255,0.7);">Legislação</p>
      </div>
      
      <!-- TÍTULO GIGANTE 3D -->
      <div class="abs w-100" style="top: 25vh; left: 50%; transform: translate(-50%, {t * -50}px) scale({getScale(t, 0)}); text-align: center; padding: 0 4vw;">
        <h2 style="font-size: clamp(2.2rem, 4.5vw, 4rem); font-weight: 400; line-height: 1.15; color: var(--color-white); letter-spacing: -0.02em; opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          O que Define a <br>
          <strong style="font-weight: 800;">Telefarmácia no Brasil?</strong>
        </h2>
        <p style="margin-top: 1.5rem; font-size: clamp(1rem, 1.3vw, 1.25rem); font-weight: 500; color: rgba(255,255,255,0.9); opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px); letter-spacing: 0.05em; text-transform: uppercase;">
          Exercício Clínico <span style="opacity: 0.4; margin: 0 0.8em; font-weight: 300;">|</span> Mero Comércio
        </p>
      </div>

      <!-- LINHA DIVISÓRIA CENTRAL ANIMADA -->
      <div class="abs center" style="width: 1px; height: 30vh; background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.5), rgba(255,255,255,0)); top: 70%; transform: translate(-50%, -50%) scaleY({getScale(t, 0.15)}); opacity: {getOp(t, 0.15)};"></div>

      <!-- TEXTO RODAPÉ ESQUERDA: PERMISSÃO -->
      <div class="abs" style="bottom: 12vh; left: 8vw; width: 38vw; transform: translateX({getTxLeft(t, 0.2)}px) translateY({Math.abs(t) * 30}px);">
        <div style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); text-align: right; padding-right: 2.5rem; position: relative;">
          <!-- 01 Gigante de Fundo (Ludic text) -->
          <span style="position: absolute; right: 0; top: -50%; font-size: 10rem; font-weight: 900; color: rgba(255,255,255,0.03); line-height: 1; pointer-events: none; z-index: -1;">01</span>
          
          <h3 style="font-size: clamp(1.1rem, 1.4vw, 1.4rem); font-weight: 700; color: var(--color-white); margin-bottom: 0.8rem; display: flex; align-items: center; justify-content: flex-end; gap: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
            Exercício Clínico
            <span style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: rgba(74, 222, 128, 0.15); color: #4ade80;">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
            </span>
          </h3>
          <p style="font-size: clamp(0.9rem, 1vw, 1rem); color: rgba(255,255,255,0.75); line-height: 1.6; font-weight: 400; max-width: 420px; margin-left: auto;">
            A telefarmácia é um ato de saúde. O foco é a avaliação clínica, o acompanhamento farmacoterapêutico e a melhoria da qualidade de vida do paciente, utilizando TICs.
          </p>
        </div>
      </div>

      <!-- TEXTO RODAPÉ DIREITA: PROIBIÇÃO -->
      <div class="abs" style="bottom: 12vh; right: 8vw; width: 38vw; transform: translateX({getTxRight(t, 0.2)}px) translateY({Math.abs(t) * 30}px);">
        <div style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); padding-left: 2.5rem; position: relative;">
          <!-- 02 Gigante de Fundo (Ludic text) -->
          <span style="position: absolute; left: 0; top: -50%; font-size: 10rem; font-weight: 900; color: rgba(255,255,255,0.03); line-height: 1; pointer-events: none; z-index: -1;">02</span>
          
          <h3 style="font-size: clamp(1.1rem, 1.4vw, 1.4rem); font-weight: 700; color: var(--color-white); margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
            <span style="display: flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; background: rgba(248, 113, 113, 0.15); color: #f87171;">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
            </span>
            Mero Comércio
          </h3>
          <p style="font-size: clamp(0.9rem, 1vw, 1rem); color: rgba(255,255,255,0.75); line-height: 1.6; font-weight: 400; max-width: 420px;">
            Não se confunde com a simples venda online de medicamentos ou dispensação sem contato clínico prévio. A venda de balcão via internet NÃO é telefarmácia clínica.
          </p>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

slides_content = re.sub(r'<!-- SLIDE 2 -->.*?{/if}', slide_2_new, slides_content, flags=re.DOTALL)

with open(slides_file, 'w', encoding='utf-8') as f:
    f.write(slides_content)

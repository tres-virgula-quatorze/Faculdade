import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

slide_2 = """  <!-- SLIDE 2 -->
  {#if true}
  {@const t = getT(1)}
  <section id="slide-2" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decorações Lottie-style (círculos e cruzes vazadas, rodando devagar) -->
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.2)}; transform: translate({getTxRight(t, 0.2)}px, {getTy(t, 0.2)}px) rotate({getRotate(t, 0.2, 1)}deg);" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="0.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxLeft(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, -1)}deg);" width="140" height="140" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="0.5"><circle cx="12" cy="12" r="11"/></svg>

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
      
      <!-- TÍTULO GIGANTE CENTRALIZADO -->
      <div class="abs w-100" style="top: 30vh; left: 50%; transform: translateX(-50%) translateY({getTy(t, 0)}px); text-align: center; padding: 0 4vw;">
        <h2 style="font-size: clamp(2.2rem, 4.5vw, 4rem); font-weight: 400; line-height: 1.15; color: var(--color-white); letter-spacing: -0.02em; opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          O que Define a <br>
          <strong style="font-weight: 800;">Telefarmácia no Brasil?</strong>
        </h2>
        <p style="margin-top: 1.5rem; font-size: clamp(1rem, 1.3vw, 1.25rem); font-weight: 500; color: rgba(255,255,255,0.9); opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px); letter-spacing: 0.05em; text-transform: uppercase;">
          Exercício Clínico <span style="opacity: 0.4; margin: 0 0.8em; font-weight: 300;">|</span> Mero Comércio
        </p>
      </div>

      <!-- LINHA DIVISÓRIA CENTRAL -->
      <div class="abs center" style="width: 1px; height: 18vh; background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0.3), rgba(255,255,255,0)); top: 75%; transform: translate(-50%, -50%) scaleY({getScale(t, 0.15)}); opacity: {getOp(t, 0.15)};"></div>

      <!-- TEXTO RODAPÉ ESQUERDA: PERMISSÃO -->
      <div class="abs" style="bottom: 12vh; left: 8vw; width: 38vw; transform: translateX({getTxLeft(t, 0.2)}px);">
        <div style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); text-align: right; padding-right: 2rem;">
          <h3 style="font-size: clamp(1rem, 1.2vw, 1.2rem); font-weight: 700; color: var(--color-white); margin-bottom: 0.8rem; display: flex; align-items: center; justify-content: flex-end; gap: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
            Exercício Clínico
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #4ade80;"><path d="M20 6 9 17l-5-5"/></svg>
          </h3>
          <p style="font-size: clamp(0.85rem, 0.95vw, 0.95rem); color: rgba(255,255,255,0.7); line-height: 1.6; font-weight: 400; max-width: 400px; margin-left: auto;">
            A telefarmácia é um ato de saúde. O foco é a avaliação clínica, o acompanhamento farmacoterapêutico e a melhoria da qualidade de vida do paciente, utilizando TICs.
          </p>
        </div>
      </div>

      <!-- TEXTO RODAPÉ DIREITA: PROIBIÇÃO -->
      <div class="abs" style="bottom: 12vh; right: 8vw; width: 38vw; transform: translateX({getTxRight(t, 0.2)}px);">
        <div style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); padding-left: 2rem;">
          <h3 style="font-size: clamp(1rem, 1.2vw, 1.2rem); font-weight: 700; color: var(--color-white); margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #f87171;"><path d="M18 6 6 18M6 6l12 12"/></svg>
            Mero Comércio
          </h3>
          <p style="font-size: clamp(0.85rem, 0.95vw, 0.95rem); color: rgba(255,255,255,0.7); line-height: 1.6; font-weight: 400; max-width: 400px;">
            Não se confunde com a simples venda online de medicamentos ou dispensação sem contato clínico prévio. A venda de balcão via internet NÃO é telefarmácia clínica.
          </p>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

content = re.sub(r'<!-- SLIDE 2 -->.*?{/if}', slide_2, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

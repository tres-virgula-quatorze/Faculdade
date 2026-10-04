import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

slide_2 = """  <!-- SLIDE 2 -->
  {#if true}
  {@const t = getT(1)}
  <section id="slide-2" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxRight(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, 1)}deg);" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"><circle cx="12" cy="12" r="11"/></svg>
      
      <div class="abs w-100" style="top: 22vh; left: 50%; transform: translateX(-50%) translateY({getTy(t, 0)}px); text-align: center; padding: 0 4vw;">
        <h2 style="font-size: clamp(2rem, 3.8vw, 3.5rem); font-weight: 400; line-height: 1.2; color: var(--color-white); letter-spacing: -0.02em; opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          O que Define a <br>
          <strong style="font-weight: 700;">Telefarmácia no Brasil?</strong>
        </h2>
        <p style="margin-top: 1.2rem; font-size: clamp(1rem, 1.4vw, 1.4rem); font-weight: 500; color: rgba(255,255,255,0.85); opacity: {getOp(t, 0.05)}; filter: blur({getBlur(t, 0.05)}px); letter-spacing: 0.01em;">
          Exercício Clínico <span style="opacity: 0.5; margin: 0 0.5em; font-weight: 300;">vs</span> Mero Comércio Eletrônico
        </p>
      </div>

      <div class="abs bottom-left w-40" style="transform: translateY({getTy(t, 0.15)}px);">
        <div style="opacity: {getOp(t, 0.15)}; filter: blur({getBlur(t, 0.15)}px); position: relative; padding-left: 1.5rem; border-left: 1px solid rgba(255,255,255,0.2);">
          <div style="position: absolute; left: -1.2rem; top: -2.5rem; font-size: 5rem; font-weight: 700; color: rgba(255,255,255,0.05); line-height: 1; pointer-events: none;">01</div>
          <h3 style="font-size: 1.05rem; font-weight: 600; color: var(--color-white); margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #4ade80;"><path d="M20 6 9 17l-5-5"/></svg>
            Exercício Clínico
          </h3>
          <p style="font-size: 0.9rem; color: rgba(255,255,255,0.8); line-height: 1.6; font-weight: 400;">
            A telefarmácia é um ato de saúde. O foco é a avaliação clínica, o acompanhamento farmacoterapêutico e a melhoria da qualidade de vida do paciente, utilizando TICs.
          </p>
        </div>
      </div>

      <div class="abs bottom-right w-40" style="transform: translateY({getTy(t, 0.2)}px);">
        <div style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); position: relative; padding-right: 1.5rem; border-right: 1px solid rgba(255,255,255,0.2); text-align: right;">
          <div style="position: absolute; right: -1.2rem; top: -2.5rem; font-size: 5rem; font-weight: 700; color: rgba(255,255,255,0.05); line-height: 1; pointer-events: none;">02</div>
          <h3 style="font-size: 1.05rem; font-weight: 600; color: var(--color-white); margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: flex-end; gap: 0.5rem; text-transform: uppercase; letter-spacing: 0.05em;">
            Mero Comércio
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color: #f87171;"><path d="M18 6 6 18M6 6l12 12"/></svg>
          </h3>
          <p style="font-size: 0.9rem; color: rgba(255,255,255,0.8); line-height: 1.6; font-weight: 400;">
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

import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the replacement for Slide 2
slide_2 = """  <!-- SLIDE 2 -->
  {#if true}
  {@const t = getT(1)}
  <section id="slide-2" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxRight(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, 1)}deg);" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="3"><circle cx="12" cy="12" r="9"/></svg>
      
      <div class="abs top-left w-50" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 02 · Conceito</span>
          <h2>O que Define a Telefarmácia no Brasil?</h2>
          <p>Exercício Clínico vs. Mero Comércio Eletrônico</p>
        </header>
      </div>

      <div class="abs mid-left w-40" style="transform: translateX({getTxLeft(t, 0.1)}px);">
        <div class="card" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px);">
          <div class="card-icon"><i class="ph ph-check-circle" style="color: var(--color-primary);"></i></div>
          <h3>Exercício Clínico Permissão</h3>
          <p>A telefarmácia é um ato de saúde. O foco é a avaliação clínica, o acompanhamento farmacoterapêutico e a melhoria da qualidade de vida do paciente, utilizando TICs.</p>
        </div>
      </div>

      <div class="abs bottom-right w-45" style="transform: translateX({getTxRight(t, 0.2)}px);">
        <div class="card card-red" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px);">
          <div class="card-icon"><i class="ph ph-x-circle" style="color: #d32f2f;"></i></div>
          <h3>Mero Comércio Proibição</h3>
          <p>Não se confunde com a simples venda online de medicamentos ou dispensação sem contato clínico prévio. A venda de balcão via internet NÃO é telefarmácia clínica.</p>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 3
slide_3 = """  <!-- SLIDE 3 -->
  {#if true}
  {@const t = getT(2)}
  <section id="slide-3" class="slide alt" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-3" style="opacity: {getOp(t, 0.45)}; transform: translate({getTxRight(t, 0.45)}px, {getTy(t, 0.45)}px) rotate({getRotate(t, 0.45, 1)}deg);" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
      
      <div class="abs top-center w-60" style="transform: translateY({getTy(t, 0)}px) translateX(-50%); text-align: center;">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 03 · Atendimento remoto</span>
          <h2 style="justify-content: center;">Modalidades da Telefarmácia</h2>
          <p>Nota Técnica CFF 2022 &amp; Resolução 727/2022</p>
        </header>
      </div>

      <div class="abs mid-left w-45" style="transform: translateX({getTxLeft(t, 0.1)}px);">
        <article class="card glass hover-lift" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px);">
          <span class="num">01</span>
          <h3>Teleconsulta Farmacêutica</h3>
          <p>Atendimento direto e em tempo real (vídeo/áudio) entre o farmacêutico e o paciente para avaliação clínica e orientação.</p>
        </article>
      </div>
      
      <div class="abs mid-right w-45" style="transform: translateX({getTxRight(t, 0.15)}px);">
        <article class="card glass hover-lift" style="opacity: {getOp(t, 0.15)}; filter: blur({getBlur(t, 0.15)}px);">
          <span class="num">02</span>
          <h3>Teleinterconsulta</h3>
          <p>Troca de informações e opiniões entre farmacêuticos ou entre o farmacêutico e outros profissionais da saúde.</p>
        </article>
      </div>

      <div class="abs bottom-left w-45" style="transform: translateY({getTy(t, 0.2)}px);">
        <article class="card glass hover-lift" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px);">
          <span class="num">03</span>
          <h3>Telemonitoramento</h3>
          <p>Acompanhamento à distância de parâmetros de saúde e adesão ao tratamento (ex: glicemia, pressão arterial).</p>
        </article>
      </div>

      <div class="abs bottom-right w-45" style="transform: translateY({getTy(t, 0.25)}px);">
        <article class="card glass hover-lift" style="opacity: {getOp(t, 0.25)}; filter: blur({getBlur(t, 0.25)}px);">
          <span class="num">04</span>
          <h3>Teleorientação</h3>
          <p>Aconselhamento geral e triagem à distância, encaminhando o paciente a serviços de saúde presenciais quando necessário.</p>
        </article>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 4
slide_4 = """  <!-- SLIDE 4 -->
  {#if true}
  {@const t = getT(3)}
  <section id="slide-4" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="3"><circle cx="12" cy="12" r="9"/></svg>
      
      <div class="abs top-left w-50" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 04 · Arcabouço Legal</span>
          <h2>Legislação e Limites da Atuação Digital</h2>
        </header>
      </div>

      <div class="abs mid-left w-45" style="transform: translateX({getTxLeft(t, 0.1)}px);">
        <div class="card" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px);">
          <div class="norm">
            <span>Base normativa</span>
            <strong>Lei Federal nº 14.510/2022</strong>
          </div>
          <p>Disciplina a Telessaúde no Brasil em âmbito nacional e no SUS.</p>
        </div>
      </div>

      <div class="abs top-right w-45" style="transform: translateX({getTxRight(t, 0.15)}px);">
        <div class="card" style="opacity: {getOp(t, 0.15)}; filter: blur({getBlur(t, 0.15)}px);">
          <div class="norm">
            <span>Base normativa</span>
            <strong>Resolução CFF nº 10/2024</strong>
          </div>
          <p>Regulamenta o uso de novas tecnologias, Saúde Digital e Inteligência Artificial na prática farmacêutica.</p>
        </div>
      </div>

      <div class="abs bottom-center w-80" style="transform: translateY({getTy(t, 0.25)}px) translateX(-50%);">
        <div class="alert-panel glow" style="opacity: {getOp(t, 0.25)}; filter: blur({getBlur(t, 0.25)}px);">
          <div class="alert-top">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></svg>
            RESOLUÇÃO CFF Nº 727/2022 · ART. 3º
          </div>
          <p>É VEDADO (PROIBIDO) assumir a Responsabilidade Técnica (RT) de farmácias de forma remota/não presencial.</p>
          <small>A presença física do RT é obrigatória.</small>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

content = re.sub(r'<!-- SLIDE 2 -->.*?{/if}', slide_2, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 3 -->.*?{/if}', slide_3, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 4 -->.*?{/if}', slide_4, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

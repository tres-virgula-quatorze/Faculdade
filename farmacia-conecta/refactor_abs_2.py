import re

file_path = 'src/lib/components/Slides.svelte'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Slide 5
slide_5 = """  <!-- SLIDE 5 -->
  {#if true}
  {@const t = getT(4)}
  <section id="slide-5" class="slide alt" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-3" style="opacity: {getOp(t, 0.45)}; transform: translate({getTxRight(t, 0.45)}px, {getTy(t, 0.45)}px) rotate({getRotate(t, 0.45, 1)}deg);" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
      
      <div class="abs top-right w-50" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 05 · Segurança cibernética</span>
          <h2>Privacidade e Registro Clínico Obrigatório</h2>
        </header>
      </div>

      <div class="abs mid-left w-40" style="transform: translateX({getTxLeft(t, 0.1)}px);">
        <div class="vault" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px);" aria-hidden="true">
          <div class="vault-body">
            <div class="vault-ring"></div>
            <svg class="doc" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6M9 13h6M9 17h4" /></svg>
            <svg class="lock" viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 8 0v4" /></svg>
            <span class="seal">LGPD</span>
          </div>
          <div class="vault-base">COFRE DIGITAL</div>
        </div>
      </div>

      <div class="abs mid-right w-45" style="transform: translateX({getTxRight(t, 0.2)}px);">
        <div class="sec-list" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px);">
          <article class="card glass sec-item" style="transform: translateY({getTy(t, 0.25)}px);" >
            <div class="sec-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" /></svg></div>
            <div>
              <h3>LGPD (Lei nº 13.709/2018)</h3>
              <p>Dados de saúde do paciente são classificados legalmente como <strong>dados pessoais sensíveis</strong>.</p>
            </div>
          </article>
          <article class="card glass sec-item" style="transform: translateY({getTy(t, 0.35)}px);" >
            <div class="sec-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 8 0v4" /></svg></div>
            <div>
              <h3>Prontuário Eletrônico</h3>
              <p>Obrigatoriedade de registrar todos os atendimentos prestados em prontuário seguro, garantindo sigilo.</p>
            </div>
          </article>
          <article class="card glass sec-item" style="transform: translateY({getTy(t, 0.45)}px);" >
            <div class="sec-icon"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="6" /><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8" /></svg></div>
            <div>
              <h3>Assinatura Digital</h3>
              <p>Todas as prescrições geradas precisam de certificação ICP-Brasil.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 6
slide_6 = """  <!-- SLIDE 6 -->
  {#if true}
  {@const t = getT(5)}
  <section id="slide-6" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="3"><circle cx="12" cy="12" r="9"/></svg>
      
      <div class="abs top-center w-80" style="transform: translateY({getTy(t, 0)}px) translateX(-50%); text-align: center;">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 06 · O protótipo</span>
          <h2 style="justify-content: center;">Fluxo de Atendimento no Nosso Protótipo Digital</h2>
          <p>A jornada do paciente no nosso site</p>
        </header>
      </div>

      <div class="abs center w-100" style="padding: 0 4vw;">
        <ol class="stepper" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px); transform: translateY({getTy(t, 0.1)}px);" >
          <div class="track"><div class="track-fill" style="--f:{Math.min(1, stepProgress * 1.25)}"></div></div>
          {#each steps as s, i}
            <li class="step" class:lit={stepProgress * 1.25 >= i / 3 - 0.001}>
              <span class="step-dot">{i + 1}</span>
              <div class="step-card card glass">
                <h3>{s.title}</h3>
                <p>{s.text}</p>
              </div>
            </li>
          {/each}
        </ol>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 7
slide_7 = """  <!-- SLIDE 7 -->
  {#if true}
  {@const t = getT(6)}
  <section id="slide-7" class="slide alt" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxRight(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, 1)}deg);" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      
      <div class="abs top-left w-50" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 07 · Prática clínica I</span>
          <h2>Cuidado Clínico na Teleconsulta</h2>
          <p>Foco em Pacientes Hipertensos, Diabéticos e Polimedicados</p>
        </header>
      </div>

      <div class="abs mid-left w-45" style="transform: translateX({getTxLeft(t, 0.15)}px);">
        <div class="video-mock" style="opacity: {getOp(t, 0.15)}; filter: blur({getBlur(t, 0.15)}px);" aria-hidden="true">
          <div class="vm-bar">
            <span class="rec"><i></i> AO VIVO</span>
            <span>Teleconsulta Farmacêutica</span>
            <span>00:12:45</span>
          </div>
          <div class="vm-stage">
            <div class="vm-patient">
              <div class="avatar"></div>
              <div class="pills"><span></span><span></span><span></span></div>
              <em>Paciente</em>
            </div>
            <div class="vm-pharma">
              <div class="avatar small"></div>
              <em>Farmacêutico</em>
            </div>
          </div>
          <div class="vm-controls"><span></span><span></span><span class="end"></span></div>
        </div>
      </div>

      <div class="abs mid-right w-40" style="transform: translateX({getTxRight(t, 0.25)}px);">
        <ul class="checklist">
          {#each checklist as c, i}
            <li class="" style="opacity: {getOp(t, 0.25)}; filter: blur({getBlur(t, 0.25)}px);" >
              <button type="button" class="check-item" class:done={checks[i]} onclick={() => (checks[i] = !checks[i])} aria-pressed={checks[i]}>
                <span class="box"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5" /></svg></span>
                <span class="check-text">
                  <strong>{c.title}</strong>
                  <small>{c.text}</small>
                </span>
              </button>
            </li>
          {/each}
        </ul>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 8
slide_8 = """  <!-- SLIDE 8 -->
  {#if true}
  {@const t = getT(7)}
  <section id="slide-8" class="slide" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-3" style="opacity: {getOp(t, 0.45)}; transform: translate({getTxRight(t, 0.45)}px, {getTy(t, 0.45)}px) rotate({getRotate(t, 0.45, 1)}deg);" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
      
      <div class="abs top-right w-50" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px); text-align: right;">
          <span class="eyebrow" style="margin-left:auto;">Slide 08 · Prática clínica II</span>
          <h2 style="justify-content: flex-end;">Diferenciação Regulatória e Prescrição</h2>
          <p>Suplementos Alimentares vs. Medicamentos</p>
        </header>
      </div>

      <div class="abs center w-80" style="transform: translate(-50%, -50%) translateY({getTy(t, 0.1)}px);">
        <div class="toggle" style="opacity: {getOp(t, 0.1)}; filter: blur({getBlur(t, 0.1)}px);" role="group" aria-label="Alternar comparação">
          <button type="button" class:on={compareMode === 'side'} onclick={() => (compareMode = 'side')}>Lado a lado</button>
          <button type="button" class:on={compareMode === 'sup'} onclick={() => (compareMode = 'sup')}>Suplemento</button>
          <button type="button" class:on={compareMode === 'med'} onclick={() => (compareMode = 'med')}>Medicamento</button>
        </div>

        <div class="compare" data-mode={compareMode}>
          <article class="card cmp cmp-sup -l" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px);" >
            <span class="chip chip-gold">Anvisa</span>
            <h3>Suplementos Alimentares</h3>
            <p>Não são medicamentos; destinam-se a suprir nutrientes em pessoas saudáveis e <strong>não tratam doenças</strong>.</p>
          </article>
          <article class="card cmp cmp-med -r" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px);" >
            <span class="chip chip-green">Res. CFF nº 586/2013</span>
            <h3>Prescrição Farmacêutica</h3>
            <p>Autonomia restrita à indicação de <strong>Medicamentos Isentos de Prescrição (MIPs)</strong> e fitoterápicos.</p>
          </article>
        </div>
      </div>

      <div class="abs bottom-right w-50" style="transform: translateX({getTxRight(t, 0.3)}px);">
        <div class="root-cause card glass" style="opacity: {getOp(t, 0.3)}; filter: blur({getBlur(t, 0.3)}px);" >
          <div class="icon-bubble sm"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg></div>
          <p><strong>Análise de Causa Raiz:</strong> queixas como cansaço ou insônia exigem investigação detalhada antes de qualquer indicação direta de suplementos.</p>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 9
slide_9 = """  <!-- SLIDE 9 -->
  {#if true}
  {@const t = getT(8)}
  <section id="slide-9" class="slide danger" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-2" style="opacity: {getOp(t, 0.35)}; transform: translate({getTxLeft(t, 0.35)}px, {getTy(t, 0.35)}px) rotate({getRotate(t, 0.35, -1)}deg);" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="3"><circle cx="12" cy="12" r="9"/></svg>
      
      <div class="abs mid-left w-45" style="transform: translateY({getTy(t, 0)}px);">
        <header class="slide-head" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow eyebrow-red">Slide 09 · Triagem digital</span>
          <h2>Limites Clínicos e Sinais de Alarme (Red Flags)</h2>
          <p>Triagem Digital e Limites do Atendimento</p>
        </header>
      </div>

      <div class="abs mid-right w-45" style="transform: scale({getScale(t, 0.15)}) translateY({getTy(t, 0.15)}px);">
        <div class="alert-panel" style="opacity: {getOp(t, 0.15)}; filter: blur({getBlur(t, 0.15)}px);" >
          <div class="alert-top">
            <svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" /><path d="M12 9v4M12 17h.01" /></svg>
            <strong>ALERTA CRÍTICO · EMERGÊNCIA</strong>
          </div>
          <ul class="risk-list" style="grid-template-columns: 1fr;">
            <li class="" style="opacity: {getOp(t, 0.2)}; filter: blur({getBlur(t, 0.2)}px); transform: translateX({getTxRight(t, 0.2)}px);" >
              <span class="risk-ico">!</span>
              <div>
                <h3>Sintomas de Emergência</h3>
                <p>Dor no peito, falta de ar súbita, febre exigem <strong>Pronto-Atendimento Presencial Imediato</strong>.</p>
              </div>
            </li>
            <li class="" style="opacity: {getOp(t, 0.3)}; filter: blur({getBlur(t, 0.3)}px); transform: translateX({getTxRight(t, 0.3)}px);" >
              <span class="risk-ico">!</span>
              <div>
                <h3>Impossibilidade do Exame Físico</h3>
                <p>O canal remoto não substitui a palpação, ausculta ou inspeção presencial.</p>
              </div>
            </li>
            <li class="" style="opacity: {getOp(t, 0.4)}; filter: blur({getBlur(t, 0.4)}px); transform: translateX({getTxRight(t, 0.4)}px);" >
              <span class="risk-ico">!</span>
              <div>
                <h3>Conduta Ética</h3>
                <p>Se a queixa ultrapassar o escopo remoto, emitir parecer de encaminhamento imediato.</p>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
  {/if}"""

# Slide 10
slide_10 = """  <!-- SLIDE 10 -->
  {#if true}
  {@const t = getT(9)}
  <section id="slide-10" class="slide final" style="opacity: {getOp(t)}; filter: blur({getBlur(t)}px); pointer-events: {Math.abs(t) < 0.9 ? 'auto' : 'none'}; z-index: {Math.abs(t) < 1 ? 2 : 1};">
    <div class="abs-layout">
      <!-- Decos -->
      <svg class="deco deco-1" style="opacity: {getOp(t, 0.25)}; transform: translate({getTxRight(t, 0.25)}px, {getTy(t, 0.25)}px) rotate({getRotate(t, 0.25, 1)}deg);" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round"><path d="M12 4v16m-8-8h16"/></svg>
      <svg class="deco deco-3" style="opacity: {getOp(t, 0.45)}; transform: translate({getTxRight(t, 0.45)}px, {getTy(t, 0.45)}px) rotate({getRotate(t, 0.45, 1)}deg);" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/></svg>
      
      <div class="abs center w-80" style="transform: translate(-50%, -50%) scale({getScale(t, 0)}); text-align: center;">
        <article class="final-card" style="opacity: {getOp(t, 0)}; filter: blur({getBlur(t, 0)}px);">
          <span class="eyebrow">Slide 10 · Conclusão e encerramento</span>
          <h2 style="justify-content: center;">Telefarmácia: Tecnologia a Serviço do Cuidado Humano</h2>
  
          <div class="final-grid">
            <div class="final-block">
              <h3>Ampliação do Acesso</h3>
              <p>Inclusão de pacientes com limitações de mobilidade ou moradores de áreas remotas.</p>
            </div>
            <div class="final-block">
              <h3>Sinergia Acadêmica</h3>
              <p>Integração entre Farmacologia, Legislação Farmacêutica, Tecnologia e Ética Profissional.</p>
            </div>
            <div class="final-block">
              <h3>Equipe de Desenvolvimento</h3>
              <p>Antonio Erick Conceição da Silva, Yara Lima da Silva, Ezequiel Olanda de Oliveira, Thamyres dos Santos de Souza.</p>
            </div>
            <div class="final-block">
              <h3>Orientadora</h3>
              <p>Prof.ª Bianca Lira</p>
              <h3 class="mt">Instituição</h3>
              <p>Centro Universitário UNIGRANDE (2026)</p>
            </div>
          </div>
  
          <div class="final-actions" style="justify-content: center; margin-top: 2rem;">
            <a class="btn btn-gold" href="#agendamento">Testar Protótipo</a>
            <button type="button" class="btn-ghost" onclick={toTop}>Voltar ao topo</button>
          </div>
        </article>
      </div>
    </div>
  </section>
  {/if}"""

content = re.sub(r'<!-- SLIDE 5 -->.*?{/if}', slide_5, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 6 -->.*?{/if}', slide_6, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 7 -->.*?{/if}', slide_7, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 8 -->.*?{/if}', slide_8, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 9 -->.*?{/if}', slide_9, content, flags=re.DOTALL)
content = re.sub(r'<!-- SLIDE 10 -->.*?{/if}', slide_10, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

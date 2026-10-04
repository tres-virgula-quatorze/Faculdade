<script>
  let { activePhase = 0, currentRatio = 0, scrollToPhase } = $props();

  const TOTAL = 10;
  
  function getT(phaseIndex) {
    const start = phaseIndex / 10;
    const end = (phaseIndex + 1) / 10;
    const center = (start + end) / 2;
    return (currentRatio - center) / 0.05; 
  }

  function easeOut(x) { return 1 - Math.pow(1 - Math.max(0, Math.min(1, x)), 4); }
  function easeIn(x) { return Math.pow(Math.max(0, Math.min(1, x)), 4); }

  function getOp(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -1 || adjustedT > 1) return 0;
    if (adjustedT >= -0.4 && adjustedT <= 0.4) return 1;
    if (adjustedT < -0.4) return easeOut((adjustedT + 1) / 0.6);
    return 1 - easeIn((adjustedT - 0.4) / 0.6);
  }

  function getTy(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -0.4) return 120 * (1 - easeOut((adjustedT + 1) / 0.6));
    if (adjustedT > 0.4) return -120 * easeIn((adjustedT - 0.4) / 0.6);
    return 0;
  }

  function getTxLeft(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -0.4) return -180 * (1 - easeOut((adjustedT + 1) / 0.6));
    if (adjustedT > 0.4) return 180 * easeIn((adjustedT - 0.4) / 0.6);
    return 0;
  }

  function getTxRight(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -0.4) return 180 * (1 - easeOut((adjustedT + 1) / 0.6));
    if (adjustedT > 0.4) return -180 * easeIn((adjustedT - 0.4) / 0.6);
    return 0;
  }

  function getScale(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -0.4) return 0.85 + 0.15 * easeOut((adjustedT + 1) / 0.6);
    if (adjustedT > 0.4) return 1 - 0.15 * easeIn((adjustedT - 0.4) / 0.6);
    return 1;
  }

  function getBlur(t, delay = 0) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT >= -0.4 && adjustedT <= 0.4) return 0;
    if (adjustedT < -0.4) return 15 * (1 - easeOut((adjustedT + 1) / 0.6));
    return 15 * easeIn((adjustedT - 0.4) / 0.6);
  }

  function getRotate(t, delay = 0, dir = 1) {
    const d = delay * 1.2;
    const adjustedT = t > 0 ? t - d : t + d;
    if (adjustedT < -0.4) return dir * 15 * (1 - easeOut((adjustedT + 1) / 0.6));
    if (adjustedT > 0.4) return -dir * 15 * easeIn((adjustedT - 0.4) / 0.6);
    return 0;
  }

  const slideIds = ['sobre', ...Array.from({ length: 9 }, (_, i) => `slide-${i + 2}`)];

  let compareMode = $state('side');
  let checks = $state([true, false, false]);

  const modalities = [
    {
      title: 'Teleconsulta Farmacêutica',
      text: 'Atendimento direto e em tempo real (vídeo/áudio) entre o farmacêutico e o paciente para avaliação clínica e orientação.',
      icon: 'video'
    },
    {
      title: 'Teleinterconsulta',
      text: 'Discussão de caso clínico realizada exclusivamente entre o farmacêutico e outros profissionais da equipe de saúde.',
      icon: 'users'
    },
    {
      title: 'Telemonitoramento / Televigilância',
      text: 'Acompanhamento contínuo e à distância de parâmetros de saúde, reações adversas e adesão ao tratamento.',
      icon: 'activity'
    },
    {
      title: 'Teleconsultoria',
      text: 'Emissão de pareceres técnicos, administrativos e operacionais entre profissionais, sem avaliação direta de paciente específico.',
      icon: 'file'
    }
  ];

  const steps = [
    { title: 'Acolhimento Acessível', text: 'Explicação clara e linguagem humanizada sobre o papel do farmacêutico.' },
    { title: 'Triagem de Necessidades', text: 'Formulário sucinto de identificação e queixa principal.' },
    { title: 'Consentimento & LGPD', text: 'Aceite transparente do uso de dados e sigilo clínico.' },
    { title: 'Direcionamento Consciente', text: 'Agendamento da Teleconsulta ou encaminhamento imediato para serviço de urgência.' }
  ];

  const checklist = [
    {
      title: 'Conciliação Terapêutica Remota',
      text: 'Conferência visual de caixas de medicamentos via câmera para evitar duplicidade ou nomes comerciais redundantes.'
    },
    {
      title: 'Adesão ao Tratamento',
      text: 'Identificação de rotinas de tomadas de dose e investigação de esquecimentos ou efeitos colaterais.'
    },
    {
      title: 'Educação em Saúde',
      text: 'Orientação sobre armazenamento correto (geladeira/temperatura ambiente) e horários de tomada.'
    }
  ];

  let stepProgress = $derived(
    activePhase === 5 
      ? Math.min(1, Math.max(0, (currentRatio - 0.5) * 10))
      : (activePhase > 5 ? 1 : 0)
  );

  function goTo(i) {
    if (scrollToPhase) scrollToPhase(i);
  }

  function toTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function pad(n) {
    return String(n).padStart(2, '0');
  }
</script>

<!-- Indicador lateral de slide ativo -->
<nav class="slide-nav show" aria-label="Navegação entre slides">
  <div class="slide-counter">
    <strong>{pad(activePhase + 1)}</strong><span>/{TOTAL}</span>
  </div>
  <ul>
    {#each slideIds as _, i}
      <li>
        <button
          type="button"
          class="dot"
          class:on={i === activePhase}
          aria-label="Ir para o slide {i + 1}"
          aria-current={i === activePhase ? 'true' : undefined}
          onclick={() => goTo(i)}
        ></button>
      </li>
    {/each}
  </ul>
</nav>

<div id="slides-wrap" class="slides-wrap">
    <!-- SLIDE 2 -->
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
  {/if}

    <!-- SLIDE 3 -->
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
  {/if}


    <!-- SLIDE 4 -->
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
  {/if}

    <!-- SLIDE 5 -->
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
  {/if}

    <!-- SLIDE 6 -->
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
  {/if}

    <!-- SLIDE 7 -->
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
  {/if}

    <!-- SLIDE 8 -->
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
  {/if}

    <!-- SLIDE 9 -->
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
  {/if}

    <!-- SLIDE 10 -->
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
  {/if}
</div>

<style>
  .slides-wrap {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    pointer-events: none;
    color: var(--color-white);
  }

  
  .deco { position: absolute; pointer-events: none; z-index: -1; }
  .deco-1 { top: -2rem; right: -3rem; }
  .deco-2 { bottom: 2rem; left: -4rem; }
  .deco-3 { top: 40%; right: -5rem; }

  /* ===== Slide base ===== */
  .slide {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(2.5rem, 5vh, 3.5rem) clamp(1rem, 3vw, 2.5rem);
    background: transparent;
    opacity: 0;
    
    pointer-events: none;
    z-index: 1;
    overflow: hidden;
  }
  .slide.alt {
    background: transparent;
  }
  .slide-inner {
    position: relative;
    width: 100%;
    max-width: 980px;
    display: flex;
    flex-direction: column;
    gap: clamp(0.9rem, 1.8vh, 1.5rem);
  }

  .slide-head h2 {
    font-size: clamp(1.25rem, 2.2vw, 1.8rem);
    line-height: 1.12;
    font-weight: 800;
    letter-spacing: -0.02em;
    padding-bottom: 0.14em;
    color: var(--color-white);
  }
  .slide-head p {
    margin-top: 0.55rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: clamp(0.8rem, 0.9vw, 0.95rem);
    font-weight: 500;
  }
  .eyebrow {
    display: inline-block;
    margin-bottom: 0.8rem;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--color-primary);
    background: rgba(22, 128, 58, 0.1);
    border: 1px solid rgba(22, 128, 58, 0.2);
  }
  .eyebrow-red {
    color: #d32f2f;
    background: rgba(211, 47, 47, 0.1);
    border-color: rgba(211, 47, 47, 0.2);
  }

  /* ===== Cards ===== */
  .abs-layout { position: absolute; inset: 0; width: 100vw; height: 100vh; overflow: hidden; pointer-events: none; }
  .abs { position: absolute; pointer-events: auto; }
  
  .top-left { top: 12vh; left: 8vw; }
  .top-right { top: 12vh; right: 8vw; }
  .top-center { top: 12vh; left: 50%; transform: translateX(-50%); }
  
  .bottom-left { bottom: 12vh; left: 8vw; }
  .bottom-right { bottom: 12vh; right: 8vw; }
  .bottom-center { bottom: 12vh; left: 50%; transform: translateX(-50%); }
  
  .mid-left { top: 50%; left: 8vw; transform: translateY(-50%); }
  .mid-right { top: 50%; right: 8vw; transform: translateY(-50%); }
  .center { top: 50%; left: 50%; transform: translate(-50%, -50%); }

  .w-30 { width: 30vw; }
  .w-40 { width: 40vw; }
  .w-45 { width: 45vw; }
  .w-50 { width: 50vw; }
  .w-60 { width: 60vw; }
  .w-80 { width: 80vw; }
  .w-100 { width: 100vw; }

  @media (max-width: 900px) {
    .w-30, .w-40, .w-45, .w-50, .w-60, .w-80 { width: 85vw; }
    .top-right, .bottom-right, .mid-right, .top-center, .bottom-center, .mid-left, .top-left, .bottom-left, .center {
      left: 7.5vw; right: auto; transform: none;
    }
    .mid-right { top: 60%; }
    .mid-left { top: 35%; }
    .bottom-right { bottom: 5vh; }
  }

  .card {
    border-radius: var(--radius-md);
    padding: clamp(1rem, 1.5vw, 1.4rem);
    position: relative;
    background: var(--color-white);
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
  }
  .card h3 {
    font-size: clamp(0.95rem, 1.1vw, 1.1rem);
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: var(--color-text);
  }
  .card p {
    color: var(--color-text-muted);
    font-size: clamp(0.85rem, 0.95vw, 0.9rem);
    line-height: 1.6;
  }
  .card strong { color: var(--color-text); }
  .glass {
    background: var(--color-white);
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
  }
  .hover-lift { transition: transform 0.25s ease, box-shadow 0.25s ease; }
  .vis .hover-lift:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
  }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(0.8rem, 1.5vw, 1.5rem); }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.8rem, 1vw, 1rem); }

  .icon-bubble {
    width: 48px; height: 48px;
    display: grid; place-items: center;
    border-radius: var(--radius-sm);
    color: var(--color-primary);
    background: rgba(22, 128, 58, 0.1);
    margin-bottom: 1rem;
  }
  .icon-bubble.sm { width: 40px; height: 40px; margin: 0; flex-shrink: 0; color: #d32f2f; background: rgba(211,47,47,.1); }
  .num {
    position: absolute; top: 1.1rem; right: 1.3rem;
    font-weight: 800; font-size: 1.6rem; color: rgba(38, 50, 56, 0.05);
  }

  /* ===== Slide 2 ===== */
  .card-ok {
    background: #e8f5e9;
    border: 1px solid #c8e6c9;
  }
  .card-no {
    overflow: hidden;
    background: #ffebee;
    border: 1px solid #ffcdd2;
  }
  .ban { position: absolute; right: -14px; bottom: -14px; color: rgba(211, 47, 47, 0.05); }
  .card-tag {
    display: inline-flex; align-items: center; gap: 0.45rem;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.35rem 0.8rem; border-radius: 999px; margin-bottom: 1rem;
  }
  .card-tag.ok { color: #2e7d32; background: #c8e6c9; }
  .card-tag.no { color: #c62828; background: #ffcdd2; }
  .norm {
    margin-top: 1.2rem; padding: 0.8rem 1rem; border-radius: 8px;
    background: rgba(38, 50, 56, 0.04); display: flex; flex-direction: column; gap: 0.15rem;
  }
  .norm span { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-primary-dark); font-weight: 700; }
  .norm strong { font-size: 0.98rem; color: var(--color-text); }

  /* ===== Slide 4 ===== */
  .mosaic { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1rem, 2vw, 1.6rem); }
  .badge-card .law {
    display: inline-block; margin-bottom: 0.7rem; padding: 0.4rem 0.9rem; border-radius: 8px;
    font-weight: 800; font-size: 0.95rem; color: var(--color-white);
    background: var(--color-primary);
  }
  .ethic-banner {
    grid-column: 1 / -1;
    padding: clamp(1.4rem, 3vw, 2.2rem);
    border-radius: var(--radius-md);
    background: #ffebee;
    border: 1px solid #ffcdd2;
    text-align: center;
  }
  .ethic-label {
    display: inline-flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;
    color: #c62828; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase;
  }
  .ethic-banner h3 { font-size: clamp(1.15rem, 2.3vw, 1.8rem); line-height: 1.3; color: #b71c1c; font-weight: 800; }
  .ethic-banner p { margin-top: 0.6rem; color: #c62828; font-weight: 600; }
  .ethic-banner.pulse { animation: none; }

  /* ===== Slide 5 ===== */
  .security-panel { display: grid; grid-template-columns: 0.8fr 1.2fr; gap: clamp(1.4rem, 3vw, 3rem); align-items: center; }
  .vault { display: flex; flex-direction: column; align-items: center; gap: 0.8rem; }
  .vault-body {
    position: relative; width: min(270px, 60vw); aspect-ratio: 1;
    border-radius: var(--radius-lg); display: grid; place-items: center;
    background: var(--color-bg);
    border: 2px solid var(--color-border);
    overflow: hidden;
  }
  .vault-ring {
    position: absolute; inset: 18%; border-radius: 50%;
    border: 3px dashed var(--color-primary);
    animation: spin 18s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .doc { position: absolute; color: var(--color-text); transform: translateY(-190px); opacity: 0; transition: transform 1.1s cubic-bezier(0.34, 1.3, 0.5, 1) 0.5s, opacity 0.5s ease 0.5s; }
  .lock { position: absolute; bottom: 14%; color: var(--color-primary-dark); transform: scale(0); transition: transform 0.5s cubic-bezier(0.34, 1.8, 0.5, 1) 1.5s; }
  .seal {
    position: absolute; top: 12%; right: 10%; padding: 0.25rem 0.6rem; border-radius: 8px;
    font-size: 0.8rem; font-weight: 800; letter-spacing: 0.08em; color: var(--color-white);
    background: var(--color-primary);
    transform: rotate(10deg) scale(0); transition: transform 0.5s cubic-bezier(0.34, 1.8, 0.5, 1) 1.9s;
  }
  .vis .doc { transform: translateY(-8px); opacity: 1; }
  .vis .lock { transform: scale(1); }
  .vis .seal { transform: rotate(10deg) scale(1); }
  .vault-base { font-size: 0.72rem; letter-spacing: 0.3em; font-weight: 700; color: var(--color-text-muted); }
  .sec-list { display: flex; flex-direction: column; gap: 1rem; }
  .sec-item { display: flex; gap: 1rem; align-items: flex-start; padding: 1.1rem 1.3rem; }
  .sec-icon {
    flex-shrink: 0; width: 46px; height: 46px; border-radius: var(--radius-sm); display: grid; place-items: center;
    color: var(--color-primary); background: rgba(22, 128, 58, 0.1); border: 1px solid rgba(22, 128, 58, 0.2);
  }

  /* ===== Slide 6 ===== */
  .stepper { position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; list-style: none; padding-top: 1rem; }
  .track { position: absolute; top: calc(1rem + 22px); left: 12%; right: 12%; height: 4px; border-radius: 4px; background: rgba(38, 50, 56, 0.1); }
  .track-fill { height: 100%; border-radius: 4px; width: 100%; transform-origin: left; transform: scaleX(var(--f)); background: var(--color-primary); }
  .step { position: relative; display: flex; flex-direction: column; align-items: center; gap: 1.2rem; text-align: center; }
  .step-dot {
    position: relative; z-index: 1; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center;
    font-weight: 800; color: var(--color-text-muted); background: var(--color-bg); border: 2px solid var(--color-border);
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .step.lit .step-dot { color: var(--color-white); background: var(--color-primary); border-color: var(--color-primary); transform: scale(1.12); }
  .step-card { opacity: 0.45; transform: translateY(10px) scale(0.97); transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1); width: 100%; padding: 1.2rem; }
  .step.lit .step-card { opacity: 1; transform: none; border-color: var(--color-primary); }

  /* ===== Slide 7 ===== */
  .grid-clinical { display: grid; grid-template-columns: 1.15fr 1fr; gap: clamp(1.2rem, 3vw, 2.6rem); align-items: center; }
  .video-mock {
    border-radius: 22px; overflow: hidden; background: var(--color-white); border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
  }
  .vm-bar { display: flex; justify-content: space-between; gap: 0.5rem; padding: 0.7rem 1rem; font-size: 0.75rem; font-weight: 600; color: var(--color-text); background: rgba(38, 50, 56, 0.05); }
  .rec { display: inline-flex; align-items: center; gap: 0.4rem; color: #d32f2f; font-weight: 800; }
  .rec i { width: 8px; height: 8px; border-radius: 50%; background: #d32f2f; animation: blink 1.2s infinite; }
  @keyframes blink { 50% { opacity: 0.2; } }
  .vm-stage { position: relative; aspect-ratio: 16 / 10; background: #e0e0e0; display: grid; place-items: center; }
  .vm-patient { display: flex; flex-direction: column; align-items: center; gap: 0.8rem; }
  .avatar { width: 84px; height: 84px; border-radius: 50%; background: var(--color-primary); }
  .avatar.small { width: 46px; height: 46px; }
  .pills { display: flex; gap: 0.5rem; }
  .pills span { width: 34px; height: 52px; border-radius: 8px; background: #bdbdbd; opacity: 0.9; }
  .vm-patient em, .vm-pharma em { font-style: normal; font-size: 0.72rem; color: var(--color-text-muted); }
  .vm-pharma { position: absolute; right: 4%; bottom: 6%; display: flex; flex-direction: column; align-items: center; gap: 0.3rem; padding: 0.6rem; border-radius: 14px; background: var(--color-white); border: 1px solid var(--color-border); }
  .vm-controls { display: flex; justify-content: center; gap: 0.8rem; padding: 0.8rem; background: var(--color-white); }
  .vm-controls span { width: 34px; height: 34px; border-radius: 50%; background: rgba(38, 50, 56, 0.1); }
  .vm-controls .end { background: #d32f2f; }
  .checklist { list-style: none; display: flex; flex-direction: column; gap: 0.9rem; }
  .check-item {
    width: 100%; display: flex; gap: 0.9rem; align-items: flex-start; text-align: left; border-radius: 18px; padding: 1rem 1.2rem;
    color: var(--color-text); background: var(--color-white); border: 1px solid var(--color-border); font-weight: 400;
  }
  .check-item:hover { background: rgba(22, 128, 58, 0.05); transform: translateX(-4px); }
  .check-item .box { flex-shrink: 0; width: 26px; height: 26px; border-radius: 8px; display: grid; place-items: center; color: transparent; border: 2px solid var(--color-border); transition: all 0.3s; margin-top: 2px; }
  .check-item.done .box { color: var(--color-white); background: var(--color-primary); border-color: var(--color-primary); }
  .check-text { display: flex; flex-direction: column; gap: 0.25rem; }
  .check-text strong { font-size: 1.02rem; color: var(--color-text); }
  .check-text small { font-size: 0.9rem; color: var(--color-text-muted); line-height: 1.5; }
  .check-item.done { border-color: var(--color-primary); }

  /* ===== Slide 8 ===== */
  .toggle { display: inline-flex; align-self: flex-start; padding: 0.3rem; border-radius: 999px; background: var(--color-white); border: 1px solid var(--color-border); }
  .toggle button { background: transparent; box-shadow: none; padding: 0.6rem 1.2rem; font-size: 0.9rem; color: var(--color-text-muted); }
  .toggle button:hover { background: rgba(38, 50, 56, 0.05); transform: none; box-shadow: none; }
  .toggle button.on { background: var(--color-primary); color: var(--color-white); font-weight: 700; }
  .compare { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1rem, 2.4vw, 2rem); }
  .cmp { transition: opacity 0.85s ease, transform 0.95s cubic-bezier(0.16, 1, 0.3, 1), filter 0.85s ease, flex 0.4s; }
  .cmp-sup { background: var(--color-white); border: 1px solid var(--color-border); }
  .cmp-med { background: var(--color-white); border: 1px solid var(--color-border); }
  .chip { display: inline-block; margin-bottom: 0.8rem; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.06em; }
  .chip-gold { color: var(--color-white); background: var(--color-primary-light); }
  .chip-green { color: var(--color-white); background: var(--color-primary); }
  .vis .compare[data-mode='sup'] .cmp-med,
  .vis .compare[data-mode='med'] .cmp-sup { opacity: 0.25; transform: scale(0.95); filter: grayscale(0.8); }
  .vis .compare[data-mode='sup'] .cmp-sup,
  .vis .compare[data-mode='med'] .cmp-med { transform: scale(1.03); box-shadow: var(--shadow-md); }
  .root-cause { display: flex; align-items: center; gap: 1rem; padding: 1.1rem 1.4rem; }

  /* ===== Slide 9 ===== */
  .slide.danger {
    background: transparent;
  }
  .alert-panel {
    border-radius: 26px; padding: clamp(1.2rem, 2.6vw, 2rem);
    background: var(--color-white);
    border: 2px solid #d32f2f;
  }
  .alert-panel.glow { box-shadow: var(--shadow-sm); }
  .alert-top { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1.2rem; color: #d32f2f; letter-spacing: 0.1em; font-size: 0.95rem; }
  .risk-list { list-style: none; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
  .risk-list li { display: flex; gap: 0.9rem; padding: 1.1rem; border-radius: 18px; background: var(--color-white); border: 1px solid #ffcdd2; }
  .risk-ico { flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font-weight: 900; color: var(--color-white); background: #d32f2f; }
  .risk-list h3 { font-size: 1.05rem; color: var(--color-text); margin-bottom: 0.35rem; }
  .risk-list p { font-size: 0.95rem; color: var(--color-text-muted); line-height: 1.55; }
  .risk-list strong { color: var(--color-text); }

  /* ===== Slide 10 ===== */
  .slide.final {
    background: transparent;
  }
  .final-card {
    position: relative; padding: clamp(1.2rem, 2.5vw, 2rem); border-radius: 30px; text-align: center;
    background: var(--color-white); border: 1px solid var(--color-border);
    overflow: hidden;
    box-shadow: var(--shadow-md);
  }
  .final-card::before, .final-card::after { display: none; }
  .final-card > * { position: relative; z-index: 1; }
  .final-card h2 { font-size: clamp(1.3rem, 2.5vw, 2rem); line-height: 1.15; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 1.8rem; color: var(--color-primary-dark); }
  .final-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: left; }
  .final-block { padding: 1.1rem; border-radius: 16px; background: rgba(38, 50, 56, 0.02); border: 1px solid var(--color-border); }
  .final-block h3 { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-primary); margin-bottom: 0.4rem; }
  .final-block h3.mt { margin-top: 0.9rem; }
  .final-block p { font-size: 0.95rem; color: var(--color-text); line-height: 1.5; }
  .final-actions { margin-top: 2rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
  .btn-gold { background: var(--color-primary); color: var(--color-white); box-shadow: var(--shadow-sm); }
  .btn-gold:hover { background: var(--color-primary-dark); }
  .btn-ghost { background: transparent; color: var(--color-text); border: 1px solid var(--color-border); box-shadow: none; }
  .btn-ghost:hover { background: rgba(38, 50, 56, 0.05); box-shadow: none; }

  /* ===== Indicador lateral ===== */
  .slide-nav {
    position: fixed; right: clamp(0.6rem, 1.6vw, 1.6rem); top: 50%; transform: translateY(-50%) translateX(30px);
    z-index: 1100; display: flex; flex-direction: column; align-items: center; gap: 0.8rem;
    padding: 0.9rem 0.55rem; border-radius: 999px; opacity: 0; pointer-events: none;
    background: var(--color-white); border: 1px solid var(--color-border);
    transition: opacity 0.4s ease, transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .slide-nav.show { opacity: 1; pointer-events: auto; transform: translateY(-50%); }
  .slide-counter { font-size: 0.7rem; color: var(--color-text-muted); writing-mode: horizontal-tb; text-align: center; line-height: 1.1; font-weight: 600; }
  .slide-counter strong { display: block; color: var(--color-text); font-size: 0.95rem; }
  .slide-nav ul { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
  .dot { width: 9px; height: 9px; padding: 0; border-radius: 50%; background: rgba(38, 50, 56, 0.15); box-shadow: none; transition: all 0.3s; }
  .dot:hover { background: rgba(38, 50, 56, 0.3); transform: scale(1.3); box-shadow: none; }
  .dot.on { background: var(--color-primary); height: 22px; border-radius: 8px; box-shadow: none; }

  /* ===== Responsivo ===== */
  @media (max-width: 1020px) {
    .grid-4 { grid-template-columns: repeat(2, 1fr); }
    .final-grid { grid-template-columns: repeat(2, 1fr); }
    .risk-list { grid-template-columns: 1fr; }
    .stepper { grid-template-columns: 1fr; gap: 1rem; padding-left: 0; }
    .track { top: 1rem; bottom: 1rem; left: 22px; right: auto; width: 4px; height: auto; }
    .track-fill { transform-origin: top; transform: scaleY(var(--f)); }
    .step { flex-direction: row; align-items: flex-start; text-align: left; }
    .step-dot { flex-shrink: 0; }
  }
  @media (max-width: 760px) {
    .grid-2, .mosaic, .security-panel, .grid-clinical, .compare { grid-template-columns: 1fr; }
    .grid-4, .final-grid { grid-template-columns: 1fr; }
    .rv-l, .rv-r, .rv-slide-l, .rv-slide-r { transform: translateY(40px); }
    .slide-nav { right: 0.3rem; padding: 0.6rem 0.35rem; }
    .slide-counter { display: none; }
    .slide { padding-top: 4rem; padding-bottom: 3rem; }
  }
  @media (prefers-reduced-motion: reduce) {
    .rv { transition-duration: 0.01s; transition-delay: 0s; }
    .alert-panel.glow, .ethic-banner.pulse, .btn-gold, .final-card::before, .vault-ring { animation: none; }
  }
</style>

<script>
  let props = $props();
  let currentRatio = $derived(props.currentRatio || 0);
  let scrollToPhase = $derived(props.scrollToPhase);
  let compareMode = $state('sup');
  let checks = $state([true, false, false]);

  const phases = [
    {
      eyebrow: '02 · Conceito-chave',
      title: 'Telefarmácia não é venda online.',
      lead: 'É exercício clínico mediado por tecnologia — com escuta, registro e responsabilidade profissional.',
      accent: 'green',
      points: [
        ['Exercício clínico', 'Avaliar, orientar e acompanhar o paciente com método.'],
        ['Mero comércio', 'Comprar e vender medicamentos sem cuidado clínico não caracteriza telefarmácia.']
      ]
    },
    {
      eyebrow: '03 · Modalidades',
      title: 'Quatro formas de levar o cuidado mais longe.',
      lead: 'A tecnologia amplia o acesso sem substituir o raciocínio clínico do farmacêutico.',
      accent: 'light',
      points: [
        ['Teleconsulta', 'Atendimento direto e em tempo real para avaliação e orientação.'],
        ['Teleinterconsulta', 'Discussão de caso entre profissionais da equipe de saúde.'],
        ['Telemonitoramento', 'Acompanhamento de parâmetros, reações e adesão.'],
        ['Teleorientação', 'Aconselhamento, triagem e encaminhamento responsável.']
      ]
    },
    {
      eyebrow: '04 · Arcabouço legal',
      title: 'Inovação também precisa de limite.',
      lead: 'O cuidado digital só é seguro quando respeita as normas que protegem paciente, profissional e serviço.',
      accent: 'light',
      laws: [
        ['Lei Federal nº 14.510/2022', 'Disciplina a telessaúde no Brasil, incluindo o SUS.'],
        ['Resolução CFF nº 10/2024', 'Regulamenta tecnologias, Saúde Digital e Inteligência Artificial na prática farmacêutica.']
      ],
      warning: 'A responsabilidade técnica de farmácias não pode ser assumida de forma remota. A presença física do RT é obrigatória.'
    },
    {
      eyebrow: '05 · Segurança da informação',
      title: 'O prontuário é parte do cuidado.',
      lead: 'Privacidade não é detalhe operacional: é requisito clínico, ético e legal.',
      accent: 'light',
      points: [
        ['LGPD', 'Dados de saúde são dados pessoais sensíveis e exigem proteção reforçada.'],
        ['Registro clínico', 'Todo atendimento deve ser documentado em prontuário seguro.'],
        ['Assinatura digital', 'Prescrições precisam de certificação ICP-Brasil quando aplicável.']
      ],
      visual: 'shield'
    },
    {
      eyebrow: '06 · Nosso protótipo',
      title: 'Uma jornada simples para uma decisão segura.',
      lead: 'O site organiza o primeiro contato e direciona cada pessoa para o próximo passo.',
      accent: 'light',
      steps: [
        ['01', 'Acolhimento', 'Linguagem clara e humanizada.'],
        ['02', 'Triagem', 'Identificação da necessidade principal.'],
        ['03', 'Consentimento', 'Transparência, sigilo e LGPD.'],
        ['04', 'Direcionamento', 'Teleconsulta ou encaminhamento presencial.']
      ]
    },
    {
      eyebrow: '07 · Prática clínica',
      title: 'Tecnologia para acompanhar — não para automatizar o cuidado.',
      lead: 'Na teleconsulta, o farmacêutico transforma informação em decisão compartilhada.',
      accent: 'light',
      points: [
        ['Conciliação terapêutica', 'Conferência visual das caixas para evitar duplicidades.'],
        ['Adesão ao tratamento', 'Investigação de esquecimentos, rotina e efeitos colaterais.'],
        ['Educação em saúde', 'Orientação sobre armazenamento e horários de tomada.']
      ],
      visual: 'call'
    },
    {
      eyebrow: '08 · Prescrição e escopo',
      title: 'Diferenciar orientação de prescrição é proteger o paciente.',
      lead: 'O farmacêutico atua dentro do seu escopo, com critério técnico e limites bem definidos.',
      accent: 'light',
      compare: true
    },
    {
      eyebrow: '09 · Red flags',
      title: 'Quando a tela não basta, o encaminhamento é cuidado.',
      lead: 'Reconhecer sinais de alarme é uma competência clínica — e uma responsabilidade ética.',
      accent: 'red',
      points: [
        ['Sintomas de emergência', 'Dor intensa, falta de ar, confusão ou piora súbita exigem serviço imediato.'],
        ['Limite do exame físico', 'Se a avaliação remota for insuficiente, não se deve concluir o caso.'],
        ['Conduta ética', 'Orientar, registrar e encaminhar sem atrasar o atendimento necessário.']
      ]
    },
    {
      eyebrow: '10 · Encerramento',
      title: 'Telefarmácia: tecnologia a serviço do cuidado humano.',
      lead: 'A proposta é ampliar acesso, fortalecer a formação e aproximar ciência da comunidade.',
      accent: 'green',
      closing: true
    }
  ];

  function getT(index) {
    const center = (index + 1.5) / 10;
    return (currentRatio - center) / 0.055;
  }

  function visibility(t) {
    const distance = Math.abs(t);
    return {
      opacity: Math.max(0, 1 - Math.max(0, distance - 0.18) * 1.8),
      transform: `translateY(${Math.max(-1, Math.min(1, t)) * 24}px) scale(${1 - Math.min(0.025, Math.abs(t) * 0.025)})`
    };
  }

  function goTo(index) {
    scrollToPhase?.(index + 1);
  }
</script>

<div class="slides-wrap" aria-label="Apresentação sobre telefarmácia">
  {#each phases as slide, index}
    {@const t = getT(index)}
    {@const style = visibility(t)}
    <section
      id={`slide-${index + 2}`}
      class={`slide redesign-slide theme-${slide.accent} ${Math.abs(t) < 0.7 ? 'is-active' : ''}`}
      aria-hidden={Math.abs(t) >= 0.9}
      style={`opacity: ${style.opacity}; transform: ${style.transform}; pointer-events: ${Math.abs(t) < 0.82 ? 'auto' : 'none'}; z-index: ${Math.abs(t) < 0.9 ? 2 : 1};`}
    >
      <div class="slide-frame">
        <div class="slide-topline">
          <span class="slide-eyebrow">{slide.eyebrow}</span>
          <span class="slide-index">{String(index + 2).padStart(2, '0')} / 10</span>
        </div>

        <div class="slide-content">
          <div class="slide-main-grid">
            <div class="slide-main">
              <header class="slide-copy">
                <h2>{slide.title}</h2>
                <p class="slide-lead">{slide.lead}</p>
              </header>

          {#if slide.points}
            <div class={`point-grid ${slide.points.length === 2 ? 'two' : ''}`}>
              {#each slide.points as point, pointIndex}
                <article class={`point ${slide.accent === 'red' ? 'point-alert' : ''}`}>
                  <span class="point-number">0{pointIndex + 1}</span>
                  <div>
                    <h3>{point[0]}</h3>
                    <p>{point[1]}</p>
                  </div>
                </article>
              {/each}
            </div>
          {:else if slide.laws}
            <div class="law-grid">
              {#each slide.laws as law}
                <article class="law-item">
                  <span class="law-mark">§</span>
                  <div><h3>{law[0]}</h3><p>{law[1]}</p></div>
                </article>
              {/each}
            </div>
            <aside class="warning-strip"><strong>Limite essencial</strong><span>{slide.warning}</span></aside>
          {:else if slide.steps}
            <div class="journey">
              {#each slide.steps as step, stepIndex}
                <button class:journey-active={stepIndex <= 2} class="journey-step" type="button" onclick={() => goTo(stepIndex + 5)}>
                  <span class="journey-number">{step[0]}</span>
                  <span><strong>{step[1]}</strong><small>{step[2]}</small></span>
                </button>
              {/each}
            </div>
          {:else if slide.compare}
            <div class="compare-header">
              <span>Escolha o enquadramento para comparar</span>
              <div class="compare-tabs">
                <button class:chosen={compareMode === 'sup'} onclick={() => compareMode = 'sup'}>Suplemento</button>
                <button class:chosen={compareMode === 'med'} onclick={() => compareMode = 'med'}>Medicamento</button>
              </div>
            </div>
            <div class="compare-grid">
              <article class:dimmed={compareMode === 'med'} class="compare-item supplement"><span class="compare-label">SUPLEMENTOS</span><h3>Orientação responsável</h3><p>Informar composição, uso adequado e limites da comunicação ao paciente.</p></article>
              <article class:dimmed={compareMode === 'sup'} class="compare-item medicine"><span class="compare-label">MEDICAMENTOS</span><h3>Prescrição farmacêutica</h3><p>Exige avaliação clínica, indicação, registro e respeito às normas profissionais.</p></article>
            </div>
          {:else if slide.closing}
            <div class="closing-grid">
              <div><span>01</span><strong>Ampliação do acesso</strong><p>Mais proximidade entre serviço e comunidade.</p></div>
              <div><span>02</span><strong>Sinergia acadêmica</strong><p>Aprendizagem aplicada à realidade local.</p></div>
              <div><span>03</span><strong>Cuidado humano</strong><p>Tecnologia com escuta e responsabilidade.</p></div>
            </div>
          {/if}
            </div>
            <aside class={`slide-art art-${slide.visual || (index % 3)}`} aria-hidden="true">
              {#if slide.visual === 'shield'}
                <div class="art-orbit orbit-a"></div><div class="art-orbit orbit-b"></div>
                <div class="art-shield"><span>LGPD</span><i>✓</i></div>
                <div class="art-caption">DADOS<br><strong>PROTEGIDOS</strong></div>
              {:else if slide.visual === 'call'}
                <div class="art-window"><div class="window-bar"><i></i><i></i><i></i><span>teleconsulta</span></div><div class="window-body"><div class="art-avatar"></div><div class="art-lines"><b></b><b></b><b></b></div></div><div class="window-footer"><span>● AO VIVO</span><span>12:45</span></div></div>
                <div class="art-pulse"></div>
              {:else if slide.warning}
                <div class="art-law">§<span>REGRA<br><strong>ANTES DA<br>INOVAÇÃO</strong></span></div>
              {:else if slide.compare}
                <div class="art-scale"><div class="scale-pan pan-left">ORIENTAR</div><div class="scale-pan pan-right">PRESCREVER</div><div class="scale-beam"></div><div class="scale-post"></div></div>
              {:else if slide.steps}
                <div class="art-route"><span>ACOLHER</span><i></i><span>AVALIAR</span><i></i><span>CUIDAR</span></div>
              {:else if slide.closing}
                <div class="art-sun"><div></div><span>CIÊNCIA<br><strong>+ CUIDADO</strong></span></div>
              {:else}
                <div class="art-number">{String(index + 2).padStart(2, '0')}</div><div class="art-line line-one"></div><div class="art-line line-two"></div><div class="art-dot"></div>
              {/if}
            </aside>
          </div>
        </div>

        <div class="slide-footer">
          <span>Telefarmácia & Serviços Digitais Farmacêuticos</span>
          <button type="button" onclick={() => goTo(index)}>{index === 0 ? 'Voltar ao início' : 'Anterior'}</button>
        </div>
      </div>
    </section>
  {/each}
</div>

<style>
  .slides-wrap { position:absolute; inset:0; z-index:10; pointer-events:none; color:#17362d; }
  .slide { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; padding:clamp(3.5rem,8vh,6rem) clamp(1.25rem,7vw,7.5rem); overflow:hidden; transition:opacity .35s ease, transform .5s cubic-bezier(.16,1,.3,1); }
  .slide::before { content:''; position:absolute; inset:0; background:radial-gradient(circle at 88% 18%, rgba(255,255,255,.7), transparent 32%), linear-gradient(135deg, rgba(255,255,255,.42), transparent 55%); pointer-events:none; }
  .theme-green { background:#0d5b3e; color:#f8f6ed; }
  .theme-light { background:#f2f1e9; color:#17362d; }
  .theme-red { background:#f6eeea; color:#2f2523; }
  .slide-frame { position:relative; width:min(1120px,100%); min-height:min(680px,86vh); display:flex; flex-direction:column; justify-content:space-between; gap:2rem; }
  .slide-topline,.slide-footer { display:flex; justify-content:space-between; align-items:center; gap:1rem; font-size:.7rem; letter-spacing:.12em; text-transform:uppercase; }
  .slide-topline { border-bottom:1px solid currentColor; padding-bottom:1rem; opacity:.72; }
  .slide-index { font-variant-numeric:tabular-nums; }
  .slide-content { display:flex; flex-direction:column; gap:clamp(2rem,5vh,3.8rem); flex:1; justify-content:center; padding:clamp(1.5rem,3vh,2.5rem) 0; }
  .slide-main-grid { display:grid; grid-template-columns:minmax(0,1.35fr) minmax(250px,.65fr); align-items:center; gap:clamp(2rem,7vw,7rem); }
  .slide-main { min-width:0; }
  .slide-copy { max-width:780px; }
  .slide-eyebrow { font-weight:800; }
  .slide-copy h2 { margin:.8rem 0 1.2rem; max-width:840px; font-size:clamp(2.3rem,5vw,5rem); line-height:.97; letter-spacing:-.055em; font-weight:800; }
  .slide-lead { max-width:680px; font-size:clamp(1rem,1.5vw,1.35rem); line-height:1.45; opacity:.78; }
  .point-grid,.law-grid,.closing-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; }
  .point-grid.two,.law-grid { grid-template-columns:repeat(2,1fr); }
  .point,.law-item,.compare-item,.closing-grid>div { position:relative; display:flex; gap:1rem; padding:1.35rem 1.4rem; border-top:2px solid currentColor; background:rgba(255,255,255,.5); min-height:150px; }
  .theme-green .point,.theme-green .closing-grid>div { background:rgba(255,255,255,.08); }
  .point-number,.law-mark,.closing-grid span { font-size:.78rem; font-weight:800; letter-spacing:.12em; opacity:.55; }
  .point h3,.law-item h3,.compare-item h3,.closing-grid strong { margin:0 0 .45rem; font-size:1.1rem; line-height:1.15; }
  .point p,.law-item p,.compare-item p,.closing-grid p { margin:0; font-size:.94rem; line-height:1.5; opacity:.72; }
  .warning-strip { display:flex; gap:1rem; align-items:baseline; padding:1.1rem 1.3rem; border-left:4px solid #b94d39; background:rgba(185,77,57,.1); color:#713126; }
  .warning-strip span { font-size:.95rem; line-height:1.45; }
  .journey { display:grid; grid-template-columns:repeat(4,1fr); gap:1rem; position:relative; }
  .journey::before { content:''; position:absolute; top:2rem; left:7%; right:7%; height:1px; background:#4e8c73; opacity:.45; }
  .journey-step { position:relative; z-index:1; display:flex; flex-direction:column; gap:1rem; align-items:flex-start; text-align:left; border:0; border-radius:0; padding:0; background:none; box-shadow:none; color:inherit; }
  .journey-number { display:grid; place-items:center; width:4rem; height:4rem; border:1px solid currentColor; border-radius:50%; background:#f2f1e9; color:#0d5b3e; font-weight:800; }
  .journey-active .journey-number { background:#0d5b3e; color:#f8f6ed; }
  .journey-step strong,.journey-step small { display:block; }
  .journey-step small { margin-top:.45rem; font-size:.85rem; line-height:1.4; opacity:.7; }
  .compare-header { display:flex; justify-content:space-between; align-items:center; gap:1rem; flex-wrap:wrap; font-size:.9rem; opacity:.7; }
  .compare-tabs { display:flex; border:1px solid currentColor; padding:.25rem; }
  .compare-tabs button { border:0; border-radius:0; padding:.65rem .9rem; box-shadow:none; color:inherit; background:transparent; font-size:.8rem; }
  .compare-tabs button.chosen { background:#0d5b3e; color:#f8f6ed; }
  .compare-grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
  .compare-item { transition:opacity .25s ease, transform .25s ease; min-height:180px; }
  .compare-item.dimmed { opacity:.35; transform:scale(.98); }
  .compare-label { font-size:.72rem; font-weight:800; letter-spacing:.12em; }
  .medicine { border-color:#b94d39; }
  .medicine .compare-label { color:#a44332; }
  .closing-grid { grid-template-columns:repeat(3,1fr); }
  .closing-grid>div { flex-direction:column; min-height:135px; }
  .slide-footer { border-top:1px solid currentColor; padding-top:1rem; opacity:.58; }
  .slide-footer button { border:0; padding:0; border-radius:0; box-shadow:none; background:none; color:inherit; font:inherit; text-transform:uppercase; letter-spacing:.12em; }
  .slide-footer button:hover { transform:none; box-shadow:none; opacity:.7; }
  .slide-art { min-height:330px; position:relative; display:grid; place-items:center; color:currentColor; opacity:.95; }
  .slide-art::before { content:''; position:absolute; inset:9% 4%; border:1px solid currentColor; border-radius:50%; opacity:.16; transform:rotate(-18deg) scaleY(.65); }
  .art-number { font-size:clamp(8rem,18vw,15rem); font-weight:800; line-height:1; letter-spacing:-.12em; opacity:.1; }
  .art-line { position:absolute; height:1px; background:currentColor; opacity:.35; transform-origin:left; }
  .line-one { width:78%; top:34%; left:8%; transform:rotate(-18deg); }.line-two { width:64%; top:60%; left:30%; transform:rotate(26deg); }
  .art-dot { width:18px; height:18px; border-radius:50%; background:#d7a95c; box-shadow:0 0 0 10px rgba(215,169,92,.16); position:absolute; top:31%; left:72%; }
  .art-orbit { position:absolute; width:240px; height:240px; border:1px solid currentColor; border-radius:50%; opacity:.3; }.orbit-a { transform:rotate(28deg) scaleX(.5); }.orbit-b { transform:rotate(-32deg) scaleX(.7); }
  .art-shield { position:relative; width:150px; height:180px; clip-path:polygon(50% 0, 92% 16%, 84% 67%, 50% 100%, 16% 67%, 8% 16%); background:#d7a95c; display:grid; place-items:center; color:#0d5b3e; font-weight:800; letter-spacing:.12em; }.art-shield span { font-size:1.2rem; }.art-shield i { position:absolute; bottom:42px; font-size:2rem; font-style:normal; }
  .art-caption { position:absolute; bottom:24%; right:0; font-size:.65rem; line-height:1.1; letter-spacing:.16em; opacity:.65; }.art-caption strong { font-size:.9rem; }
  .art-window { width:min(310px,100%); background:#fff; color:#17362d; box-shadow:18px 18px 0 rgba(13,91,62,.12); border:1px solid rgba(13,91,62,.2); transform:rotate(3deg); }.window-bar,.window-footer { display:flex; align-items:center; gap:6px; padding:.65rem .8rem; font-size:.62rem; letter-spacing:.1em; text-transform:uppercase; }.window-bar { border-bottom:1px solid #e4e5dd; }.window-bar i { width:7px; height:7px; border-radius:50%; background:#d7a95c; }.window-bar span { margin-left:auto; opacity:.55; }.window-body { height:150px; display:grid; place-items:center; background:linear-gradient(135deg,#dfe9df,#f7f6ef); }.art-avatar { width:75px; height:75px; border-radius:50%; background:#0d5b3e; box-shadow:0 0 0 14px rgba(13,91,62,.12); }.art-lines { position:absolute; margin:90px 0 0 150px; }.art-lines b { display:block; width:46px; height:5px; margin:6px; background:#8db9a1; }.window-footer { justify-content:space-between; color:#0d5b3e; }.art-pulse { position:absolute; width:200px; height:200px; border:1px solid #d7a95c; border-radius:50%; opacity:.45; }
  .art-law { display:flex; align-items:center; gap:1rem; font-size:9rem; line-height:.8; color:#b94d39; transform:rotate(-8deg); }.art-law span { font-size:.8rem; line-height:1.15; letter-spacing:.14em; }.art-law strong { font-size:1.25rem; }
  .art-route { display:flex; flex-direction:column; align-items:flex-start; gap:1.2rem; font-size:1rem; font-weight:800; letter-spacing:.1em; }.art-route i { display:block; width:1px; height:42px; background:currentColor; margin-left:7px; opacity:.4; }
  .art-scale { position:relative; width:270px; height:220px; }.scale-post { position:absolute; width:10px; height:180px; bottom:0; left:50%; background:currentColor; opacity:.6; }.scale-beam { position:absolute; width:220px; height:4px; top:50px; left:25px; background:currentColor; transform:rotate(-7deg); }.scale-pan { position:absolute; top:85px; border:1px solid currentColor; padding:1.2rem .8rem; font-size:.65rem; letter-spacing:.1em; }.pan-left { left:12px; transform:rotate(-7deg); }.pan-right { right:12px; transform:rotate(7deg); }
  .art-sun { width:230px; height:230px; display:grid; place-items:center; border:1px solid #d7a95c; border-radius:50%; position:relative; text-align:center; font-size:1rem; line-height:1.1; letter-spacing:.12em; }.art-sun::before,.art-sun::after { content:''; position:absolute; inset:-18px; border:1px solid #d7a95c; border-radius:50%; opacity:.35; }.art-sun::after { inset:-38px; opacity:.18; }.art-sun div { position:absolute; inset:36%; background:#d7a95c; border-radius:50%; opacity:.55; }.art-sun span { position:relative; z-index:1; }.art-sun strong { font-size:1.25rem; }
  @media (max-width:900px) {
    .slide { align-items:flex-start; overflow-y:auto; padding:4.5rem 1.25rem 2rem; }
    .slide-frame { min-height:calc(100vh - 6.5rem); gap:1.3rem; }
    .slide-content { justify-content:flex-start; gap:1.6rem; padding:1.2rem 0; }
    .slide-main-grid { grid-template-columns:1fr; gap:1.5rem; }
    .slide-art { min-height:170px; order:-1; }
    .slide-art::before { inset:5% 22%; }
    .art-number { font-size:7rem; }
    .art-shield { transform:scale(.72); }.art-orbit { transform:scale(.72); }
    .art-law { transform:scale(.72) rotate(-8deg); }.art-scale { transform:scale(.72); }
    .slide-copy h2 { font-size:clamp(2rem,8.5vw,3.5rem); }
    .slide-lead { font-size:1rem; }
    .point-grid,.point-grid.two,.law-grid,.closing-grid,.compare-grid { grid-template-columns:1fr; }
    .journey { grid-template-columns:1fr; gap:1rem; }
    .journey::before { top:2rem; bottom:2rem; left:2rem; right:auto; width:1px; height:auto; }
    .journey-step { flex-direction:row; align-items:flex-start; width:100%; }
    .journey-step span:last-child { padding-top:.45rem; }
    .slide-footer { font-size:.6rem; }
  }
  @media (prefers-reduced-motion:reduce) { .slide,.compare-item { transition:none; } }
</style>

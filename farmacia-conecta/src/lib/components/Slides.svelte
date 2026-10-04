<script>
  import { onMount } from 'svelte';

  const TOTAL = 10;
  const slideIds = ['sobre', ...Array.from({ length: 9 }, (_, i) => `slide-${i + 2}`)];

  let activeIndex = $state(0);
  let showNav = $state(false);
  let visible = $state({});
  let stepProgress = $state(0);
  let compareMode = $state('side');
  let checks = $state([true, false, false]);
  let slide6Ref = $state(null);

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

  function goTo(i) {
    const el = document.getElementById(slideIds[i]);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function toTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function pad(n) {
    return String(n).padStart(2, '0');
  }

  onMount(() => {
    const vh = () => window.innerHeight;
    let ticking = false;

    const update = () => {
      ticking = false;
      const mid = vh() * 0.5;
      let idx = 0;
      let first = null;
      let last = null;
      slideIds.forEach((id, i) => {
        const el = document.getElementById(id);
        if (!el) return;
        const r = el.getBoundingClientRect();
        if (i === 0) first = r;
        if (i === slideIds.length - 1) last = r;
        if (r.top <= mid + 2) idx = i;
      });
      activeIndex = idx;
      showNav = !!first && !!last && first.top <= mid && last.bottom >= mid;

      // Progresso do stepper (slide 6)
      if (slide6Ref) {
        const r = slide6Ref.getBoundingClientRect();
        const p = (vh() * 0.85 - r.top) / (r.height * 0.85);
        stepProgress = Math.max(0, Math.min(1, p));
      }
    };

    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };

    // Revelação por slide
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          visible[e.target.id] = e.intersectionRatio > 0.35;
        });
      },
      { threshold: [0, 0.2, 0.35, 0.6, 1] }
    );
    slideIds.slice(1).forEach((id) => {
      const el = document.getElementById(id);
      if (el) io.observe(el);
    });

    // Scroll snap suave apenas enquanto os slides estão na tela
    const snapIo = new IntersectionObserver(
      (entries) => {
        const on = entries.some((e) => e.isIntersecting);
        document.documentElement.style.scrollSnapType = on ? 'y proximity' : '';
      },
      { threshold: 0.05 }
    );
    const wrap = document.getElementById('slides-wrap');
    if (wrap) snapIo.observe(wrap);

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
    update();

    return () => {
      io.disconnect();
      snapIo.disconnect();
      document.documentElement.style.scrollSnapType = '';
      window.removeEventListener('scroll', onScroll);
      window.removeEventListener('resize', onScroll);
    };
  });
</script>

<!-- Indicador lateral de slide ativo -->
<nav class="slide-nav" class:show={showNav} aria-label="Navegação entre slides">
  <div class="slide-counter">
    <strong>{pad(activeIndex + 1)}</strong><span>/{TOTAL}</span>
  </div>
  <ul>
    {#each slideIds as _, i}
      <li>
        <button
          type="button"
          class="dot"
          class:on={i === activeIndex}
          aria-label="Ir para o slide {i + 1}"
          aria-current={i === activeIndex ? 'true' : undefined}
          onclick={() => goTo(i)}
        ></button>
      </li>
    {/each}
  </ul>
</nav>

<div id="slides-wrap" class="slides-wrap">
  <!-- SLIDE 2 -->
  <section id="slide-2" class="slide" class:vis={visible['slide-2']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 02 · Conceito</span>
        <h2>O que Define a Telefarmácia no Brasil?</h2>
        <p>Exercício Clínico vs. Mero Comércio Eletrônico</p>
      </header>

      <div class="grid-2">
        <article class="card card-ok rv rv-l" style="--d:.15s">
          <div class="card-tag ok">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5" /></svg>
            Definição Legal
          </div>
          <h3>Farmácia Clínica a distância</h3>
          <p>
            É o exercício da <strong>Farmácia Clínica a distância</strong>, prestado de forma síncrona ou assíncrona,
            focado na promoção da saúde e no uso racional de medicamentos.
          </p>
          <div class="norm">
            <span>Base normativa</span>
            <strong>Art. 2º · Resolução CFF nº 727/2022</strong>
          </div>
        </article>

        <article class="card card-no rv rv-r" style="--d:.3s">
          <svg class="ban" viewBox="0 0 24 24" width="120" height="120" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="12" cy="12" r="10" /><path d="m4.9 4.9 14.2 14.2" /></svg>
          <div class="card-tag no">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12" /></svg>
            Alerta · Diferenciação Crucial
          </div>
          <h3>E-commerce não é Telefarmácia</h3>
          <p>
            A simples venda on-line de produtos ou e-commerce por aplicativos <strong>NÃO constitui Telefarmácia</strong>.
          </p>
        </article>
      </div>
    </div>
  </section>

  <!-- SLIDE 3 -->
  <section id="slide-3" class="slide alt" class:vis={visible['slide-3']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 03 · Atendimento remoto</span>
        <h2>Modalidades da Telefarmácia</h2>
        <p>Nota Técnica CFF 2022 &amp; Resolução 727/2022</p>
      </header>

      <div class="grid-4">
        {#each modalities as m, i}
          <article class="card glass hover-lift rv rv-up" style="--d:{0.15 + i * 0.14}s">
            <div class="icon-bubble">
              {#if m.icon === 'video'}
                <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 8-6 4 6 4V8Z" /><rect x="2" y="6" width="14" height="12" rx="2" /></svg>
              {:else if m.icon === 'users'}
                <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" /><circle cx="9" cy="7" r="4" /><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" /></svg>
              {:else if m.icon === 'activity'}
                <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>
              {:else}
                <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6M8 13h8M8 17h6" /></svg>
              {/if}
            </div>
            <span class="num">0{i + 1}</span>
            <h3>{m.title}</h3>
            <p>{m.text}</p>
          </article>
        {/each}
      </div>
    </div>
  </section>

  <!-- SLIDE 4 -->
  <section id="slide-4" class="slide" class:vis={visible['slide-4']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 04 · Arcabouço legal</span>
        <h2>Legislação e Limites da Atuação Digital</h2>
      </header>

      <div class="mosaic">
        <article class="card glass badge-card rv rv-l" style="--d:.15s">
          <span class="law">Lei Federal nº 14.510/2022</span>
          <p>Disciplina a Telessaúde no Brasil em âmbito nacional e no SUS.</p>
        </article>
        <article class="card glass badge-card rv rv-r" style="--d:.3s">
          <span class="law">Resolução CFF nº 10/2024</span>
          <p>Regulamenta o uso de novas tecnologias, Saúde Digital e Inteligência Artificial na prática farmacêutica.</p>
        </article>
        <article class="ethic-banner pulse-red rv rv-zoom" class:pulse={activeIndex === 3} style="--d:.45s">
          <div class="ethic-label">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" /><path d="M12 9v4M12 17h.01" /></svg>
            Resolução CFF nº 727/2022 · Art. 3º
          </div>
          <h3>É VEDADO (PROIBIDO) assumir a Responsabilidade Técnica (RT) de farmácias de forma remota/não presencial.</h3>
          <p>A presença física do RT é obrigatória.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- SLIDE 5 -->
  <section id="slide-5" class="slide alt" class:vis={visible['slide-5']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 05 · Segurança cibernética</span>
        <h2>Privacidade e Registro Clínico Obrigatório</h2>
      </header>

      <div class="security-panel">
        <div class="vault rv rv-zoom" style="--d:.1s" aria-hidden="true">
          <div class="vault-body">
            <div class="vault-ring"></div>
            <svg class="doc" viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" /><path d="M14 2v6h6M9 13h6M9 17h4" /></svg>
            <svg class="lock" viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 8 0v4" /></svg>
            <span class="seal">LGPD</span>
          </div>
          <div class="vault-base">COFRE DIGITAL</div>
        </div>

        <div class="sec-list">
          <article class="card glass sec-item rv rv-r" style="--d:.2s">
            <div class="sec-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" /></svg>
            </div>
            <div>
              <h3>LGPD (Lei nº 13.709/2018)</h3>
              <p>Dados de saúde do paciente são classificados legalmente como <strong>dados pessoais sensíveis</strong>.</p>
            </div>
          </article>
          <article class="card glass sec-item rv rv-r" style="--d:.35s">
            <div class="sec-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="11" width="16" height="10" rx="2" /><path d="M8 11V7a4 4 0 0 1 8 0v4" /></svg>
            </div>
            <div>
              <h3>Prontuário Eletrônico (Art. 5º da Res. 727/22)</h3>
              <p>Obrigatoriedade de registrar todos os atendimentos prestados em prontuário seguro, garantindo sigilo profissional.</p>
            </div>
          </article>
          <article class="card glass sec-item rv rv-r" style="--d:.5s">
            <div class="sec-icon">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="9" r="6" /><path d="m8.5 14-1.5 8 5-3 5 3-1.5-8" /></svg>
            </div>
            <div>
              <h3>Assinatura Digital Rastreável</h3>
              <p>Todas as orientações, pareceres e prescrições geradas precisam de certificação ICP-Brasil ou assinatura digital válida.</p>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- SLIDE 6 -->
  <section id="slide-6" class="slide" class:vis={visible['slide-6']} bind:this={slide6Ref}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 06 · O protótipo</span>
        <h2>Fluxo de Atendimento no Nosso Protótipo Digital</h2>
        <p>A jornada do paciente no nosso site</p>
      </header>

      <ol class="stepper rv" style="--d:.1s; --p:{stepProgress}">
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
  </section>

  <!-- SLIDE 7 -->
  <section id="slide-7" class="slide alt" class:vis={visible['slide-7']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 07 · Prática clínica I</span>
        <h2>Cuidado Clínico na Teleconsulta</h2>
        <p>Foco em Pacientes Hipertensos, Diabéticos e Polimedicados</p>
      </header>

      <div class="grid-clinical">
        <div class="video-mock rv rv-focus" style="--d:.15s" aria-hidden="true">
          <div class="vm-bar">
            <span class="rec"><i></i> AO VIVO</span>
            <span>Teleconsulta Farmacêutica</span>
            <span>00:12:45</span>
          </div>
          <div class="vm-stage">
            <div class="vm-patient">
              <div class="avatar"></div>
              <div class="pills">
                <span></span><span></span><span></span>
              </div>
              <em>Paciente · caixas de medicamentos</em>
            </div>
            <div class="vm-pharma">
              <div class="avatar small"></div>
              <em>Farmacêutico</em>
            </div>
          </div>
          <div class="vm-controls">
            <span></span><span></span><span class="end"></span>
          </div>
        </div>

        <ul class="checklist">
          {#each checklist as c, i}
            <li class="rv rv-r" style="--d:{0.3 + i * 0.15}s">
              <button type="button" class="check-item" class:done={checks[i]} onclick={() => (checks[i] = !checks[i])} aria-pressed={checks[i]}>
                <span class="box">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5" /></svg>
                </span>
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

  <!-- SLIDE 8 -->
  <section id="slide-8" class="slide" class:vis={visible['slide-8']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow">Slide 08 · Prática clínica II</span>
        <h2>Diferenciação Regulatória e Prescrição</h2>
        <p>Suplementos Alimentares vs. Medicamentos</p>
      </header>

      <div class="toggle rv" style="--d:.1s" role="group" aria-label="Alternar comparação">
        <button type="button" class:on={compareMode === 'side'} onclick={() => (compareMode = 'side')}>Lado a lado</button>
        <button type="button" class:on={compareMode === 'sup'} onclick={() => (compareMode = 'sup')}>Suplemento</button>
        <button type="button" class:on={compareMode === 'med'} onclick={() => (compareMode = 'med')}>Medicamento</button>
      </div>

      <div class="compare" data-mode={compareMode}>
        <article class="card cmp cmp-sup rv rv-slide-l" style="--d:.2s">
          <span class="chip chip-gold">Anvisa</span>
          <h3>Suplementos Alimentares</h3>
          <p>Não são medicamentos; destinam-se a suprir nutrientes em pessoas saudáveis e <strong>não tratam doenças</strong>.</p>
        </article>
        <article class="card cmp cmp-med rv rv-slide-r" style="--d:.2s">
          <span class="chip chip-green">Res. CFF nº 586/2013</span>
          <h3>Prescrição Farmacêutica</h3>
          <p>Autonomia restrita à indicação de <strong>Medicamentos Isentos de Prescrição (MIPs)</strong> e fitoterápicos.</p>
        </article>
      </div>

      <div class="root-cause card glass rv rv-up" style="--d:.45s">
        <div class="icon-bubble sm">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.3-4.3" /></svg>
        </div>
        <p><strong>Análise de Causa Raiz:</strong> queixas como cansaço ou insônia exigem investigação detalhada antes de qualquer indicação direta de suplementos.</p>
      </div>
    </div>
  </section>

  <!-- SLIDE 9 -->
  <section id="slide-9" class="slide danger" class:vis={visible['slide-9']}>
    <div class="slide-inner">
      <header class="slide-head rv">
        <span class="eyebrow eyebrow-red">Slide 09 · Triagem digital</span>
        <h2>Limites Clínicos e Sinais de Alarme (Red Flags)</h2>
        <p>Triagem Digital e Limites do Atendimento</p>
      </header>

      <div class="alert-panel rv rv-zoom" class:glow={activeIndex === 8} style="--d:.15s">
        <div class="alert-top">
          <svg viewBox="0 0 24 24" width="30" height="30" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" /><path d="M12 9v4M12 17h.01" /></svg>
          <strong>ALERTA CRÍTICO · EMERGÊNCIA</strong>
        </div>
        <ul class="risk-list">
          <li class="rv rv-up" style="--d:.3s">
            <span class="risk-ico">!</span>
            <div>
              <h3>Sintomas de Emergência</h3>
              <p>Dor no peito, falta de ar súbita, febre alta persistente ou sinais de AVC exigem <strong>Pronto-Atendimento Presencial Imediato</strong>.</p>
            </div>
          </li>
          <li class="rv rv-up" style="--d:.45s">
            <span class="risk-ico">!</span>
            <div>
              <h3>Impossibilidade do Exame Físico</h3>
              <p>O canal remoto não substitui a palpação, ausculta ou inspeção presencial.</p>
            </div>
          </li>
          <li class="rv rv-up" style="--d:.6s">
            <span class="risk-ico">!</span>
            <div>
              <h3>Conduta Ética</h3>
              <p>Quando a queixa ultrapassar o escopo remoto, o sistema e o farmacêutico devem emitir parecer de encaminhamento imediato.</p>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- SLIDE 10 -->
  <section id="slide-10" class="slide final" class:vis={visible['slide-10']}>
    <div class="slide-inner">
      <article class="final-card rv rv-zoom" style="--d:.1s">
        <span class="eyebrow">Slide 10 · Conclusão e encerramento</span>
        <h2>Telefarmácia: Tecnologia a Serviço do Cuidado Humano</h2>

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

        <div class="final-actions">
          <a class="btn btn-gold" href="#agendamento">Testar Protótipo</a>
          <button type="button" class="btn-ghost" onclick={toTop}>Voltar ao topo</button>
        </div>
      </article>
    </div>
  </section>
</div>

<style>
  .slides-wrap {
    --navy: #0b1f3a;
    --navy-2: #12305a;
    --navy-3: #0a1830;
    --green: #1fbf6b;
    --green-deep: #0d8d4b;
    --gold: #f5b942;
    --orange: #ff8a3d;
    --red: #ff4d5e;
    --ink: #eaf3ff;
    --muted: #a9bad3;
    position: relative;
    z-index: 2;
    color: var(--ink);
    background: var(--navy);
  }

  /* ===== Slide base ===== */
  .slide {
    position: relative;
    min-height: 100vh;
    min-height: 100dvh;
    scroll-snap-align: start;
    scroll-snap-stop: normal;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(4.5rem, 9vh, 7rem) clamp(1.25rem, 6vw, 6rem);
    background:
      radial-gradient(ellipse 60% 50% at 85% 0%, rgba(31, 191, 107, 0.16), transparent 70%),
      radial-gradient(ellipse 50% 50% at 0% 100%, rgba(245, 185, 66, 0.08), transparent 70%),
      linear-gradient(160deg, var(--navy) 0%, var(--navy-2) 100%);
    overflow: hidden;
  }
  .slide.alt {
    background:
      radial-gradient(ellipse 55% 55% at 10% 0%, rgba(31, 191, 107, 0.18), transparent 70%),
      radial-gradient(ellipse 50% 50% at 100% 100%, rgba(245, 185, 66, 0.1), transparent 70%),
      linear-gradient(200deg, var(--navy-3) 0%, #0f2a4d 100%);
  }
  .slide::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 28px 28px;
    mask-image: radial-gradient(ellipse at center, #000 20%, transparent 75%);
    pointer-events: none;
  }
  .slide-inner {
    position: relative;
    width: 100%;
    max-width: 1180px;
    display: flex;
    flex-direction: column;
    gap: clamp(1.4rem, 3.5vh, 2.6rem);
  }

  .slide-head h2 {
    font-size: clamp(1.7rem, 3.6vw, 3rem);
    line-height: 1.12;
    font-weight: 800;
    letter-spacing: -0.02em;
    padding-bottom: 0.14em;
    background: linear-gradient(90deg, #fff 30%, #bff0d6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
  }
  .slide-head p {
    margin-top: 0.55rem;
    color: var(--muted);
    font-size: clamp(1rem, 1.5vw, 1.2rem);
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
    color: var(--gold);
    background: rgba(245, 185, 66, 0.12);
    border: 1px solid rgba(245, 185, 66, 0.3);
  }
  .eyebrow-red {
    color: #ffb4a0;
    background: rgba(255, 77, 94, 0.14);
    border-color: rgba(255, 77, 94, 0.4);
  }

  /* ===== Reveal on scroll ===== */
  .rv {
    opacity: 0;
    transform: translateY(30px);
    filter: blur(8px);
    transition:
      opacity 0.85s ease,
      transform 0.95s cubic-bezier(0.16, 1, 0.3, 1),
      filter 0.85s ease;
    transition-delay: var(--d, 0s);
    will-change: transform, opacity;
  }
  .rv-l { transform: translateX(-90px); }
  .rv-r { transform: translateX(90px); }
  .rv-up { transform: translateY(50px); }
  .rv-zoom { transform: scale(0.92) translateY(20px); }
  .rv-focus { transform: scale(0.82); filter: blur(18px); }
  .rv-slide-l { transform: translateX(-220px); }
  .rv-slide-r { transform: translateX(220px); }
  .vis .rv {
    opacity: 1;
    transform: none;
    filter: none;
  }

  /* ===== Cards ===== */
  .card {
    border-radius: 22px;
    padding: clamp(1.3rem, 2.4vw, 2rem);
    position: relative;
  }
  .card h3 {
    font-size: clamp(1.05rem, 1.5vw, 1.3rem);
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #fff;
  }
  .card p {
    color: var(--muted);
    font-size: clamp(0.92rem, 1.2vw, 1.05rem);
    line-height: 1.6;
  }
  .card strong { color: #fff; }
  .glass {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);
  }
  .hover-lift { transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s, background 0.3s, opacity 0.85s ease, filter 0.85s ease; }
  .vis .hover-lift:hover {
    transform: translateY(-8px);
    border-color: rgba(31, 191, 107, 0.6);
    background: rgba(31, 191, 107, 0.1);
  }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1rem, 2.4vw, 2rem); }
  .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: clamp(0.9rem, 1.6vw, 1.4rem); }

  .icon-bubble {
    width: 56px; height: 56px;
    display: grid; place-items: center;
    border-radius: 16px;
    color: var(--green);
    background: rgba(31, 191, 107, 0.14);
    border: 1px solid rgba(31, 191, 107, 0.35);
    margin-bottom: 1rem;
  }
  .icon-bubble.sm { width: 46px; height: 46px; margin: 0; flex-shrink: 0; color: var(--gold); background: rgba(245,185,66,.12); border-color: rgba(245,185,66,.35); }
  .num {
    position: absolute; top: 1.1rem; right: 1.3rem;
    font-weight: 800; font-size: 1.6rem; color: rgba(255, 255, 255, 0.1);
  }

  /* ===== Slide 2 ===== */
  .card-ok {
    background: linear-gradient(160deg, rgba(31, 191, 107, 0.22), rgba(13, 141, 75, 0.1));
    border: 1px solid rgba(31, 191, 107, 0.5);
    box-shadow: 0 20px 50px rgba(13, 141, 75, 0.25);
  }
  .card-no {
    overflow: hidden;
    background: linear-gradient(160deg, rgba(255, 77, 94, 0.2), rgba(120, 20, 40, 0.14));
    border: 1px solid rgba(255, 77, 94, 0.5);
    box-shadow: 0 20px 50px rgba(255, 77, 94, 0.18);
  }
  .ban { position: absolute; right: -14px; bottom: -14px; color: rgba(255, 77, 94, 0.22); }
  .card-tag {
    display: inline-flex; align-items: center; gap: 0.45rem;
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 0.35rem 0.8rem; border-radius: 999px; margin-bottom: 1rem;
  }
  .card-tag.ok { color: #a8f5cb; background: rgba(31, 191, 107, 0.2); }
  .card-tag.no { color: #ffb0b8; background: rgba(255, 77, 94, 0.2); }
  .norm {
    margin-top: 1.2rem; padding: 0.8rem 1rem; border-radius: 14px;
    background: rgba(0, 0, 0, 0.22); display: flex; flex-direction: column; gap: 0.15rem;
  }
  .norm span { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--gold); font-weight: 700; }
  .norm strong { font-size: 0.98rem; }

  /* ===== Slide 4 ===== */
  .mosaic { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1rem, 2vw, 1.6rem); }
  .badge-card .law {
    display: inline-block; margin-bottom: 0.7rem; padding: 0.4rem 0.9rem; border-radius: 10px;
    font-weight: 800; font-size: 0.95rem; color: var(--navy);
    background: linear-gradient(90deg, var(--gold), #ffd98a);
  }
  .ethic-banner {
    grid-column: 1 / -1;
    padding: clamp(1.4rem, 3vw, 2.2rem);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(255, 77, 94, 0.22), rgba(255, 138, 61, 0.14));
    border: 2px solid rgba(255, 77, 94, 0.6);
    text-align: center;
  }
  .ethic-label {
    display: inline-flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem;
    color: #ffc2c8; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase;
  }
  .ethic-banner h3 { font-size: clamp(1.15rem, 2.3vw, 1.8rem); line-height: 1.3; color: #fff; font-weight: 800; }
  .ethic-banner p { margin-top: 0.6rem; color: #ffd0d4; font-weight: 600; }
  .ethic-banner.pulse { animation: redPulse 1.8s ease-in-out infinite; }
  @keyframes redPulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255, 77, 94, 0.55), 0 0 30px rgba(255, 77, 94, 0.25); }
    50% { box-shadow: 0 0 0 16px rgba(255, 77, 94, 0), 0 0 60px rgba(255, 77, 94, 0.55); }
  }

  /* ===== Slide 5 ===== */
  .security-panel { display: grid; grid-template-columns: 0.8fr 1.2fr; gap: clamp(1.4rem, 3vw, 3rem); align-items: center; }
  .vault { display: flex; flex-direction: column; align-items: center; gap: 0.8rem; }
  .vault-body {
    position: relative; width: min(270px, 60vw); aspect-ratio: 1;
    border-radius: 28px; display: grid; place-items: center;
    background: linear-gradient(145deg, #17335c, #0a1a33);
    border: 2px solid rgba(255, 255, 255, 0.15);
    box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.5), 0 24px 50px rgba(0, 0, 0, 0.45), 0 0 50px rgba(31, 191, 107, 0.15);
    overflow: hidden;
  }
  .vault-ring {
    position: absolute; inset: 18%; border-radius: 50%;
    border: 3px dashed rgba(245, 185, 66, 0.5);
    animation: spin 18s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  .doc { position: absolute; color: #fff; transform: translateY(-190px); opacity: 0; transition: transform 1.1s cubic-bezier(0.34, 1.3, 0.5, 1) 0.5s, opacity 0.5s ease 0.5s; }
  .lock { position: absolute; bottom: 14%; color: var(--gold); transform: scale(0); transition: transform 0.5s cubic-bezier(0.34, 1.8, 0.5, 1) 1.5s; }
  .seal {
    position: absolute; top: 12%; right: 10%; padding: 0.25rem 0.6rem; border-radius: 8px;
    font-size: 0.8rem; font-weight: 800; letter-spacing: 0.08em; color: var(--navy);
    background: linear-gradient(90deg, var(--green), #8cf0b9);
    transform: rotate(10deg) scale(0); transition: transform 0.5s cubic-bezier(0.34, 1.8, 0.5, 1) 1.9s;
  }
  .vis .doc { transform: translateY(-8px); opacity: 1; }
  .vis .lock { transform: scale(1); }
  .vis .seal { transform: rotate(10deg) scale(1); }
  .vault-base { font-size: 0.72rem; letter-spacing: 0.3em; font-weight: 700; color: var(--muted); }
  .sec-list { display: flex; flex-direction: column; gap: 1rem; }
  .sec-item { display: flex; gap: 1rem; align-items: flex-start; padding: 1.1rem 1.3rem; }
  .sec-icon {
    flex-shrink: 0; width: 46px; height: 46px; border-radius: 14px; display: grid; place-items: center;
    color: var(--green); background: rgba(31, 191, 107, 0.14); border: 1px solid rgba(31, 191, 107, 0.35);
  }

  /* ===== Slide 6 ===== */
  .stepper { position: relative; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; list-style: none; padding-top: 1rem; }
  .track { position: absolute; top: calc(1rem + 22px); left: 12%; right: 12%; height: 4px; border-radius: 4px; background: rgba(255, 255, 255, 0.12); }
  .track-fill { height: 100%; border-radius: 4px; width: 100%; transform-origin: left; transform: scaleX(var(--f)); background: linear-gradient(90deg, var(--green), var(--gold)); box-shadow: 0 0 14px rgba(31, 191, 107, 0.7); }
  .step { position: relative; display: flex; flex-direction: column; align-items: center; gap: 1.2rem; text-align: center; }
  .step-dot {
    position: relative; z-index: 1; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center;
    font-weight: 800; color: var(--muted); background: var(--navy-2); border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .step.lit .step-dot { color: var(--navy); background: var(--green); border-color: #bff0d6; box-shadow: 0 0 0 8px rgba(31, 191, 107, 0.2), 0 0 28px rgba(31, 191, 107, 0.7); transform: scale(1.12); }
  .step-card { opacity: 0.45; transform: translateY(10px) scale(0.97); transition: all 0.6s cubic-bezier(0.16, 1, 0.3, 1); width: 100%; padding: 1.2rem; }
  .step.lit .step-card { opacity: 1; transform: none; border-color: rgba(31, 191, 107, 0.5); }

  /* ===== Slide 7 ===== */
  .grid-clinical { display: grid; grid-template-columns: 1.15fr 1fr; gap: clamp(1.2rem, 3vw, 2.6rem); align-items: center; }
  .video-mock {
    border-radius: 22px; overflow: hidden; background: #060f1f; border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 28px 60px rgba(0, 0, 0, 0.5), 0 0 60px rgba(31, 191, 107, 0.15);
  }
  .vm-bar { display: flex; justify-content: space-between; gap: 0.5rem; padding: 0.7rem 1rem; font-size: 0.75rem; font-weight: 600; color: var(--muted); background: rgba(255, 255, 255, 0.05); }
  .rec { display: inline-flex; align-items: center; gap: 0.4rem; color: #ff8a95; font-weight: 800; }
  .rec i { width: 8px; height: 8px; border-radius: 50%; background: var(--red); animation: blink 1.2s infinite; }
  @keyframes blink { 50% { opacity: 0.2; } }
  .vm-stage { position: relative; aspect-ratio: 16 / 10; background: radial-gradient(circle at 50% 40%, #1a3d6b, #08162b); display: grid; place-items: center; }
  .vm-patient { display: flex; flex-direction: column; align-items: center; gap: 0.8rem; }
  .avatar { width: 84px; height: 84px; border-radius: 50%; background: linear-gradient(145deg, #3d7dd8, #1fbf6b); box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.08); }
  .avatar.small { width: 46px; height: 46px; box-shadow: none; }
  .pills { display: flex; gap: 0.5rem; }
  .pills span { width: 34px; height: 52px; border-radius: 8px; background: linear-gradient(180deg, #fff 0 35%, var(--orange) 35% 100%); opacity: 0.9; }
  .pills span:nth-child(2) { background: linear-gradient(180deg, #fff 0 35%, var(--green) 35% 100%); }
  .pills span:nth-child(3) { background: linear-gradient(180deg, #fff 0 35%, var(--gold) 35% 100%); }
  .vm-patient em, .vm-pharma em { font-style: normal; font-size: 0.72rem; color: var(--muted); }
  .vm-pharma { position: absolute; right: 4%; bottom: 6%; display: flex; flex-direction: column; align-items: center; gap: 0.3rem; padding: 0.6rem; border-radius: 14px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.15); }
  .vm-controls { display: flex; justify-content: center; gap: 0.8rem; padding: 0.8rem; background: rgba(255, 255, 255, 0.04); }
  .vm-controls span { width: 34px; height: 34px; border-radius: 50%; background: rgba(255, 255, 255, 0.14); }
  .vm-controls .end { background: var(--red); }
  .checklist { list-style: none; display: flex; flex-direction: column; gap: 0.9rem; }
  .check-item {
    width: 100%; display: flex; gap: 0.9rem; align-items: flex-start; text-align: left; border-radius: 18px; padding: 1rem 1.2rem;
    color: var(--ink); background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: none; font-weight: 400;
  }
  .check-item:hover { background: rgba(31, 191, 107, 0.1); transform: translateX(-4px); box-shadow: none; }
  .check-item .box { flex-shrink: 0; width: 26px; height: 26px; border-radius: 8px; display: grid; place-items: center; color: transparent; border: 2px solid rgba(255, 255, 255, 0.3); transition: all 0.3s; margin-top: 2px; }
  .check-item.done .box { color: var(--navy); background: var(--green); border-color: var(--green); }
  .check-text { display: flex; flex-direction: column; gap: 0.25rem; }
  .check-text strong { font-size: 1.02rem; color: #fff; }
  .check-text small { font-size: 0.9rem; color: var(--muted); line-height: 1.5; }
  .check-item.done { border-color: rgba(31, 191, 107, 0.55); }

  /* ===== Slide 8 ===== */
  .toggle { display: inline-flex; align-self: flex-start; padding: 0.3rem; border-radius: 999px; background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.14); }
  .toggle button { background: transparent; box-shadow: none; padding: 0.6rem 1.2rem; font-size: 0.9rem; color: var(--muted); }
  .toggle button:hover { background: rgba(255, 255, 255, 0.08); transform: none; box-shadow: none; }
  .toggle button.on { background: linear-gradient(90deg, var(--green), #38d98a); color: var(--navy); font-weight: 700; }
  .compare { display: grid; grid-template-columns: 1fr 1fr; gap: clamp(1rem, 2.4vw, 2rem); }
  .cmp { transition: opacity 0.85s ease, transform 0.95s cubic-bezier(0.16, 1, 0.3, 1), filter 0.85s ease, flex 0.4s; }
  .cmp-sup { background: linear-gradient(160deg, rgba(245, 185, 66, 0.18), rgba(255, 138, 61, 0.08)); border: 1px solid rgba(245, 185, 66, 0.45); }
  .cmp-med { background: linear-gradient(160deg, rgba(31, 191, 107, 0.2), rgba(13, 141, 75, 0.08)); border: 1px solid rgba(31, 191, 107, 0.5); }
  .chip { display: inline-block; margin-bottom: 0.8rem; padding: 0.3rem 0.8rem; border-radius: 999px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.06em; }
  .chip-gold { color: var(--navy); background: var(--gold); }
  .chip-green { color: var(--navy); background: var(--green); }
  .vis .compare[data-mode='sup'] .cmp-med,
  .vis .compare[data-mode='med'] .cmp-sup { opacity: 0.25; transform: scale(0.95); filter: grayscale(0.8); }
  .vis .compare[data-mode='sup'] .cmp-sup,
  .vis .compare[data-mode='med'] .cmp-med { transform: scale(1.03); box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35); }
  .root-cause { display: flex; align-items: center; gap: 1rem; padding: 1.1rem 1.4rem; }

  /* ===== Slide 9 ===== */
  .slide.danger {
    background:
      radial-gradient(ellipse 60% 55% at 50% 0%, rgba(255, 77, 94, 0.28), transparent 70%),
      radial-gradient(ellipse 50% 50% at 100% 100%, rgba(255, 138, 61, 0.2), transparent 70%),
      linear-gradient(170deg, #2a0f1c 0%, #3b1620 55%, #1b1020 100%);
  }
  .alert-panel {
    border-radius: 26px; padding: clamp(1.2rem, 2.6vw, 2rem);
    background: linear-gradient(145deg, rgba(255, 77, 94, 0.2), rgba(255, 138, 61, 0.12));
    border: 2px solid rgba(255, 98, 80, 0.6);
  }
  .alert-panel.glow { animation: alertGlow 1.6s ease-in-out infinite; }
  @keyframes alertGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 77, 94, 0.35), inset 0 0 20px rgba(255, 77, 94, 0.08); }
    50% { box-shadow: 0 0 70px rgba(255, 98, 80, 0.75), inset 0 0 40px rgba(255, 77, 94, 0.18); }
  }
  .alert-top { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 1.2rem; color: #ffd0b8; letter-spacing: 0.1em; font-size: 0.95rem; }
  .risk-list { list-style: none; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }
  .risk-list li { display: flex; gap: 0.9rem; padding: 1.1rem; border-radius: 18px; background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 138, 61, 0.35); }
  .risk-ico { flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font-weight: 900; color: #2a0f1c; background: linear-gradient(145deg, var(--orange), var(--red)); }
  .risk-list h3 { font-size: 1.05rem; color: #fff; margin-bottom: 0.35rem; }
  .risk-list p { font-size: 0.95rem; color: #ffd9d1; line-height: 1.55; }
  .risk-list strong { color: #fff; }

  /* ===== Slide 10 ===== */
  .slide.final {
    background:
      radial-gradient(ellipse 60% 60% at 50% 40%, rgba(31, 191, 107, 0.25), transparent 70%),
      radial-gradient(ellipse 40% 40% at 80% 90%, rgba(245, 185, 66, 0.16), transparent 70%),
      linear-gradient(170deg, var(--navy-3), var(--navy-2));
  }
  .final-card {
    position: relative; padding: clamp(1.6rem, 4vw, 3rem); border-radius: 30px; text-align: center;
    background: rgba(255, 255, 255, 0.07); border: 1px solid rgba(255, 255, 255, 0.18);
    backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); overflow: hidden;
    box-shadow: 0 30px 70px rgba(0, 0, 0, 0.4), 0 0 80px rgba(31, 191, 107, 0.18);
  }
  .final-card::before {
    content: ''; position: absolute; inset: -50%;
    background: conic-gradient(from 0deg, transparent 0 70%, rgba(245, 185, 66, 0.35) 80%, transparent 90%);
    animation: spin 9s linear infinite; z-index: 0;
  }
  .final-card::after { content: ''; position: absolute; inset: 2px; border-radius: 28px; background: linear-gradient(170deg, #0f2a4d, #0b1f3a); z-index: 0; }
  .final-card > * { position: relative; z-index: 1; }
  .final-card h2 { font-size: clamp(1.6rem, 3.4vw, 2.7rem); line-height: 1.15; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 1.8rem; color: #fff; }
  .final-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: left; }
  .final-block { padding: 1.1rem; border-radius: 16px; background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); }
  .final-block h3 { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--gold); margin-bottom: 0.4rem; }
  .final-block h3.mt { margin-top: 0.9rem; }
  .final-block p { font-size: 0.95rem; color: var(--ink); line-height: 1.5; }
  .final-actions { margin-top: 2rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; }
  .btn-gold { background: linear-gradient(90deg, var(--gold), #ffd98a); color: var(--navy); box-shadow: 0 8px 26px rgba(245, 185, 66, 0.45); animation: goldGlow 2.4s ease-in-out infinite; }
  .btn-gold:hover { background: linear-gradient(90deg, #ffd98a, var(--gold)); }
  @keyframes goldGlow { 50% { box-shadow: 0 8px 42px rgba(245, 185, 66, 0.85); } }
  .btn-ghost { background: transparent; color: var(--ink); border: 1px solid rgba(255, 255, 255, 0.3); box-shadow: none; }
  .btn-ghost:hover { background: rgba(255, 255, 255, 0.1); box-shadow: none; }

  /* ===== Indicador lateral ===== */
  .slide-nav {
    position: fixed; right: clamp(0.6rem, 1.6vw, 1.6rem); top: 50%; transform: translateY(-50%) translateX(30px);
    z-index: 1100; display: flex; flex-direction: column; align-items: center; gap: 0.8rem;
    padding: 0.9rem 0.55rem; border-radius: 999px; opacity: 0; pointer-events: none;
    background: rgba(8, 22, 43, 0.6); border: 1px solid rgba(255, 255, 255, 0.16);
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    transition: opacity 0.4s ease, transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .slide-nav.show { opacity: 1; pointer-events: auto; transform: translateY(-50%); }
  .slide-counter { font-size: 0.7rem; color: rgba(255, 255, 255, 0.6); writing-mode: horizontal-tb; text-align: center; line-height: 1.1; font-weight: 600; }
  .slide-counter strong { display: block; color: #fff; font-size: 0.95rem; }
  .slide-nav ul { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
  .dot { width: 9px; height: 9px; padding: 0; border-radius: 50%; background: rgba(255, 255, 255, 0.3); box-shadow: none; transition: all 0.3s; }
  .dot:hover { background: rgba(255, 255, 255, 0.7); transform: scale(1.3); box-shadow: none; }
  .dot.on { background: var(--gold); height: 22px; border-radius: 8px; box-shadow: 0 0 12px rgba(245, 185, 66, 0.8); }

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

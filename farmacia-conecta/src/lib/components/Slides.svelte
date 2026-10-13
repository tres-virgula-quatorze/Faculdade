<script>
  let props = $props();
  let currentRatio = $derived(props.currentRatio || 0);
  let scrollToPhase = $derived(props.scrollToPhase);
  let mobile = $derived(Boolean(props.mobile));
  let compareMode = $state('sup');

  const phases = [
    {
      eyebrow: '02 · Conceito-chave',
      title: 'Telefarmácia não é venda online.',
      lead: 'É exercício clínico mediado por tecnologia — com escuta, registro e responsabilidade profissional.',
      accent: 'green',
      family: 0,
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
      family: 1,
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
      family: 2,
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
      family: 3,
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
      family: 0,
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
      family: 1,
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
      family: 2,
      compare: true
    },
    {
      eyebrow: '09 · Red flags',
      title: 'Quando a tela não basta, o encaminhamento é cuidado.',
      lead: 'Reconhecer sinais de alarme é uma competência clínica — e uma responsabilidade ética.',
      accent: 'red',
      family: 4,
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
      family: 5,
      closing: true
    }
  ];

  function clamp01(x) {
    return Math.max(0, Math.min(1, x));
  }

  function subWindow(t, start, end) {
    if (t <= start) return 0;
    if (t >= end) return 1;
    return (t - start) / (end - start);
  }

  function easeOutCubic(x) {
    return 1 - Math.pow(1 - x, 3);
  }

  function easeInCubic(x) {
    return x * x * x;
  }

  function computeLayer(tIn, tOut, inStart, inEnd, outStart, outEnd) {
    const pIn = easeOutCubic(subWindow(tIn, inStart, inEnd));
    const pOut = easeInCubic(subWindow(tOut, outStart, outEnd));
    const opacity = Math.max(0, Math.min(1, pIn * (1 - pOut)));
    return { pIn, pOut, opacity };
  }

  // Fundo persistente por camadas contínuas:
  // Slide 1 (esmeralda #0d8d4b) -> Slide 2 (floresta #0d5b3e): transição 0.07 a 0.12
  // Slide 2 (floresta) -> Slide 3 (claro #f2f1e9): transição 0.165 a 0.215
  // Slides 3 até 8: mantêm fundo claro 100% contínuo e estável
  // Slide 8 (claro) -> Slide 9 (alerta vermelho #f6eeea): transição 0.765 a 0.815
  // Slide 9 (alerta) -> Slide 10 (floresta #0d5b3e): transição 0.865 a 0.915
  const bgForestInS2 = $derived(clamp01((currentRatio - 0.07) / 0.05));
  const bgLightIn = $derived(clamp01((currentRatio - 0.165) / 0.05));
  const bgRedIn = $derived(clamp01((currentRatio - 0.765) / 0.05));
  const bgForestInS10 = $derived(clamp01((currentRatio - 0.865) / 0.05));

  function getCardStyle(tIn, tOut, family, cardIndex) {
    const step = 0.08;
    const inStart = Math.min(0.60, 0.25 + cardIndex * step);
    const inEnd = Math.min(1.00, inStart + 0.45);
    const outStart = Math.min(0.50, 0.10 + cardIndex * 0.06);
    const outEnd = Math.min(1.00, outStart + 0.45);

    const layer = computeLayer(tIn, tOut, inStart, inEnd, outStart, outEnd);
    const pIn = layer.pIn;
    const pOut = layer.pOut;

    let transform = 'none';
    if (family === 0) {
      const dxIn = -36 * (1 - pIn);
      const dyIn = 16 * (1 - pIn);
      const dxOut = -25 * pOut;
      const dyOut = -16 * pOut;
      transform = `translate3d(${(dxIn + dxOut).toFixed(1)}px, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 1) {
      const dyIn = 55 * (1 - pIn);
      const dyOut = -32 * pOut;
      const scale = (0.94 + 0.06 * pIn) * (1 - 0.04 * pOut);
      transform = `translate3d(0, ${(dyIn + dyOut).toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
    } else if (family === 2) {
      const scale = (0.92 + 0.08 * pIn) * (1 - 0.05 * pOut);
      const rot = (1.5 * (1 - pIn)) - (1.0 * pOut);
      const dyOut = -22 * pOut;
      transform = `translate3d(0, ${dyOut.toFixed(1)}px, 0) scale(${scale.toFixed(3)}) rotate(${rot.toFixed(2)}deg)`;
    } else if (family === 3) {
      const dxIn = -30 * (1 - pIn);
      const dyIn = 22 * (1 - pIn);
      const dyOut = -26 * pOut;
      transform = `translate3d(${dxIn.toFixed(1)}px, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 4) {
      const dyIn = 22 * (1 - pIn);
      const dyOut = -16 * pOut;
      transform = `translate3d(0, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 5) {
      const dyIn = 30 * (1 - pIn);
      const dyOut = -20 * pOut;
      const scale = (0.92 + 0.08 * pIn) * (1 - 0.04 * pOut);
      transform = `translate3d(0, ${(dyIn + dyOut).toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
    }

    return {
      opacity: Number(layer.opacity.toFixed(3)),
      transform
    };
  }

  function getSlideStyles(index, ratio, isMob) {
    if (isMob) {
      return {
        visibility: 'visible',
        pointerEvents: 'auto',
        isCentered: true,
        deco: { opacity: 1, transform: 'none' },
        topline: { opacity: 1, transform: 'none' },
        title: { opacity: 1, transform: 'none' },
        lead: { opacity: 1, transform: 'none' },
        art: { opacity: 1, transform: 'none' },
        footer: { opacity: 1, transform: 'none' },
        cards: [
          { opacity: 1, transform: 'none' },
          { opacity: 1, transform: 'none' },
          { opacity: 1, transform: 'none' },
          { opacity: 1, transform: 'none' }
        ]
      };
    }

    const family = phases[index].family;
    const center = 0.14 + index * 0.10;
    const inStart = index === 0 ? 0.070 : center - 0.065;
    const inEnd = center - 0.020;
    const outStart = center + 0.020;
    const outEnd = index === 8 ? center + 0.075 : center + 0.065;

    const tIn = clamp01((ratio - inStart) / (inEnd - inStart));
    const tOut = clamp01((ratio - outStart) / (outEnd - outStart));
    const isVisible = ratio >= (inStart - 0.015) && ratio <= (outEnd + 0.015);
    const isInteractive = Math.abs(ratio - center) <= 0.035;

    if (!isVisible) {
      return {
        visibility: 'hidden',
        pointerEvents: 'none',
        isCentered: false,
        deco: { opacity: 0, transform: 'none' },
        topline: { opacity: 0, transform: 'none' },
        title: { opacity: 0, transform: 'none' },
        lead: { opacity: 0, transform: 'none' },
        art: { opacity: 0, transform: 'none' },
        footer: { opacity: 0, transform: 'none' },
        cards: [
          { opacity: 0, transform: 'none' },
          { opacity: 0, transform: 'none' },
          { opacity: 0, transform: 'none' },
          { opacity: 0, transform: 'none' }
        ]
      };
    }

    // Camada Topline (Eyebrow entra primeiro)
    const lTopline = computeLayer(tIn, tOut, 0.00, 0.45, 0.45, 0.95);
    // Camada Título (depois da topline)
    const lTitle = computeLayer(tIn, tOut, 0.10, 0.60, 0.35, 0.85);
    // Camada Lead (depois do título)
    const lLead = computeLayer(tIn, tOut, 0.20, 0.70, 0.25, 0.75);
    // Camada Arte (timing visual próprio)
    const lArt = computeLayer(tIn, tOut, 0.15, 0.75, 0.20, 0.80);
    // Camada Rodapé (entra por último, sai mais cedo)
    const lFooter = computeLayer(tIn, tOut, 0.60, 1.00, 0.05, 0.55);
    // Camada Decorativa
    const lDeco = computeLayer(tIn, tOut, 0.05, 0.65, 0.30, 0.90);

    let tTopline = 'none';
    let tTitle = 'none';
    let tLead = 'none';
    let tArt = 'none';
    let tFooter = 'none';
    let tDeco = 'none';

    if (family === 0) {
      // Família 0: Conteúdo entrando pela esquerda e arte vindo da direita
      tTopline = `translate3d(${((-45 * (1 - lTopline.pIn)) - (35 * lTopline.pOut)).toFixed(1)}px, 0, 0)`;
      tTitle = `translate3d(${((-55 * (1 - lTitle.pIn)) - (40 * lTitle.pOut)).toFixed(1)}px, 0, 0)`;
      tLead = `translate3d(${((-40 * (1 - lLead.pIn)) - (30 * lLead.pOut)).toFixed(1)}px, 0, 0)`;
      const artScale = (0.92 + 0.08 * lArt.pIn) * (1 - 0.06 * lArt.pOut);
      tArt = `translate3d(${((70 * (1 - lArt.pIn)) + (50 * lArt.pOut)).toFixed(1)}px, 0, 0) scale(${artScale.toFixed(3)})`;
      tFooter = `translate3d(0, ${((16 * (1 - lFooter.pIn)) - (14 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(${((35 * (1 - lDeco.pIn)) - (35 * lDeco.pOut)).toFixed(1)}px, 0, 0) scale(${(0.8 + 0.2 * lDeco.pIn).toFixed(3)})`;
    } else if (family === 1) {
      // Família 1: Título subindo e cards entrando em sequência vertical
      tTopline = `translate3d(0, ${((-24 * (1 - lTopline.pIn)) - (20 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((50 * (1 - lTitle.pIn)) - (40 * lTitle.pOut)).toFixed(1)}px, 0) scale(${(0.96 + 0.04 * lTitle.pIn).toFixed(3)})`;
      tLead = `translate3d(0, ${((38 * (1 - lLead.pIn)) - (30 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artScale = (0.92 + 0.08 * lArt.pIn) * (1 - 0.04 * lArt.pOut);
      tArt = `translate3d(0, ${((55 * (1 - lArt.pIn)) - (38 * lArt.pOut)).toFixed(1)}px, 0) scale(${artScale.toFixed(3)})`;
      tFooter = `translate3d(0, ${((20 * (1 - lFooter.pIn)) - (15 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(0, ${((-35 * (1 - lDeco.pIn)) + (35 * lDeco.pOut)).toFixed(1)}px, 0)`;
    } else if (family === 2) {
      // Família 2: Elementos surgindo por escala e rotação suave
      tTopline = `translate3d(0, ${((-16 * (1 - lTopline.pIn)) - (18 * lTopline.pOut)).toFixed(1)}px, 0) scale(${(0.96 + 0.04 * lTopline.pIn).toFixed(3)})`;
      const titleScale = (0.93 + 0.07 * lTitle.pIn) * (1 + 0.03 * lTitle.pOut);
      const titleRot = (-1.4 * (1 - lTitle.pIn)) + (0.9 * lTitle.pOut);
      tTitle = `translate3d(0, ${((26 * (1 - lTitle.pIn)) - (26 * lTitle.pOut)).toFixed(1)}px, 0) scale(${titleScale.toFixed(3)}) rotate(${titleRot.toFixed(2)}deg)`;
      tLead = `translate3d(0, ${((20 * (1 - lLead.pIn)) - (22 * lLead.pOut)).toFixed(1)}px, 0) scale(${(0.95 + 0.05 * lLead.pIn).toFixed(3)})`;
      const artScale = (0.84 + 0.16 * lArt.pIn) * (1 - 0.1 * lArt.pOut);
      const artRot = (-4.5 * (1 - lArt.pIn)) + (3 * lArt.pOut);
      tArt = `scale(${artScale.toFixed(3)}) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((16 * (1 - lFooter.pIn)) - (14 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${(0.8 + 0.2 * lDeco.pIn).toFixed(3)}) rotate(${((-20 * (1 - lDeco.pIn)) + (20 * lDeco.pOut)).toFixed(2)}deg)`;
    } else if (family === 3) {
      // Família 3: Conteúdo entrando em diagonal
      tTopline = `translate3d(${((-26 * (1 - lTopline.pIn)) - (20 * lTopline.pOut)).toFixed(1)}px, ${((-16 * (1 - lTopline.pIn)) - (20 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(${((-46 * (1 - lTitle.pIn)) - (32 * lTitle.pOut)).toFixed(1)}px, ${((36 * (1 - lTitle.pIn)) - (32 * lTitle.pOut)).toFixed(1)}px, 0)`;
      tLead = `translate3d(${((-36 * (1 - lLead.pIn)) - (24 * lLead.pOut)).toFixed(1)}px, ${((26 * (1 - lLead.pIn)) - (24 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artRot = (-3.5 * (1 - lArt.pIn)) + (4 * lArt.pOut);
      tArt = `translate3d(${((52 * (1 - lArt.pIn)) + (36 * lArt.pOut)).toFixed(1)}px, ${((-38 * (1 - lArt.pIn)) + (30 * lArt.pOut)).toFixed(1)}px, 0) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((16 * (1 - lFooter.pIn)) - (14 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(${((40 * (1 - lDeco.pIn)) - (40 * lDeco.pOut)).toFixed(1)}px, ${((40 * (1 - lDeco.pIn)) - (40 * lDeco.pOut)).toFixed(1)}px, 0)`;
    } else if (family === 4) {
      // Família 4: Slide de alerta com movimento mais contido e direto
      tTopline = `translate3d(0, ${((-14 * (1 - lTopline.pIn)) - (14 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((24 * (1 - lTitle.pIn)) - (18 * lTitle.pOut)).toFixed(1)}px, 0)`;
      tLead = `translate3d(0, ${((18 * (1 - lLead.pIn)) - (14 * lLead.pOut)).toFixed(1)}px, 0)`;
      tArt = `translate3d(0, ${(-16 * lArt.pOut).toFixed(1)}px, 0) scale(${(0.94 + 0.06 * lArt.pIn).toFixed(3)})`;
      tFooter = `translate3d(0, ${((12 * (1 - lFooter.pIn)) - (12 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${(0.9 + 0.1 * lDeco.pIn).toFixed(3)})`;
    } else if (family === 5) {
      // Família 5: Slide final com composição mais lenta e centralizada
      tTopline = `translate3d(0, ${((-22 * (1 - lTopline.pIn)) - (18 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((38 * (1 - lTitle.pIn)) - (28 * lTitle.pOut)).toFixed(1)}px, 0) scale(${(0.96 + 0.04 * lTitle.pIn).toFixed(3)})`;
      tLead = `translate3d(0, ${((26 * (1 - lLead.pIn)) - (20 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artScale = (0.84 + 0.16 * lArt.pIn) * (1 + 0.05 * lArt.pOut);
      const artRot = -6 * (1 - lArt.pIn);
      tArt = `translate3d(0, ${(-25 * lArt.pOut).toFixed(1)}px, 0) scale(${artScale.toFixed(3)}) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((18 * (1 - lFooter.pIn)) - (15 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${((0.8 + 0.2 * lDeco.pIn) * (1 + 0.15 * lDeco.pOut)).toFixed(3)})`;
    }

    return {
      visibility: isVisible ? 'visible' : 'hidden',
      pointerEvents: isInteractive ? 'auto' : 'none',
      isCentered: isInteractive,
      topline: { opacity: Number(lTopline.opacity.toFixed(3)), transform: tTopline },
      title: { opacity: Number(lTitle.opacity.toFixed(3)), transform: tTitle },
      lead: { opacity: Number(lLead.opacity.toFixed(3)), transform: tLead },
      art: { opacity: Number(lArt.opacity.toFixed(3)), transform: tArt },
      footer: { opacity: Number(lFooter.opacity.toFixed(3)), transform: tFooter },
      deco: { opacity: Number(lDeco.opacity.toFixed(3)), transform: tDeco },
      cards: [
        getCardStyle(tIn, tOut, family, 0),
        getCardStyle(tIn, tOut, family, 1),
        getCardStyle(tIn, tOut, family, 2),
        getCardStyle(tIn, tOut, family, 3)
      ]
    };
  }

  let slideStates = $derived(phases.map((_, i) => getSlideStyles(i, currentRatio, mobile)));

  function goTo(index) {
    if (mobile) {
      if (index <= 0) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        document.getElementById(`slide-${index + 1}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
      return;
    }
    scrollToPhase?.(index + 1);
  }
</script>

{#if !mobile}
  <!-- Palco de fundos persistente desktop: estabilidade absoluta, zero piscadas -->
  <div class="stage-backgrounds" aria-hidden="true">
    <div class="stage-bg-layer bg-forest" style={`opacity: ${bgForestInS2.toFixed(3)};`}></div>
    <div class="stage-bg-layer bg-light" style={`opacity: ${bgLightIn.toFixed(3)};`}></div>
    <div class="stage-bg-layer bg-red" style={`opacity: ${bgRedIn.toFixed(3)};`}></div>
    <div class="stage-bg-layer bg-closing" style={`opacity: ${bgForestInS10.toFixed(3)};`}></div>
  </div>
{/if}

<div class={`slides-wrap ${mobile ? 'is-mobile-wrap' : ''}`} aria-label="Apresentação sobre telefarmácia">
  {#each phases as slide, index}
    {@const st = slideStates[index]}
    <section
      id={`slide-${index + 2}`}
      class={`slide redesign-slide theme-${slide.accent} family-${slide.family} ${mobile ? 'mobile-slide' : ''}`}
      aria-hidden={!st.isCentered}
      style={mobile ? '' : `visibility: ${st.visibility}; pointer-events: ${st.pointerEvents}; z-index: ${st.isCentered ? 3 : 2};`}
    >
      <!-- Camada Decorativa de Ambientação -->
      <div class="slide-deco" style={mobile ? '' : `opacity: ${st.deco.opacity}; transform: ${st.deco.transform};`} aria-hidden="true">
        {#if slide.accent === 'green'}
          <div class="deco-mesh mesh-green"></div>
          <div class="deco-symbol deco-cross">
            <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 4v16M4 12h16" />
            </svg>
          </div>
        {:else if slide.accent === 'red'}
          <div class="deco-mesh mesh-red"></div>
          <div class="deco-symbol deco-alert-badge">
            <span>ALERTA CLÍNICO</span>
          </div>
        {:else}
          <div class="deco-mesh mesh-light"></div>
          <div class="deco-symbol deco-dots">
            <span></span><span></span><span></span>
          </div>
        {/if}
      </div>

      <!-- Palco Estável do Conteúdo -->
      <div class="slide-frame">
        <!-- Camada Cabeçalho / Eyebrow -->
        <div class="slide-topline" style={mobile ? '' : `opacity: ${st.topline.opacity}; transform: ${st.topline.transform};`}>
          <span class="slide-eyebrow">{slide.eyebrow}</span>
          <span class="slide-index">{String(index + 2).padStart(2, '0')} / 10</span>
        </div>

        <div class="slide-content">
          <div class="slide-main-grid">
            <div class="slide-main">
              <!-- Camada de Texto: Título e Lead com animações independentes -->
              <header class="slide-copy">
                <h2 style={mobile ? '' : `opacity: ${st.title.opacity}; transform: ${st.title.transform};`}>{slide.title}</h2>
                <p class="slide-lead" style={mobile ? '' : `opacity: ${st.lead.opacity}; transform: ${st.lead.transform};`}>{slide.lead}</p>
              </header>

              <!-- Camada de Cards / Conteúdo Principal (cada elemento com delay próprio) -->
              {#if slide.points}
                <div class={`point-grid ${slide.points.length === 2 ? 'two' : ''}`}>
                  {#each slide.points as point, pointIndex}
                    <article
                      class={`point ${slide.accent === 'red' ? 'point-alert' : ''}`}
                      style={mobile ? '' : `opacity: ${st.cards[pointIndex].opacity}; transform: ${st.cards[pointIndex].transform};`}
                    >
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
                  {#each slide.laws as law, lawIndex}
                    <article
                      class="law-item"
                      style={mobile ? '' : `opacity: ${st.cards[lawIndex].opacity}; transform: ${st.cards[lawIndex].transform};`}
                    >
                      <span class="law-mark">§</span>
                      <div><h3>{law[0]}</h3><p>{law[1]}</p></div>
                    </article>
                  {/each}
                </div>
                <aside
                  class="warning-strip"
                  style={mobile ? '' : `opacity: ${st.cards[2].opacity}; transform: ${st.cards[2].transform};`}
                >
                  <strong>Limite essencial</strong><span>{slide.warning}</span>
                </aside>
              {:else if slide.steps}
                <div class="journey">
                  {#each slide.steps as step, stepIndex}
                    <button
                      class:journey-active={stepIndex <= 2}
                      class="journey-step"
                      type="button"
                      onclick={() => goTo(stepIndex + 5)}
                      style={mobile ? '' : `opacity: ${st.cards[stepIndex].opacity}; transform: ${st.cards[stepIndex].transform};`}
                    >
                      <span class="journey-number">{step[0]}</span>
                      <span><strong>{step[1]}</strong><small>{step[2]}</small></span>
                    </button>
                  {/each}
                </div>
              {:else if slide.compare}
                <div
                  class="compare-header"
                  style={mobile ? '' : `opacity: ${st.cards[0].opacity}; transform: ${st.cards[0].transform};`}
                >
                  <span>Escolha o enquadramento para comparar</span>
                  <div class="compare-tabs">
                    <button class:chosen={compareMode === 'sup'} type="button" onclick={() => compareMode = 'sup'}>Suplemento</button>
                    <button class:chosen={compareMode === 'med'} type="button" onclick={() => compareMode = 'med'}>Medicamento</button>
                  </div>
                </div>
                <div class="compare-grid">
                  <article
                    class:dimmed={compareMode === 'med'}
                    class="compare-item supplement"
                    style={mobile ? '' : `opacity: ${st.cards[1].opacity}; transform: ${st.cards[1].transform};`}
                  >
                    <span class="compare-label">SUPLEMENTOS</span>
                    <h3>Orientação responsável</h3>
                    <p>Informar composição, uso adequado e limites da comunicação ao paciente.</p>
                  </article>
                  <article
                    class:dimmed={compareMode === 'sup'}
                    class="compare-item medicine"
                    style={mobile ? '' : `opacity: ${st.cards[2].opacity}; transform: ${st.cards[2].transform};`}
                  >
                    <span class="compare-label">MEDICAMENTOS</span>
                    <h3>Prescrição farmacêutica</h3>
                    <p>Exige avaliação clínica, indicação, registro e respeito às normas profissionais.</p>
                  </article>
                </div>
              {:else if slide.closing}
                <div class="closing-grid">
                  <div style={mobile ? '' : `opacity: ${st.cards[0].opacity}; transform: ${st.cards[0].transform};`}>
                    <span>01</span><strong>Ampliação do acesso</strong><p>Mais proximidade entre serviço e comunidade.</p>
                  </div>
                  <div style={mobile ? '' : `opacity: ${st.cards[1].opacity}; transform: ${st.cards[1].transform};`}>
                    <span>02</span><strong>Sinergia acadêmica</strong><p>Aprendizagem aplicada à realidade local.</p>
                  </div>
                  <div style={mobile ? '' : `opacity: ${st.cards[2].opacity}; transform: ${st.cards[2].transform};`}>
                    <span>03</span><strong>Cuidado humano</strong><p>Tecnologia com escuta e responsabilidade.</p>
                  </div>
                </div>
              {/if}
            </div>

            <!-- Camada Ilustração Lateral (timing e transform específicos) -->
            <aside
              class={`slide-art art-${slide.visual || (index % 3)}`}
              style={mobile ? '' : `opacity: ${st.art.opacity}; transform: ${st.art.transform};`}
              aria-hidden="true"
            >
              {#if slide.visual === 'shield'}
                <div class="art-orbit orbit-a"></div><div class="art-orbit orbit-b"></div>
                <div class="official-brand"><img src="/assets/anpd-symbol-official.png" alt="" /><strong>ANPD</strong><span>Autoridade Nacional<br>de Proteção de Dados</span></div>
                <div class="art-caption">MARCA OFICIAL<br><strong>ANPD</strong></div>
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

        <!-- Camada Rodapé -->
        <div class="slide-footer" style={mobile ? '' : `opacity: ${st.footer.opacity}; transform: ${st.footer.transform};`}>
          <span>Telefarmácia & Serviços Digitais Farmacêuticos</span>
          <button type="button" onclick={() => goTo(index)}>{index === 0 ? 'Voltar ao início' : 'Anterior'}</button>
        </div>
      </div>
    </section>
  {/each}
</div>

<style>
  /* Palco de Fundos Persistente Desktop */
  .stage-backgrounds {
    position: absolute;
    inset: 0;
    z-index: 1;
    pointer-events: none;
    overflow: hidden;
  }
  .stage-bg-layer {
    position: absolute;
    inset: 0;
    pointer-events: none;
    will-change: opacity;
  }
  .bg-forest {
    background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.15), transparent 32%), #0d5b3e;
  }
  .bg-light {
    background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.7), transparent 32%), linear-gradient(135deg, rgba(255,255,255,0.42), transparent 55%), #f2f1e9;
  }
  .bg-red {
    background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.6), transparent 32%), #f6eeea;
  }
  .bg-closing {
    background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.15), transparent 32%), #0d5b3e;
  }

  /* Deck de Slides */
  .slides-wrap {
    position: absolute;
    inset: 0;
    z-index: 5;
    pointer-events: none;
    color: #17362d;
  }

  /* Container do Slide (estável no Desktop) */
  .slide {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(3.5rem, 8vh, 6rem) clamp(1.25rem, 7vw, 7.5rem);
    overflow: hidden;
    /* Container estável: sem transform ou opacity no bloco geral */
  }

  .theme-green { color: #f8f6ed; }
  .theme-light { color: #17362d; }
  .theme-red { color: #2f2523; }

  /* Camada Decorativa */
  .slide-deco {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
    will-change: transform, opacity;
  }
  .deco-mesh {
    position: absolute;
    width: 60vw;
    height: 60vw;
    border-radius: 50%;
    filter: blur(80px);
    top: -15%;
    right: -10%;
    pointer-events: none;
  }
  .mesh-green { background: #16a34a; opacity: 0.16; }
  .mesh-light { background: #0d5b3e; opacity: 0.05; }
  .mesh-red { background: #b94d39; opacity: 0.14; }
  .deco-symbol {
    position: absolute;
    top: 3.5rem;
    left: 4.5rem;
    opacity: 0.18;
    pointer-events: none;
  }
  .deco-alert-badge {
    top: 3.2rem;
    left: auto;
    right: 4.5rem;
    font-size: 0.65rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    padding: 0.35rem 0.75rem;
    border: 1px solid currentColor;
    border-radius: 999px;
    opacity: 0.35;
  }
  .deco-dots {
    display: flex;
    gap: 8px;
    top: auto;
    bottom: 3.2rem;
    left: 4.5rem;
  }
  .deco-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.35;
  }

  /* Palco de Conteúdo Estável */
  .slide-frame {
    position: relative;
    z-index: 1;
    width: min(1120px, 100%);
    min-height: min(680px, 86vh);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 2rem;
  }

  .slide-topline, .slide-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    will-change: transform, opacity;
  }
  .slide-topline {
    border-bottom: 1px solid currentColor;
    padding-bottom: 1rem;
    opacity: 0.72;
  }
  .slide-index { font-variant-numeric: tabular-nums; }
  .slide-content {
    display: flex;
    flex-direction: column;
    gap: clamp(2rem, 5vh, 3.8rem);
    flex: 1;
    justify-content: center;
    padding: clamp(1.5rem, 3vh, 2.5rem) 0;
  }
  .slide-main-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(250px, 0.65fr);
    align-items: center;
    gap: clamp(2rem, 7vw, 7rem);
  }
  .slide-main { min-width: 0; }
  .slide-copy { max-width: 780px; }
  .slide-eyebrow { font-weight: 800; }
  .slide-copy h2 {
    margin: 0.8rem 0 1.2rem;
    max-width: 840px;
    font-size: clamp(2.3rem, 5vw, 5rem);
    line-height: 0.97;
    letter-spacing: -0.055em;
    font-weight: 800;
    will-change: transform, opacity;
  }
  .slide-lead {
    max-width: 680px;
    font-size: clamp(1rem, 1.5vw, 1.35rem);
    line-height: 1.45;
    opacity: 0.78;
    will-change: transform, opacity;
  }

  /* Cards e Itens Principais */
  .point-grid, .law-grid, .closing-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }
  .point-grid.two, .law-grid { grid-template-columns: repeat(2, 1fr); }
  .point, .law-item, .compare-item, .closing-grid > div {
    position: relative;
    display: flex;
    gap: 1rem;
    padding: 1.35rem 1.4rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.5);
    min-height: 150px;
    will-change: transform, opacity;
  }
  .theme-green .point, .theme-green .closing-grid > div { background: rgba(255, 255, 255, 0.08); }
  .point-number, .law-mark, .closing-grid span {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    opacity: 0.55;
  }
  .point h3, .law-item h3, .compare-item h3, .closing-grid strong {
    margin: 0 0 0.45rem;
    font-size: 1.1rem;
    line-height: 1.15;
  }
  .point p, .law-item p, .compare-item p, .closing-grid p {
    margin: 0;
    font-size: 0.94rem;
    line-height: 1.5;
    opacity: 0.72;
  }
  .warning-strip {
    display: flex;
    gap: 1rem;
    align-items: baseline;
    padding: 1.1rem 1.3rem;
    border-left: 4px solid #b94d39;
    background: rgba(185, 77, 57, 0.1);
    color: #713126;
    margin-top: 1rem;
    will-change: transform, opacity;
  }
  .warning-strip span { font-size: 0.95rem; line-height: 1.45; }

  /* Protótipo: Jornada */
  .journey {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    position: relative;
  }
  .journey::before {
    content: '';
    position: absolute;
    top: 2rem;
    left: 7%;
    right: 7%;
    height: 1px;
    background: #4e8c73;
    opacity: 0.45;
  }
  .journey-step {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    text-align: left;
    border: 0;
    border-radius: 0;
    padding: 0;
    background: none;
    box-shadow: none;
    color: inherit;
    cursor: pointer;
    will-change: transform, opacity;
  }
  .journey-number {
    display: grid;
    place-items: center;
    width: 4rem;
    height: 4rem;
    border: 1px solid currentColor;
    border-radius: 50%;
    background: #f2f1e9;
    color: #0d5b3e;
    font-weight: 800;
  }
  .journey-active .journey-number { background: #0d5b3e; color: #f8f6ed; }
  .journey-step strong, .journey-step small { display: block; }
  .journey-step small { margin-top: 0.45rem; font-size: 0.85rem; line-height: 1.4; opacity: 0.7; }

  /* Comparativo: Suplemento vs Medicamento */
  .compare-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    font-size: 0.9rem;
    opacity: 0.8;
    margin-bottom: 0.8rem;
    will-change: transform, opacity;
  }
  .compare-tabs { display: flex; border: 1px solid currentColor; padding: 0.25rem; }
  .compare-tabs button {
    border: 0;
    border-radius: 0;
    padding: 0.65rem 0.9rem;
    box-shadow: none;
    color: inherit;
    background: transparent;
    font-size: 0.8rem;
    cursor: pointer;
  }
  .compare-tabs button.chosen { background: #0d5b3e; color: #f8f6ed; }
  .compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .compare-item { min-height: 180px; }
  .compare-item.dimmed { opacity: 0.35 !important; }
  .compare-label { font-size: 0.72rem; font-weight: 800; letter-spacing: 0.12em; }
  .medicine { border-color: #b94d39; }
  .medicine .compare-label { color: #a44332; }

  .closing-grid { grid-template-columns: repeat(3, 1fr); }
  .closing-grid > div { flex-direction: column; min-height: 135px; }

  .slide-footer {
    border-top: 1px solid currentColor;
    padding-top: 1rem;
    opacity: 0.58;
  }
  .slide-footer button {
    border: 0;
    padding: 0;
    border-radius: 0;
    box-shadow: none;
    background: none;
    color: inherit;
    font: inherit;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    cursor: pointer;
  }
  .slide-footer button:hover { transform: none; box-shadow: none; opacity: 0.7; }

  /* Camada de Ilustração Lateral */
  .slide-art {
    min-height: 330px;
    position: relative;
    display: grid;
    place-items: center;
    color: currentColor;
    opacity: 0.95;
    will-change: transform, opacity;
  }
  .slide-art::before {
    content: '';
    position: absolute;
    inset: 9% 4%;
    border: 1px solid currentColor;
    border-radius: 50%;
    opacity: 0.16;
    transform: rotate(-18deg) scaleY(0.65);
  }
  .art-number {
    font-size: clamp(8rem, 18vw, 15rem);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.12em;
    opacity: 0.1;
  }
  .art-line {
    position: absolute;
    height: 1px;
    background: currentColor;
    opacity: 0.35;
    transform-origin: left;
  }
  .line-one { width: 78%; top: 34%; left: 8%; transform: rotate(-18deg); }
  .line-two { width: 64%; top: 60%; left: 30%; transform: rotate(26deg); }
  .art-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #d7a95c;
    box-shadow: 0 0 0 10px rgba(215, 169, 92, 0.16);
    position: absolute;
    top: 31%;
    left: 72%;
  }
  .art-orbit {
    position: absolute;
    width: 240px;
    height: 240px;
    border: 1px solid currentColor;
    border-radius: 50%;
    opacity: 0.3;
  }
  .orbit-a { transform: rotate(28deg) scaleX(0.5); }
  .orbit-b { transform: rotate(-32deg) scaleX(0.7); }
  .official-brand {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.45rem;
    color: #17362d;
    text-align: center;
    transform: rotate(-4deg);
  }
  .official-brand img { width: 180px; height: 135px; object-fit: contain; }
  .official-brand strong { font-size: 2.3rem; line-height: 0.8; letter-spacing: 0.08em; }
  .official-brand span {
    font-size: 0.58rem;
    line-height: 1.15;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.72;
  }
  .art-caption {
    position: absolute;
    bottom: 24%;
    right: 0;
    font-size: 0.65rem;
    line-height: 1.1;
    letter-spacing: 0.16em;
    opacity: 0.65;
  }
  .art-caption strong { font-size: 0.9rem; }
  .art-window {
    width: min(310px, 100%);
    background: #fff;
    color: #17362d;
    box-shadow: 18px 18px 0 rgba(13, 91, 62, 0.12);
    border: 1px solid rgba(13, 91, 62, 0.2);
    transform: rotate(3deg);
  }
  .window-bar, .window-footer {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0.65rem 0.8rem;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
  .window-bar { border-bottom: 1px solid #e4e5dd; }
  .window-bar i { width: 7px; height: 7px; border-radius: 50%; background: #d7a95c; }
  .window-bar span { margin-left: auto; opacity: 0.55; }
  .window-body {
    height: 150px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #dfe9df, #f7f6ef);
  }
  .art-avatar {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    background: #0d5b3e;
    box-shadow: 0 0 0 14px rgba(13, 91, 62, 0.12);
  }
  .art-lines { position: absolute; margin: 90px 0 0 150px; }
  .art-lines b {
    display: block;
    width: 46px;
    height: 5px;
    margin: 6px;
    background: #8db9a1;
  }
  .window-footer { justify-content: space-between; color: #0d5b3e; }
  .art-pulse {
    position: absolute;
    width: 200px;
    height: 200px;
    border: 1px solid #d7a95c;
    border-radius: 50%;
    opacity: 0.45;
  }
  .art-law {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 9rem;
    line-height: 0.8;
    color: #b94d39;
    transform: rotate(-8deg);
  }
  .art-law span { font-size: 0.8rem; line-height: 1.15; letter-spacing: 0.14em; }
  .art-law strong { font-size: 1.25rem; }
  .art-route {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 1.2rem;
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.1em;
  }
  .art-route i {
    display: block;
    width: 1px;
    height: 42px;
    background: currentColor;
    margin-left: 7px;
    opacity: 0.4;
  }
  .art-scale { position: relative; width: 270px; height: 220px; }
  .scale-post {
    position: absolute;
    width: 10px;
    height: 180px;
    bottom: 0;
    left: 50%;
    background: currentColor;
    opacity: 0.6;
  }
  .scale-beam {
    position: absolute;
    width: 220px;
    height: 4px;
    top: 50px;
    left: 25px;
    background: currentColor;
    transform: rotate(-7deg);
  }
  .scale-pan {
    position: absolute;
    top: 85px;
    border: 1px solid currentColor;
    padding: 1.2rem 0.8rem;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
  }
  .pan-left { left: 12px; transform: rotate(-7deg); }
  .pan-right { right: 12px; transform: rotate(7deg); }
  .art-sun {
    width: 230px;
    height: 230px;
    display: grid;
    place-items: center;
    border: 1px solid #d7a95c;
    border-radius: 50%;
    position: relative;
    text-align: center;
    font-size: 1rem;
    line-height: 1.1;
    letter-spacing: 0.12em;
  }
  .art-sun::before, .art-sun::after {
    content: '';
    position: absolute;
    inset: -18px;
    border: 1px solid #d7a95c;
    border-radius: 50%;
    opacity: 0.35;
  }
  .art-sun::after { inset: -38px; opacity: 0.18; }
  .art-sun div {
    position: absolute;
    inset: 36%;
    background: #d7a95c;
    border-radius: 50%;
    opacity: 0.55;
  }
  .art-sun span { position: relative; z-index: 1; }
  .art-sun strong { font-size: 1.25rem; }

  /* =====================================================================
     MOBILE (Fluxo Vertical Normal sem Absolute Stacking)
     ===================================================================== */
  @media (max-width: 900px) {
    .stage-backgrounds {
      display: none !important;
    }
    .slides-wrap {
      position: relative;
      inset: auto;
      pointer-events: auto;
      display: block;
    }
    .slide {
      position: relative !important;
      inset: auto !important;
      min-height: 100svh;
      height: auto;
      visibility: visible !important;
      opacity: 1 !important;
      transform: none !important;
      pointer-events: auto !important;
      overflow: visible;
      padding: 4.5rem 1.25rem 2.5rem;
      align-items: flex-start;
    }

    /* Cores de fundo nativas por bloco no fluxo mobile */
    .slide.theme-green {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.15), transparent 32%), #0d5b3e !important;
    }
    .slide.theme-light {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.7), transparent 32%), linear-gradient(135deg, rgba(255,255,255,0.42), transparent 55%), #f2f1e9 !important;
    }
    .slide.theme-red {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.6), transparent 32%), #f6eeea !important;
    }

    .slide-deco {
      display: none !important;
    }
    .slide-frame {
      min-height: calc(100svh - 6.5rem);
      gap: 1.4rem;
    }
    .slide-content {
      justify-content: flex-start;
      gap: 1.6rem;
      padding: 1.2rem 0;
    }
    .slide-main-grid {
      grid-template-columns: 1fr;
      gap: 1.8rem;
    }
    .slide-art {
      min-height: 170px;
      order: -1;
    }
    .slide-art::before { inset: 5% 22%; }
    .art-number { font-size: 7rem; }
    .official-brand { transform: scale(0.8) rotate(-4deg); }
    .art-orbit { transform: scale(0.72); }
    .art-law { transform: scale(0.72) rotate(-8deg); }
    .art-scale { transform: scale(0.72); }
    .slide-copy h2 { font-size: clamp(2rem, 8.5vw, 3.2rem); }
    .slide-lead { font-size: 1rem; }
    .point-grid, .point-grid.two, .law-grid, .closing-grid, .compare-grid {
      grid-template-columns: 1fr;
    }
    .journey {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    .journey::before {
      top: 2rem;
      bottom: 2rem;
      left: 2rem;
      right: auto;
      width: 1px;
      height: auto;
    }
    .journey-step {
      flex-direction: row;
      align-items: flex-start;
      width: 100%;
    }
    .journey-step span:last-child { padding-top: 0.45rem; }
    .slide-footer { font-size: 0.6rem; }
  }

  @media (prefers-reduced-motion: reduce) {
    .slide-topline, .slide-copy h2, .slide-lead, .point, .law-item, .compare-item, .closing-grid > div, .slide-art, .slide-footer, .slide-deco {
      transform: none !important;
      transition: none !important;
    }
  }
</style>

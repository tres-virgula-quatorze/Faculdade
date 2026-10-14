<script>
  let props = $props();
  let currentRatio = $derived(props.currentRatio || 0);
  let scrollToPhase = $derived(props.scrollToPhase);
  let mobile = $derived(Boolean(props.mobile));
  let compareMode = $state('sup');

  const phases = [
    {
      eyebrow: '02 · Conceito-Chave',
      badge: 'CLÍNICA vs. COMÉRCIO',
      title: 'Telefarmácia não é venda online.',
      lead: 'É exercício clínico mediado por tecnologia — com escuta atenta, registro sistemático e responsabilidade técnica indelegável.',
      accent: 'green',
      family: 0,
      divergence: {
        tag: 'Mero Comércio',
        desc: 'Comprar e vender medicamentos por aplicativo sem raciocínio nem cuidado clínico não caracteriza telefarmácia.'
      },
      pillars: [
        ['Escuta Ativa', 'Acolher a queixa, histórico e contexto real do paciente.'],
        ['Registro em Prontuário', 'Documentar condutas, orientações e parâmetros clínicos.'],
        ['Responsabilidade Técnica', 'Ato privativo do profissional com método e ética.']
      ]
    },
    {
      eyebrow: '03 · Modalidades',
      badge: 'ECOSSISTEMA DE CUIDADO',
      title: 'Quatro formas de levar o cuidado mais longe.',
      lead: 'A tecnologia amplia o acesso geográfico sem substituir a soberania do raciocínio clínico farmacêutico.',
      accent: 'light',
      family: 1,
      modalities: [
        { code: '01', name: 'Teleconsulta', desc: 'Atendimento síncrono direto para avaliação, conciliação e plano de cuidado.' },
        { code: '02', name: 'Teleinterconsulta', desc: 'Discussão clínica estruturada entre o farmacêutico e outros membros da equipe.' },
        { code: '03', name: 'Telemonitoramento', desc: 'Acompanhamento longitudinal de parâmetros, adesão e reações adversas.' },
        { code: '04', name: 'Teleorientação', desc: 'Triagem ética, aconselhamento pontual e direcionamento responsável.' }
      ]
    },
    {
      eyebrow: '04 · Arcabouço Legal',
      badge: 'SEGURANÇA JURÍDICA',
      title: 'Inovação também precisa de limite.',
      lead: 'O cuidado digital só é sustentável quando respeita os marcos normativos que protegem o paciente, o profissional e o serviço.',
      accent: 'light',
      family: 2,
      laws: [
        { num: 'Lei Federal nº 14.510/2022', desc: 'Disciplina e autoriza a telessaúde em todo o território nacional, incluindo as diretrizes do SUS.' },
        { num: 'Resolução CFF nº 10/2024', desc: 'Regulamenta o uso de tecnologias, Saúde Digital e Inteligência Artificial na prática farmacêutica.' }
      ],
      warning: 'A responsabilidade técnica de estabelecimentos farmacêuticos não pode ser assumida de forma remota. A presença física do RT é mandatória por lei.'
    },
    {
      eyebrow: '05 · Segurança da Informação',
      badge: 'LGPD & PRONTUÁRIO',
      title: 'O prontuário é parte do cuidado.',
      lead: 'Privacidade não é detalhe burocrático: é requisito clínico, ético e legal que fundamenta o sigilo profissional.',
      accent: 'light',
      family: 3,
      securityPoints: [
        { code: 'LGPD', title: 'Dados Sensíveis', desc: 'Informações de saúde exigem bases legais estritas e proteção reforçada.' },
        { code: 'PEP', title: 'Registro Seguro', desc: 'Todo atendimento deve ser registrado com rastreabilidade e integridade.' },
        { code: 'ICP', title: 'Assinatura Digital', desc: 'Prescrições e declarações exigem certificados digitais válidos ICP-Brasil.' }
      ],
      visual: 'shield'
    },
    {
      eyebrow: '06 · Nosso Protótipo',
      badge: 'JORNADA DO PACIENTE',
      title: 'Uma jornada simples para uma decisão segura.',
      lead: 'O fluxo organiza a chegada do paciente e direciona cada necessidade para o nível adequado de atenção à saúde.',
      accent: 'light',
      family: 0,
      steps: [
        { step: '01', title: 'Acolhimento', desc: 'Linguagem clara, humanizada e empática.' },
        { step: '02', title: 'Triagem', desc: 'Identificação da necessidade principal e gravidade.' },
        { step: '03', title: 'Consentimento', desc: 'Transparência, esclarecimento e aceite LGPD.' },
        { step: '04', title: 'Direcionamento', desc: 'Teleconsulta clínica ou encaminhamento presencial.' }
      ]
    },
    {
      eyebrow: '07 · Prática Clínica',
      badge: 'TELECONSULTA AO VIVO',
      title: 'Tecnologia para acompanhar — não para automatizar o cuidado.',
      lead: 'No encontro virtual, o farmacêutico transforma informações esparsas em decisões clínicas compartilhadas.',
      accent: 'light',
      family: 1,
      practicePoints: [
        { num: '01', title: 'Conciliação Terapêutica', desc: 'Conferência visual das embalagens para evitar duplicidades e interações.' },
        { num: '02', title: 'Adesão ao Tratamento', desc: 'Investigação profunda de esquecimentos, rotinas e manejo de efeitos adversos.' },
        { num: '03', title: 'Educação em Saúde', desc: 'Orientações práticas de descarte, horários ideais e armazenamento seguro.' }
      ],
      visual: 'call'
    },
    {
      eyebrow: '08 · Prescrição e Escopo',
      badge: 'CRITÉRIO TÉCNICO',
      title: 'Diferenciar orientação de prescrição é proteger o paciente.',
      lead: 'O farmacêutico atua estritamente dentro do seu escopo legal, com limites bem demarcados e responsabilidade ética.',
      accent: 'light',
      family: 2,
      compare: true
    },
    {
      eyebrow: '09 · Red Flags',
      badge: 'SINAIS DE ALARME',
      title: 'Quando a tela não basta, o encaminhamento é cuidado.',
      lead: 'Reconhecer a insuficiência do meio remoto é competência diagnóstica — e dever bioético essencial.',
      accent: 'red',
      family: 4,
      alerts: [
        { num: '01', title: 'Sintomas de Emergência', desc: 'Dor precordial, dispneia súbita, confusão ou sinais focais exigem suporte médico imediato.' },
        { num: '02', title: 'Limite do Exame Físico', desc: 'Se a palpação, ausculta ou inspeção direta forem indispensáveis, não se conclui caso à distância.' },
        { num: '03', title: 'Conduta Ética e Registro', desc: 'Orientar com clareza, documentar a suspeita e encaminhar com relatório sem perda de tempo.' }
      ]
    },
    {
      eyebrow: '10 · Encerramento',
      badge: 'SÍNTESE & COMPROMISSO',
      title: 'Telefarmácia: tecnologia a serviço do cuidado humano.',
      lead: 'O objetivo é aproximar o conhecimento científico das comunidades, fortalecendo a formação acadêmica e o vínculo em saúde.',
      accent: 'green',
      family: 5,
      closingPillars: [
        { num: '01', title: 'Ampliação do Acesso', desc: 'Transpor barreiras geográficas com rigor técnico e humanização.' },
        { num: '02', title: 'Sinergia Acadêmica', desc: 'Fortalecer o ensino prático conectado às demandas reais da população.' },
        { num: '03', title: 'Cuidado Centrado', desc: 'Preservar a escuta empática e o compromisso ético como centro de tudo.' }
      ],
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

  // Helper para sub-intervalos cinéticos com curva cúbica
  function subProg(p, start, end) {
    if (p <= start) return 0;
    if (p >= end) return 1;
    const t = (p - start) / (end - start);
    return 1 - Math.pow(1 - t, 3);
  }

  // Progresso de entrada do Slide 2:
  // Janela: 0.050 (quando o Slide 1 inicia a separação física) até 0.130 (quando o Slide 2 estabiliza)
  const s2InProg = $derived(clamp01((currentRatio - 0.050) / (0.130 - 0.050)));
  const s2IsVisible = $derived(currentRatio >= 0.048 && currentRatio <= 0.230);
  const s2IsActive = $derived(currentRatio >= 0.125 && currentRatio <= 0.165);
  const s2OutProg = $derived(clamp01((currentRatio - 0.150) / (0.225 - 0.150)));

  const s2Anim = $derived.by(() => {
    const p = s2InProg;
    const pOut = s2OutProg;
    const outDx0 = -160 * pOut;
    const outDx1 = 160 * pOut;
    const outDyTitle = -70 * pOut;
    const outDxArt = 180 * pOut;

    // Fundo sólido sem esmaecer: expansão circular simétrica do centro da tela (50% 50%)
    const pBg = subProg(p, 0.00, 0.55);
    const bgClip = p >= 1 ? 'none' : `circle(${(pBg * 165).toFixed(1)}% at 50% 50%)`;

    // Barra superior e cabeçalho editorial
    const pTopBar = subProg(p, 0.10, 0.60);
    const pTopText = subProg(p, 0.15, 0.65);
    const topBarScale = pTopBar.toFixed(3);
    const topTextTrans = `translate3d(0, ${(((1 - pTopText) * -45) + (outDyTitle * 0.7)).toFixed(1)}px, 0)`;
    const topBadgeScale = (0.7 + 0.3 * pTopText).toFixed(3);
    const topIndexTrans = `translate3d(${(((1 - pTopText) * 60) + (outDxArt * 0.5)).toFixed(1)}px, 0, 0)`;

    // Título cinético (2 linhas cortadas por máscaras overflow: hidden)
    const pTitle1 = subProg(p, 0.18, 0.68);
    const pTitle2 = subProg(p, 0.26, 0.76);
    const titleLine1Trans = `translate3d(0, ${(((1 - pTitle1) * 115) + outDyTitle).toFixed(1)}%, 0)`;
    const titleLine2Trans = `translate3d(0, ${(((1 - pTitle2) * 115) + outDyTitle).toFixed(1)}%, 0)`;

    // Lead text
    const pLead = subProg(p, 0.32, 0.80);
    const leadTrans = `translate3d(${(((1 - pLead) * -65) + outDx0).toFixed(1)}px, 0, 0)`;

    // Card esquerdo: "Mero Comércio"
    const pCard0 = subProg(p, 0.30, 0.78);
    const card0Trans = `translate3d(${(((1 - pCard0) * -120) + outDx0).toFixed(1)}px, 0, 0) scale(${(0.88 + 0.12 * pCard0).toFixed(3)})`;

    // Barra de risco vermelha: corta a palavra fisicamente em tempo real
    const pStrike = subProg(p, 0.55, 0.90);
    const strikeScale = `scaleX(${pStrike.toFixed(3)}) rotate(-3deg)`;

    // Card direito: "Cuidado Clínico Estruturado"
    const pCard1 = subProg(p, 0.38, 0.85);
    const card1Trans = `translate3d(${(((1 - pCard1) * 85) + outDx1).toFixed(1)}px, ${((1 - pCard1) * 30).toFixed(1)}px, 0) scale(${(0.90 + 0.10 * pCard1).toFixed(3)})`;

    // Beacon de pulso verde
    const pBeacon = subProg(p, 0.45, 0.80);
    const beaconScale = `scale(${pBeacon < 1 ? (pBeacon * 1.35).toFixed(3) : '1.0'})`;

    // 3 Pilares com número saltando, linha esticando e texto deslizando
    const pP1 = subProg(p, 0.45, 0.82);
    const pillar1 = {
      idxScale: `scale(${pP1 < 1 ? (pP1 * 1.4).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pP1.toFixed(3)})`,
      textTrans: `translate3d(${((1 - pP1) * 40).toFixed(1)}px, 0, 0)`
    };

    const pP2 = subProg(p, 0.58, 0.90);
    const pillar2 = {
      idxScale: `scale(${pP2 < 1 ? (pP2 * 1.4).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pP2.toFixed(3)})`,
      textTrans: `translate3d(${((1 - pP2) * 40).toFixed(1)}px, 0, 0)`
    };

    const pP3 = subProg(p, 0.70, 0.98);
    const pillar3 = {
      idxScale: `scale(${pP3 < 1 ? (pP3 * 1.4).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pP3.toFixed(3)})`,
      textTrans: `translate3d(${((1 - pP3) * 40).toFixed(1)}px, 0, 0)`
    };

    // Arte Lateral: Número 02, Bússola e Linhas
    const pArt = subProg(p, 0.05, 0.75);
    const artNumberTrans = `translate3d(${(((1 - pArt) * 160) + outDxArt).toFixed(1)}px, 0, 0) scale(${(1 + (1 - pArt) * 1.15).toFixed(3)})`;
    const artCompassTrans = `rotate(${((1 - pArt) * -180).toFixed(1)}deg) scale(${pArt.toFixed(3)})`;
    const artLineOne = `scaleX(${subProg(p, 0.15, 0.80).toFixed(3)})`;
    const artLineTwo = `scaleX(${subProg(p, 0.25, 0.85).toFixed(3)})`;
    const pDot = subProg(p, 0.35, 0.80);
    const artDot = `scale(${pDot < 1 ? (pDot * 1.35).toFixed(3) : '1.0'})`;

    // Micro-ornamentos (anel e cruz médica)
    const pRing = subProg(p, 0.10, 0.75);
    const decoRing = `rotate(${(pRing * 180).toFixed(1)}deg) scale(${pRing.toFixed(3)})`;
    const pCross = subProg(p, 0.25, 0.82);
    const decoCross = `rotate(${((1 - pCross) * 90).toFixed(1)}deg) scale(${pCross.toFixed(3)})`;

    // Rodapé
    const pFooter = subProg(p, 0.40, 0.85);
    const footerTrans = `translate3d(0, ${((1 - pFooter) * 25).toFixed(1)}px, 0)`;

    return {
      bgClip,
      topBarScale,
      topTextTrans,
      topBadgeScale,
      topIndexTrans,
      titleLine1Trans,
      titleLine2Trans,
      leadTrans,
      card0Trans,
      strikeScale,
      card1Trans,
      beaconScale,
      pillar1,
      pillar2,
      pillar3,
      artNumberTrans,
      artCompassTrans,
      artLineOne,
      artLineTwo,
      artDot,
      decoRing,
      decoCross,
      footerTrans
    };
  });

  // Progresso de entrada do Slide 3:
  // Janela: 0.150 (quando o Slide 2 inicia separação física) até 0.230 (quando o Slide 3 estabiliza no centro 0.24)
  const s3InProg = $derived(clamp01((currentRatio - 0.150) / (0.230 - 0.150)));
  const s3IsVisible = $derived(currentRatio >= 0.148 && currentRatio <= 0.330);
  const s3IsActive = $derived(currentRatio >= 0.225 && currentRatio <= 0.265);

  const s3Anim = $derived.by(() => {
    const p = s3InProg;

    // Fundo sólido medicinal claro (#f2f1e9): expansão circular sólida do centro (50% 50%)
    const pBg = subProg(p, 0.00, 0.55);
    const bgClip = p >= 1 ? 'none' : `circle(${(pBg * 165).toFixed(1)}% at 50% 50%)`;

    // Barra superior e cabeçalho editorial
    const pTopBar = subProg(p, 0.10, 0.60);
    const pTopText = subProg(p, 0.15, 0.65);
    const topBarScale = pTopBar.toFixed(3);
    const topTextTrans = `translate3d(0, ${((1 - pTopText) * -45).toFixed(1)}px, 0)`;
    const topBadgeScale = (0.7 + 0.3 * pTopText).toFixed(3);
    const topIndexTrans = `translate3d(${((1 - pTopText) * 60).toFixed(1)}px, 0, 0)`;

    // Título cinético (2 linhas cortadas por máscaras overflow: hidden)
    const pTitle1 = subProg(p, 0.18, 0.68);
    const pTitle2 = subProg(p, 0.26, 0.76);
    const titleLine1Trans = `translate3d(0, ${((1 - pTitle1) * 115).toFixed(1)}%, 0)`;
    const titleLine2Trans = `translate3d(0, ${((1 - pTitle2) * 115).toFixed(1)}%, 0)`;

    // Lead text
    const pLead = subProg(p, 0.30, 0.78);
    const leadTrans = `translate3d(${((1 - pLead) * -65).toFixed(1)}px, 0, 0)`;

    // As 4 Estações de Modalidades (em cascata rítmica com subida física e expansão elástica)
    const pM1 = subProg(p, 0.35, 0.75);
    const station1 = {
      cardTrans: `translate3d(0, ${((1 - pM1) * 65).toFixed(1)}px, 0) scale(${(0.86 + 0.14 * pM1).toFixed(3)})`,
      codeScale: `scale(${pM1 < 1 ? (pM1 * 1.35).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pM1.toFixed(3)})`,
      textTrans: `translate3d(0, ${((1 - pM1) * 20).toFixed(1)}px, 0)`
    };

    const pM2 = subProg(p, 0.45, 0.82);
    const station2 = {
      cardTrans: `translate3d(0, ${((1 - pM2) * 65).toFixed(1)}px, 0) scale(${(0.86 + 0.14 * pM2).toFixed(3)})`,
      codeScale: `scale(${pM2 < 1 ? (pM2 * 1.35).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pM2.toFixed(3)})`,
      textTrans: `translate3d(0, ${((1 - pM2) * 20).toFixed(1)}px, 0)`
    };

    const pM3 = subProg(p, 0.55, 0.89);
    const station3 = {
      cardTrans: `translate3d(0, ${((1 - pM3) * 65).toFixed(1)}px, 0) scale(${(0.86 + 0.14 * pM3).toFixed(3)})`,
      codeScale: `scale(${pM3 < 1 ? (pM3 * 1.35).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pM3.toFixed(3)})`,
      textTrans: `translate3d(0, ${((1 - pM3) * 20).toFixed(1)}px, 0)`
    };

    const pM4 = subProg(p, 0.65, 0.96);
    const station4 = {
      cardTrans: `translate3d(0, ${((1 - pM4) * 65).toFixed(1)}px, 0) scale(${(0.86 + 0.14 * pM4).toFixed(3)})`,
      codeScale: `scale(${pM4 < 1 ? (pM4 * 1.35).toFixed(3) : '1.0'})`,
      lineScale: `scaleX(${pM4.toFixed(3)})`,
      textTrans: `translate3d(0, ${((1 - pM4) * 20).toFixed(1)}px, 0)`
    };

    // Arte Lateral: Número 03, Bússola e Coordenadas
    const pArt = subProg(p, 0.05, 0.75);
    const artNumberTrans = `translate3d(${((1 - pArt) * 160).toFixed(1)}px, 0, 0) scale(${(1 + (1 - pArt) * 1.15).toFixed(3)})`;
    const artCompassTrans = `rotate(${((1 - pArt) * -180).toFixed(1)}deg) scale(${pArt.toFixed(3)})`;
    const artLineOne = `scaleX(${subProg(p, 0.15, 0.80).toFixed(3)})`;
    const artLineTwo = `scaleX(${subProg(p, 0.25, 0.85).toFixed(3)})`;
    const pDot = subProg(p, 0.35, 0.80);
    const artDot = `scale(${pDot < 1 ? (pDot * 1.35).toFixed(3) : '1.0'})`;

    // Micro-ornamentos (arco, carimbo e trio de pontos)
    const pArc = subProg(p, 0.12, 0.75);
    const decoArcScale = (0.7 + 0.3 * pArc).toFixed(3);
    const pStamp = subProg(p, 0.40, 0.85);
    const decoStampTrans = `scale(${pStamp < 1 ? (pStamp * 1.25).toFixed(3) : '1.0'})`;
    const pDots = subProg(p, 0.45, 0.90);
    const decoDotsScale = (pDots < 1 ? pDots * 1.3 : 1.0).toFixed(3);

    // Rodapé
    const pFooter = subProg(p, 0.40, 0.85);
    const footerTrans = `translate3d(0, ${((1 - pFooter) * 25).toFixed(1)}px, 0)`;

    return {
      bgClip,
      topBarScale,
      topTextTrans,
      topBadgeScale,
      topIndexTrans,
      titleLine1Trans,
      titleLine2Trans,
      leadTrans,
      station1,
      station2,
      station3,
      station4,
      artNumberTrans,
      artCompassTrans,
      artLineOne,
      artLineTwo,
      artDot,
      decoArcScale,
      decoStampTrans,
      decoDotsScale,
      footerTrans
    };
  });

  // Camadas de Fundo Contínuas (Desktop)
  const bgForestInS2 = $derived(clamp01((currentRatio - 0.07) / 0.05));
  const bgLightIn = $derived(clamp01((currentRatio - 0.165) / 0.05));
  const bgRedIn = $derived(clamp01((currentRatio - 0.765) / 0.05));
  const bgForestInS10 = $derived(clamp01((currentRatio - 0.865) / 0.05));

  function getCardStyle(tIn, tOut, family, cardIndex) {
    const step = 0.07;
    const inStart = Math.min(0.60, 0.22 + cardIndex * step);
    const inEnd = Math.min(1.00, inStart + 0.42);
    const outStart = Math.min(0.50, 0.08 + cardIndex * 0.05);
    const outEnd = Math.min(1.00, outStart + 0.42);

    const layer = computeLayer(tIn, tOut, inStart, inEnd, outStart, outEnd);
    const pIn = layer.pIn;
    const pOut = layer.pOut;

    let transform = 'none';
    if (family === 0) {
      const dxIn = -40 * (1 - pIn);
      const dyIn = 14 * (1 - pIn);
      const dxOut = -30 * pOut;
      const dyOut = -14 * pOut;
      transform = `translate3d(${(dxIn + dxOut).toFixed(1)}px, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 1) {
      const dyIn = 50 * (1 - pIn);
      const dyOut = -28 * pOut;
      const scale = (0.95 + 0.05 * pIn) * (1 - 0.03 * pOut);
      transform = `translate3d(0, ${(dyIn + dyOut).toFixed(1)}px, 0) scale(${scale.toFixed(3)})`;
    } else if (family === 2) {
      const scale = (0.93 + 0.07 * pIn) * (1 - 0.04 * pOut);
      const rot = (1.2 * (1 - pIn)) - (0.8 * pOut);
      const dyOut = -20 * pOut;
      transform = `translate3d(0, ${dyOut.toFixed(1)}px, 0) scale(${scale.toFixed(3)}) rotate(${rot.toFixed(2)}deg)`;
    } else if (family === 3) {
      const dxIn = -28 * (1 - pIn);
      const dyIn = 20 * (1 - pIn);
      const dyOut = -22 * pOut;
      transform = `translate3d(${dxIn.toFixed(1)}px, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 4) {
      const dyIn = 20 * (1 - pIn);
      const dyOut = -14 * pOut;
      transform = `translate3d(0, ${(dyIn + dyOut).toFixed(1)}px, 0)`;
    } else if (family === 5) {
      const dyIn = 26 * (1 - pIn);
      const dyOut = -18 * pOut;
      const scale = (0.94 + 0.06 * pIn) * (1 - 0.03 * pOut);
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

    const lTopline = computeLayer(tIn, tOut, 0.00, 0.40, 0.50, 0.95);
    const lTitle = computeLayer(tIn, tOut, 0.08, 0.55, 0.40, 0.88);
    const lLead = computeLayer(tIn, tOut, 0.16, 0.65, 0.30, 0.80);
    const lArt = computeLayer(tIn, tOut, 0.12, 0.70, 0.22, 0.82);
    const lFooter = computeLayer(tIn, tOut, 0.55, 0.98, 0.05, 0.50);
    const lDeco = computeLayer(tIn, tOut, 0.04, 0.60, 0.35, 0.90);

    let tTopline = 'none';
    let tTitle = 'none';
    let tLead = 'none';
    let tArt = 'none';
    let tFooter = 'none';
    let tDeco = 'none';

    if (family === 0) {
      tTopline = `translate3d(${((-40 * (1 - lTopline.pIn)) - (30 * lTopline.pOut)).toFixed(1)}px, 0, 0)`;
      tTitle = `translate3d(${((-50 * (1 - lTitle.pIn)) - (35 * lTitle.pOut)).toFixed(1)}px, 0, 0)`;
      tLead = `translate3d(${((-35 * (1 - lLead.pIn)) - (25 * lLead.pOut)).toFixed(1)}px, 0, 0)`;
      const artScale = (0.94 + 0.06 * lArt.pIn) * (1 - 0.05 * lArt.pOut);
      tArt = `translate3d(${((60 * (1 - lArt.pIn)) + (40 * lArt.pOut)).toFixed(1)}px, 0, 0) scale(${artScale.toFixed(3)})`;
      tFooter = `translate3d(0, ${((14 * (1 - lFooter.pIn)) - (12 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(${((30 * (1 - lDeco.pIn)) - (30 * lDeco.pOut)).toFixed(1)}px, 0, 0) scale(${(0.85 + 0.15 * lDeco.pIn).toFixed(3)})`;
    } else if (family === 1) {
      tTopline = `translate3d(0, ${((-20 * (1 - lTopline.pIn)) - (18 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((45 * (1 - lTitle.pIn)) - (35 * lTitle.pOut)).toFixed(1)}px, 0) scale(${(0.97 + 0.03 * lTitle.pIn).toFixed(3)})`;
      tLead = `translate3d(0, ${((32 * (1 - lLead.pIn)) - (25 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artScale = (0.93 + 0.07 * lArt.pIn) * (1 - 0.04 * lArt.pOut);
      tArt = `translate3d(0, ${((48 * (1 - lArt.pIn)) - (32 * lArt.pOut)).toFixed(1)}px, 0) scale(${artScale.toFixed(3)})`;
      tFooter = `translate3d(0, ${((16 * (1 - lFooter.pIn)) - (14 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(0, ${((-30 * (1 - lDeco.pIn)) + (30 * lDeco.pOut)).toFixed(1)}px, 0)`;
    } else if (family === 2) {
      tTopline = `translate3d(0, ${((-14 * (1 - lTopline.pIn)) - (16 * lTopline.pOut)).toFixed(1)}px, 0) scale(${(0.97 + 0.03 * lTopline.pIn).toFixed(3)})`;
      const titleScale = (0.94 + 0.06 * lTitle.pIn) * (1 + 0.02 * lTitle.pOut);
      const titleRot = (-1.2 * (1 - lTitle.pIn)) + (0.8 * lTitle.pOut);
      tTitle = `translate3d(0, ${((24 * (1 - lTitle.pIn)) - (24 * lTitle.pOut)).toFixed(1)}px, 0) scale(${titleScale.toFixed(3)}) rotate(${titleRot.toFixed(2)}deg)`;
      tLead = `translate3d(0, ${((18 * (1 - lLead.pIn)) - (20 * lLead.pOut)).toFixed(1)}px, 0) scale(${(0.96 + 0.04 * lLead.pIn).toFixed(3)})`;
      const artScale = (0.88 + 0.12 * lArt.pIn) * (1 - 0.08 * lArt.pOut);
      const artRot = (-3.5 * (1 - lArt.pIn)) + (2.5 * lArt.pOut);
      tArt = `scale(${artScale.toFixed(3)}) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((14 * (1 - lFooter.pIn)) - (12 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${(0.85 + 0.15 * lDeco.pIn).toFixed(3)}) rotate(${((-18 * (1 - lDeco.pIn)) + (18 * lDeco.pOut)).toFixed(2)}deg)`;
    } else if (family === 3) {
      tTopline = `translate3d(${((-22 * (1 - lTopline.pIn)) - (18 * lTopline.pOut)).toFixed(1)}px, ${((-14 * (1 - lTopline.pIn)) - (18 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(${((-40 * (1 - lTitle.pIn)) - (28 * lTitle.pOut)).toFixed(1)}px, ${((30 * (1 - lTitle.pIn)) - (28 * lTitle.pOut)).toFixed(1)}px, 0)`;
      tLead = `translate3d(${((-30 * (1 - lLead.pIn)) - (20 * lLead.pOut)).toFixed(1)}px, ${((22 * (1 - lLead.pIn)) - (20 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artRot = (-3 * (1 - lArt.pIn)) + (3.5 * lArt.pOut);
      tArt = `translate3d(${((45 * (1 - lArt.pIn)) + (30 * lArt.pOut)).toFixed(1)}px, ${((-32 * (1 - lArt.pIn)) + (26 * lArt.pOut)).toFixed(1)}px, 0) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((14 * (1 - lFooter.pIn)) - (12 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `translate3d(${((35 * (1 - lDeco.pIn)) - (35 * lDeco.pOut)).toFixed(1)}px, ${((35 * (1 - lDeco.pIn)) - (35 * lDeco.pOut)).toFixed(1)}px, 0)`;
    } else if (family === 4) {
      tTopline = `translate3d(0, ${((-12 * (1 - lTopline.pIn)) - (12 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((20 * (1 - lTitle.pIn)) - (16 * lTitle.pOut)).toFixed(1)}px, 0)`;
      tLead = `translate3d(0, ${((15 * (1 - lLead.pIn)) - (12 * lLead.pOut)).toFixed(1)}px, 0)`;
      tArt = `translate3d(0, ${(-14 * lArt.pOut).toFixed(1)}px, 0) scale(${(0.95 + 0.05 * lArt.pIn).toFixed(3)})`;
      tFooter = `translate3d(0, ${((10 * (1 - lFooter.pIn)) - (10 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${(0.92 + 0.08 * lDeco.pIn).toFixed(3)})`;
    } else if (family === 5) {
      tTopline = `translate3d(0, ${((-18 * (1 - lTopline.pIn)) - (16 * lTopline.pOut)).toFixed(1)}px, 0)`;
      tTitle = `translate3d(0, ${((32 * (1 - lTitle.pIn)) - (24 * lTitle.pOut)).toFixed(1)}px, 0) scale(${(0.97 + 0.03 * lTitle.pIn).toFixed(3)})`;
      tLead = `translate3d(0, ${((22 * (1 - lLead.pIn)) - (18 * lLead.pOut)).toFixed(1)}px, 0)`;
      const artScale = (0.88 + 0.12 * lArt.pIn) * (1 + 0.04 * lArt.pOut);
      const artRot = -5 * (1 - lArt.pIn);
      tArt = `translate3d(0, ${(-20 * lArt.pOut).toFixed(1)}px, 0) scale(${artScale.toFixed(3)}) rotate(${artRot.toFixed(2)}deg)`;
      tFooter = `translate3d(0, ${((16 * (1 - lFooter.pIn)) - (14 * lFooter.pOut)).toFixed(1)}px, 0)`;
      tDeco = `scale(${((0.85 + 0.15 * lDeco.pIn) * (1 + 0.12 * lDeco.pOut)).toFixed(3)})`;
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
  <!-- Palco de fundos persistente desktop -->
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
      style={mobile ? '' : (
        index === 0
          ? `visibility: ${s2IsVisible ? 'visible' : 'hidden'}; pointer-events: ${s2IsActive ? 'auto' : 'none'}; z-index: ${s2IsVisible ? 4 : 2}; opacity: 1; clip-path: ${s2Anim.bgClip}; background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.14), transparent 45%), #0d5b3e;`
          : (index === 1
            ? `visibility: ${s3IsVisible ? 'visible' : 'hidden'}; pointer-events: ${s3IsActive ? 'auto' : 'none'}; z-index: ${s3IsVisible ? 5 : 2}; opacity: 1; clip-path: ${s3Anim.bgClip}; background: radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.7), transparent 45%), linear-gradient(135deg, rgba(255, 255, 255, 0.42), transparent 55%), #f2f1e9;`
            : `visibility: ${st.visibility}; pointer-events: ${st.pointerEvents}; z-index: ${st.isCentered ? 3 : 2};`
          )
      )}
    >
      <!-- Camada Decorativa de Ambientação com Micro-Elementos Científicos (Igual ao Slide 1) -->
      <div
        class="slide-deco"
        style={index === 0 && !mobile
          ? 'opacity: 1; transform: none;'
          : (index === 1 && !mobile
            ? 'opacity: 1; transform: none;'
            : (mobile ? '' : `opacity: ${st.deco.opacity}; transform: ${st.deco.transform};`)
          )}
        aria-hidden="true"
      >
        {#if slide.accent === 'green'}
          <div
            class="deco-mesh mesh-green"
            style={index === 0 && !mobile ? `transform: scale(${(0.8 + 0.2 * s2InProg).toFixed(3)});` : ''}
          ></div>
          <!-- Anel tracejado flutuante igual Slide 1 com expansão e rotação -->
          <svg
            class="deco-ring"
            width="140"
            height="140"
            viewBox="0 0 100 100"
            fill="none"
            stroke="currentColor"
            style={index === 0 && !mobile ? `transform: ${s2Anim.decoRing};` : ''}
          >
            <circle cx="50" cy="50" r="42" stroke-dasharray="4 6" stroke-width="1.2" opacity="0.22" />
            <circle cx="50" cy="50" r="18" stroke-width="0.8" opacity="0.14" />
          </svg>
          <div
            class="deco-cross-clean"
            style={index === 0 && !mobile ? `transform: ${s2Anim.decoCross};` : ''}
          >
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M12 4v16M4 12h16" />
            </svg>
          </div>
        {:else if slide.accent === 'red'}
          <div class="deco-mesh mesh-red"></div>
          <svg class="deco-radar" width="180" height="180" viewBox="0 0 100 100" fill="none" stroke="#b94d39">
            <circle cx="50" cy="50" r="45" stroke-dasharray="2 4" stroke-width="1" opacity="0.3" />
            <circle cx="50" cy="50" r="28" stroke-width="0.8" opacity="0.2" />
            <path d="M50 5v90M5 50h90" stroke-width="0.6" opacity="0.15" />
          </svg>
          <div class="deco-alert-badge">
            <span class="pulse-point"></span>
            <span>PROTOCOLO DE URGÊNCIA</span>
          </div>
        {:else}
          <div class="deco-mesh mesh-light"></div>
          <!-- Ornamentos editoriais finos em lâmina clara -->
          <svg
            class="deco-arc"
            width="160"
            height="90"
            viewBox="0 0 160 90"
            fill="none"
            stroke="currentColor"
            style={index === 1 && !mobile ? `transform: scale(${s3Anim.decoArcScale}); transform-origin: bottom left;` : ''}
          >
            <path d="M10 80 A70 70 0 0 1 150 80" stroke-width="1" stroke-dasharray="3 5" opacity="0.25" />
          </svg>
          <div
            class="deco-stamp"
            style={index === 1 && !mobile ? `transform: ${s3Anim.decoStampTrans};` : ''}
          >
            <span>SEC. 0{index + 2} // CLINICAL METHOD</span>
          </div>
          <div
            class="deco-dots-trio"
            style={index === 1 && !mobile ? `transform: scale(${s3Anim.decoDotsScale});` : ''}
          >
            <span></span><span></span><span></span>
          </div>
        {/if}
      </div>

      <!-- Palco Estável do Conteúdo -->
      <div class="slide-frame">
        <!-- Topline Editorial com Badge de Alta Precisão -->
        <div
          class="slide-topline"
          style={index === 0 && !mobile
            ? `opacity: 1; transform: ${s2Anim.topTextTrans}; border-bottom: none;`
            : (index === 1 && !mobile
              ? `opacity: 1; transform: ${s3Anim.topTextTrans}; border-bottom: none;`
              : (mobile ? '' : `opacity: ${st.topline.opacity}; transform: ${st.topline.transform};`)
            )}
        >
          <div class="topline-left">
            <span class="slide-eyebrow">{slide.eyebrow}</span>
            <span
              class="topline-tag"
              style={index === 0 && !mobile
                ? `transform: scale(${s2Anim.topBadgeScale}); display: inline-block;`
                : (index === 1 && !mobile
                  ? `transform: scale(${s3Anim.topBadgeScale}); display: inline-block;`
                  : ''
                )}
            >{slide.badge}</span>
          </div>
          <span
            class="slide-index"
            style={index === 0 && !mobile
              ? `transform: ${s2Anim.topIndexTrans};`
              : (index === 1 && !mobile
                ? `transform: ${s3Anim.topIndexTrans};`
                : ''
              )}
          >{String(index + 2).padStart(2, '0')} / 10</span>

          {#if index === 0 && !mobile}
            <div class="topline-rail-line" style={`transform: scaleX(${s2Anim.topBarScale});`}></div>
          {:else if index === 1 && !mobile}
            <div class="topline-rail-line" style={`transform: scaleX(${s3Anim.topBarScale});`}></div>
          {/if}
        </div>

        <div class="slide-content">
          <div class="slide-main-grid">
            <div class="slide-main">
              <!-- Cabeçalho Tipográfico com Respiração Cinética e Corte Sólido -->
              <header class="slide-copy">
                {#if index === 0 && !mobile}
                  <h2 class="kinetic-title">
                    <span class="kinetic-line-mask">
                      <span class="kinetic-line" style={`transform: ${s2Anim.titleLine1Trans};`}>
                        Telefarmácia não é
                      </span>
                    </span>
                    <span class="kinetic-line-mask">
                      <span class="kinetic-line line-highlight" style={`transform: ${s2Anim.titleLine2Trans};`}>
                        venda online.
                      </span>
                    </span>
                  </h2>
                {:else if index === 1 && !mobile}
                  <h2 class="kinetic-title">
                    <span class="kinetic-line-mask">
                      <span class="kinetic-line" style={`transform: ${s3Anim.titleLine1Trans};`}>
                        Quatro formas de levar
                      </span>
                    </span>
                    <span class="kinetic-line-mask">
                      <span class="kinetic-line line-highlight" style={`transform: ${s3Anim.titleLine2Trans};`}>
                        o cuidado mais longe.
                      </span>
                    </span>
                  </h2>
                {:else}
                  <h2 style={mobile ? '' : `opacity: ${st.title.opacity}; transform: ${st.title.transform};`}>
                    {slide.title}
                  </h2>
                {/if}
                <p
                  class="slide-lead"
                  style={index === 0 && !mobile
                    ? `opacity: 1; transform: ${s2Anim.leadTrans};`
                    : (index === 1 && !mobile
                      ? `opacity: 1; transform: ${s3Anim.leadTrans};`
                      : (mobile ? '' : `opacity: ${st.lead.opacity}; transform: ${st.lead.transform};`)
                    )}
                >
                  {slide.lead}
                </p>
              </header>

              <!-- CONTEÚDO ESPECÍFICO REFINADO POR SLIDE -->

              <!-- SLIDE 2: Ruptura Editorial (Comércio vs. Exercício Clínico) -->
              {#if slide.divergence}
                <div class="editorial-duo">
                  <!-- Lado Não-Clínico Riscado -->
                  <div
                    class="duo-side duo-negated"
                    style={index === 0 && !mobile ? `opacity: 1; transform: ${s2Anim.card0Trans};` : (mobile ? '' : `opacity: ${st.cards[0].opacity}; transform: ${st.cards[0].transform};`)}
                  >
                    <div class="duo-tag">
                      <span
                        class="strike-bar"
                        style={index === 0 && !mobile ? `transform: ${s2Anim.strikeScale}; transform-origin: left;` : ''}
                      ></span>
                      <strong>{slide.divergence.tag}</strong>
                    </div>
                    <p>{slide.divergence.desc}</p>
                  </div>

                  <!-- Lado Clínico em Destaque com 3 Nós Conectados -->
                  <div
                    class="duo-side duo-clinical"
                    style={index === 0 && !mobile ? `opacity: 1; transform: ${s2Anim.card1Trans};` : (mobile ? '' : `opacity: ${st.cards[1].opacity}; transform: ${st.cards[1].transform};`)}
                  >
                    <div class="clinical-head">
                      <span
                        class="clinical-beacon"
                        style={index === 0 && !mobile ? `transform: ${s2Anim.beaconScale};` : ''}
                      ></span>
                      <strong>Cuidado Clínico Estruturado</strong>
                    </div>
                    <div class="clinical-pillars">
                      {#each slide.pillars as pillar, pIdx}
                        {@const pAnim = pIdx === 0 ? s2Anim.pillar1 : pIdx === 1 ? s2Anim.pillar2 : s2Anim.pillar3}
                        <div class="pillar-row">
                          <span
                            class="pillar-idx"
                            style={index === 0 && !mobile ? `transform: ${pAnim.idxScale}; display: inline-block;` : ''}
                          >0{pIdx + 1}</span>
                          <div
                            class="pillar-body"
                            style={index === 0 && !mobile ? `transform: ${pAnim.textTrans};` : ''}
                          >
                            <h4>{pillar[0]}</h4>
                            <small>{pillar[1]}</small>
                          </div>
                          {#if index === 0 && !mobile}
                            <div class="pillar-divider-line" style={`transform: ${pAnim.lineScale};`}></div>
                          {/if}
                        </div>
                      {/each}
                    </div>
                  </div>
                </div>

              <!-- SLIDE 3: Matriz de 4 Modalidades em Rede -->
              {:else if slide.modalities}
                <div class="modalities-net">
                  {#each slide.modalities as mod, mIdx}
                    {@const stAnim = mIdx === 0 ? s3Anim.station1 : mIdx === 1 ? s3Anim.station2 : mIdx === 2 ? s3Anim.station3 : s3Anim.station4}
                    <article
                      class="mod-station"
                      style={index === 1 && !mobile
                        ? `opacity: 1; transform: ${stAnim.cardTrans};`
                        : (mobile ? '' : `opacity: ${st.cards[mIdx].opacity}; transform: ${st.cards[mIdx].transform};`)}
                    >
                      <div class="station-meta">
                        <span
                          class="station-code"
                          style={index === 1 && !mobile ? `transform: ${stAnim.codeScale}; display: inline-block;` : ''}
                        >{mod.code}</span>
                        <span
                          class="station-line"
                          style={index === 1 && !mobile ? `transform: ${stAnim.lineScale}; transform-origin: left;` : ''}
                        ></span>
                      </div>
                      <div class="station-body" style={index === 1 && !mobile ? `transform: ${stAnim.textTrans};` : ''}>
                        <h3>{mod.name}</h3>
                        <p>{mod.desc}</p>
                      </div>
                    </article>
                  {/each}
                </div>

              <!-- SLIDE 4: Arcabouço Legal e Selo de RT Presencial -->
              {:else if slide.laws}
                <div class="legal-framework">
                  <div class="laws-duo">
                    {#each slide.laws as law, lIdx}
                      <article
                        class="law-plaque"
                        style={mobile ? '' : `opacity: ${st.cards[lIdx].opacity}; transform: ${st.cards[lIdx].transform};`}
                      >
                        <span class="law-symbol">§</span>
                        <div>
                          <h3>{law.num}</h3>
                          <p>{law.desc}</p>
                        </div>
                      </article>
                    {/each}
                  </div>
                  <aside
                    class="solemn-warning"
                    style={mobile ? '' : `opacity: ${st.cards[2].opacity}; transform: ${st.cards[2].transform};`}
                  >
                    <div class="warning-anchor">
                      <span class="anchor-bullet"></span>
                      <strong>PRESENÇA FÍSICA DO RT</strong>
                    </div>
                    <p>{slide.warning}</p>
                  </aside>
                </div>

              <!-- SLIDE 5: Nós Criptográficos de Segurança e LGPD -->
              {:else if slide.securityPoints}
                <div class="security-cluster">
                  {#each slide.securityPoints as sec, sIdx}
                    <article
                      class="sec-card"
                      style={mobile ? '' : `opacity: ${st.cards[sIdx].opacity}; transform: ${st.cards[sIdx].transform};`}
                    >
                      <div class="sec-badge-row">
                        <span class="sec-code">{sec.code}</span>
                        <span class="sec-pip"></span>
                      </div>
                      <h3>{sec.title}</h3>
                      <p>{sec.desc}</p>
                    </article>
                  {/each}
                </div>

              <!-- SLIDE 6: Trilho Contínuo da Jornada Clínica -->
              {:else if slide.steps}
                <div class="journey-track">
                  <div class="track-spine" aria-hidden="true"></div>
                  {#each slide.steps as stp, stpIdx}
                    <button
                      class:journey-active={stpIdx <= 2}
                      class="track-station"
                      type="button"
                      onclick={() => goTo(stpIdx + 5)}
                      style={mobile ? '' : `opacity: ${st.cards[stpIdx].opacity}; transform: ${st.cards[stpIdx].transform};`}
                    >
                      <div class="station-node">
                        <span class="node-num">{stp.step}</span>
                      </div>
                      <div class="station-text">
                        <strong>{stp.title}</strong>
                        <small>{stp.desc}</small>
                      </div>
                    </button>
                  {/each}
                </div>

              <!-- SLIDE 7: Prática Clínica na Teleconsulta -->
              {:else if slide.practicePoints}
                <div class="practice-stream">
                  {#each slide.practicePoints as prc, prIdx}
                    <article
                      class="practice-card"
                      style={mobile ? '' : `opacity: ${st.cards[prIdx].opacity}; transform: ${st.cards[prIdx].transform};`}
                    >
                      <div class="practice-left">
                        <span class="practice-code">{prc.num}</span>
                      </div>
                      <div class="practice-right">
                        <h3>{prc.title}</h3>
                        <p>{prc.desc}</p>
                      </div>
                    </article>
                  {/each}
                </div>

              <!-- SLIDE 8: Escopo Clínico e Balança de Decisão -->
              {:else if slide.compare}
                <div class="scope-comparison">
                  <div class="scope-nav">
                    <span class="scope-prompt">Enquadramento Regulatório</span>
                    <div class="scope-tabs">
                      <button class:chosen={compareMode === 'sup'} type="button" onclick={() => compareMode = 'sup'}>
                        Suplementos Alimentares
                      </button>
                      <button class:chosen={compareMode === 'med'} type="button" onclick={() => compareMode = 'med'}>
                        Medicamentos e Prescrição
                      </button>
                    </div>
                  </div>
                  <div class="scope-panes">
                    <article
                      class:dimmed={compareMode === 'med'}
                      class="scope-pane pane-supp"
                      style={mobile ? '' : `opacity: ${st.cards[1].opacity}; transform: ${st.cards[1].transform};`}
                    >
                      <span class="pane-badge">ORIENTAÇÃO FARMACÊUTICA</span>
                      <h3>Comunicação e Educação</h3>
                      <p>Esclarecer composição, dosagens adequadas, interações alimentares e limites éticos sem indução comercial.</p>
                    </article>
                    <article
                      class:dimmed={compareMode === 'sup'}
                      class="scope-pane pane-med"
                      style={mobile ? '' : `opacity: ${st.cards[2].opacity}; transform: ${st.cards[2].transform};`}
                    >
                      <span class="pane-badge alert-color">ATO PRESCRITIVO</span>
                      <h3>Prescrição Farmacêutica</h3>
                      <p>Exige anamnese, raciocínio clínico formal, registro em prontuário e respeito integral às resoluções do CFF.</p>
                    </article>
                  </div>
                </div>

              <!-- SLIDE 9: Red Flags e Parâmetros de Urgência -->
              {:else if slide.alerts}
                <div class="red-flag-cluster">
                  {#each slide.alerts as al, aIdx}
                    <article
                      class="alert-entry"
                      style={mobile ? '' : `opacity: ${st.cards[aIdx].opacity}; transform: ${st.cards[aIdx].transform};`}
                    >
                      <span class="alert-mark">!</span>
                      <div>
                        <h3>{al.title}</h3>
                        <p>{al.desc}</p>
                      </div>
                    </article>
                  {/each}
                </div>

              <!-- SLIDE 10: Síntese e Compromisso Humanizado -->
              {:else if slide.closingPillars}
                <div class="closing-triptych">
                  {#each slide.closingPillars as pil, pIdx}
                    <div
                      class="triptych-column"
                      style={mobile ? '' : `opacity: ${st.cards[pIdx].opacity}; transform: ${st.cards[pIdx].transform};`}
                    >
                      <span class="triptych-idx">0{pIdx + 1}</span>
                      <h3>{pil.title}</h3>
                      <p>{pil.desc}</p>
                    </div>
                  {/each}
                </div>
              {/if}
            </div>

            <!-- Camada de Ilustração Lateral Vetorial e Dinâmica -->
            <aside
              class={`slide-art art-${slide.visual || (index % 3)}`}
              style={mobile ? '' : `opacity: ${st.art.opacity}; transform: ${st.art.transform};`}
              aria-hidden="true"
            >
              {#if slide.visual === 'shield'}
                <!-- Escudo de Privacidade com Marca Oficial da ANPD -->
                <div class="art-orbit orbit-a"></div>
                <div class="art-orbit orbit-b"></div>
                <div class="official-brand">
                  <img src="/assets/anpd-symbol-official.png" alt="" />
                  <strong>ANPD</strong>
                  <span>Autoridade Nacional<br>de Proteção de Dados</span>
                </div>
                <div class="art-caption">COMPLIANCE LGPD<br><strong>SAÚDE DIGITAL</strong></div>

              {:else if slide.visual === 'call'}
                <!-- Janela de Teleconsulta com Osciloscópio Vital -->
                <div class="art-window">
                  <div class="window-bar">
                    <i></i><i></i><i></i>
                    <span>TELECONSULTA CLÍNICA</span>
                  </div>
                  <div class="window-body">
                    <div class="art-avatar"></div>
                    <div class="clinical-waves">
                      <span></span><span></span><span></span><span></span>
                    </div>
                  </div>
                  <div class="window-footer">
                    <span>● AO VIVO</span>
                    <span>SALA CRIPTOGRAFADA</span>
                  </div>
                </div>

              {:else if slide.compare}
                <!-- Balança de Precisão Farmacêutica Dinâmica -->
                <div class="art-scale" class:tilt-right={compareMode === 'med'}>
                  <div class="scale-post"></div>
                  <div class="scale-beam"></div>
                  <div class="scale-pan pan-left">ORIENTAR</div>
                  <div class="scale-pan pan-right">PRESCREVER</div>
                  <div class="scale-fulcrum"></div>
                </div>

              {:else if slide.accent === 'red'}
                <!-- Radar de Atenção Clínica -->
                <div class="art-emergency-radar">
                  <div class="radar-circle ring-outer"></div>
                  <div class="radar-circle ring-mid"></div>
                  <div class="radar-pulse-core"></div>
                  <div class="radar-label">TRIAGEM<br><strong>IMEDIATA</strong></div>
                </div>

              {:else if slide.closing}
                <!-- Aurora Solar Poética da Ciência e Cuidado -->
                <div class="art-sun">
                  <div class="sun-core"></div>
                  <div class="sun-orbit"></div>
                  <span>CIÊNCIA<br><strong>+ CUIDADO</strong></span>
                </div>

              {:else}
                <!-- Escultura Vetorial Editorial com Coordenadas -->
                <div
                  class="art-number"
                  style={index === 0 && !mobile
                    ? `transform: ${s2Anim.artNumberTrans};`
                    : (index === 1 && !mobile
                      ? `transform: ${s3Anim.artNumberTrans};`
                      : '')}
                >
                  {String(index + 2).padStart(2, '0')}
                </div>
                <div
                  class="art-line line-one"
                  style={index === 0 && !mobile
                    ? `transform: ${s2Anim.artLineOne}; transform-origin: left;`
                    : (index === 1 && !mobile
                      ? `transform: ${s3Anim.artLineOne}; transform-origin: left;`
                      : '')}
                ></div>
                <div
                  class="art-line line-two"
                  style={index === 0 && !mobile
                    ? `transform: ${s2Anim.artLineTwo}; transform-origin: left;`
                    : (index === 1 && !mobile
                      ? `transform: ${s3Anim.artLineTwo}; transform-origin: left;`
                      : '')}
                ></div>
                <div
                  class="art-dot"
                  style={index === 0 && !mobile
                    ? `transform: ${s2Anim.artDot};`
                    : (index === 1 && !mobile
                      ? `transform: ${s3Anim.artDot};`
                      : '')}
                ></div>
                <div
                  class="art-compass"
                  style={index === 0 && !mobile
                    ? `transform: ${s2Anim.artCompassTrans};`
                    : (index === 1 && !mobile
                      ? `transform: ${s3Anim.artCompassTrans};`
                      : '')}
                >
                  <svg width="60" height="60" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="0.8" opacity="0.35">
                    <circle cx="20" cy="20" r="16" stroke-dasharray="2 3"/>
                    <path d="M20 4v32M4 20h32"/>
                  </svg>
                </div>
              {/if}
            </aside>
          </div>
        </div>

        <!-- Rodapé Editorial -->
        <div
          class="slide-footer"
          style={index === 0 && !mobile
            ? `opacity: 1; transform: ${s2Anim.footerTrans};`
            : (index === 1 && !mobile
              ? `opacity: 1; transform: ${s3Anim.footerTrans};`
              : (mobile ? '' : `opacity: ${st.footer.opacity}; transform: ${st.footer.transform};`))}
        >
          <div class="footer-left">
            <span>Telefarmácia & Serviços Digitais Farmacêuticos</span>
            <span class="footer-pipe">|</span>
            <span class="footer-spec">Bacharelado em Farmácia · UNIGRANDE</span>
          </div>
          <button type="button" onclick={() => goTo(index)}>
            {index === 0 ? 'Voltar ao início' : '← Slide Anterior'}
          </button>
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

  /* Palco de Slide Estável */
  .slide {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: clamp(3rem, 7vh, 5.5rem) clamp(1.25rem, 6.5vw, 6.8rem);
    overflow: hidden;
  }

  .theme-green { color: #f8f6ed; }
  .theme-light { color: #17362d; }
  .theme-red { color: #2f2523; }

  /* Canvas sólido exclusivo para entrada do Slide 2 sem esmaecer */
  .slide-solid-canvas {
    position: absolute;
    inset: 0;
    z-index: 0;
    background: radial-gradient(circle at 82% 44%, rgba(255, 255, 255, 0.14), transparent 38%), #0d5b3e;
    pointer-events: none;
    will-change: clip-path;
  }

  /* Camada Decorativa de Precisão (Igual ao Slide 1) */
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

  .deco-ring {
    position: absolute;
    top: 10%;
    right: 12%;
    opacity: 0.8;
    animation: slowSpin 35s linear infinite;
  }
  .deco-cross-clean {
    position: absolute;
    top: 25%;
    left: 8%;
    opacity: 0.22;
  }
  .deco-radar {
    position: absolute;
    top: 8%;
    right: 15%;
    opacity: 0.6;
  }
  .deco-alert-badge {
    position: absolute;
    top: 3.2rem;
    right: 5rem;
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    padding: .35rem .75rem;
    border: 1px solid rgba(185, 77, 57, 0.4);
    border-radius: 999px;
    font-size: .65rem;
    font-weight: 800;
    letter-spacing: .16em;
    color: #b94d39;
    background: rgba(185, 77, 57, 0.08);
  }
  .pulse-point {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #b94d39;
    box-shadow: 0 0 0 4px rgba(185, 77, 57, 0.2);
  }
  .deco-arc {
    position: absolute;
    bottom: 12%;
    left: 7%;
    opacity: 0.6;
  }
  .deco-stamp {
    position: absolute;
    bottom: 3rem;
    left: 5rem;
    font-size: .62rem;
    font-family: monospace;
    letter-spacing: .15em;
    opacity: 0.35;
  }
  .deco-dots-trio {
    position: absolute;
    top: 3.5rem;
    left: 5rem;
    display: flex;
    gap: 8px;
  }
  .deco-dots-trio span {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.35;
  }

  @keyframes slowSpin { to { transform: rotate(360deg); } }

  /* Frame Principal */
  .slide-frame {
    position: relative;
    z-index: 1;
    width: min(1140px, 100%);
    min-height: min(670px, 86vh);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1.8rem;
  }

  .slide-topline, .slide-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    font-size: 0.68rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    will-change: transform, opacity;
  }
  .slide-topline {
    position: relative;
    border-bottom: 1px solid currentColor;
    padding-bottom: 0.85rem;
    opacity: 0.75;
  }
  .topline-rail-line {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: currentColor;
    transform-origin: left;
    will-change: transform;
    opacity: 0.75;
  }
  .topline-left {
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }
  .slide-eyebrow { font-weight: 800; }
  .topline-tag {
    padding: 0.2rem 0.55rem;
    border: 1px solid currentColor;
    border-radius: 999px;
    font-size: 0.58rem;
    opacity: 0.75;
    letter-spacing: 0.1em;
  }
  .slide-index { font-variant-numeric: tabular-nums; opacity: 0.65; }

  .slide-content {
    display: flex;
    flex-direction: column;
    gap: clamp(1.8rem, 4vh, 3.2rem);
    flex: 1;
    justify-content: center;
    padding: clamp(1rem, 2vh, 2rem) 0;
  }
  .slide-main-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.4fr) minmax(260px, 0.6fr);
    align-items: center;
    gap: clamp(2rem, 6vw, 6.5rem);
  }
  .slide-main { min-width: 0; }
  .slide-copy { max-width: 780px; }
  .slide-copy h2 {
    margin: 0.6rem 0 1rem;
    max-width: 820px;
    font-size: clamp(2.2rem, 4.8vw, 4.6rem);
    line-height: 0.98;
    letter-spacing: -0.05em;
    font-weight: 800;
    will-change: transform, opacity;
  }
  .kinetic-title {
    margin: 0.6rem 0 1rem;
    max-width: 820px;
    font-size: clamp(2.2rem, 4.8vw, 4.6rem);
    line-height: 0.98;
    letter-spacing: -0.05em;
    font-weight: 800;
  }
  .kinetic-line-mask {
    display: block;
    overflow: hidden;
    padding-bottom: 0.08em;
  }
  .kinetic-line {
    display: block;
    will-change: transform;
    color: inherit;
  }
  .kinetic-line.line-highlight {
    color: #f8f6ed;
  }
  .slide-lead {
    max-width: 660px;
    font-size: clamp(0.98rem, 1.4vw, 1.25rem);
    line-height: 1.45;
    opacity: 0.8;
    will-change: transform, opacity;
  }

  /* =========================================================================
     SLIDE 2: Ruptura Editorial (Mero Comércio vs. Cuidado Clínico)
     ========================================================================= */
  .editorial-duo {
    display: grid;
    grid-template-columns: 0.85fr 1.15fr;
    gap: 1.25rem;
    margin-top: 1.2rem;
  }
  .duo-side {
    padding: 1.35rem 1.4rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.08);
    position: relative;
    will-change: transform, opacity;
  }
  .duo-negated {
    opacity: 0.75;
    background: rgba(0, 0, 0, 0.08);
    border-color: rgba(255, 255, 255, 0.3);
  }
  .duo-tag {
    position: relative;
    display: inline-block;
    margin-bottom: 0.6rem;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .strike-bar {
    position: absolute;
    left: -4px;
    right: -4px;
    top: 50%;
    height: 2px;
    background: #b94d39;
    transform: rotate(-3deg);
  }
  .duo-negated p {
    margin: 0;
    font-size: 0.9rem;
    line-height: 1.45;
    opacity: 0.65;
  }
  .duo-clinical {
    background: rgba(255, 255, 255, 0.14);
    border-color: #d7a95c;
  }
  .clinical-head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #d7a95c;
    margin-bottom: 0.85rem;
  }
  .clinical-beacon {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #d7a95c;
    box-shadow: 0 0 0 4px rgba(215, 169, 92, 0.25);
  }
  .clinical-pillars {
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }
  .pillar-row {
    position: relative;
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
  }
  .pillar-row:last-child { border-bottom: none; padding-bottom: 0; }
  .pillar-idx {
    font-size: 0.7rem;
    font-weight: 800;
    opacity: 0.5;
    font-family: monospace;
    will-change: transform;
    transform-origin: center;
  }
  .pillar-body {
    flex: 1;
    will-change: transform;
  }
  .pillar-divider-line {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: rgba(255, 255, 255, 0.12);
    transform-origin: left;
    will-change: transform;
  }
  .pillar-row h4 { margin: 0 0 0.15rem; font-size: 0.92rem; font-weight: 700; }
  .pillar-row small { font-size: 0.82rem; opacity: 0.75; line-height: 1.35; display: block; }

  /* =========================================================================
     SLIDE 3: Matriz de 4 Modalidades
     ========================================================================= */
  .modalities-net {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.85rem;
    margin-top: 1rem;
    position: relative;
  }
  .mod-station {
    padding: 1.25rem 1.15rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.55);
    min-height: 145px;
    position: relative;
    will-change: transform, opacity;
  }
  .station-meta {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }
  .station-code {
    font-size: 0.75rem;
    font-weight: 800;
    opacity: 0.55;
    font-family: monospace;
    will-change: transform;
    transform-origin: center;
  }
  .station-line {
    flex: 1;
    height: 1px;
    background: currentColor;
    opacity: 0.2;
    transform-origin: left;
    will-change: transform;
  }
  .station-body {
    will-change: transform;
  }
  .mod-station h3 { margin: 0 0 0.4rem; font-size: 1.05rem; line-height: 1.15; }
  .mod-station p { margin: 0; font-size: 0.86rem; line-height: 1.45; opacity: 0.72; }

  /* =========================================================================
     SLIDE 4: Arcabouço Legal
     ========================================================================= */
  .legal-framework { margin-top: 1rem; display: flex; flex-direction: column; gap: 1rem; }
  .laws-duo { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .law-plaque {
    display: flex;
    gap: 1rem;
    padding: 1.25rem 1.4rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.55);
    will-change: transform, opacity;
  }
  .law-symbol { font-size: 1.8rem; font-weight: 800; line-height: 1; opacity: 0.35; }
  .law-plaque h3 { margin: 0 0 0.35rem; font-size: 1.05rem; }
  .law-plaque p { margin: 0; font-size: 0.88rem; line-height: 1.45; opacity: 0.72; }
  .solemn-warning {
    display: flex;
    gap: 1.2rem;
    align-items: baseline;
    padding: 1rem 1.3rem;
    border-left: 4px solid #b94d39;
    background: rgba(185, 77, 57, 0.08);
    color: #713126;
    will-change: transform, opacity;
  }
  .warning-anchor {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    white-space: nowrap;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: #b94d39;
  }
  .anchor-bullet { width: 6px; height: 6px; border-radius: 50%; background: #b94d39; }
  .solemn-warning p { margin: 0; font-size: 0.92rem; line-height: 1.45; }

  /* =========================================================================
     SLIDE 5: Segurança e LGPD
     ========================================================================= */
  .security-cluster {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }
  .sec-card {
    padding: 1.35rem 1.4rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.55);
    will-change: transform, opacity;
  }
  .sec-badge-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  .sec-code {
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    padding: 0.2rem 0.5rem;
    background: rgba(13, 91, 62, 0.1);
    color: #0d5b3e;
    border-radius: 4px;
  }
  .sec-pip { width: 5px; height: 5px; border-radius: 50%; background: #d7a95c; }
  .sec-card h3 { margin: 0 0 0.35rem; font-size: 1.08rem; }
  .sec-card p { margin: 0; font-size: 0.88rem; line-height: 1.45; opacity: 0.72; }

  /* =========================================================================
     SLIDE 6: Jornada Clínica Contínua
     ========================================================================= */
  .journey-track {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.85rem;
    position: relative;
    margin-top: 1.2rem;
  }
  .track-spine {
    position: absolute;
    top: 2rem;
    left: 8%;
    right: 8%;
    height: 1px;
    background: currentColor;
    opacity: 0.25;
  }
  .track-station {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
    align-items: flex-start;
    text-align: left;
    border: 0;
    padding: 0;
    background: none;
    box-shadow: none;
    color: inherit;
    cursor: pointer;
    will-change: transform, opacity;
  }
  .station-node {
    display: grid;
    place-items: center;
    width: 3.8rem;
    height: 3.8rem;
    border: 1px solid currentColor;
    border-radius: 50%;
    background: #f2f1e9;
    color: #0d5b3e;
    font-weight: 800;
    font-size: 1.05rem;
    transition: all 0.2s ease;
  }
  .journey-active .station-node {
    background: #0d5b3e;
    color: #f8f6ed;
    box-shadow: 0 0 0 6px rgba(13, 91, 62, 0.12);
  }
  .station-text strong { display: block; font-size: 0.98rem; }
  .station-text small { display: block; margin-top: 0.3rem; font-size: 0.82rem; line-height: 1.35; opacity: 0.7; }

  /* =========================================================================
     SLIDE 7: Prática Clínica
     ========================================================================= */
  .practice-stream {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin-top: 1rem;
  }
  .practice-card {
    display: flex;
    align-items: baseline;
    gap: 1.2rem;
    padding: 1.1rem 1.35rem;
    border-left: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.55);
    will-change: transform, opacity;
  }
  .practice-code { font-size: 0.8rem; font-weight: 800; opacity: 0.55; font-family: monospace; }
  .practice-right h3 { margin: 0 0 0.25rem; font-size: 1.05rem; }
  .practice-right p { margin: 0; font-size: 0.88rem; line-height: 1.45; opacity: 0.72; }

  /* =========================================================================
     SLIDE 8: Escopo e Comparativo de Balança
     ========================================================================= */
  .scope-comparison { margin-top: 1rem; }
  .scope-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 0.85rem;
  }
  .scope-prompt { font-size: 0.75rem; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.65; }
  .scope-tabs { display: flex; border: 1px solid currentColor; padding: 0.2rem; border-radius: 999px; }
  .scope-tabs button {
    border: 0;
    border-radius: 999px;
    padding: 0.45rem 0.85rem;
    background: transparent;
    color: inherit;
    font: inherit;
    font-size: 0.74rem;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  .scope-tabs button.chosen { background: #0d5b3e; color: #f8f6ed; }
  .scope-panes { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
  .scope-pane {
    padding: 1.4rem;
    border-top: 2px solid currentColor;
    background: rgba(255, 255, 255, 0.55);
    min-height: 165px;
    transition: opacity 0.25s ease;
    will-change: transform, opacity;
  }
  .scope-pane.dimmed { opacity: 0.35 !important; }
  .pane-badge { font-size: 0.68rem; font-weight: 800; letter-spacing: 0.12em; display: block; margin-bottom: 0.45rem; }
  .alert-color { color: #a44332; }
  .pane-med { border-color: #b94d39; }
  .scope-pane h3 { margin: 0 0 0.35rem; font-size: 1.1rem; }
  .scope-pane p { margin: 0; font-size: 0.88rem; line-height: 1.45; opacity: 0.72; }

  /* =========================================================================
     SLIDE 9: Red Flags
     ========================================================================= */
  .red-flag-cluster {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }
  .alert-entry {
    padding: 1.35rem 1.4rem;
    border-top: 2px solid #b94d39;
    background: rgba(255, 255, 255, 0.65);
    position: relative;
    will-change: transform, opacity;
  }
  .alert-mark {
    display: grid;
    place-items: center;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #b94d39;
    color: #fff;
    font-weight: 800;
    font-size: 0.75rem;
    margin-bottom: 0.6rem;
  }
  .alert-entry h3 { margin: 0 0 0.35rem; font-size: 1.05rem; color: #713126; }
  .alert-entry p { margin: 0; font-size: 0.88rem; line-height: 1.45; opacity: 0.75; }

  /* =========================================================================
     SLIDE 10: Tríptico de Encerramento
     ========================================================================= */
  .closing-triptych {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1rem;
  }
  .triptych-column {
    padding: 1.4rem 1.4rem;
    border-top: 2px solid #d7a95c;
    background: rgba(255, 255, 255, 0.08);
    display: flex;
    flex-direction: column;
    will-change: transform, opacity;
  }
  .triptych-idx { font-size: 0.75rem; font-weight: 800; color: #d7a95c; font-family: monospace; margin-bottom: 0.4rem; }
  .triptych-column h3 { margin: 0 0 0.45rem; font-size: 1.15rem; line-height: 1.15; }
  .triptych-column p { margin: 0; font-size: 0.9rem; line-height: 1.5; opacity: 0.75; }

  /* =========================================================================
     ILUSTRAÇÃO LATERAL (Camada Art)
     ========================================================================= */
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
  .art-compass {
    position: absolute;
    bottom: 15%;
    left: 12%;
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
  .official-brand img { width: 175px; height: 130px; object-fit: contain; }
  .official-brand strong { font-size: 2.2rem; line-height: 0.8; letter-spacing: 0.08em; }
  .official-brand span {
    font-size: 0.58rem;
    line-height: 1.15;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.72;
  }
  .art-caption {
    position: absolute;
    bottom: 22%;
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
    box-shadow: 16px 16px 0 rgba(13, 91, 62, 0.12);
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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    background: linear-gradient(135deg, #dfe9df, #f7f6ef);
  }
  .art-avatar {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background: #0d5b3e;
    box-shadow: 0 0 0 10px rgba(13, 91, 62, 0.12);
  }
  .clinical-waves {
    display: flex;
    gap: 4px;
    align-items: flex-end;
    height: 16px;
  }
  .clinical-waves span {
    width: 3px;
    height: 12px;
    background: #0d5b3e;
    border-radius: 999px;
    opacity: 0.5;
    animation: waveBob 1.2s ease-in-out infinite alternate;
  }
  .clinical-waves span:nth-child(2) { height: 16px; animation-delay: 0.2s; opacity: 0.8; }
  .clinical-waves span:nth-child(3) { height: 8px; animation-delay: 0.4s; }
  .clinical-waves span:nth-child(4) { height: 14px; animation-delay: 0.6s; opacity: 0.6; }
  @keyframes waveBob { to { transform: scaleY(0.4); } }
  .window-footer { justify-content: space-between; color: #0d5b3e; }

  /* Balança de Decisão Analítica */
  .art-scale {
    position: relative;
    width: 270px;
    height: 220px;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .scale-post {
    position: absolute;
    width: 8px;
    height: 175px;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    background: currentColor;
    opacity: 0.6;
  }
  .scale-beam {
    position: absolute;
    width: 220px;
    height: 4px;
    top: 55px;
    left: 25px;
    background: currentColor;
    transform: rotate(-7deg);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .scale-pan {
    position: absolute;
    top: 85px;
    border: 1px solid currentColor;
    padding: 1.1rem 0.8rem;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    background: rgba(255, 255, 255, 0.3);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  }
  .pan-left { left: 12px; transform: rotate(-7deg); }
  .pan-right { right: 12px; transform: rotate(7deg); }
  .scale-fulcrum {
    position: absolute;
    top: 47px;
    left: 50%;
    transform: translateX(-50%);
    width: 20px;
    height: 20px;
    border: 2px solid currentColor;
    border-radius: 50%;
    background: #d7a95c;
  }
  .art-scale.tilt-right .scale-beam { transform: rotate(7deg); }
  .art-scale.tilt-right .pan-left { transform: translateY(18px) rotate(-7deg); }
  .art-scale.tilt-right .pan-right { transform: translateY(-18px) rotate(7deg); }

  /* Radar de Emergência */
  .art-emergency-radar {
    position: relative;
    width: 220px;
    height: 220px;
    display: grid;
    place-items: center;
  }
  .radar-circle {
    position: absolute;
    border: 1px solid #b94d39;
    border-radius: 50%;
    opacity: 0.35;
  }
  .ring-outer { width: 210px; height: 210px; border-style: dashed; }
  .ring-mid { width: 140px; height: 140px; }
  .radar-pulse-core {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #b94d39;
    box-shadow: 0 0 0 12px rgba(185, 77, 57, 0.2);
  }
  .radar-label {
    position: absolute;
    bottom: -15px;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: #b94d39;
    text-align: center;
  }

  /* Aurora Solar do Encerramento */
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
  .sun-core {
    position: absolute;
    inset: 34%;
    background: #d7a95c;
    border-radius: 50%;
    opacity: 0.5;
  }
  .sun-orbit {
    position: absolute;
    inset: -20px;
    border: 1px solid #d7a95c;
    border-radius: 50%;
    opacity: 0.3;
  }
  .art-sun span { position: relative; z-index: 1; }
  .art-sun strong { font-size: 1.25rem; }

  /* Rodapé */
  .slide-footer {
    border-top: 1px solid currentColor;
    padding-top: 0.85rem;
    opacity: 0.6;
  }
  .footer-left { display: flex; align-items: center; gap: 0.6rem; }
  .footer-pipe { opacity: 0.4; }
  .footer-spec { opacity: 0.75; font-size: 0.62rem; }
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
  .slide-footer button:hover { transform: none; box-shadow: none; opacity: 0.85; }

  /* =========================================================================
     MOBILE (Fluxo Vertical Limpo e Responsivo)
     ========================================================================= */
  @media (max-width: 900px) {
    .stage-backgrounds { display: none !important; }
    .slides-wrap { position: relative; inset: auto; pointer-events: auto; display: block; }
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

    .slide.theme-green {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.15), transparent 32%), #0d5b3e !important;
    }
    .slide.theme-light {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.7), transparent 32%), linear-gradient(135deg, rgba(255,255,255,0.42), transparent 55%), #f2f1e9 !important;
    }
    .slide.theme-red {
      background: radial-gradient(circle at 88% 18%, rgba(255,255,255,0.6), transparent 32%), #f6eeea !important;
    }

    .slide-deco { display: none !important; }
    .slide-frame { min-height: calc(100svh - 6.5rem); gap: 1.4rem; }
    .slide-content { justify-content: flex-start; gap: 1.6rem; padding: 1.2rem 0; }
    .slide-main-grid { grid-template-columns: 1fr; gap: 1.8rem; }
    .slide-art { min-height: 170px; order: -1; }
    .slide-art::before { inset: 5% 22%; }
    .art-number { font-size: 7rem; }
    .official-brand { transform: scale(0.8) rotate(-4deg); }
    .art-scale { transform: scale(0.75); }
    .slide-copy h2 { font-size: clamp(2rem, 8.5vw, 3.2rem); }
    .slide-lead { font-size: 1rem; }

    .editorial-duo { grid-template-columns: 1fr; gap: 1rem; }
    .modalities-net { grid-template-columns: 1fr; gap: 0.85rem; }
    .laws-duo { grid-template-columns: 1fr; gap: 0.85rem; }
    .security-cluster { grid-template-columns: 1fr; gap: 0.85rem; }
    .journey-track { grid-template-columns: 1fr; gap: 1rem; }
    .track-spine { display: none; }
    .track-station { flex-direction: row; align-items: flex-start; width: 100%; }
    .track-station small { margin-top: 0.25rem; }
    .scope-panes { grid-template-columns: 1fr; gap: 0.85rem; }
    .red-flag-cluster { grid-template-columns: 1fr; gap: 0.85rem; }
    .closing-triptych { grid-template-columns: 1fr; gap: 0.85rem; }

    .slide-footer { font-size: 0.6rem; }
    .footer-spec { display: none; }
  }

  @media (prefers-reduced-motion: reduce) {
    .slide-topline, .slide-copy h2, .slide-lead, .slide-art, .slide-footer, .slide-deco,
    .duo-side, .mod-station, .law-plaque, .solemn-warning, .sec-card, .track-station,
    .practice-card, .scope-pane, .alert-entry, .triptych-column {
      transform: none !important;
      transition: none !important;
    }
  }
</style>

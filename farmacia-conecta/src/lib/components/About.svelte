<script>
  import { onMount } from 'svelte';
  import Slides from './Slides.svelte';

  let scrollTrackRef = $state(null);
  let lottieContainer = $state(null);
  let anim = null;
  let isLoading = $state(true);
  let hasError = $state(false);

  // Progresso do scroll com interpolação suave (lerp)
  let targetScrollRatio = $state(0);
  let currentScrollRatio = $state(0);
  let activePhase = $derived(Math.min(9, Math.floor(currentScrollRatio * 10)));
  
  // ===== SAÍDA INDIVIDUAL DO SLIDE 1 =====
  // Cada grupo sai para sua própria direção de forma coordenada, terminando antes do Slide 2.
  const EXIT_START = 0.05;
  const EXIT_END = 0.096;
  const clamp01 = (x) => Math.max(0, Math.min(1, x));
  let exitG = $derived(Math.max(0, Math.min(1, (currentScrollRatio - EXIT_START) / (EXIT_END - EXIT_START))));
  
  let liqProgress = $derived(clamp01((currentScrollRatio - 0.03) / 0.06));
  let waveHeight = $derived(Math.sin(liqProgress * Math.PI) * 45);
  let waveY = $derived(100 - liqProgress * 100);

  let transitionProgress = $derived.by(() => {
    if (currentScrollRatio <= 0.32 || currentScrollRatio >= 0.52) return 0;
    return Math.sin(((currentScrollRatio - 0.32) / 0.20) * Math.PI);
  });

  function scrollToPhase(phaseIndex) {
    if (!scrollTrackRef) return;
    const rect = scrollTrackRef.getBoundingClientRect();
    const maxScroll = scrollTrackRef.scrollHeight - window.innerHeight;
    const targetY = window.scrollY + rect.top + (phaseIndex / 10) * maxScroll + 5; 
    window.scrollTo({ top: targetY, behavior: 'smooth' });
  }

  // Mapeamento linear do scroll para a timeline do Lottie (Slide 1):
  // 0.00 a 0.04: Entrada suave completa de todos os elementos (frame 0 a 270) copiada do Lottie
  // 0.04 a 0.05: Pausa / leitura com slide 1 totalmente montado e estático (frame 270)
  // 0.05 a 0.096: Saída individual, sincronizada e elegante de cada grupo (frame 270 a 360)
  // >= 0.096: Slide 1 100% invisível (opacidade 0), pronto para o Slide 2 entrar no ratio 0.10
  function mapScrollToFrame(s) {
    if (s < 0.04) {
      const t = s / 0.04;
      return t * 270;
    } else if (s <= 0.05) {
      return 270;
    } else if (s <= 0.096) {
      const t = (s - 0.05) / (0.096 - 0.05);
      return 270 + (t * (360 - 270));
    } else {
      return 400;
    }
  }

  let currentFrame = $derived(mapScrollToFrame(currentScrollRatio));

  import LiquidCanvas from './LiquidCanvas.svelte';

  function adaptAnimationData(orig, targetW, targetH) {
    const data = JSON.parse(JSON.stringify(orig));
    data.w = targetW;
    data.h = targetH;
    data.op = 450;

    // Garante que todas as camadas de precomposição em assets também fiquem ativas até o frame 450!
    if (data.assets) {
      data.assets.forEach((asset) => {
        if (asset.layers) {
          asset.layers.forEach((l) => {
            l.op = 450;
          });
        }
      });
    }

    const layers = {};
    data.layers.forEach((l) => {
      layers[l.ind] = l;
      l.op = 450;
    });

    // Base scale is 0.38 for 1920x880 (compact & elegant layout).
    const scaleH = targetH / 880;
    const scaleW = targetW / 1920;
    let scale = 0.38 * Math.min(scaleW, scaleH);
    scale = Math.max(0.24, Math.min(0.38, scale));
    const scaleVec = [scale * 100, scale * 100];

    const marginX = 40;
    const marginY = 35;
    const marginBot = 45;

    // Apply scale to layers
    [842, 756, 4, 13, 434, 435, 304, 668].forEach((ind) => {
      if (layers[ind] && layers[ind].ks && layers[ind].ks.s) {
        if (layers[ind].ks.s.a === 0) {
          layers[ind].ks.s = { a: 0, k: scaleVec };
        }
      }
    });

    // Helper to set static position without breaking keyframes
    const setPos = (ind, x, y) => {
      if (!layers[ind]) return;
      if (!layers[ind].ks) layers[ind].ks = {};
      layers[ind].ks.p = { a: 0, k: [x, y] };
    };

    // 1. Cabeçalho Superior: Centro Universitário UNIGRANDE (esquerda) e Curso de Bacharelado em Farmácia (direita)
    // 434 é o container de todo o cabeçalho superior
    setPos(434, marginX, marginY);

    if (layers[543]) {
      layers[543].parent = 434;
      setPos(543, 0, 0);
    }

    // Alinha o texto do curso ("Curso de Bacharelado em Farmácia") exatamente na margem direita
    const courseTargetRight = (targetW - marginX - marginX) / scale;
    const shiftCourse = courseTargetRight - 4843;
    [595, 590, 567, 562, 545].forEach(ind => {
      if (layers[ind] && layers[ind].ks && layers[ind].ks.p && layers[ind].ks.p.a === 0) {
        const origX = orig.layers.find(x => x.ind === ind)?.ks?.p?.k?.[0] || layers[ind].ks.p.k[0];
        layers[ind].ks.p = { a: 0, k: [origX + shiftCourse, 0] };
      }
    });

    // 3. Bottom-Left: Disciplina & Professor (304, 435)
    const lineSpacing = 32 * (scale / 0.38);
    setPos(304, marginX, targetH - marginBot);
    setPos(435, marginX, targetH - marginBot - lineSpacing);

    // 4. Bottom-Right: Buriticupu (668)
    const buriWidth = 219.056 * scale;
    setPos(668, targetW - marginX - buriWidth, targetH - marginBot);

    // 5. Hide old Lottie title glyph layers completely (rendered in prominent HTML capslock)
    const titleLayers = [842, 843, 883, 909, 943, 977, 978, 1012, 1034, 1082, 1083, 1119, 1155, 1177, 1221];
    titleLayers.forEach(ind => {
      if (layers[ind]) {
        layers[ind].hd = true;
        if (layers[ind].ks) {
          if (layers[ind].ks.o) layers[ind].ks.o = { a: 0, k: 0 };
          if (layers[ind].ks.s) layers[ind].ks.s = { a: 0, k: [0, 0] };
        }
      }
    });

    // 6. Seminário (756) & Logo (4) - Centered group at targetW / 2
    const semW = 485 * scale;
    const logoW = 921 * scale;
    const gap = 160 * scale;
    const totalW = semW + gap + logoW;
    const groupStart = targetW / 2 - totalW / 2;
    const semEndX = groupStart;
    const logoEndX = semEndX + semW + gap;
    const semAloneX = targetW / 2 - semW / 2;
    const logoDelta = 100 * scale;
    const logoStartX = logoEndX - logoDelta;

    // Baixa a posição da logo, data e seminário conforme solicitado
    const midY = Math.round(targetH * 0.49);
    const logoYOffset = 46 * (scale / 0.38);

    if (layers[756]) {
      layers[756].ks.p = {
        a: 1,
        k: [
          { t: 0, s: [semAloneX, midY], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 193.122, s: [semAloneX, midY], i: { x: [0, 1], y: [1, 1] }, o: { x: [0.5, 0], y: [0, 0] } },
          { t: 241.122, s: [semEndX, midY], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 270, s: [semEndX, midY], h: 1 }
        ]
      };
    }

    if (layers[4]) {
      layers[4].ks.p = {
        a: 1,
        k: [
          { t: 0, s: [logoStartX, midY + logoYOffset], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 208.02, s: [logoStartX, midY + logoYOffset], i: { x: [0, 1], y: [1, 1] }, o: { x: [0.5, 0], y: [0, 0] } },
          { t: 256.02, s: [logoEndX, midY + logoYOffset], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 270, s: [logoEndX, midY + logoYOffset], h: 1 }
        ]
      };
    }

    // 7. Integrantes (13) - Right Lateral
    const intWidth = 638 * scale;
    const intHeight = 244 * scale;
    const intY = targetH - marginBot - intHeight - (20 * (scale / 0.38));
    if (layers[13]) setPos(13, targetW - marginX - intWidth, intY);

    // ===== SAÍDAS COORDENADAS POR GRUPO (Sem quebrar palavras/letras) =====
    const easeI2D = { x: [0.35, 0.35], y: [1, 1] };
    const easeO2D = { x: [0.35, 0.35], y: [0, 0] };
    const easeI1D = { x: [0.35], y: [1] };
    const easeO1D = { x: [0.35], y: [0] };

    const addGroupExit = (ind, delay, dx, dy, scaleMult) => {
      const l = layers[ind];
      if (!l) return;
      if (!l.ks) l.ks = {};
      const tStart = 270 + delay;
      const tEnd = 360;

      // Movimento de saída do grupo
      if (!l.ks.p) l.ks.p = { a: 0, k: [0, 0] };
      if (l.ks.p.a === 0) {
        const p0 = l.ks.p.k;
        l.ks.p = {
          a: 1,
          k: [
            { t: 0, s: p0, h: 1 },
            { t: tStart, s: p0, i: easeI2D, o: easeO2D },
            { t: tEnd, s: [p0[0] + dx, p0[1] + dy], h: 1 }
          ]
        };
      } else {
        const pk = l.ks.p.k;
        const lastKf = pk[pk.length - 1];
        const p0 = lastKf.s;
        delete lastKf.h;
        lastKf.i = easeI2D;
        lastKf.o = easeO2D;
        pk.push({ t: tStart, s: p0, i: easeI2D, o: easeO2D });
        pk.push({ t: tEnd, s: [p0[0] + dx, p0[1] + dy], h: 1 });
      }

      // Redução de escala suave no final
      if (!l.ks.s) l.ks.s = { a: 0, k: [100, 100] };
      if (l.ks.s.a === 0) {
        const s0 = l.ks.s.k;
        l.ks.s = {
          a: 1,
          k: [
            { t: 0, s: s0, h: 1 },
            { t: tStart, s: s0, i: easeI2D, o: easeO2D },
            { t: tEnd, s: [s0[0] * scaleMult, s0[1] * scaleMult], h: 1 }
          ]
        };
      }
    };

    // Trajetórias distintas para cada seção:
    const partDist = targetW * 0.28;
    addGroupExit(756, 6, -partDist, 0, 0.5);                  // Seminário: Desliza para esquerda
    addGroupExit(4, 6, partDist, 0, 0.5);                     // Logo: Desliza para direita na MESMA velocidade, distância e proporção
    addGroupExit(13, 6, targetW * 0.25, 0, 0.5);             // Integrantes: Desliza para direita
    addGroupExit(434, 4, 0, -targetH * 0.35, 0.5);            // Cabeçalho Superior: Sobe reto
    addGroupExit(304, 4, -targetW * 0.20, targetH * 0.20, 0.5);  // Disciplina (Inf. Esq.): Sai na diagonal inf. esq.
    addGroupExit(435, 4, -targetW * 0.20, targetH * 0.20, 0.5);  // Professor (Inf. Esq.): Sai na diagonal inf. esq.
    addGroupExit(668, 4, targetW * 0.20, targetH * 0.20, 0.5);   // Buriticupu (Inf. Dir.): Sai na diagonal inf. dir.

    // ===== TRANSIÇÃO DE OPACIDADE EM 100% DOS ELEMENTOS VISUAIS =====
    // Garante que absolutamente NADA fique estático ou visível ao passar para o Slide 2
    const fadeOutLayer = (l, delay = 0) => {
      if (l.ind === 2 || l.ind === 3) return;
      l.op = 450;
      if (!l.ks) l.ks = {};
      const tStart = 270 + delay;
      const tEnd = 360;

      if (!l.ks.o) {
        l.ks.o = { a: 0, k: 100 };
      }

      if (l.ks.o.a === 0) {
        let op0 = 100;
        if (Array.isArray(l.ks.o.k)) {
          op0 = l.ks.o.k[0] !== undefined ? l.ks.o.k[0] : 100;
        } else if (typeof l.ks.o.k === 'number') {
          op0 = l.ks.o.k;
        }
        l.ks.o = {
          a: 1,
          k: [
            { t: 0, s: [op0], h: 1 },
            { t: tStart, s: [op0], i: easeI1D, o: easeO1D },
            { t: tEnd, s: [0], h: 1 }
          ]
        };
      } else if (l.ks.o.a === 1 && Array.isArray(l.ks.o.k)) {
        const kfs = l.ks.o.k;
        const lastKf = kfs[kfs.length - 1];
        let op0 = 100;
        if (lastKf && lastKf.s) {
          op0 = Array.isArray(lastKf.s) ? lastKf.s[0] : lastKf.s;
        }
        if (lastKf) {
          delete lastKf.h;
          lastKf.i = easeI1D;
          lastKf.o = easeO1D;
        }
        kfs.push({ t: tStart, s: [op0], i: easeI1D, o: easeO1D });
        kfs.push({ t: tEnd, s: [0], h: 1 });
      }
    };

    // Aplica fade-out a todas as camadas do arquivo raiz
    data.layers.forEach(l => fadeOutLayer(l, (l.ind % 6) * 2));
    
    // Aplica fade-out a todas as camadas de pré-composições internas (assets)
    if (data.assets) {
      data.assets.forEach(a => {
        if (a.layers) {
          a.layers.forEach(al => fadeOutLayer(al, (al.ind % 6) * 2));
        }
      });
    }

    return data;
  }

  onMount(() => {
    let isCancelled = false;
    let rafId = null;
    let resizeTimer = null;
    let lottieModuleRef = null;
    let rawAnimationData = null;
    let lastW = 0;
    let lastH = 0;

    function renderLottie() {
      if (isCancelled || !lottieContainer || !lottieModuleRef || !rawAnimationData) return;

      const w = lottieContainer.clientWidth || window.innerWidth;
      const h = lottieContainer.clientHeight || window.innerHeight;
      lastW = w;
      lastH = h;

      const adaptedData = adaptAnimationData(rawAnimationData, w, h);

      if (anim) {
        anim.destroy();
        anim = null;
      }

      const lottie = lottieModuleRef.default || lottieModuleRef;

      anim = lottie.loadAnimation({
        container: lottieContainer,
        renderer: 'svg',
        loop: false,
        autoplay: false,
        animationData: adaptedData,
        rendererSettings: {
          preserveAspectRatio: 'none',
          progressiveLoad: true,
          hideOnTransparent: true
        }
      });

      const handleReady = () => {
        if (!isCancelled) {
          isLoading = false;
          if (anim) {
            const frame = mapScrollToFrame(currentScrollRatio || targetScrollRatio);
            anim.goToAndStop(frame, true);
          }
        }
      };

      if (anim.isLoaded) {
        handleReady();
      }

      anim.addEventListener('DOMLoaded', handleReady);
      anim.addEventListener('data_ready', handleReady);
      anim.addEventListener('firstFrame', handleReady);
      setTimeout(handleReady, 300);
    }

    async function loadLottie() {
      try {
        const [lottieMod, jsonResponse] = await Promise.all([
          import('lottie-web'),
          fetch('/16-10.json?v=' + Date.now())
        ]);

        if (isCancelled || !lottieContainer) return;

        if (!jsonResponse.ok) {
          throw new Error('Falha ao carregar arquivo de animação');
        }

        lottieModuleRef = lottieMod;
        rawAnimationData = await jsonResponse.json();

        renderLottie();
      } catch (err) {
        console.error('Erro ao carregar animação Lottie:', err);
        if (!isCancelled) {
          isLoading = false;
          hasError = true;
        }
      }
    }

    loadLottie();

    const handleScroll = () => {
      if (!scrollTrackRef) return;
      const rect = scrollTrackRef.getBoundingClientRect();
      const maxScroll = rect.height - window.innerHeight;
      if (maxScroll <= 0) return;

      const scrolled = -rect.top;
      targetScrollRatio = Math.max(0, Math.min(1, scrolled / maxScroll));
    };

    const handleResize = () => {
      handleScroll();
      if (!lottieContainer || !rawAnimationData) return;
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        const newW = lottieContainer.clientWidth || window.innerWidth;
        const newH = lottieContainer.clientHeight || window.innerHeight;
        if (Math.abs(newW - lastW) > 15 || Math.abs(newH - lastH) > 15) {
          renderLottie();
        }
      }, 200);
    };

    let lastRenderedFrame = -1;
    const tick = () => {
      const diff = targetScrollRatio - currentScrollRatio;
      if (Math.abs(diff) > 0.00005) {
        currentScrollRatio += diff * 0.18;
      } else {
        currentScrollRatio = targetScrollRatio;
      }

      if (anim && !isLoading) {
        const frame = mapScrollToFrame(currentScrollRatio);
        if (Math.abs(frame - lastRenderedFrame) > 0.04) {
          lastRenderedFrame = frame;
          anim.goToAndStop(frame, true);
        }
      }

      rafId = requestAnimationFrame(tick);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleResize, { passive: true });
    handleScroll();
    rafId = requestAnimationFrame(tick);

    return () => {
      isCancelled = true;
      clearTimeout(resizeTimer);
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
      if (rafId) cancelAnimationFrame(rafId);
      if (anim) {
        anim.destroy();
        anim = null;
      }
    };
  });
</script>

<!-- Trilha com 350vh para navegação fluida por scroll -->
<section id="sobre" class="scroll-showcase-section" bind:this={scrollTrackRef}>
  
  <!-- Viewport fixo preenchendo 100% da tela do monitor de ponta a ponta -->
  <div class="sticky-viewport">

    <!-- Palco Principal: Animação original do JSON em tela cheia verde -->
    <div class="stage-container">
      {#if isLoading}
        <div class="loading-state">
          <div class="spinner"></div>
          <p>Preparando apresentação...</p>
        </div>
      {/if}

      {#if hasError}
        <div class="error-state">
          <p>Não foi possível carregar a apresentação.</p>
        </div>
      {/if}

      
      <!-- ENFEITES DO SLIDE 1 (flat, lúdicos) — cada um com entrada, flutuação e saída própria -->
      <div class="s1-ornaments" style="opacity: {currentScrollRatio >= 0.096 ? 0 : 1};
          --exit-g: {exitG}; pointer-events: none;">
        <div class="orn glow glow-1" style="transform: translate(-50%, -50%) scale({1 + exitG * 0.9}); opacity: {1 - exitG};"></div>
        <div class="orn glow glow-2" style="transform: translate(30%, 30%) scale({1 - exitG * 0.6}); opacity: {1 - exitG};"></div>

        <!-- Anel tracejado: gira e foge pelo canto superior -->
        <div class="orn orn-ring" style="transform: translate({exitG * 140}px, {-exitG * 180}px) rotate({exitG * 240}deg) scale({1 - exitG * 0.7}); opacity: {1 - clamp01(exitG * 1.3)};">
          <svg class="float-a" width="120" height="120" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="1">
            <circle cx="50" cy="50" r="40" stroke-dasharray="4 6" />
            <circle cx="50" cy="50" r="20" />
            <circle cx="90" cy="50" r="3" fill="white" />
          </svg>
        </div>

        <!-- Losango duplo: rola para fora pela esquerda -->
        <div class="orn orn-diamond" style="transform: translate({-exitG * 220}px, {exitG * 140}px) rotate({-exitG * 135}deg); opacity: {1 - clamp01(exitG * 1.5)};">
          <svg class="float-b" width="150" height="150" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="1">
            <rect x="20" y="20" width="60" height="60" transform="rotate(45 50 50)" />
            <rect x="35" y="35" width="30" height="30" transform="rotate(45 50 50)" />
          </svg>
        </div>

        <!-- Cruz (farmácia): encolhe girando -->
        <div class="orn orn-plus" style="transform: rotate({exitG * 180}deg) scale({1 - clamp01(exitG * 1.2)});">
          <svg class="float-c" width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round"><path d="M12 4v16M4 12h16" /></svg>
        </div>

        <!-- Trio de pontos: espalha -->
        <div class="orn orn-dots">
          {#each [0, 1, 2] as i}
            <span class="dot-pill" style="transform: translate({(i - 1) * exitG * 90}px, {-exitG * (60 + i * 40)}px) scale({1 - exitG}); animation-delay: {i * 0.25}s;"></span>
          {/each}
        </div>

        <!-- Arco: desenrola (stroke) -->
        <svg class="orn orn-arc" width="220" height="120" viewBox="0 0 220 120" fill="none" stroke="white" stroke-width="1.2" stroke-linecap="round">
          <path d="M10 110 A100 100 0 0 1 210 110" pathLength="1" stroke-dasharray="1" stroke-dashoffset={exitG} />
        </svg>

        <!-- Cápsula flat -->
        <div class="orn orn-capsule" style="transform: translate({exitG * 60}px, {exitG * 260}px) rotate({-35 + exitG * 70}deg); opacity: {1 - clamp01(exitG * 1.4)};">
          <span class="float-d"></span>
        </div>
      </div>

      <div 
        class="lottie-wrapper"
        style="
          position: absolute; top: 0; left: 0; width: 100%; height: 100%;
          opacity: {currentScrollRatio >= 0.096 ? 0 : 1};
          --exit-g: {exitG};
          pointer-events: {currentScrollRatio < 0.096 ? 'auto' : 'none'};
        "
      >
        <div 
          bind:this={lottieContainer}  
          class="lottie-fullscreen"
          class:is-ready={!isLoading && !hasError}
        ></div>
      </div>
      
      <!-- Título Slide 1 (Capslock com Entrada e Saída Copiada do Lottie) -->
      <div 
        class="slide1-hero-title-box"
        style="
          opacity: {currentFrame < 25 ? 0 : 1 - clamp01(exitG * 1.35)};
          transform: translate(-50%, {-exitG * 80}px);
          display: {currentScrollRatio >= 0.096 ? 'none' : 'block'};
        "
      >
        <h1 class="slide1-hero-title">
          <span class="w" class:show={currentFrame >= 30}>TELEFARMÁCIA</span>{' '}
          <span class="w" class:show={currentFrame >= 34}>E</span>{' '}
          <span class="w" class:show={currentFrame >= 37}>SERVIÇOS</span>{' '}
          <span class="w" class:show={currentFrame >= 41}>DIGITAIS</span>{' '}
          <span class="w" class:show={currentFrame >= 45}>FARMACÊUTICOS:</span><br>
          <span class="slide1-hero-sub">
            <span class="w" class:show={currentFrame >= 48}>O</span>{' '}
            <span class="w" class:show={currentFrame >= 52}>CUIDADO</span>{' '}
            <span class="w" class:show={currentFrame >= 56}>CLÍNICO</span>{' '}
            <span class="w" class:show={currentFrame >= 59}>MEDIADO</span>{' '}
            <span class="w" class:show={currentFrame >= 63}>POR</span>{' '}
            <span class="w" class:show={currentFrame >= 67}>TECNOLOGIA</span>
          </span>
        </h1>
      </div>

      <!-- Simulação Líquida em Canvas 2D (Estilo enchendo tanque) -->
      <LiquidCanvas progress={liqProgress} />

      <!-- Slides 2-10 rendered absolutely over the stage -->
      <Slides {activePhase} currentRatio={currentScrollRatio} {scrollToPhase} />
    </div>

  </div>
</section>

<!-- Slides component now inside stage-container -->

<style>
  /* Esconde a barra de rolagem vertical da página (corrimão) mantendo o scroll fluido */
  :global(html), :global(body) {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
  }
  :global(::-webkit-scrollbar) {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
  }

  /* Trilha de rolagem estendida */
  .scroll-showcase-section {
    position: relative;
    height: 1200vh; /* 250vh por slide (10 slides) */
    background: #0d8d4b;
    margin: 0;
    padding: 0;
  }

  /* Viewport fixo cobrindo 100% da tela do monitor de ponta a ponta */
  .sticky-viewport {
    position: sticky;
    top: 0;
    left: 0;
    
    width: 100%;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    background: #0d8d4b;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0;
    box-sizing: border-box;
    z-index: 1001; /* Fica acima da navbar durante a apresentação */
  }

  /* Palco Principal */
  .stage-container {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    box-sizing: border-box;
    overflow: hidden;
  }

  .lottie-fullscreen {
    position: relative;
    z-index: 1;
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  /* Classes do SVG estático antigo removidas para limpar código */

  .lottie-fullscreen.is-ready {
    opacity: 1;
  }

  .lottie-fullscreen :global(svg) {
    width: 100% !important;
    height: 100% !important;
    max-width: 100% !important;
    max-height: 100% !important;
    display: block !important;
  }

  

  /* Título Slide 1 em Capslock (Tamanho Reduzido e Elegante) */
  .slide1-hero-title-box {
    position: absolute;
    top: 17vh;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 920px;
    text-align: center;
    z-index: 10;
    pointer-events: none;
  }

  .slide1-hero-title {
    font-family: var(--font-sans);
    font-size: clamp(1.3rem, 2.1vw, 2.2rem);
    font-weight: 800;
    color: #ffffff;
    line-height: 1.28;
    letter-spacing: 0.01em;
    text-transform: uppercase;
    text-shadow: 0 3px 18px rgba(0, 0, 0, 0.15);
  }

  .slide1-hero-title .w {
    display: inline-block;
    opacity: 0;
    transform: translateY(12px) scale(0.92);
    transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1), transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .slide1-hero-title .w.show {
    opacity: 1;
    transform: translateY(0) scale(1);
  }

  .slide1-hero-sub {
    display: block;
    margin-top: 0.35rem;
    font-size: clamp(1.1rem, 1.75vw, 1.8rem);
    font-weight: 700;
    opacity: 0.95;
    letter-spacing: 0.015em;
  }

  /* ===== Enfeites do Slide 1 ===== */
  .s1-ornaments {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
  }
  .orn { position: absolute; will-change: transform, opacity; }
  .glow { border-radius: 50%; }
  .glow-1 {
    top: 10%; left: 20%; width: 40vw; height: 40vw;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0) 70%);
  }
  .glow-2 {
    bottom: 0; right: 10%; width: 50vw; height: 50vw;
    background: radial-gradient(circle, rgba(255,255,255,0.045) 0%, rgba(255,255,255,0) 70%);
  }
  .orn-ring { top: 14%; right: 14%; opacity: 1; }
  .orn-ring svg { opacity: 0.18; }
  .orn-diamond { bottom: 24%; left: 9%; }
  .orn-diamond svg { opacity: 0.12; }
  .orn-plus { top: 30%; left: 22%; }
  .orn-plus svg { opacity: 0.22; }
  .orn-dots { bottom: 16%; left: 42%; display: flex; gap: 14px; }
  .dot-pill {
    display: block; width: 8px; height: 8px; border-radius: 50%;
    background: rgba(255,255,255,0.28);
    animation: dotBob 2.4s ease-in-out infinite;
  }
  .orn-arc { bottom: 7%; right: 24%; opacity: 0.14; }
  .orn-capsule { top: 62%; right: 9%; }
  .float-d {
    display: block; width: 18px; height: 52px; border-radius: 999px;
    border: 1.5px solid rgba(255,255,255,0.22);
    background: linear-gradient(to bottom, rgba(255,255,255,0.14) 50%, transparent 50%);
    animation: ornIn 1.1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.6s both, floatD 7s ease-in-out 1.7s infinite;
  }
  .float-a { display: block; animation: ornIn 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s both, floatA 14s linear 1.4s infinite; }
  .float-b { display: block; animation: ornIn 1.2s cubic-bezier(0.34, 1.56, 0.64, 1) 0.4s both, floatB 9s ease-in-out 1.6s infinite; }
  .float-c { display: block; animation: ornIn 1s cubic-bezier(0.34, 1.56, 0.64, 1) 0.8s both, floatC 6s ease-in-out 1.8s infinite; }

  @keyframes ornIn {
    from { transform: scale(0) rotate(-90deg); opacity: 0; }
    to { transform: scale(1) rotate(0deg); opacity: 1; }
  }
  @keyframes floatA { to { transform: rotate(360deg); } }
  @keyframes floatB {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-14px) rotate(8deg); }
  }
  @keyframes floatC {
    0%, 100% { transform: scale(1) rotate(0deg); }
    50% { transform: scale(1.18) rotate(45deg); }
  }
  @keyframes floatD {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(12px) rotate(-10deg); }
  }
  @keyframes dotBob {
    0%, 100% { translate: 0 0; }
    50% { translate: 0 -8px; }
  }

  @media (prefers-reduced-motion: reduce) {
    .float-a, .float-b, .float-c, .float-d, .dot-pill { animation: none; }
  }

  /* Loading e Erro */
  .loading-state, .error-state {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    color: #ffffff;
    font-weight: 600;
    font-size: 0.95rem;
    z-index: 20;
  }

  .spinner {
    width: 38px;
    height: 38px;
    border: 3.5px solid rgba(255, 255, 255, 0.25);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.85s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Seção de Detalhes Subsequente */
  .about-details-section {
    padding: 6rem 0;
    background: #ffffff;
    position: relative;
    border-top: 1px solid rgba(22, 128, 58, 0.12);
    z-index: 11;
  }

  .section-header {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 3.5rem;
  }

  .section-badge {
    display: inline-block;
    color: var(--color-primary);
    font-weight: 700;
    font-size: 0.88rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
  }

  .section-title {
    font-size: clamp(2rem, 3.5vw, 2.6rem);
    font-weight: 800;
    color: var(--color-text);
    margin-bottom: 0.85rem;
    letter-spacing: -0.02em;
  }

  .section-subtitle {
    font-size: 1.05rem;
    color: var(--color-text-muted);
    line-height: 1.6;
  }

  .about-highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.75rem;
  }

  .highlight-card {
    background: var(--color-bg);
    border: 1px solid rgba(22, 128, 58, 0.18);
    border-radius: var(--radius-md);
    padding: 1.85rem 1.6rem;
    transition: all 0.25s ease;
  }

  .highlight-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
    background: #edf8f1;
  }

  .highlight-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: var(--color-white);
    color: var(--color-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow-sm);
  }

  .highlight-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: 0.5rem;
  }

  .highlight-desc {
    font-size: 0.94rem;
    color: var(--color-text-muted);
    line-height: 1.6;
  }



  @media (max-width: 820px) {
    .about-highlights {
      grid-template-columns: 1fr;
      gap: 1.25rem;
    }

    .scroll-showcase-section {
      height: 2000vh;
    }
  }







</style>

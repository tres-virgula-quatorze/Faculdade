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

  // Mapeamento por patamares:
  // 1. Título aparece (0 a 75) e repousa
  // 2. Nome Seminário, data e logo aparecem e deslizam até suas posições centrais (75 a 258) e repousam
  // 3. Integrantes e dados finais aparecem (258 a 308.4) e repousam
  function mapScrollToFrame(s) {
    if (s < 0.15) {
      // Entrada do Título
      const t = s / 0.15;
      return t * 75;
    } else if (s < 0.32) {
      // Repouso do Título
      return 75;
    } else if (s < 0.52) {
      // Entrada do Seminário, Data e deslizamento com a Logo
      const t = (s - 0.32) / 0.20;
      return 75 + t * (258 - 75);
    } else if (s < 0.70) {
      // Repouso do Seminário, Data e Logo juntos
      return 258;
    } else if (s < 0.88) {
      // Entrada dos Integrantes e dados finais
      const t = (s - 0.70) / 0.18;
      return 258 + t * (308.4 - 258);
    } else {
      // Repouso final completo
      return 308.4;
    }
  }

  function adaptAnimationData(orig, targetW, targetH) {
    const data = JSON.parse(JSON.stringify(orig));
    data.w = targetW;
    data.h = targetH;

    const layers = {};
    data.layers.forEach((l) => (layers[l.ind] = l));

    // Base scale is 0.38 for 1920x880 (compact & elegant layout).
    const scaleH = targetH / 880;
    const scaleW = targetW / 1920;
    let scale = 0.38 * Math.min(scaleW, scaleH);
    scale = Math.max(0.24, Math.min(0.38, scale));

    const scaleVec = [scale * 100, scale * 100];

    const marginX = 20;
    const marginY = 30;
    const marginBot = 45;

    // Apply scale to layers
    [842, 756, 4, 13, 434, 435, 304, 668].forEach((ind) => {
      if (layers[ind] && layers[ind].ks && layers[ind].ks.s) {
        // Keep original animation if present, just multiply scale
        if (layers[ind].ks.s.a === 0) {
          layers[ind].ks.s = { a: 0, k: scaleVec };
        }
      }
    });

    // Apply class to corner elements for CSS effects
    [434, 595, 590, 567, 562, 545, 304, 435, 668, 842].forEach(ind => {
      if (layers[ind]) {
        layers[ind].cl = "corner-element";
      }
    });

    // Helper to override position without destroying keyframes if we just want static pos
    const setPos = (ind, x, y) => {
      if (!layers[ind]) return;
      layers[ind].ks.p = { a: 0, k: [x, y] };
    };

    // 1. Top-Left: College (434)
    setPos(434, marginX, marginY);

    // 2. Top-Right: Course (543 / 544 / 595, etc.)
    const xEndIn544 = (targetW - marginX) / scale;
    const shiftCourse = xEndIn544 - 1305.66;
    setPos(595, 656.388 + shiftCourse, 0);
    setPos(590, 770.112 + shiftCourse, 0);
    setPos(567, 825.696 + shiftCourse, 0);
    setPos(562, 1063.44 + shiftCourse, 0);
    setPos(545, 1132.812 + shiftCourse, 0);

    // 3. Bottom-Left: Disciplina (435, 304)
    const lineSpacing = 32 * (scale / 0.38);
    setPos(304, marginX, targetH - marginBot);
    setPos(435, marginX, targetH - marginBot - lineSpacing);

    // 4. Bottom-Right: Buriticupu (668)
    const buriWidth = 219.056 * scale;
    setPos(668, targetW - marginX - buriWidth, targetH - marginBot);

    // 5. Title (842) - Centered at targetW / 2
    const titleX = targetW / 2 - 691.545 * scale;
    const titleY = Math.max(marginY + 20, targetH * 0.18);
    setPos(842, titleX, titleY);

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

    const midY = Math.max(titleY + 110 * scale, targetH * 0.52);
    const logoYOffset = 50 * (scale / 0.38);

    if (layers[756]) {
      layers[756].ks.p = {
        a: 1,
        k: [
          { t: 0, s: [semAloneX, midY], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 193.122, s: [semAloneX, midY], i: { x: [0, 1], y: [1, 1] }, o: { x: [0.5, 0], y: [0, 0] } },
          { t: 241.122, s: [semEndX, midY], i: { x: [1, 1], y: [1, 1] }, o: { x: [0, 0], y: [0, 0] } },
          { t: 308.4, s: [semEndX, midY], h: 1 }
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
          { t: 308.4, s: [logoEndX, midY + logoYOffset], h: 1 }
        ]
      };
    }

    // 7. Integrantes (13) - Right Lateral
    const intWidth = 638 * scale;
    const intHeight = 244 * scale;
    const intY = targetH - marginBot - intHeight - (20 * (scale / 0.38));
    if (layers[13]) layers[13].ks.p = { a: 0, k: [targetW - marginX - intWidth, intY] };

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

    const tick = () => {
      const diff = targetScrollRatio - currentScrollRatio;
      if (Math.abs(diff) > 0.0001) {
        currentScrollRatio += diff * 0.16;
        if (anim && !isLoading) {
          // Lottie is active from 0 to 0.1 (phase 0)
          const lottieRatio = Math.min(1, Math.max(0, currentScrollRatio * 10));
          const frame = mapScrollToFrame(lottieRatio);
          anim.goToAndStop(frame, true);
        }
      } else {
        currentScrollRatio = targetScrollRatio;
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

      <div 
        bind:this={lottieContainer} 
        class="lottie-fullscreen"
        class:is-ready={!isLoading && !hasError}
        style="opacity: {activePhase === 0 ? 1 : 0}; pointer-events: {activePhase === 0 ? 'auto' : 'none'}; transition: opacity 0.5s ease; --corner-blur: {transitionProgress * 6}px; --corner-opacity: {1 - (transitionProgress * 0.7)};"
      ></div>
      
      <!-- Slides 2-10 rendered absolutely over the stage -->
      <Slides {activePhase} currentRatio={currentScrollRatio} {scrollToPhase} />
    </div>

    <!-- Dica de Rolagem Inicial -->
    {#if targetScrollRatio < 0.05}
      <div class="scroll-hint">
        <div class="mouse-icon">
          <div class="mouse-wheel"></div>
        </div>
        <span>Role para baixo para animar</span>
      </div>
    {/if}

    <!-- Barra de Progresso Fina na Extremidade Inferior -->
    <div class="bottom-progress-bar">
      <div class="bottom-progress-fill" style="width: {currentScrollRatio * 100}%;"></div>
    </div>

  </div>
</section>

<!-- Slides component now inside stage-container -->

<style>
  /* Trilha de rolagem estendida */
  .scroll-showcase-section {
    position: relative;
    height: 2500vh; /* 250vh por slide (10 slides) */
    background: #0d8d4b;
    margin: 0;
    padding: 0;
  }

  /* Viewport fixo cobrindo 100% da tela do monitor de ponta a ponta */
  .sticky-viewport {
    position: sticky;
    top: 0;
    left: 0;
    width: 100vw;
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

  .lottie-fullscreen :global(.corner-element) {
    filter: blur(var(--corner-blur, 0px));
    opacity: var(--corner-opacity, 1);
    transition: filter 0.1s linear, opacity 0.1s linear;
  }

  /* Dica de Rolagem */
  .scroll-hint {
    position: absolute;
    bottom: 3.5rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.45rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    pointer-events: none;
    animation: fadeIn 0.4s ease;
    z-index: 25;
  }

  .mouse-icon {
    width: 20px;
    height: 32px;
    border: 2px solid #ffffff;
    border-radius: 12px;
    position: relative;
    display: flex;
    justify-content: center;
    padding-top: 5px;
  }

  .mouse-wheel {
    width: 3px;
    height: 7px;
    background-color: #ffffff;
    border-radius: 2px;
    animation: scrollWheel 1.6s ease infinite;
  }

  @keyframes scrollWheel {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(10px); opacity: 0; }
  }

  /* Linha de Progresso na Base */
  .bottom-progress-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: rgba(0, 0, 0, 0.25);
    z-index: 30;
  }

  .bottom-progress-fill {
    height: 100%;
    background: #ffffff;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.9);
    transition: width 0.05s linear;
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

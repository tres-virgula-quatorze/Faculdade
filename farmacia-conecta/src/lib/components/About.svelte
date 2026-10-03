<script>
  import { onMount } from 'svelte';

  let scrollTrackRef = $state(null);
  let lottieContainer = $state(null);
  let anim = null;
  let isLoading = $state(true);
  let hasError = $state(false);

  // Progresso do scroll com interpolação suave (lerp)
  let targetScrollRatio = $state(0);
  let currentScrollRatio = $state(0);
  let activeSceneIndex = $state(0);
  let progressPercent = $state(0);

  const sceneTitles = [
    "01. Abertura & Identidade",
    "02. Tema do Seminário",
    "03. Integrantes & Dados"
  ];

  // Mapeamento por patamares: cada cena tem sua animação e um momento de repouso para leitura
  function mapScrollToFrame(s) {
    if (s < 0.15) {
      // 0 a 75
      const t = s / 0.15;
      return t * 75;
    } else if (s < 0.35) {
      // Repouso na Cena 1
      return 75;
    } else if (s < 0.55) {
      // Transição 75 a 180
      const t = (s - 0.35) / 0.20;
      return 75 + t * (180 - 75);
    } else if (s < 0.75) {
      // Repouso na Cena 2
      return 180;
    } else if (s < 0.95) {
      // Transição 180 a 308.4
      const t = (s - 0.75) / 0.20;
      return 180 + t * (308.4 - 180);
    } else {
      // Repouso na Cena 3 (conclusão)
      return 308.4;
    }
  }

  onMount(() => {
    let isCancelled = false;
    let rafId = null;

    async function loadLottie() {
      try {
        const [lottieModule, jsonResponse] = await Promise.all([
          import('lottie-web'),
          fetch('/16-10.json')
        ]);

        if (isCancelled || !lottieContainer) return;

        if (!jsonResponse.ok) {
          throw new Error('Falha ao carregar arquivo de animação');
        }

        const animationData = await jsonResponse.json();
        if (isCancelled || !lottieContainer) return;

        const lottie = lottieModule.default || lottieModule;

        anim = lottie.loadAnimation({
          container: lottieContainer,
          renderer: 'svg',
          loop: false,
          autoplay: false,
          animationData: animationData,
          rendererSettings: {
            preserveAspectRatio: 'xMidYMid meet',
            progressiveLoad: true,
            hideOnTransparent: false
          }
        });

        const handleReady = () => {
          if (!isCancelled) {
            isLoading = false;
            if (anim) {
              const initialFrame = mapScrollToFrame(targetScrollRatio);
              anim.goToAndStop(initialFrame, true);
            }
          }
        };

        if (anim.isLoaded) {
          handleReady();
        }

        anim.addEventListener('DOMLoaded', handleReady);
        anim.addEventListener('data_ready', handleReady);
        anim.addEventListener('firstFrame', handleReady);

        setTimeout(handleReady, 600);

      } catch (err) {
        console.error('Erro ao carregar animação Lottie:', err);
        if (!isCancelled) {
          isLoading = false;
          hasError = true;
        }
      }
    }

    loadLottie();

    // Rastreia a posição de rolagem
    const handleScroll = () => {
      if (!scrollTrackRef) return;
      const rect = scrollTrackRef.getBoundingClientRect();
      const maxScroll = rect.height - window.innerHeight;
      if (maxScroll <= 0) return;

      const scrolled = -rect.top;
      targetScrollRatio = Math.max(0, Math.min(1, scrolled / maxScroll));
      progressPercent = Math.round(targetScrollRatio * 100);

      if (targetScrollRatio < 0.35) {
        activeSceneIndex = 0;
      } else if (targetScrollRatio < 0.75) {
        activeSceneIndex = 1;
      } else {
        activeSceneIndex = 2;
      }
    };

    // Loop com lerp suave a 60fps
    const tick = () => {
      const diff = targetScrollRatio - currentScrollRatio;
      if (Math.abs(diff) > 0.0001) {
        currentScrollRatio += diff * 0.15;
        if (anim && !isLoading) {
          const frame = mapScrollToFrame(currentScrollRatio);
          anim.goToAndStop(frame, true);
        }
      } else {
        currentScrollRatio = targetScrollRatio;
      }

      rafId = requestAnimationFrame(tick);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    handleScroll();
    rafId = requestAnimationFrame(tick);

    return () => {
      isCancelled = true;
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
      if (rafId) cancelAnimationFrame(rafId);
      if (anim) {
        anim.destroy();
        anim = null;
      }
    };
  });
</script>

<!-- Seção com trilha de rolagem estendida para navegação fluida por scroll -->
<section id="sobre" class="scroll-showcase-section" bind:this={scrollTrackRef}>
  
  <!-- Viewport fixo preenchendo 100% da tela do monitor de ponta a ponta -->
  <div class="sticky-viewport">
    
    <!-- Barra Superior Sutil (sem cobrir o conteúdo) -->
    <div class="hud-top">
      <div class="hud-badge">
        <span class="badge-dot"></span>
        <span class="badge-title">Seminário Acadêmico</span>
        <span class="badge-sub">• Role a página para avançar</span>
      </div>
      <div class="hud-progress">
        <span>{progressPercent}%</span>
      </div>
    </div>

    <!-- Palco Principal: 100% visível, nunca cortado no topo ou base -->
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
      ></div>
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

    <!-- Rodapé do Player com Marcador de Cenas Ativas e Progresso -->
    <div class="hud-bottom">
      <div class="scene-pills">
        {#each sceneTitles as title, idx}
          <div class="scene-pill" class:active={activeSceneIndex === idx}>
            <span class="scene-dot"></span>
            <span>{title}</span>
          </div>
        {/each}
      </div>

      <div class="bottom-progress-bar">
        <div class="bottom-progress-fill" style="width: {currentScrollRatio * 100}%;"></div>
      </div>
    </div>

  </div>
</section>

<!-- Continuação natural do site após a apresentação em tela cheia -->
<section class="about-details-section">
  <div class="container">
    <div class="section-header">
      <span class="section-badge">Farmácia Conecta</span>
      <h2 class="section-title">Pilares do Nosso Cuidado</h2>
      <p class="section-subtitle">
        Conheça os fundamentos que norteiam a nossa prática acadêmica e compromisso comunitário em Buriticupu - MA.
      </p>
    </div>

    <div class="about-highlights">
      <div class="highlight-card">
        <div class="highlight-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
            <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
          </svg>
        </div>
        <h4 class="highlight-title">Ensino & Prática Farmacêutica</h4>
        <p class="highlight-desc">
          Desenvolvido no âmbito do Bacharelado em Farmácia (Unigrande), unindo teoria acadêmica e atendimento clínico qualificado.
        </p>
      </div>

      <div class="highlight-card">
        <div class="highlight-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
          </svg>
        </div>
        <h4 class="highlight-title">Cuidado Centrado na Pessoa</h4>
        <p class="highlight-desc">
          Consultas humanizadas, revisão clínica de receitas, análise de interações e acompanhamento terapêutico dedicado.
        </p>
      </div>

      <div class="highlight-card">
        <div class="highlight-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="2" y1="12" x2="22" y2="12"></line>
            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
          </svg>
        </div>
        <h4 class="highlight-title">Comunidade de Buriticupu</h4>
        <p class="highlight-desc">
          Orientação acessível para a população local, promovendo a segurança, o uso racional de medicamentos e o bem-estar diário.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  /* Trilha de rolagem estendida para navegação confortável */
  .scroll-showcase-section {
    position: relative;
    height: 350vh;
    background: #0d8d4b;
    margin: 0;
    padding: 0;
  }

  /* Viewport fixo que ocupa 100% da tela do monitor de ponta a ponta */
  .sticky-viewport {
    position: sticky;
    top: 0;
    left: 0;
    width: 100vw;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    /* Fundo verde contínuo idêntico ao da apresentação */
    background: #0d8d4b;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    /* Espaçamento superior para nunca conflitar com a barra fixa do site */
    padding-top: 76px;
    padding-bottom: 50px;
    box-sizing: border-box;
    z-index: 10;
  }

  /* HUD Superior */
  .hud-top {
    position: absolute;
    top: 86px;
    left: 1.5rem;
    right: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 25;
    pointer-events: none;
  }

  .hud-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(13, 141, 75, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 0.45rem 1.1rem;
    border-radius: var(--radius-full);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
  }

  .badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.35);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
  }

  .badge-title {
    font-size: 0.86rem;
    font-weight: 700;
    color: #ffffff;
  }

  .badge-sub {
    font-size: 0.8rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.85);
  }

  .hud-progress {
    background: rgba(13, 141, 75, 0.85);
    backdrop-filter: blur(12px);
    color: #ffffff;
    font-size: 0.88rem;
    font-weight: 800;
    padding: 0.45rem 0.9rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    font-variant-numeric: tabular-nums;
  }

  /* Palco Principal */
  .stage-container {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem 1.5rem;
    box-sizing: border-box;
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
    /* meet garante preservação absoluta sem cortes */
    object-fit: contain !important;
  }

  /* Dica de Rolagem */
  .scroll-hint {
    position: absolute;
    bottom: 4.5rem;
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

  /* Rodapé do HUD */
  .hud-bottom {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 25;
    pointer-events: none;
  }

  .scene-pills {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(13, 141, 75, 0.85);
    backdrop-filter: blur(12px);
    padding: 0.4rem 0.9rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-bottom: 0.85rem;
  }

  .scene-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.65);
    padding: 0.15rem 0.5rem;
    border-radius: var(--radius-full);
    transition: all 0.2s ease;
  }

  .scene-pill.active {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.22);
  }

  .scene-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: currentColor;
  }

  /* Linha de Progresso */
  .bottom-progress-bar {
    width: 100%;
    height: 4px;
    background: rgba(0, 0, 0, 0.2);
  }

  .bottom-progress-fill {
    height: 100%;
    background: #ffffff;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
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
      height: 260vh;
    }

    .scene-pills {
      display: none;
    }

    .badge-sub {
      display: none;
    }
  }
</style>

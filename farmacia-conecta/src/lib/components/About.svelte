<script>
  import { onMount } from 'svelte';

  let scrollTrackRef = $state(null);
  let lottieContainer = $state(null);
  let anim = null;
  let isLoading = $state(true);
  let hasError = $state(false);

  // Progresso suave com interpolação
  let targetProgress = 0;
  let currentProgress = $state(0);
  let totalFrames = 308.4;

  let progressPercent = $derived(Math.round(currentProgress * 100));

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
          throw new Error('Não foi possível carregar a animação');
        }

        const animationData = await jsonResponse.json();
        if (isCancelled || !lottieContainer) return;

        const lottie = lottieModule.default || lottieModule;
        totalFrames = animationData.op || 308.4;

        anim = lottie.loadAnimation({
          container: lottieContainer,
          renderer: 'svg',
          loop: false,
          autoplay: false,
          animationData: animationData,
          rendererSettings: {
            preserveAspectRatio: 'xMidYMid slice',
            progressiveLoad: true,
            hideOnTransparent: false
          }
        });

        const markReady = () => {
          if (!isCancelled) {
            isLoading = false;
            if (anim) {
              anim.goToAndStop(0, true);
            }
          }
        };

        if (anim.isLoaded) {
          markReady();
        }

        anim.addEventListener('DOMLoaded', markReady);
        anim.addEventListener('data_ready', markReady);
        anim.addEventListener('firstFrame', markReady);

        setTimeout(markReady, 800);

      } catch (err) {
        console.error('Erro ao carregar animação Lottie:', err);
        if (!isCancelled) {
          isLoading = false;
          hasError = true;
        }
      }
    }

    loadLottie();

    // Cálculo da rolagem no scroll track
    const handleScroll = () => {
      if (!scrollTrackRef) return;
      const rect = scrollTrackRef.getBoundingClientRect();
      const maxScroll = rect.height - window.innerHeight;
      if (maxScroll <= 0) return;

      const scrolled = -rect.top;
      targetProgress = Math.max(0, Math.min(1, scrolled / maxScroll));
    };

    // Loop de interpolação contínua (lerp) para 60fps macio
    const tick = () => {
      const diff = targetProgress - currentProgress;
      if (Math.abs(diff) > 0.0002) {
        currentProgress += diff * 0.16;
        if (anim && !isLoading) {
          const frame = currentProgress * totalFrames;
          anim.goToAndStop(frame, true);
        }
      } else {
        currentProgress = targetProgress;
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

<section id="sobre" class="scroll-showcase-section" bind:this={scrollTrackRef}>
  <!-- Viewport fixo que ocupa 100% da tela do monitor de ponta a ponta -->
  <div class="sticky-viewport">
    
    <!-- Elementos Flutuantes da Interface (HUD) -->
    <div class="hud-top">
      <div class="hud-badge">
        <span class="badge-dot"></span>
        <span class="badge-title">Apresentação Institucional</span>
        <span class="badge-sub">• Role para explorar</span>
      </div>
      <div class="progress-counter">
        <span>{progressPercent}%</span>
      </div>
    </div>

    <!-- Palco Principal da Animação Fullscreen Edge-to-Edge -->
    <div class="stage-container">
      {#if isLoading}
        <div class="loading-state">
          <div class="spinner"></div>
          <p>Carregando apresentação...</p>
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

    <!-- Indicador de Rolagem na Parte Inferior -->
    {#if currentProgress < 0.08}
      <div class="scroll-hint">
        <div class="mouse-icon">
          <div class="mouse-wheel"></div>
        </div>
        <span>Role para baixo</span>
      </div>
    {/if}

    <!-- Linha de Progresso na borda inferior da tela -->
    <div class="bottom-progress-bar">
      <div class="bottom-progress-fill" style="width: {currentProgress * 100}%;"></div>
    </div>
  </div>
</section>

<!-- Seção explicativa complementar que surge naturalmente ao concluir o scroll -->
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
  /* Trilha de Rolagem para controle suave da animação */
  .scroll-showcase-section {
    position: relative;
    height: 280vh;
    background: #0d8d4b;
    margin: 0;
    padding: 0;
  }

  /* Viewport fixo na tela inteira do monitor (100vw x 100vh de ponta a ponta) */
  .sticky-viewport {
    position: sticky;
    top: 0;
    left: 0;
    width: 100vw;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    background: #0d8d4b; /* Fundo idêntico ao verde da apresentação */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
  }

  /* HUD Superior */
  .hud-top {
    position: absolute;
    top: 5.5rem; /* Abaixo do menu superior */
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
    padding: 0.5rem 1.1rem;
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
    font-size: 0.88rem;
    font-weight: 700;
    color: #ffffff;
  }

  .badge-sub {
    font-size: 0.82rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.85);
  }

  .progress-counter {
    background: rgba(13, 141, 75, 0.85);
    backdrop-filter: blur(12px);
    color: #ffffff;
    font-size: 0.88rem;
    font-weight: 800;
    padding: 0.5rem 0.9rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    font-variant-numeric: tabular-nums;
  }

  /* Palco Fullscreen Edge-to-Edge */
  .stage-container {
    width: 100vw;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    margin: 0;
    overflow: hidden;
  }

  .lottie-fullscreen {
    width: 100vw;
    width: 100%;
    height: 100vh;
    height: 100dvh;
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
    width: 100vw !important;
    width: 100% !important;
    height: 100vh !important;
    height: 100% !important;
    min-width: 100vw !important;
    min-height: 100vh !important;
    display: block !important;
    object-fit: cover !important;
  }

  /* Dica de Rolagem */
  .scroll-hint {
    position: absolute;
    bottom: 2rem;
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

  /* Linha de Progresso Inferior */
  .bottom-progress-bar {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: rgba(0, 0, 0, 0.2);
    z-index: 25;
  }

  .bottom-progress-fill {
    height: 100%;
    background: #ffffff;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    transition: width 0.05s linear;
  }

  /* Estados de Loading e Erro */
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
      height: 220vh;
    }

    .hud-top {
      top: 4.8rem;
    }

    .badge-sub {
      display: none;
    }
  }
</style>

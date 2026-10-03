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
  let isScrolling = $state(false);

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
          throw new Error('Não foi possível carregar o arquivo da animação');
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
            preserveAspectRatio: 'xMidYMid meet',
            progressiveLoad: true,
            hideOnTransparent: true
          }
        });

        const markReady = () => {
          if (!isCancelled) {
            isLoading = false;
            // Posiciona no primeiro quadro
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

        // Timeout de segurança para ocultar o spinner
        setTimeout(markReady, 1000);

      } catch (err) {
        console.error('Erro ao carregar animação Lottie:', err);
        if (!isCancelled) {
          isLoading = false;
          hasError = true;
        }
      }
    }

    loadLottie();

    // Cálculo do scroll em relação ao container de rolagem
    const handleScroll = () => {
      if (!scrollTrackRef) return;
      const rect = scrollTrackRef.getBoundingClientRect();
      const maxScroll = rect.height - window.innerHeight;
      if (maxScroll <= 0) return;

      const scrolled = -rect.top;
      targetProgress = Math.max(0, Math.min(1, scrolled / maxScroll));
      isScrolling = true;
    };

    // Loop de animação contínuo para interpolação suave (lerp)
    const tick = () => {
      // Lerp suave (fator 0.16 para resposta rápida e macia)
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
  <!-- Viewport fixo que ocupa 100% da tela do monitor -->
  <div class="sticky-viewport">
    
    <!-- Elementos Flutuantes da Interface (HUD) -->
    <div class="hud-top">
      <div class="hud-badge">
        <span class="badge-dot"></span>
        <span class="badge-title">Apresentação Interativa</span>
        <span class="badge-sub">• Role para explorar</span>
      </div>
      <div class="progress-counter">
        <span>{progressPercent}%</span>
      </div>
    </div>

    <!-- Palco Principal da Animação Fullscreen -->
    <div class="stage-container">
      {#if isLoading}
        <div class="loading-state">
          <div class="spinner"></div>
          <p>Preparando animação...</p>
        </div>
      {/if}

      {#if hasError}
        <div class="error-state">
          <p>Não foi possível carregar a animação.</p>
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
  /* Trilha de Rolagem: altura estendida para permitir rolagem suave da animação */
  .scroll-showcase-section {
    position: relative;
    height: 280vh;
    background: #ffffff;
  }

  /* Viewport fixo na tela inteira do monitor */
  .sticky-viewport {
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    background: radial-gradient(circle at 50% 50%, #f7fdf9 0%, #eef8f2 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 10;
  }

  /* HUD Superior */
  .hud-top {
    position: absolute;
    top: 1.5rem;
    left: 1.5rem;
    right: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 20;
    pointer-events: none;
  }

  .hud-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 0.5rem 1.1rem;
    border-radius: var(--radius-full);
    box-shadow: 0 4px 16px rgba(22, 128, 58, 0.1);
    border: 1px solid rgba(22, 128, 58, 0.18);
  }

  .badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(22, 128, 58, 0.25);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
  }

  .badge-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: var(--color-text);
  }

  .badge-sub {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--color-text-muted);
  }

  .progress-counter {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    color: var(--color-primary);
    font-size: 0.88rem;
    font-weight: 800;
    padding: 0.5rem 0.9rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(22, 128, 58, 0.18);
    box-shadow: 0 4px 16px rgba(22, 128, 58, 0.1);
    font-variant-numeric: tabular-nums;
  }

  /* Palco Fullscreen */
  .stage-container {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
  }

  .lottie-fullscreen {
    width: 100%;
    height: 100%;
    max-width: 100vw;
    max-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.4s ease;
  }

  .lottie-fullscreen.is-ready {
    opacity: 1;
  }

  .lottie-fullscreen :global(svg) {
    width: 100% !important;
    height: 100% !important;
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transform: translate3d(0, 0, 0);
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
    color: var(--color-text-muted);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    pointer-events: none;
    animation: fadeIn 0.4s ease;
    z-index: 20;
  }

  .mouse-icon {
    width: 20px;
    height: 32px;
    border: 2px solid var(--color-primary);
    border-radius: 12px;
    position: relative;
    display: flex;
    justify-content: center;
    padding-top: 5px;
  }

  .mouse-wheel {
    width: 3px;
    height: 7px;
    background-color: var(--color-primary);
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
    height: 4px;
    background: rgba(22, 128, 58, 0.08);
    z-index: 20;
  }

  .bottom-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
    transition: width 0.05s linear;
  }

  /* Estados de Loading e Erro */
  .loading-state, .error-state {
    position: absolute;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    color: var(--color-text-muted);
    font-weight: 600;
    font-size: 0.95rem;
  }

  .spinner {
    width: 38px;
    height: 38px;
    border: 3.5px solid rgba(22, 128, 58, 0.15);
    border-top-color: var(--color-primary);
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

    .badge-sub {
      display: none;
    }
  }
</style>

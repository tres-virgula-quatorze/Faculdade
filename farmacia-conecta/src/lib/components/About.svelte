<script>
  import { onMount } from 'svelte';

  let animContainer = $state(null);
  let anim = null;
  let isPlaying = $state(true);
  let isLoading = $state(true);
  let hasError = $state(false);
  let playbackSpeed = $state(1);
  let isFullscreen = $state(false);
  let playerWrapper = $state(null);

  onMount(() => {
    let isCancelled = false;

    // Dynamically load lottie-web to optimize initial bundle and ensure browser environment
    import('lottie-web')
      .then((lottieModule) => {
        if (isCancelled || !animContainer) return;
        const lottie = lottieModule.default || lottieModule;

        try {
          anim = lottie.loadAnimation({
            container: animContainer,
            renderer: 'svg',
            loop: true,
            autoplay: true,
            path: '/16-10.json'
          });

          anim.addEventListener('DOMLoaded', () => {
            isLoading = false;
          });

          anim.addEventListener('data_failed', () => {
            isLoading = false;
            hasError = true;
          });

          anim.addEventListener('error', () => {
            isLoading = false;
            hasError = true;
          });
        } catch (e) {
          console.error('Falha ao iniciar animação Lottie:', e);
          isLoading = false;
          hasError = true;
        }
      })
      .catch((err) => {
        console.error('Erro ao importar lottie-web:', err);
        isLoading = false;
        hasError = true;
      });

    const handleFullscreenChange = () => {
      isFullscreen = !!document.fullscreenElement;
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);

    return () => {
      isCancelled = true;
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      if (anim) {
        anim.destroy();
        anim = null;
      }
    };
  });

  function togglePlay() {
    if (!anim) return;
    if (isPlaying) {
      anim.pause();
      isPlaying = false;
    } else {
      anim.play();
      isPlaying = true;
    }
  }

  function restart() {
    if (!anim) return;
    anim.goToAndPlay(0, true);
    isPlaying = true;
  }

  function setSpeed(speed) {
    if (!anim) return;
    playbackSpeed = speed;
    anim.setSpeed(speed);
  }

  function toggleFullscreen() {
    if (!playerWrapper) return;
    if (!document.fullscreenElement) {
      playerWrapper.requestFullscreen?.().catch((err) => {
        console.warn('Fullscreen error:', err);
      });
    } else {
      document.exitFullscreen?.().catch((err) => {
        console.warn('Exit fullscreen error:', err);
      });
    }
  }
</script>

<section id="sobre" class="about-section">
  <div class="container">
    <div class="section-header">
      <span class="section-badge">Sobre o Projeto</span>
      <h2 class="section-title">Nossa História & Apresentação</h2>
      <p class="section-subtitle">
        Conheça a essência da Farmácia Conecta Buriticupu: integração do conhecimento científico com o atendimento acolhedor à comunidade.
      </p>
    </div>

    <!-- Container do Player da Animação Jitter/Lottie -->
    <div class="player-wrapper" bind:this={playerWrapper} class:is-fullscreen={isFullscreen}>
      <!-- Barra superior do mockup de mídia -->
      <div class="player-topbar">
        <div class="player-status">
          <span class="pulse-indicator"></span>
          <span class="status-label">Apresentação Institucional</span>
          <span class="format-tag">16:10 • 60 FPS</span>
        </div>

        <div class="player-controls">
          <div class="speed-selector" title="Velocidade de reprodução">
            <button 
              type="button" 
              class="speed-btn" 
              class:active={playbackSpeed === 0.75} 
              onclick={() => setSpeed(0.75)}
            >0.75x</button>
            <button 
              type="button" 
              class="speed-btn" 
              class:active={playbackSpeed === 1} 
              onclick={() => setSpeed(1)}
            >1x</button>
            <button 
              type="button" 
              class="speed-btn" 
              class:active={playbackSpeed === 1.5} 
              onclick={() => setSpeed(1.5)}
            >1.5x</button>
          </div>

          <button 
            type="button" 
            class="control-btn" 
            onclick={restart} 
            title="Reiniciar animação"
            aria-label="Reiniciar"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
              <polyline points="3 3 3 8 8 8"></polyline>
            </svg>
          </button>

          <button 
            type="button" 
            class="control-btn play-btn" 
            onclick={togglePlay} 
            title={isPlaying ? "Pausar" : "Reproduzir"}
            aria-label={isPlaying ? "Pausar" : "Reproduzir"}
          >
            {#if isPlaying}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
              </svg>
            {:else}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
            {/if}
          </button>

          <button 
            type="button" 
            class="control-btn" 
            onclick={toggleFullscreen} 
            title={isFullscreen ? "Sair da tela cheia" : "Tela cheia"}
            aria-label="Alternar tela cheia"
          >
            {#if isFullscreen}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="4 14 10 14 10 20"></polyline>
                <polyline points="20 10 14 10 14 4"></polyline>
                <line x1="14" y1="10" x2="21" y2="3"></line>
                <line x1="3" y1="21" x2="10" y2="14"></line>
              </svg>
            {:else}
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 3 21 3 21 9"></polyline>
                <polyline points="9 21 3 21 3 15"></polyline>
                <line x1="21" y1="3" x2="14" y2="10"></line>
                <line x1="3" y1="21" x2="10" y2="14"></line>
              </svg>
            {/if}
          </button>
        </div>
      </div>

      <!-- Área de Visualização da Animação -->
      <div class="animation-stage">
        {#if isLoading}
          <div class="loading-overlay">
            <div class="spinner"></div>
            <p class="loading-text">Carregando animação...</p>
            <span class="loading-subtext">Arquivo de apresentação 16:10</span>
          </div>
        {/if}

        {#if hasError}
          <div class="error-overlay">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p>Não foi possível carregar a animação.</p>
          </div>
        {/if}

        <div 
          bind:this={animContainer} 
          class="lottie-box"
          class:hidden={isLoading || hasError}
        ></div>
      </div>
    </div>

    <!-- Cards informativos complementares de "Sobre" -->
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
          Desenvolvido no âmbito do Bacharelado em Farmácia (Unigrande), integrando a prática clínica com rigor científico.
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
          Consultas farmacêuticas humanizadas, escuta qualificada e acompanhamento individualizado para o paciente e família.
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
          Incentivo constante ao uso racional e seguro de medicamentos, prevenção de interações nocivas e promoção do bem-estar.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  .about-section {
    padding: 5rem 0;
    background: #ffffff;
    position: relative;
    border-top: 1px solid rgba(22, 128, 58, 0.1);
  }

  .section-header {
    text-align: center;
    max-width: 680px;
    margin: 0 auto 3rem;
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

  /* Mockup Player */
  .player-wrapper {
    background: #0f172a;
    border-radius: var(--radius-lg);
    box-shadow: 0 20px 40px -15px rgba(22, 128, 58, 0.25), 0 0 0 1px rgba(255, 255, 255, 0.1);
    overflow: hidden;
    margin: 0 auto 3.5rem;
    max-width: 980px;
    display: flex;
    flex-direction: column;
    transition: all 0.3s ease;
  }

  .player-wrapper.is-fullscreen {
    max-width: 100%;
    border-radius: 0;
    height: 100vh;
    justify-content: space-between;
  }

  .player-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.4rem;
    background: #1e293b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .player-status {
    display: flex;
    align-items: center;
    gap: 0.65rem;
  }

  .pulse-indicator {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.3);
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
  }

  .status-label {
    color: #f8fafc;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: -0.01em;
  }

  .format-tag {
    font-size: 0.75rem;
    background: rgba(255, 255, 255, 0.1);
    color: #94a3b8;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-weight: 500;
  }

  .player-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .speed-selector {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    padding: 2px;
    margin-right: 0.25rem;
  }

  .speed-btn {
    background: transparent;
    color: #94a3b8;
    border: none;
    padding: 0.25rem 0.5rem;
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 4px;
    cursor: pointer;
    box-shadow: none;
    transition: all 0.2s ease;
  }

  .speed-btn:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.12);
    transform: none;
    box-shadow: none;
  }

  .speed-btn.active {
    background: var(--color-primary);
    color: #fff;
  }

  .control-btn {
    background: rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.12);
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    padding: 0;
    box-shadow: none;
    transition: all 0.2s ease;
  }

  .control-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: none;
  }

  .control-btn.play-btn {
    background: var(--color-primary);
    border-color: var(--color-primary);
    color: #ffffff;
    width: 36px;
    height: 36px;
  }

  .control-btn.play-btn:hover {
    background: var(--color-primary-light);
  }

  /* Área da Animação */
  .animation-stage {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: #090d16;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }

  .is-fullscreen .animation-stage {
    flex: 1;
    aspect-ratio: auto;
  }

  .lottie-box {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .lottie-box :global(svg) {
    width: 100% !important;
    height: 100% !important;
    max-height: 100%;
    object-fit: contain;
  }

  .hidden {
    opacity: 0;
    pointer-events: none;
  }

  .loading-overlay, .error-overlay {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(15, 23, 42, 0.95);
    z-index: 10;
    color: #f8fafc;
    gap: 0.6rem;
  }

  .spinner {
    width: 44px;
    height: 44px;
    border: 3.5px solid rgba(255, 255, 255, 0.15);
    border-top-color: var(--color-primary-light);
    border-radius: 50%;
    animation: spin 0.9s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .loading-text {
    font-size: 1rem;
    font-weight: 600;
  }

  .loading-subtext {
    font-size: 0.8rem;
    color: #94a3b8;
  }

  /* Cards de Destaque */
  .about-highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.75rem;
    max-width: 980px;
    margin: 0 auto;
  }

  .highlight-card {
    background: var(--color-bg);
    border: 1px solid rgba(22, 128, 58, 0.18);
    border-radius: var(--radius-md);
    padding: 1.75rem 1.5rem;
    transition: all 0.25s ease;
  }

  .highlight-card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-md);
    background: #edf8f1;
  }

  .highlight-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: var(--color-white);
    color: var(--color-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
  }

  .highlight-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: 0.5rem;
  }

  .highlight-desc {
    font-size: 0.92rem;
    color: var(--color-text-muted);
    line-height: 1.55;
  }

  @media (max-width: 820px) {
    .about-highlights {
      grid-template-columns: 1fr;
      gap: 1.25rem;
    }

    .player-topbar {
      flex-direction: column;
      align-items: stretch;
    }

    .player-controls {
      justify-content: space-between;
    }
  }
</style>

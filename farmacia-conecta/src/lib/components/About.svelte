<script>
  import { onMount } from 'svelte';

  let videoElement = $state(null);
  let playerWrapper = $state(null);
  let progressBar = $state(null);
  let sectionRef = $state(null);

  // Estados do player
  let isPlaying = $state(true);
  let currentTime = $state(0);
  let duration = $state(0);
  let playbackSpeed = $state(1);
  let isFullscreen = $state(false);
  let isScrollMode = $state(false); // Alternar entre Modo Loop e Modo Scroll Scrubbing
  let isHovered = $state(false);
  let isDraggingProgress = $state(false);

  // Efeito 3D Tilt suave
  let tiltX = $state(0);
  let tiltY = $state(0);
  let glareX = $state(50);
  let glareY = $state(50);

  // Capítulos / Cenas da animação
  const chapters = [
    { title: "Identidade & Marca", timeRatio: 0.05, desc: "Apresentação visual da Farmácia Conecta" },
    { title: "Cuidado Clínico", timeRatio: 0.50, desc: "Uso racional e orientação de receitas" },
    { title: "Buriticupu & Acolhimento", timeRatio: 0.88, desc: "Atenção humanizada à comunidade" }
  ];

  let progressPercent = $derived(
    duration > 0 ? (currentTime / duration) * 100 : 0
  );

  let activeChapterIndex = $derived.by(() => {
    if (!duration) return 0;
    const ratio = currentTime / duration;
    if (ratio < 0.35) return 0;
    if (ratio < 0.72) return 1;
    return 2;
  });

  onMount(() => {
    // Sincronização ao carregar metadados
    const handleLoadedMetadata = () => {
      if (videoElement) {
        duration = videoElement.duration || 5.14;
        if (!isScrollMode) {
          videoElement.play().catch(() => {
            // Autoplay com som bloqueado pode requerer muted
            if (videoElement) {
              videoElement.muted = true;
              videoElement.play().catch(() => {});
            }
          });
        }
      }
    };

    const handleTimeUpdate = () => {
      if (videoElement && !isDraggingProgress && !isScrollMode) {
        currentTime = videoElement.currentTime;
      }
    };

    const handleFullscreenChange = () => {
      isFullscreen = !!document.fullscreenElement;
    };

    // Scroll Scrubbing Listener (efeito Apple)
    const handleScroll = () => {
      if (!isScrollMode || !sectionRef || !videoElement || !duration) return;

      const rect = sectionRef.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      // Calcular o progresso de visibilidade da seção no viewport
      const totalScrollable = rect.height + windowHeight * 0.5;
      const currentScroll = windowHeight - rect.top;
      const progress = Math.max(0, Math.min(1, currentScroll / totalScrollable));

      const targetTime = progress * duration;
      videoElement.currentTime = targetTime;
      currentTime = targetTime;
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    document.addEventListener('fullscreenchange', handleFullscreenChange);

    if (videoElement) {
      videoElement.addEventListener('loadedmetadata', handleLoadedMetadata);
      videoElement.addEventListener('timeupdate', handleTimeUpdate);
      if (videoElement.readyState >= 1) {
        handleLoadedMetadata();
      }
    }

    return () => {
      window.removeEventListener('scroll', handleScroll);
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      if (videoElement) {
        videoElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
        videoElement.removeEventListener('timeupdate', handleTimeUpdate);
      }
    };
  });

  function togglePlay() {
    if (!videoElement) return;
    if (isScrollMode) {
      setMode(false);
      return;
    }
    if (isPlaying) {
      videoElement.pause();
      isPlaying = false;
    } else {
      videoElement.play();
      isPlaying = true;
    }
  }

  function restart() {
    if (!videoElement) return;
    videoElement.currentTime = 0;
    currentTime = 0;
    if (!isScrollMode) {
      videoElement.play();
      isPlaying = true;
    }
  }

  function setSpeed(speed) {
    if (!videoElement) return;
    playbackSpeed = speed;
    videoElement.playbackRate = speed;
  }

  function setMode(scrollMode) {
    isScrollMode = scrollMode;
    if (!videoElement) return;
    if (isScrollMode) {
      videoElement.pause();
      isPlaying = false;
    } else {
      videoElement.playbackRate = playbackSpeed;
      videoElement.play().catch(() => {});
      isPlaying = true;
    }
  }

  function seekToChapter(chapter) {
    if (!videoElement || !duration) return;
    const target = chapter.timeRatio * duration;
    videoElement.currentTime = target;
    currentTime = target;
    if (!isScrollMode && !isPlaying) {
      videoElement.play();
      isPlaying = true;
    }
  }

  function handleProgressBarClick(e) {
    if (!progressBar || !videoElement || !duration) return;
    const rect = progressBar.getBoundingClientRect();
    const clickX = e.clientX - rect.left;
    const ratio = Math.max(0, Math.min(1, clickX / rect.width));
    const newTime = ratio * duration;
    videoElement.currentTime = newTime;
    currentTime = newTime;
  }

  function handleMouseMove(e) {
    if (!playerWrapper || isFullscreen) return;
    const rect = playerWrapper.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    // Rotação sutil de -4 a 4 graus
    tiltY = ((x - centerX) / centerX) * 4;
    tiltX = -((y - centerY) / centerY) * 4;

    glareX = (x / rect.width) * 100;
    glareY = (y / rect.height) * 100;
    isHovered = true;
  }

  function handleMouseLeave() {
    tiltX = 0;
    tiltY = 0;
    isHovered = false;
  }

  function toggleFullscreen() {
    if (!playerWrapper) return;
    if (!document.fullscreenElement) {
      playerWrapper.requestFullscreen?.().catch((err) => {
        console.warn('Erro fullscreen:', err);
      });
    } else {
      document.exitFullscreen?.().catch((err) => {
        console.warn('Erro exit fullscreen:', err);
      });
    }
  }

  function formatTime(seconds) {
    if (isNaN(seconds) || seconds < 0) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  }
</script>

<section id="sobre" class="about-section" bind:this={sectionRef}>
  <div class="container">
    <div class="section-header">
      <span class="section-badge">Animação & Identidade</span>
      <h2 class="section-title">Sobre a Farmácia Conecta</h2>
      <p class="section-subtitle">
        Uma experiência audiovisual interativa com nossa proposta pedagógica, prática clínica e vínculo com Buriticupu.
      </p>

      <!-- Seletor de Modo de Interação -->
      <div class="mode-switcher-container">
        <div class="mode-switcher" role="group" aria-label="Modo de interação">
          <button 
            type="button" 
            class="mode-btn" 
            class:active={!isScrollMode} 
            onclick={() => setMode(false)}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            <span>Reprodução Fluida</span>
          </button>
          <button 
            type="button" 
            class="mode-btn" 
            class:active={isScrollMode} 
            onclick={() => setMode(true)}
            title="Avança e retrocede o vídeo conforme você rola a página"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 2v20M17 7l-5-5-5 5M17 17l-5 5-5-5"/>
            </svg>
            <span>Sincronizado ao Scroll</span>
            <span class="interactive-tag">Interativo</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Card 3D do Player WebM -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div 
      class="player-wrapper" 
      bind:this={playerWrapper} 
      class:is-fullscreen={isFullscreen}
      class:is-hovered={isHovered}
      onmousemove={handleMouseMove}
      onmouseleave={handleMouseLeave}
      style="transform: perspective(1000px) rotateX({tiltX}deg) rotateY({tiltY}deg);"
    >
      <!-- Efeito de brilho especular dinâmico com o mouse -->
      <div 
        class="glare-effect"
        style="background: radial-gradient(circle at {glareX}% {glareY}%, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0) 65%);"
      ></div>

      <!-- Barra superior de status -->
      <div class="player-topbar">
        <div class="player-status">
          <span class="pulse-indicator" class:scroll-pulse={isScrollMode}></span>
          <span class="status-label">
            {isScrollMode ? 'Modo Rolagem Ativa (Role para mover)' : 'Apresentação Institucional (WebM 60 FPS)'}
          </span>
          <span class="format-badge">3.5 MB • GPU</span>
        </div>

        <div class="player-controls">
          {#if !isScrollMode}
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
          {/if}

          <button 
            type="button" 
            class="control-btn" 
            onclick={restart} 
            title="Reiniciar animação"
            aria-label="Reiniciar"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
              <polyline points="3 3 3 8 8 8"></polyline>
            </svg>
          </button>

          {#if !isScrollMode}
            <button 
              type="button" 
              class="control-btn play-btn" 
              onclick={togglePlay} 
              title={isPlaying ? "Pausar" : "Reproduzir"}
              aria-label={isPlaying ? "Pausar" : "Reproduzir"}
            >
              {#if isPlaying}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="6" y="4" width="4" height="16"></rect>
                  <rect x="14" y="4" width="4" height="16"></rect>
                </svg>
              {:else}
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
              {/if}
            </button>
          {/if}

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

      <!-- Palco de Visualização do Vídeo WebM -->
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <div class="video-stage" onclick={togglePlay}>
        <video 
          bind:this={videoElement} 
          class="main-video"
          playsinline
          muted
          loop={!isScrollMode}
          preload="auto"
        >
          <source src="/16-10.webm" type="video/webm" />
          <source src="/16-10.mp4" type="video/mp4" />
          Seu navegador não suporta a tag de vídeo HTML5.
        </video>

        {#if isScrollMode}
          <div class="scroll-helper-badge">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5v14M19 12l-7 7-7-7"/>
            </svg>
            <span>Role para avançar o vídeo</span>
          </div>
        {/if}
      </div>

      <!-- Barra de Linha do Tempo Interativa (Scrubber) -->
      <div class="timeline-bar">
        <span class="time-display">{formatTime(currentTime)}</span>
        
        <!-- svelte-ignore a11y_click_events_have_key_events -->
        <!-- svelte-ignore a11y_no_static_element_interactions -->
        <div 
          class="progress-track" 
          bind:this={progressBar} 
          onclick={handleProgressBarClick}
          title="Clique ou arraste para navegar no vídeo"
        >
          <div 
            class="progress-fill" 
            style="width: {progressPercent}%;"
          >
            <div class="progress-handle"></div>
          </div>
        </div>

        <span class="time-display">{formatTime(duration)}</span>
      </div>

      <!-- Seletor de Cenas / Capítulos -->
      <div class="chapters-row">
        {#each chapters as ch, index}
          <button 
            type="button" 
            class="chapter-chip" 
            class:active={activeChapterIndex === index}
            onclick={() => seekToChapter(ch)}
            title={ch.desc}
          >
            <span class="chapter-dot"></span>
            <span class="chapter-title">{ch.title}</span>
          </button>
        {/each}
      </div>
    </div>

    <!-- Cards informativos complementares -->
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
    padding: 5rem 0 6rem;
    background: #ffffff;
    position: relative;
    border-top: 1px solid rgba(22, 128, 58, 0.1);
  }

  .section-header {
    text-align: center;
    max-width: 720px;
    margin: 0 auto 2.5rem;
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
    margin-bottom: 1.8rem;
  }

  /* Seletor de Modo */
  .mode-switcher-container {
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
  }

  .mode-switcher {
    display: inline-flex;
    align-items: center;
    background: #f1f5f9;
    border: 1px solid rgba(22, 128, 58, 0.2);
    border-radius: var(--radius-full);
    padding: 4px;
    gap: 4px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
  }

  .mode-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: transparent;
    color: #475569;
    border: none;
    padding: 0.55rem 1.15rem;
    font-size: 0.88rem;
    font-weight: 600;
    border-radius: var(--radius-full);
    cursor: pointer;
    box-shadow: none;
    transition: all 0.25s ease;
  }

  .mode-btn:hover {
    color: var(--color-primary);
    background: rgba(255, 255, 255, 0.6);
    transform: none;
    box-shadow: none;
  }

  .mode-btn.active {
    background: var(--color-primary);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(22, 128, 58, 0.3);
  }

  .interactive-tag {
    font-size: 0.72rem;
    padding: 0.1rem 0.45rem;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.25);
    font-weight: 700;
    text-transform: uppercase;
  }

  /* Player Card 3D */
  .player-wrapper {
    background: #0f172a;
    border-radius: var(--radius-lg);
    box-shadow: 0 24px 50px -15px rgba(22, 128, 58, 0.28), 0 0 0 1px rgba(255, 255, 255, 0.12);
    overflow: hidden;
    margin: 1.5rem auto 3.5rem;
    max-width: 980px;
    display: flex;
    flex-direction: column;
    position: relative;
    transition: transform 0.15s ease-out, box-shadow 0.3s ease;
    transform-style: preserve-3d;
  }

  .player-wrapper.is-hovered {
    box-shadow: 0 32px 64px -18px rgba(22, 128, 58, 0.38), 0 0 0 1px rgba(34, 197, 94, 0.3);
  }

  .player-wrapper.is-fullscreen {
    max-width: 100%;
    border-radius: 0;
    height: 100vh;
    transform: none !important;
  }

  .glare-effect {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 5;
    mix-blend-mode: overlay;
    border-radius: inherit;
    transition: background 0.05s ease;
  }

  /* Topbar */
  .player-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.85rem 1.4rem;
    background: #1e293b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    flex-wrap: wrap;
    gap: 0.75rem;
    position: relative;
    z-index: 6;
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

  .pulse-indicator.scroll-pulse {
    background: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.3);
  }

  @keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
  }

  .status-label {
    color: #f8fafc;
    font-size: 0.88rem;
    font-weight: 600;
  }

  .format-badge {
    font-size: 0.72rem;
    background: rgba(255, 255, 255, 0.1);
    color: #94a3b8;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-weight: 600;
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

  /* Palco de Vídeo */
  .video-stage {
    position: relative;
    width: 100%;
    aspect-ratio: 16 / 10;
    background: #090d16;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    overflow: hidden;
  }

  .is-fullscreen .video-stage {
    flex: 1;
    aspect-ratio: auto;
  }

  .main-video {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    background: transparent;
  }

  .scroll-helper-badge {
    position: absolute;
    bottom: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(8px);
    color: #f8fafc;
    padding: 0.5rem 1.2rem;
    border-radius: var(--radius-full);
    font-size: 0.86rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    border: 1px solid rgba(56, 189, 248, 0.4);
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    pointer-events: none;
    animation: bounce 2s infinite;
  }

  @keyframes bounce {
    0%, 100% { transform: translate(-50%, 0); }
    50% { transform: translate(-50%, -6px); }
  }

  /* Linha do Tempo (Timeline Scrubber) */
  .timeline-bar {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding: 0.75rem 1.4rem;
    background: #131d2e;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    position: relative;
    z-index: 6;
  }

  .time-display {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
    min-width: 32px;
    font-variant-numeric: tabular-nums;
  }

  .progress-track {
    flex: 1;
    height: 8px;
    background: rgba(255, 255, 255, 0.12);
    border-radius: var(--radius-full);
    position: relative;
    cursor: pointer;
    transition: height 0.15s ease;
  }

  .progress-track:hover {
    height: 10px;
  }

  .progress-fill {
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    background: linear-gradient(90deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }

  .progress-handle {
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background: #ffffff;
    box-shadow: 0 0 6px rgba(0, 0, 0, 0.4);
    margin-right: -7px;
    opacity: 0;
    transition: opacity 0.2s ease, transform 0.2s ease;
  }

  .progress-track:hover .progress-handle {
    opacity: 1;
    transform: scale(1.1);
  }

  /* Capítulos / Cenas */
  .chapters-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.65rem 1.4rem 0.9rem;
    background: #0f172a;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    overflow-x: auto;
    position: relative;
    z-index: 6;
  }

  .chapter-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(255, 255, 255, 0.05);
    color: #94a3b8;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-full);
    padding: 0.35rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 600;
    cursor: pointer;
    box-shadow: none;
    white-space: nowrap;
    transition: all 0.2s ease;
  }

  .chapter-chip:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #ffffff;
    transform: none;
    box-shadow: none;
  }

  .chapter-chip.active {
    background: rgba(22, 128, 58, 0.25);
    border-color: var(--color-primary-light);
    color: #4ade80;
  }

  .chapter-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
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

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

  // Mapeamento por patamares:
  // 1. Título aparece (0 a 75) e repousa
  // 2. Nome Seminário, data e logo aparecem (75 a 245) e repousam
  // 3. Integrantes e dados finais aparecem (245 a 308.4) e repousam
  function mapScrollToFrame(s) {
    if (s < 0.15) {
      // Entrada do Título
      const t = s / 0.15;
      return t * 75;
    } else if (s < 0.32) {
      // Repouso do Título
      return 75;
    } else if (s < 0.50) {
      // Entrada do Seminário, Data e Logo
      const t = (s - 0.32) / 0.18;
      return 75 + t * (245 - 75);
    } else if (s < 0.68) {
      // Repouso do Seminário, Data e Logo
      return 245;
    } else if (s < 0.86) {
      // Entrada dos Integrantes e dados finais
      const t = (s - 0.68) / 0.18;
      return 245 + t * (308.4 - 245);
    } else {
      // Repouso final completo
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
          fetch('/16-10.json?v=' + Date.now())
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
            hideOnTransparent: true
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

        setTimeout(handleReady, 500);

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

    const tick = () => {
      const diff = targetScrollRatio - currentScrollRatio;
      if (Math.abs(diff) > 0.0001) {
        currentScrollRatio += diff * 0.16;
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

<!-- Trilha com 350vh para navegação fluida por scroll -->
<section id="sobre" class="scroll-showcase-section" bind:this={scrollTrackRef}>
  
  <!-- Viewport fixo preenchendo 100% da tela do monitor de ponta a ponta -->
  <div class="sticky-viewport">

    <!-- Canto Superior Esquerdo: Faculdade (marcação em vermelho) -->
    <div class="corner-element top-left">
      <span class="corner-text institution-name">Centro Universitário UNIGRANDE</span>
    </div>

    <!-- Canto Superior Direito: Curso (marcação em vermelho) -->
    <div class="corner-element top-right">
      <span class="corner-text course-name">Curso de Bacharelado em Farmácia</span>
    </div>

    <!-- Canto Inferior Esquerdo: Disciplina (marcação em vermelho) -->
    <div class="corner-element bottom-left">
      <span class="corner-subtext">+ Disciplina:</span>
      <span class="corner-text discipline-name">Fundamentos da Prática Farmacêutica (Prof.ª Bianca Lira)</span>
    </div>

    <!-- Canto Inferior Direito: Buriticupu - MA (marcação em vermelho) -->
    <div class="corner-element bottom-right">
      <span class="corner-text location-name">Buriticupu - MA</span>
    </div>

    <!-- Área Direita: Nomes dos Integrantes (marcação em vermelho na etapa 3) -->
    <div class="right-integrantes-box" class:is-visible={currentScrollRatio >= 0.65}>
      <ul class="integrantes-list">
        <li class="integrante-item" style="transition-delay: 0.05s;">Yara Lima da Silva</li>
        <li class="integrante-item" style="transition-delay: 0.12s;">Ezequiel Olanda de Oliveira</li>
        <li class="integrante-item" style="transition-delay: 0.19s;">Thamyres dos Santos de Souza</li>
        <li class="integrante-item" style="transition-delay: 0.26s;">Antonio Erick Conceição da Silva</li>
      </ul>
    </div>

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

    <!-- Barra de Progresso Fina na Extremidade Inferior -->
    <div class="bottom-progress-bar">
      <div class="bottom-progress-fill" style="width: {currentScrollRatio * 100}%;"></div>
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
  /* Trilha de rolagem estendida */
  .scroll-showcase-section {
    position: relative;
    height: 350vh;
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

  /* Elementos ancorados aos 4 cantos da tela (marcações em vermelho) */
  .corner-element {
    position: absolute;
    z-index: 25;
    pointer-events: none;
    user-select: none;
  }

  .corner-element.top-left {
    top: 2rem;
    left: 2.5rem;
  }

  .corner-element.top-right {
    top: 2rem;
    right: 2.5rem;
    text-align: right;
  }

  .corner-element.bottom-left {
    bottom: 2rem;
    left: 2.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .corner-element.bottom-right {
    bottom: 2rem;
    right: 2.5rem;
    text-align: right;
  }

  .corner-text {
    font-size: 0.95rem;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.92);
    letter-spacing: 0.015em;
    line-height: 1.4;
  }

  .corner-subtext {
    font-size: 0.78rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.8);
    letter-spacing: 0.03em;
  }

  /* Bloco de Integrantes na Área Direita (marcação vermelha) */
  .right-integrantes-box {
    position: absolute;
    right: 3.5rem;
    top: 55%;
    transform: translateY(-50%);
    z-index: 25;
    pointer-events: none;
    text-align: right;
    opacity: 0;
    transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .right-integrantes-box.is-visible {
    opacity: 1;
    transform: translateY(-50%);
  }

  .integrantes-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.55rem;
  }

  .integrante-item {
    font-size: 1.05rem;
    font-weight: 500;
    color: #ffffff;
    letter-spacing: 0.01em;
    text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    opacity: 0;
    transform: translateX(18px);
    transition: opacity 0.45s ease, transform 0.45s ease;
  }

  .right-integrantes-box.is-visible .integrante-item {
    opacity: 1;
    transform: translateX(0);
  }

  @media (max-width: 900px) {
    .corner-element.top-left {
      top: 1.2rem;
      left: 1.2rem;
    }
    .corner-element.top-right {
      top: 1.2rem;
      right: 1.2rem;
    }
    .corner-element.bottom-left {
      bottom: 1.2rem;
      left: 1.2rem;
    }
    .corner-element.bottom-right {
      bottom: 1.2rem;
      right: 1.2rem;
    }
    .right-integrantes-box {
      right: 1.5rem;
      top: 72%;
    }
    .corner-text {
      font-size: 0.82rem;
    }
    .integrante-item {
      font-size: 0.9rem;
    }
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
    object-fit: contain !important;
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
      height: 280vh;
    }
  }
</style>

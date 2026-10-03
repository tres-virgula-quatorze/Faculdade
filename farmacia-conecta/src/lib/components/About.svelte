<script>
  let videoEl;
  let isPaused = $state(false);

  function togglePlay() {
    if (!videoEl) return;
    if (videoEl.paused) {
      videoEl.play().catch(() => {});
      isPaused = false;
    } else {
      videoEl.pause();
      isPaused = true;
    }
  }
</script>

<section id="sobre" class="about-section">
  <div class="container">
    <div class="section-header">
      <span class="section-badge">Sobre o Projeto</span>
      <h2 class="section-title">Conheça a Farmácia Conecta</h2>
      <p class="section-subtitle">
        Conectando o rigor da formação farmacêutica com o cuidado humanizado para toda a comunidade de Buriticupu - MA.
      </p>
    </div>

    <!-- Animação WebM nativa e integrada à página (sem modal) -->
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="video-container" onclick={togglePlay} title="Clique para pausar ou reproduzir">
      <video
        bind:this={videoEl}
        src="/16-10.webm"
        autoplay
        loop
        muted
        playsinline
        class="seamless-video"
      >
        Seu navegador não suporta o formato WebM.
      </video>

      {#if isPaused}
        <div class="pause-overlay">
          <div class="play-pill">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <polygon points="5 3 19 12 5 21 5 3"></polygon>
            </svg>
            <span>Pausado • Clique para continuar</span>
          </div>
        </div>
      {/if}
    </div>

    <!-- Destaques Institucionais -->
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
  .about-section {
    padding: 5rem 0 6rem;
    background: #ffffff;
    position: relative;
    border-top: 1px solid rgba(22, 128, 58, 0.1);
  }

  .section-header {
    text-align: center;
    max-width: 700px;
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

  /* Container da animação WebM integrada à página */
  .video-container {
    width: 100%;
    max-width: 960px;
    margin: 0 auto 3.5rem;
    border-radius: var(--radius-lg);
    overflow: hidden;
    position: relative;
    box-shadow: 0 16px 40px -12px rgba(22, 128, 58, 0.18);
    border: 1px solid rgba(22, 128, 58, 0.18);
    background: #ffffff;
    cursor: pointer;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .video-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 20px 48px -12px rgba(22, 128, 58, 0.24);
  }

  .seamless-video {
    width: 100%;
    height: auto;
    display: block;
    object-fit: contain;
    background: transparent;
  }

  .pause-overlay {
    position: absolute;
    inset: 0;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(3px);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.2s ease;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  .play-pill {
    background: var(--color-white);
    color: var(--color-primary);
    padding: 0.7rem 1.4rem;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.95rem;
    font-weight: 700;
    box-shadow: var(--shadow-lg);
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
  }
</style>

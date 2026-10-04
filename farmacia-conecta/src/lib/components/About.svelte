<script>
  import { onMount } from 'svelte';

  let scrollTrackRef = $state(null);
  let targetScrollRatio = $state(0);
  let currentScrollRatio = $state(0);
  let activeScene = $state(0); // 0, 1, 2
  let progressPercent = $state(0);

  // Calcula opacidade e translateY para transições puras e ultra-suaves a 60fps
  let scene1Opacity = $state(1);
  let scene1TranslateY = $state(0);

  let scene2Opacity = $state(0);
  let scene2TranslateY = $state(30);

  let scene3Opacity = $state(0);
  let scene3TranslateY = $state(30);

  const sceneTitles = [
    { num: "01", label: "Título & Abertura" },
    { num: "02", label: "Seminário & Logo" },
    { num: "03", label: "Integrantes & Dados" }
  ];

  function scrollToScene(idx) {
    if (!scrollTrackRef) return;
    const rect = scrollTrackRef.getBoundingClientRect();
    const scrollTop = window.scrollY || window.pageYOffset;
    const trackTop = rect.top + scrollTop;
    const maxScroll = rect.height - window.innerHeight;
    
    // Alvos de scroll: 0%, 50%, 90%
    const targetRatios = [0.05, 0.50, 0.88];
    const targetScroll = trackTop + (maxScroll * targetRatios[idx]);
    
    window.scrollTo({
      top: targetScroll,
      behavior: 'smooth'
    });
  }

  onMount(() => {
    let rafId = null;

    const handleScroll = () => {
      if (!scrollTrackRef) return;
      const rect = scrollTrackRef.getBoundingClientRect();
      const maxScroll = rect.height - window.innerHeight;
      if (maxScroll <= 0) return;

      const scrolled = -rect.top;
      targetScrollRatio = Math.max(0, Math.min(1, scrolled / maxScroll));
      progressPercent = Math.round(targetScrollRatio * 100);

      if (targetScrollRatio < 0.35) {
        activeScene = 0;
      } else if (targetScrollRatio < 0.70) {
        activeScene = 1;
      } else {
        activeScene = 2;
      }
    };

    const updateTransitions = (r) => {
      // Cena 1 (0 a 0.35)
      if (r <= 0.25) {
        scene1Opacity = 1;
        scene1TranslateY = 0;
      } else if (r < 0.38) {
        const t = (r - 0.25) / 0.13;
        scene1Opacity = Math.max(0, 1 - t);
        scene1TranslateY = -t * 40;
      } else {
        scene1Opacity = 0;
        scene1TranslateY = -40;
      }

      // Cena 2 (0.30 a 0.72)
      if (r < 0.28) {
        scene2Opacity = 0;
        scene2TranslateY = 40;
      } else if (r < 0.40) {
        const t = (r - 0.28) / 0.12;
        scene2Opacity = Math.min(1, t);
        scene2TranslateY = 40 * (1 - t);
      } else if (r <= 0.62) {
        scene2Opacity = 1;
        scene2TranslateY = 0;
      } else if (r < 0.74) {
        const t = (r - 0.62) / 0.12;
        scene2Opacity = Math.max(0, 1 - t);
        scene2TranslateY = -t * 40;
      } else {
        scene2Opacity = 0;
        scene2TranslateY = -40;
      }

      // Cena 3 (0.64 a 1.0)
      if (r < 0.64) {
        scene3Opacity = 0;
        scene3TranslateY = 40;
      } else if (r < 0.76) {
        const t = (r - 0.64) / 0.12;
        scene3Opacity = Math.min(1, t);
        scene3TranslateY = 40 * (1 - t);
      } else {
        scene3Opacity = 1;
        scene3TranslateY = 0;
      }
    };

    const tick = () => {
      const diff = targetScrollRatio - currentScrollRatio;
      if (Math.abs(diff) > 0.0002) {
        currentScrollRatio += diff * 0.15;
      } else {
        currentScrollRatio = targetScrollRatio;
      }

      updateTransitions(currentScrollRatio);
      rafId = requestAnimationFrame(tick);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll, { passive: true });
    handleScroll();
    rafId = requestAnimationFrame(tick);

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
      if (rafId) cancelAnimationFrame(rafId);
    };
  });
</script>

<!-- Trilha com 350vh para navegação fluida por scroll -->
<section id="sobre" class="scroll-showcase-section" bind:this={scrollTrackRef}>
  
  <!-- Viewport fixo preenchendo 100% da tela do monitor de ponta a ponta -->
  <div class="sticky-viewport">
    
    <!-- HUD Superior elegante com atalhos de navegação entre as 3 cenas -->
    <div class="hud-top">
      <div class="hud-badge">
        <span class="badge-dot"></span>
        <span class="badge-title">Seminário Acadêmico</span>
        <span class="badge-sub">• Role a página para avançar</span>
      </div>

      <!-- Pílulas das 3 etapas -->
      <div class="scene-nav-pills">
        {#each sceneTitles as item, idx}
          <button 
            type="button"
            class="scene-nav-btn" 
            class:active={activeScene === idx}
            onclick={() => scrollToScene(idx)}
            aria-label="Ir para {item.label}"
          >
            <span class="pill-num">{item.num}</span>
            <span class="pill-text">{item.label}</span>
          </button>
        {/each}
      </div>

      <div class="hud-progress">
        <span>{progressPercent}%</span>
      </div>
    </div>

    <!-- Palco Principal: Cada cena ocupa 100% da tela exclusiva e respirada -->
    <div class="stage-container">
      
      <!-- CENA 1: TÍTULO & ABERTURA -->
      <div 
        class="scene scene-1"
        style="opacity: {scene1Opacity}; transform: translateY({scene1TranslateY}px); pointer-events: {scene1Opacity > 0.5 ? 'auto' : 'none'};"
      >
        <div class="scene-content">
          <div class="institution-tag">
            <span class="tag-icon">🏛️</span>
            <span>Centro Universitário UNIGRANDE • Bacharelado em Farmácia</span>
          </div>

          <h1 class="main-title">
            Telefarmácia e Serviços Farmacêuticos Digitais:
            <span class="title-highlight">O Cuidado Clínico Mediado por Tecnologia</span>
          </h1>

          <div class="scroll-prompt">
            <div class="mouse-icon">
              <div class="mouse-wheel"></div>
            </div>
            <span>Role para baixo para ver a data, evento e logo ↓</span>
          </div>
        </div>

        <div class="scene-footer">
          <span>Disciplina: Fundamentos da Prática Farmacêutica</span>
          <span>Buriticupu - MA</span>
        </div>
      </div>

      <!-- CENA 2: SEMINÁRIO, DATA & LOGO UNIGRANDE -->
      <div 
        class="scene scene-2"
        style="opacity: {scene2Opacity}; transform: translateY({scene2TranslateY}px); pointer-events: {scene2Opacity > 0.5 ? 'auto' : 'none'};"
      >
        <div class="scene-content">
          <div class="date-badge">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <span>14 de Outubro de 2026</span>
          </div>

          <h2 class="event-headline">SEMINÁRIO ACADÊMICO</h2>

          <!-- Logo Oficial UNIGRANDE Nítida e em Destaque -->
          <div class="logo-showcase-box">
            <img 
              src="/unigrande-logo.png" 
              alt="Centro Universitário UNIGRANDE" 
              class="unigrande-large-logo"
            />
          </div>

          <p class="event-caption">
            Apresentação sobre a regulamentação, prática clínica e expansão do atendimento farmacêutico remoto.
          </p>

          <div class="scroll-prompt subtle">
            <span>Role para ver os integrantes ↓</span>
          </div>
        </div>

        <div class="scene-footer">
          <span>Centro Universitário UNIGRANDE</span>
          <span>Buriticupu - MA</span>
        </div>
      </div>

      <!-- CENA 3: INTEGRANTES & DADOS -->
      <div 
        class="scene scene-3"
        style="opacity: {scene3Opacity}; transform: translateY({scene3TranslateY}px); pointer-events: {scene3Opacity > 0.5 ? 'auto' : 'none'};"
      >
        <div class="scene-content">
          <div class="team-header">
            <span class="section-tag-mini">Equipe do Seminário</span>
            <h2 class="team-title">Integrantes & Apresentação</h2>
            <p class="team-subtitle">
              Acadêmicos responsáveis pela condução do estudo e apresentação da temática:
            </p>
          </div>

          <!-- Grid dos 4 Integrantes Espaçoso e Elegante -->
          <div class="team-grid">
            <div class="member-card">
              <div class="member-avatar">
                <span>YL</span>
              </div>
              <div class="member-info">
                <span class="member-role">Acadêmica de Farmácia</span>
                <h4 class="member-name">Yara Lima da Silva</h4>
              </div>
            </div>

            <div class="member-card">
              <div class="member-avatar">
                <span>EH</span>
              </div>
              <div class="member-info">
                <span class="member-role">Acadêmico de Farmácia</span>
                <h4 class="member-name">Ezequiel Holanda de Oliveira</h4>
              </div>
            </div>

            <div class="member-card">
              <div class="member-avatar">
                <span>TS</span>
              </div>
              <div class="member-info">
                <span class="member-role">Acadêmica de Farmácia</span>
                <h4 class="member-name">Thamyres dos Santos de Souza</h4>
              </div>
            </div>

            <div class="member-card">
              <div class="member-avatar">
                <span>AE</span>
              </div>
              <div class="member-info">
                <span class="member-role">Acadêmico de Farmácia</span>
                <h4 class="member-name">Antonio Erick Conceição da Silva</h4>
              </div>
            </div>
          </div>
        </div>

        <div class="scene-footer">
          <span>Curso de Bacharelado em Farmácia • UNIGRANDE</span>
          <span>Seminário 2026</span>
        </div>
      </div>

    </div>

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

  /* HUD Superior */
  .hud-top {
    position: absolute;
    top: 1.25rem;
    left: 2rem;
    right: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
    z-index: 30;
  }

  .hud-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 0.45rem 1.1rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.2);
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

  /* Navegação por Pílulas no Topo */
  .scene-nav-pills {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 0.35rem 0.5rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .scene-nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: transparent;
    border: none;
    padding: 0.35rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.75);
    border-radius: var(--radius-full);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .scene-nav-btn:hover {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.15);
  }

  .scene-nav-btn.active {
    color: #ffffff;
    background: rgba(255, 255, 255, 0.25);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .pill-num {
    font-weight: 800;
    font-size: 0.76rem;
    opacity: 0.9;
  }

  .hud-progress {
    background: rgba(0, 0, 0, 0.25);
    backdrop-filter: blur(12px);
    color: #ffffff;
    font-size: 0.88rem;
    font-weight: 800;
    padding: 0.45rem 0.95rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.2);
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
    overflow: hidden;
  }

  /* Estrutura Base de Cada Cena */
  .scene {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 6rem 3.5rem 3rem;
    box-sizing: border-box;
    transition: opacity 0.1s linear, transform 0.1s linear;
  }

  .scene-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    max-width: 1300px;
    margin: 0 auto;
    width: 100%;
  }

  .scene-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    font-size: 0.88rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    letter-spacing: 0.03em;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 1rem;
  }

  /* Estilos Cena 1 */
  .institution-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.15);
    color: #ffffff;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 0.5rem 1.3rem;
    border-radius: var(--radius-full);
    border: 1px solid rgba(255, 255, 255, 0.25);
    margin-bottom: 2rem;
    letter-spacing: 0.02em;
  }

  .main-title {
    font-size: clamp(2.4rem, 4.8vw, 4.5rem);
    font-weight: 900;
    color: #ffffff;
    line-height: 1.15;
    letter-spacing: -0.03em;
    max-width: 1150px;
    margin: 0 0 3rem;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
  }

  .title-highlight {
    display: block;
    margin-top: 0.85rem;
    color: #e2fbe8;
    font-weight: 700;
    font-size: 0.75em;
    letter-spacing: -0.01em;
  }

  .scroll-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.6rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.92rem;
    font-weight: 600;
  }

  .scroll-prompt.subtle {
    color: rgba(255, 255, 255, 0.75);
    font-size: 0.85rem;
    margin-top: 1.5rem;
  }

  .mouse-icon {
    width: 22px;
    height: 36px;
    border: 2px solid #ffffff;
    border-radius: 14px;
    position: relative;
    display: flex;
    justify-content: center;
    padding-top: 6px;
  }

  .mouse-wheel {
    width: 3.5px;
    height: 8px;
    background-color: #ffffff;
    border-radius: 2px;
    animation: scrollWheel 1.6s ease infinite;
  }

  @keyframes scrollWheel {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(12px); opacity: 0; }
  }

  /* Estilos Cena 2 */
  .date-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: #ffffff;
    color: #0d8d4b;
    font-size: 1.05rem;
    font-weight: 800;
    padding: 0.6rem 1.5rem;
    border-radius: var(--radius-full);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    margin-bottom: 1.25rem;
  }

  .event-headline {
    font-size: clamp(2.8rem, 5.5vw, 5.2rem);
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.04em;
    margin: 0 0 2rem;
    text-transform: uppercase;
    text-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
  }

  .logo-showcase-box {
    background: rgba(255, 255, 255, 0.98);
    padding: 2rem 3.5rem;
    border-radius: 24px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.5);
    margin-bottom: 2rem;
    max-width: 650px;
    width: 90%;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.3s ease;
  }

  .logo-showcase-box:hover {
    transform: scale(1.02);
  }

  .unigrande-large-logo {
    max-width: 100%;
    height: auto;
    max-height: 120px;
    object-fit: contain;
    display: block;
  }

  .event-caption {
    font-size: 1.15rem;
    color: rgba(255, 255, 255, 0.92);
    max-width: 760px;
    line-height: 1.6;
    margin: 0;
  }

  /* Estilos Cena 3 */
  .team-header {
    margin-bottom: 2.5rem;
  }

  .section-tag-mini {
    display: inline-block;
    color: #e2fbe8;
    font-weight: 800;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
  }

  .team-title {
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    font-weight: 900;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0 0 0.75rem;
  }

  .team-subtitle {
    font-size: 1.05rem;
    color: rgba(255, 255, 255, 0.85);
    max-width: 680px;
    margin: 0 auto;
    line-height: 1.5;
  }

  .team-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
    width: 100%;
    max-width: 980px;
  }

  .member-card {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 18px;
    padding: 1.35rem 1.6rem;
    text-align: left;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transition: all 0.25s ease;
  }

  .member-card:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
  }

  .member-avatar {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: #ffffff;
    color: #0d8d4b;
    font-weight: 900;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  }

  .member-info {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .member-role {
    font-size: 0.82rem;
    font-weight: 700;
    color: #e2fbe8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .member-name {
    font-size: 1.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.01em;
  }

  /* Barra de Progresso */
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
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.9);
    transition: width 0.05s linear;
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

  @media (max-width: 900px) {
    .team-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .scene-nav-pills {
      display: none;
    }

    .hud-top {
      left: 1rem;
      right: 1rem;
    }

    .scene {
      padding: 5rem 1.5rem 2rem;
    }

    .badge-sub {
      display: none;
    }

    .logo-showcase-box {
      padding: 1.5rem;
    }
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

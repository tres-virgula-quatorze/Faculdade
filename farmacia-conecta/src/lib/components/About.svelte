<script>
  import { onMount } from 'svelte';

  let sectionRef = $state(null);
  let lottieContainer = $state(null);
  let anim = null;
  let isPlaying = $state(false);
  let isLoading = $state(true);
  let hasError = $state(false);
  let currentScene = $state(1);

  // Cenas da Apresentação
  const scenes = [
    { id: 1, label: "01. Abertura", startFrame: 0, endFrame: 75, desc: "Introdução institucional" },
    { id: 2, label: "02. Tema do Seminário", startFrame: 75, endFrame: 180, desc: "Telefarmácia e Cuidado Clínico" },
    { id: 3, label: "03. Integrantes & Dados", startFrame: 180, endFrame: 308, desc: "Equipe de alunos e disciplina" }
  ];

  onMount(() => {
    let isCancelled = false;

    async function initLottie() {
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
          loop: true,
          autoplay: false,
          animationData: animationData,
          rendererSettings: {
            // meet garante que NADA seja cortado em nenhum monitor
            preserveAspectRatio: 'xMidYMid meet',
            progressiveLoad: true,
            hideOnTransparent: false
          }
        });

        const handleReady = () => {
          if (!isCancelled) {
            isLoading = false;
          }
        };

        if (anim.isLoaded) {
          handleReady();
        }

        anim.addEventListener('DOMLoaded', handleReady);
        anim.addEventListener('data_ready', handleReady);
        anim.addEventListener('firstFrame', handleReady);

        setTimeout(handleReady, 600);

        // Observer: Inicia a animação quando a seção entra na tela do usuário
        const observer = new IntersectionObserver((entries) => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              if (anim && !isPlaying) {
                anim.play();
                isPlaying = true;
              }
            } else {
              if (anim && isPlaying) {
                anim.pause();
                isPlaying = false;
              }
            }
          });
        }, { threshold: 0.25 });

        if (sectionRef) {
          observer.observe(sectionRef);
        }

        return () => {
          observer.disconnect();
        };

      } catch (err) {
        console.error('Erro ao inicializar animação:', err);
        if (!isCancelled) {
          isLoading = false;
          hasError = true;
        }
      }
    }

    initLottie();

    return () => {
      isCancelled = true;
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

  function playScene(scene) {
    if (!anim) return;
    currentScene = scene.id;
    anim.playSegments([scene.startFrame, scene.endFrame], true);
    isPlaying = true;
  }

  function playFull() {
    if (!anim) return;
    currentScene = 0;
    anim.playSegments([0, 308.4], true);
    anim.setLoop(true);
    isPlaying = true;
  }
</script>

<section id="sobre" class="about-section" bind:this={sectionRef}>
  <div class="container-full">
    
    <!-- Cabeçalho da Seção -->
    <div class="section-header">
      <span class="section-badge">Apresentação Acadêmica</span>
      <h2 class="section-title">Seminário Farmácia Conecta</h2>
      <p class="section-subtitle">
        Acompanhe a apresentação sobre Telefarmácia e Serviços Farmacêuticos Digitais, desenvolvida para o Bacharelado em Farmácia — Unigrande.
      </p>

      <!-- Navegação por Cenas (visualizar cada uma de uma vez) -->
      <div class="scenes-nav" role="group" aria-label="Navegar pelas cenas da animação">
        <button 
          type="button" 
          class="scene-btn" 
          class:active={currentScene === 0}
          onclick={playFull}
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="5 3 19 12 5 21 5 3"></polygon>
          </svg>
          <span>Apresentação Completa</span>
        </button>

        {#each scenes as sc}
          <button 
            type="button" 
            class="scene-btn" 
            class:active={currentScene === sc.id}
            onclick={() => playScene(sc)}
            title={sc.desc}
          >
            <span>{sc.label}</span>
          </button>
        {/each}
      </div>
    </div>

    <!-- Palco Principal: Não cortado, preenchendo de um lado a outro com verde contínuo -->
    <div class="presentation-stage">
      
      <!-- Fundo verde expansivo que cobre toda a largura da tela -->
      <div class="presentation-backdrop">
        
        {#if isLoading}
          <div class="stage-loading">
            <div class="spinner"></div>
            <p>Carregando apresentação...</p>
          </div>
        {/if}

        {#if hasError}
          <div class="stage-error">
            <p>Não foi possível carregar o arquivo da apresentação.</p>
          </div>
        {/if}

        <!-- Canvas do Lottie: Centralizado, 100% visível, nada cortado -->
        <div 
          bind:this={lottieContainer} 
          class="lottie-viewport"
          class:is-ready={!isLoading && !hasError}
        ></div>

        <!-- Barra flutuante de controle na base da apresentação -->
        <div class="floating-controls">
          <button 
            type="button" 
            class="ctrl-pill-btn" 
            onclick={togglePlay}
            title={isPlaying ? "Pausar" : "Reproduzir"}
          >
            {#if isPlaying}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <rect x="6" y="4" width="4" height="16"></rect>
                <rect x="14" y="4" width="4" height="16"></rect>
              </svg>
              <span>Pausar</span>
            {:else}
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                <polygon points="5 3 19 12 5 21 5 3"></polygon>
              </svg>
              <span>Reproduzir</span>
            {/if}
          </button>

          <button 
            type="button" 
            class="ctrl-pill-btn" 
            onclick={playFull}
            title="Reiniciar do começo"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
              <polyline points="3 3 3 8 8 8"></polyline>
            </svg>
            <span>Reiniciar</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Cards informativos complementares -->
    <div class="container">
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

  </div>
</section>

<style>
  .about-section {
    padding: 5rem 0 6rem;
    background: #ffffff;
    position: relative;
    border-top: 1px solid rgba(22, 128, 58, 0.12);
  }

  .container-full {
    width: 100%;
    margin: 0 auto;
  }

  .section-header {
    text-align: center;
    max-width: 740px;
    margin: 0 auto 2.5rem;
    padding: 0 1.5rem;
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

  /* Navegação pelas Cenas */
  .scenes-nav {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: #f1f8f3;
    padding: 6px;
    border-radius: var(--radius-full);
    border: 1px solid rgba(22, 128, 58, 0.2);
  }

  .scene-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: transparent;
    color: #334155;
    border: none;
    padding: 0.55rem 1.15rem;
    font-size: 0.86rem;
    font-weight: 600;
    border-radius: var(--radius-full);
    cursor: pointer;
    box-shadow: none;
    transition: all 0.2s ease;
  }

  .scene-btn:hover {
    color: var(--color-primary);
    background: rgba(255, 255, 255, 0.7);
    transform: none;
    box-shadow: none;
  }

  .scene-btn.active {
    background: var(--color-primary);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(22, 128, 58, 0.25);
  }

  /* Palco Principal da Apresentação */
  .presentation-stage {
    width: 100%;
    margin-bottom: 4.5rem;
  }

  .presentation-backdrop {
    width: 100%;
    /* O mesmo verde da apresentação preenchendo de ponta a ponta */
    background: #0d8d4b;
    position: relative;
    padding: 3rem 1.5rem 4rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 4px 16px rgba(0, 0, 0, 0.1), inset 0 -4px 16px rgba(0, 0, 0, 0.1);
  }

  .lottie-viewport {
    width: 100%;
    max-width: 960px;
    /* Aspect ratio idêntico ao canvas 1920x1713 da apresentação */
    aspect-ratio: 1920 / 1713;
    margin: 0 auto;
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .lottie-viewport.is-ready {
    opacity: 1;
  }

  .lottie-viewport :global(svg) {
    width: 100% !important;
    height: 100% !important;
    display: block !important;
    /* meet garante que 100% dos textos fiquem perfeitamente visíveis sem nenhum corte */
    object-fit: contain !important;
  }

  /* Controles Flutuantes */
  .floating-controls {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-top: 1.5rem;
    z-index: 10;
  }

  .ctrl-pill-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.95);
    color: var(--color-primary);
    border: none;
    border-radius: var(--radius-full);
    padding: 0.55rem 1.25rem;
    font-size: 0.88rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
    transition: all 0.2s ease;
  }

  .ctrl-pill-btn:hover {
    background: #ffffff;
    color: var(--color-primary-dark);
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
  }

  /* Loading e Erro */
  .stage-loading, .stage-error {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    gap: 0.75rem;
    font-weight: 600;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3.5px solid rgba(255, 255, 255, 0.25);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: spin 0.85s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  /* Cards de Destaque */
  .about-highlights {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.75rem;
    max-width: 1160px;
    margin: 0 auto;
    padding: 0 1.5rem;
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

    .scenes-nav {
      border-radius: 16px;
    }

    .presentation-backdrop {
      padding: 2rem 1rem 3rem;
    }
  }
</style>

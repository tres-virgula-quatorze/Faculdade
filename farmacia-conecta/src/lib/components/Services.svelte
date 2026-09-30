<script>
  const services = [
    {
      id: 1,
      title: "Você sabe como funciona uma consulta farmacêutica?",
      description: "Uma avaliação clínica aprofundada para revisar suas receitas, analisar possíveis interações entre remédios e elaborar um plano de cuidado sob medida.",
      badge: "Orientação Clínica",
      iconType: "consultation"
    },
    {
      id: 2,
      title: "Cuidado com seus medicamentos",
      description: "Instruções claras e seguras sobre horários, dosagens, armazenamento doméstico adequado e descarte correto para garantir a máxima eficácia do tratamento.",
      badge: "Segurança & Adesão",
      iconType: "medicine"
    },
    {
      id: 3,
      title: "Converse com a farmacêutica",
      description: "Canal aberto e humanizado para esclarecer dúvidas sobre reações adversas, mitos da automedicação e apoio contínuo para o seu bem-estar diário.",
      badge: "Acolhimento Direto",
      iconType: "chat"
    }
  ];
</script>

<section id="servicos" class="services-section">
  <div class="container">
    <div class="section-header">
      <span class="section-badge">Nossos Serviços</span>
      <h2 class="section-title">Atenção Especializada para Você</h2>
      <p class="section-subtitle">
        Conheça as principais frentes de atuação farmacêutica focadas na promoção da saúde e qualidade de vida.
      </p>
    </div>

    <div class="services-grid">
      {#each services as item}
        <article class="service-card">
          <div class="card-icon-box">
            {#if item.iconType === 'consultation'}
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
            {:else if item.iconType === 'medicine'}
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"></path>
                <path d="m8.5 8.5 7 7"></path>
              </svg>
            {:else}
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                <path d="M8 9h8"></path>
                <path d="M8 13h6"></path>
              </svg>
            {/if}
          </div>

          <span class="card-category">{item.badge}</span>
          <h3 class="card-title">{item.title}</h3>
          <p class="card-text">{item.description}</p>

          <a href="#agendamento" class="card-link">
            <span>Solicitar atendimento</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </a>
        </article>
      {/each}
    </div>
  </div>
</section>

<style>
  .services-section {
    padding: 5rem 0;
    background: linear-gradient(180deg, rgba(223, 243, 230, 0.4) 0%, rgba(223, 243, 230, 0.8) 100%);
  }

  .section-header {
    text-align: center;
    max-width: 650px;
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
    font-size: clamp(1.9rem, 3.2vw, 2.5rem);
    font-weight: 800;
    color: var(--color-text);
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
  }

  .section-subtitle {
    font-size: 1.05rem;
    color: var(--color-text-muted);
    line-height: 1.6;
  }

  .services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
    gap: 2rem;
  }

  .service-card {
    background-color: var(--color-white);
    color: var(--color-text);
    border-radius: var(--radius-lg);
    padding: 2.25rem 2rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid rgba(22, 128, 58, 0.1);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    overflow: hidden;
  }

  .service-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .service-card:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-lg);
    border-color: rgba(22, 128, 58, 0.25);
  }

  .service-card:hover::before {
    opacity: 1;
  }

  .card-icon-box {
    width: 62px;
    height: 62px;
    border-radius: var(--radius-md);
    background-color: var(--color-bg);
    color: var(--color-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease;
  }

  .service-card:hover .card-icon-box {
    transform: scale(1.08) rotate(3deg);
  }

  .card-category {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--color-primary);
    margin-bottom: 0.5rem;
  }

  .card-title {
    font-size: 1.3rem;
    font-weight: 700;
    line-height: 1.35;
    margin-bottom: 1rem;
    color: var(--color-text);
  }

  .card-text {
    font-size: 0.95rem;
    color: var(--color-text-muted);
    line-height: 1.65;
    margin-bottom: 1.75rem;
    flex-grow: 1;
  }

  .card-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 700;
    font-size: 0.92rem;
    color: var(--color-primary);
    transition: gap 0.2s ease, color 0.2s ease;
  }

  .card-link:hover {
    color: var(--color-primary-dark);
    gap: 0.75rem;
  }

  @media (max-width: 768px) {
    .services-section {
      padding: 3.5rem 0;
    }

    .services-grid {
      grid-template-columns: 1fr;
    }
  }
</style>

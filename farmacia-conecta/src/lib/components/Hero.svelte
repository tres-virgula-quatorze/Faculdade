<section id="inicio" class="hero-section">
  <div class="container hero-container">
    <div class="hero-content">
      <div class="hero-badge">
        <span class="badge-dot"></span>
        <span>Atenção Farmacêutica Integrada</span>
      </div>
      
      <h1 class="hero-title">
        Farmácia Conecta <span class="highlight">Buriticupu</span>
      </h1>
      
      <p class="hero-subtitle">
        Cuidado farmacêutico perto de você
      </p>

      <p class="hero-description">
        Promovendo a saúde e o uso racional de medicamentos através de um atendimento humanizado, 
        escuta atenta e acompanhamento clínico personalizado para toda a comunidade de Buriticupu.
      </p>

      <div class="hero-actions">
        <a href="#agendamento" class="btn btn-hero">
          <span>Agendar Consulta</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </a>
        <a href="#servicos" class="btn-secondary">
          Conhecer Serviços
        </a>
      </div>

      <div class="hero-features">
        <div class="feature-item">
          <div class="feature-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <span>Uso Racional de Medicamentos</span>
        </div>
        <div class="feature-item">
          <div class="feature-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <span>Atendimento Personalizado</span>
        </div>
      </div>
    </div>

    <div class="hero-visual">
      <div class="visual-card-wrapper">
        <div class="visual-glow"></div>
        <div class="visual-card">
          <div class="visual-icon-circle">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#16803A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>
              <path d="M12 5v14"></path>
              <path d="M5 12h14"></path>
            </svg>
          </div>
          <h3 class="visual-card-title">Cuidado que Conecta</h3>
          <p class="visual-card-text">
            Sua saúde tratada com responsabilidade técnica e o carinho que você e sua família merecem.
          </p>
          <div class="visual-card-stats">
            <div class="stat-box">
              <span class="stat-number">100%</span>
              <span class="stat-label">Gratuito & Didático</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-box">
              <span class="stat-number">Presencial</span>
              <span class="stat-label">Buriticupu - MA</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .hero-section {
    padding: 4.5rem 0 3.5rem;
    position: relative;
    overflow: hidden;
  }

  .hero-container {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 3.5rem;
    align-items: center;
  }

  .hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background-color: rgba(22, 128, 58, 0.12);
    color: var(--color-primary);
    padding: 0.4rem 1rem;
    border-radius: var(--radius-full);
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 1.25rem;
    border: 1px solid rgba(22, 128, 58, 0.2);
  }

  .badge-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(22, 128, 58, 0.2);
  }

  .hero-title {
    font-size: clamp(2.3rem, 4.5vw, 3.4rem);
    font-weight: 800;
    line-height: 1.15;
    color: var(--color-text);
    margin-bottom: 0.85rem;
    letter-spacing: -0.025em;
  }

  .highlight {
    color: var(--color-primary);
    position: relative;
    display: inline-block;
  }

  .hero-subtitle {
    font-size: clamp(1.25rem, 2.5vw, 1.6rem);
    font-weight: 600;
    color: var(--color-primary-dark);
    margin-bottom: 1.2rem;
    letter-spacing: -0.01em;
  }

  .hero-description {
    font-size: 1.05rem;
    color: var(--color-text-muted);
    max-width: 560px;
    margin-bottom: 2rem;
    line-height: 1.7;
  }

  .hero-actions {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
  }

  .btn-hero {
    padding: 0.95rem 2.2rem;
    font-size: 1.05rem;
  }

  .btn-secondary {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.95rem 1.8rem;
    border-radius: var(--radius-full);
    background-color: var(--color-white);
    color: var(--color-text);
    font-weight: 600;
    font-size: 1.05rem;
    border: 1.5px solid rgba(22, 128, 58, 0.2);
    transition: all 0.25s ease;
  }

  .btn-secondary:hover {
    background-color: #f7fdf9;
    border-color: var(--color-primary);
    color: var(--color-primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
  }

  .hero-features {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(22, 128, 58, 0.15);
  }

  .feature-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--color-text);
  }

  .feature-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background-color: var(--color-white);
    color: var(--color-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-sm);
  }

  .hero-visual {
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .visual-card-wrapper {
    position: relative;
    width: 100%;
    max-width: 400px;
  }

  .visual-glow {
    position: absolute;
    inset: -15px;
    background: radial-gradient(circle, rgba(22, 128, 58, 0.25) 0%, rgba(223, 243, 230, 0) 70%);
    filter: blur(20px);
    z-index: 1;
    border-radius: 30px;
  }

  .visual-card {
    position: relative;
    z-index: 2;
    background: var(--color-white);
    border-radius: var(--radius-lg);
    padding: 2.5rem 2rem;
    box-shadow: var(--shadow-lg);
    border: 1px solid rgba(22, 128, 58, 0.12);
    text-align: center;
  }

  .visual-icon-circle {
    width: 84px;
    height: 84px;
    margin: 0 auto 1.5rem;
    background: var(--color-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 2px 6px rgba(22, 128, 58, 0.15);
  }

  .visual-card-title {
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: 0.6rem;
  }

  .visual-card-text {
    font-size: 0.95rem;
    color: var(--color-text-muted);
    line-height: 1.6;
    margin-bottom: 1.75rem;
  }

  .visual-card-stats {
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding-top: 1.25rem;
    border-top: 1px solid rgba(0, 0, 0, 0.06);
  }

  .stat-box {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stat-number {
    font-size: 1.2rem;
    font-weight: 800;
    color: var(--color-primary);
  }

  .stat-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--color-text-muted);
  }

  .stat-divider {
    width: 1px;
    height: 32px;
    background: rgba(0, 0, 0, 0.08);
  }

  @media (max-width: 920px) {
    .hero-container {
      grid-template-columns: 1fr;
      text-align: left;
      gap: 2.5rem;
    }

    .hero-visual {
      order: 2;
    }
  }

  @media (max-width: 580px) {
    .hero-section {
      padding: 3rem 0 2rem;
    }

    .hero-actions {
      flex-direction: column;
      align-items: stretch;
    }

    .btn-hero, .btn-secondary {
      width: 100%;
    }
  }
</style>

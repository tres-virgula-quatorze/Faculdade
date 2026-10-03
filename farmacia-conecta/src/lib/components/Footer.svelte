<footer class="footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <div class="brand-row">
          <img 
            src="/logo.png" 
            alt="Farmácia Conecta" 
            class="footer-logo" 
            onerror={(e) => { e.currentTarget.style.display = 'none'; }} 
          />
          <span class="footer-brand-title">Farmácia Conecta</span>
        </div>
        <p class="footer-tagline">
          Conectando a ciência farmacêutica ao cuidado humano em Buriticupu.
        </p>
      </div>

      <div class="footer-academic">
        <h3 class="footer-section-title">Sobre o Projeto</h3>
        <p class="academic-text">
          <strong>Trabalho acadêmico</strong> desenvolvido para a disciplina de 
          <em>Fundamentos da Prática Farmacêutica</em>.
        </p>
        <p class="academic-institution">
          <strong>Instituição:</strong> Curso de Bacharelado em Farmácia — Unigrande
        </p>
        <p class="academic-location">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
          <strong>Localização:</strong> Buriticupu, MA
        </p>
      </div>

      <div class="footer-nav">
        <h3 class="footer-section-title">Navegação Rápida</h3>
        <ul class="footer-links">
          <li><a href="#inicio">Início</a></li>
          <li><a href="#servicos">Serviços Farmacêuticos</a></li>
          <li><a href="#agendamento">Agendar Atendimento</a></li>
          <li><a href="#sobre">Sobre a Disciplina</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <p class="copyright">
        © {new Date().getFullYear()} Farmácia Conecta Buriticupu. Projeto Acadêmico de Extensão e Prática Farmacêutica.
      </p>
      <p class="academic-note">
        Desenvolvido para fins didáticos e científicos.
      </p>
    </div>
  </div>
</footer>

<style>
  .footer {
    background-color: #1a252c;
    color: #e0e6ed;
    padding: 4.5rem 0 2rem;
    margin-top: auto;
    border-top: 4px solid var(--color-primary);
  }

  .footer-top {
    display: grid;
    grid-template-columns: 1.2fr 1.5fr 1fr;
    gap: 3rem;
    padding-bottom: 3rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .brand-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  .footer-logo {
    height: 40px;
    width: auto;
    border-radius: var(--radius-sm);
    background: #fff;
    padding: 2px;
  }

  .footer-brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--color-white);
    letter-spacing: -0.01em;
  }

  .footer-tagline {
    font-size: 0.92rem;
    color: #94a3b8;
    line-height: 1.6;
    max-width: 320px;
  }

  .footer-section-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--color-white);
    margin-bottom: 1.2rem;
    position: relative;
    padding-bottom: 0.4rem;
  }

  .footer-section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 28px;
    height: 2px;
    background-color: var(--color-primary);
    border-radius: 2px;
  }

  .academic-text {
    font-size: 0.95rem;
    color: #cbd5e1;
    line-height: 1.6;
    margin-bottom: 0.75rem;
  }

  .academic-institution, .academic-location {
    font-size: 0.92rem;
    color: #94a3b8;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
  }

  .academic-location svg {
    color: var(--color-primary-light);
    flex-shrink: 0;
  }

  .academic-institution strong, .academic-location strong {
    color: #e2e8f0;
  }

  .footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
  }

  .footer-links a {
    color: #94a3b8;
    font-size: 0.92rem;
    transition: all 0.2s ease;
    display: inline-block;
  }

  .footer-links a:hover {
    color: var(--color-primary-light);
    transform: translateX(4px);
  }

  .footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    padding-top: 2rem;
    font-size: 0.84rem;
    color: #64748b;
  }

  .copyright {
    color: #94a3b8;
  }

  .academic-note {
    font-weight: 500;
  }

  @media (max-width: 900px) {
    .footer-top {
      grid-template-columns: 1fr;
      gap: 2.5rem;
    }

    .footer-bottom {
      flex-direction: column;
      align-items: flex-start;
    }
  }
</style>

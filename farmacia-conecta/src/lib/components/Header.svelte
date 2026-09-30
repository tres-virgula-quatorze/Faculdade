<script>
  let menuOpen = $state(false);

  function toggleMenu() {
    menuOpen = !menuOpen;
  }

  function closeMenu() {
    menuOpen = false;
  }
</script>

<header class="header">
  <div class="container header-container">
    <a href="#inicio" class="brand" onclick={closeMenu}>
      <img 
        src="/logo.png" 
        alt="Logo Farmácia Conecta" 
        class="brand-logo" 
        onerror={(e) => { e.currentTarget.style.display = 'none'; }} 
      />
      <span class="brand-text">Farmácia Conecta</span>
    </a>

    <button 
      class="mobile-toggle" 
      aria-label="Abrir menu de navegação" 
      aria-expanded={menuOpen}
      onclick={toggleMenu}
    >
      <svg class="menu-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        {#if menuOpen}
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        {:else}
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        {/if}
      </svg>
    </button>

    <nav class="nav-links {menuOpen ? 'is-open' : ''}">
      <a href="#inicio" class="nav-link" onclick={closeMenu}>Início</a>
      <a href="#servicos" class="nav-link" onclick={closeMenu}>Serviços</a>
      <a href="#agendamento" class="nav-link" onclick={closeMenu}>Agendamento</a>
      <a href="#sobre" class="nav-link" onclick={closeMenu}>Sobre</a>
      <a href="#agendamento" class="btn btn-header-cta" onclick={closeMenu}>
        <span>Agendar</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="5" y1="12" x2="19" y2="12"></line>
          <polyline points="12 5 19 12 12 19"></polyline>
        </svg>
      </a>
    </nav>
  </div>
</header>

<style>
  .header {
    position: sticky;
    top: 0;
    left: 0;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--color-border);
    box-shadow: 0 4px 16px rgba(22, 128, 58, 0.05);
    z-index: 1000;
  }

  .header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 72px;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    text-decoration: none;
  }

  .brand-logo {
    height: 42px;
    width: auto;
    object-fit: contain;
    border-radius: var(--radius-sm);
  }

  .brand-text {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--color-primary);
    letter-spacing: -0.02em;
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 1.75rem;
  }

  .nav-link {
    font-size: 0.98rem;
    font-weight: 600;
    color: var(--color-text);
    transition: color 0.2s ease;
    position: relative;
    padding: 0.25rem 0;
  }

  .nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background-color: var(--color-primary);
    transition: width 0.2s ease;
    border-radius: 2px;
  }

  .nav-link:hover {
    color: var(--color-primary);
  }

  .nav-link:hover::after {
    width: 100%;
  }

  .btn-header-cta {
    padding: 0.55rem 1.25rem;
    font-size: 0.9rem;
  }

  .mobile-toggle {
    display: none;
    background: transparent;
    border: none;
    box-shadow: none;
    color: var(--color-primary);
    padding: 0.5rem;
    cursor: pointer;
  }

  .mobile-toggle:hover {
    background: transparent;
    transform: none;
    box-shadow: none;
  }

  .menu-icon {
    width: 28px;
    height: 28px;
  }

  @media (max-width: 820px) {
    .mobile-toggle {
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .nav-links {
      position: absolute;
      top: 72px;
      left: 0;
      right: 0;
      background: var(--color-white);
      flex-direction: column;
      align-items: stretch;
      padding: 1.5rem;
      gap: 1.25rem;
      box-shadow: var(--shadow-lg);
      border-bottom: 1px solid var(--color-border);
      display: none;
    }

    .nav-links.is-open {
      display: flex;
    }

    .nav-link {
      padding: 0.5rem 0;
      font-size: 1.05rem;
    }

    .btn-header-cta {
      margin-top: 0.5rem;
      text-align: center;
      justify-content: center;
    }
  }
</style>

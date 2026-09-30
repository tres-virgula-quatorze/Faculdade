<script>
  let name = $state('');
  let email = $state('');
  let phone = $state('');
  let reason = $state('');
  let date = $state('');
  
  let errors = $state({});
  let successMessage = $state('');

  function validate() {
    const newErrors = {};
    if (!name.trim()) {
      newErrors.name = 'Por favor, informe seu nome completo.';
    }
    if (!email.trim() || !email.includes('@')) {
      newErrors.email = 'Informe um endereço de e-mail válido.';
    }
    if (!phone.trim() || phone.replace(/\D/g, '').length < 8) {
      newErrors.phone = 'Informe um telefone de contato válido com DDD.';
    }
    if (!reason) {
      newErrors.reason = 'Selecione o motivo da sua consulta.';
    }
    if (!date) {
      newErrors.date = 'Selecione uma data preferencial.';
    }
    errors = newErrors;
    return Object.keys(newErrors).length === 0;
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!validate()) {
      return;
    }

    const formattedDate = date ? new Date(date + 'T00:00:00').toLocaleDateString('pt-BR') : date;

    // Simulação do agendamento com alert conforme especificado
    const alertText = `✅ Agendamento Solicitado com Sucesso!\n\n` +
      `Paciente: ${name}\n` +
      `Data: ${formattedDate}\n` +
      `Motivo: ${reason}\n` +
      `Contato: ${phone}\n\n` +
      `Nossa equipe farmacêutica entrará em contato via WhatsApp/E-mail para confirmar seu horário.`;

    alert(alertText);

    successMessage = `Agendamento registrado para ${name} no dia ${formattedDate}! Em breve entraremos em contato no número ${phone}.`;

    // Limpar formulário
    name = '';
    email = '';
    phone = '';
    reason = '';
    date = '';
    errors = {};
  }
</script>

<section id="agendamento" class="booking-section">
  <div class="container">
    <div class="booking-wrapper">
      <div class="booking-intro">
        <span class="booking-tag">Atendimento Farmacêutico</span>
        <h2 class="booking-title">Agende sua Consulta</h2>
        <p class="booking-text">
          O atendimento é individual, humanizado e focado em tirar todas as suas dúvidas 
          sobre seus tratamentos de saúde. Escolha a data de sua preferência.
        </p>

        <div class="info-list">
          <div class="info-item">
            <div class="info-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <div>
              <strong>Duração estimada</strong>
              <p>De 30 a 45 minutos de escuta qualificada.</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
            </div>
            <div>
              <strong>Local do Atendimento</strong>
              <p>Unidade Acadêmica / Polo Buriticupu - MA</p>
            </div>
          </div>

          <div class="info-item">
            <div class="info-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <div>
              <strong>Sigilo Profissional</strong>
              <p>Seus dados e histórico clínico 100% protegidos.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="form-card">
        {#if successMessage}
          <div class="success-banner" role="alert">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <div>
              <strong>Sucesso!</strong>
              <p>{successMessage}</p>
            </div>
          </div>
        {/if}

        <form onsubmit={handleSubmit} novalidate>
          <div class="form-group">
            <label for="name">Nome Completo *</label>
            <input 
              id="name" 
              type="text" 
              placeholder="Ex: Maria José de Sousa" 
              bind:value={name} 
              class={errors.name ? 'has-error' : ''}
            />
            {#if errors.name}
              <span class="error-msg">{errors.name}</span>
            {/if}
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="email">E-mail *</label>
              <input 
                id="email" 
                type="email" 
                placeholder="seu.email@exemplo.com" 
                bind:value={email} 
                class={errors.email ? 'has-error' : ''}
              />
              {#if errors.email}
                <span class="error-msg">{errors.email}</span>
              {/if}
            </div>

            <div class="form-group">
              <label for="phone">Telefone / WhatsApp *</label>
              <input 
                id="phone" 
                type="tel" 
                placeholder="(98) 99999-9999" 
                bind:value={phone} 
                class={errors.phone ? 'has-error' : ''}
              />
              {#if errors.phone}
                <span class="error-msg">{errors.phone}</span>
              {/if}
            </div>
          </div>

          <div class="form-group">
            <label for="reason">Motivo do Atendimento *</label>
            <select 
              id="reason" 
              bind:value={reason} 
              class={errors.reason ? 'has-error' : ''}
            >
              <option value="" disabled>Selecione o motivo da consulta...</option>
              <option value="Revisão geral das receitas e medicamentos em uso">Revisão geral das receitas e medicamentos em uso</option>
              <option value="Dúvidas sobre posologia e horários de tomada">Dúvidas sobre posologia e horários de tomada</option>
              <option value="Possíveis efeitos colaterais ou reações adversas">Possíveis efeitos colaterais ou reações adversas</option>
              <option value="Orientações sobre automedicação responsável">Orientações sobre automedicação responsável</option>
              <option value="Descarte correto de remédios vencidos">Descarte correto de remédios vencidos</option>
              <option value="Outros esclarecimentos com a farmacêutica">Outros esclarecimentos com a farmacêutica</option>
            </select>
            {#if errors.reason}
              <span class="error-msg">{errors.reason}</span>
            {/if}
          </div>

          <div class="form-group">
            <label for="date">Data Preferencial *</label>
            <input 
              id="date" 
              type="date" 
              bind:value={date} 
              class={errors.date ? 'has-error' : ''}
            />
            {#if errors.date}
              <span class="error-msg">{errors.date}</span>
            {/if}
          </div>

          <button type="submit" class="btn btn-submit">
            <span>Confirmar Agendamento</span>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"></path>
              <path d="m12 5 7 7-7 7"></path>
            </svg>
          </button>
        </form>
      </div>
    </div>
  </div>
</section>

<style>
  .booking-section {
    padding: 5rem 0;
    background-color: var(--color-bg);
  }

  .booking-wrapper {
    display: grid;
    grid-template-columns: 0.9fr 1.1fr;
    gap: 3.5rem;
    align-items: flex-start;
  }

  .booking-tag {
    display: inline-block;
    color: var(--color-primary);
    font-weight: 700;
    font-size: 0.88rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.6rem;
  }

  .booking-title {
    font-size: clamp(2rem, 3.5vw, 2.6rem);
    font-weight: 800;
    color: var(--color-text);
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
  }

  .booking-text {
    font-size: 1.05rem;
    color: var(--color-text-muted);
    line-height: 1.7;
    margin-bottom: 2rem;
  }

  .info-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
  }

  .info-item {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background: rgba(255, 255, 255, 0.6);
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    border: 1px solid rgba(22, 128, 58, 0.1);
  }

  .info-icon {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background-color: var(--color-primary);
    color: var(--color-white);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }

  .info-item strong {
    display: block;
    font-size: 0.98rem;
    color: var(--color-text);
    margin-bottom: 0.2rem;
  }

  .info-item p {
    font-size: 0.88rem;
    color: var(--color-text-muted);
    line-height: 1.4;
    margin: 0;
  }

  .form-card {
    background-color: var(--color-white);
    padding: 2.75rem 2.5rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    border: 1px solid rgba(22, 128, 58, 0.12);
  }

  .success-banner {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    background-color: #eafaf1;
    border: 1px solid #16803a;
    color: #10632d;
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    margin-bottom: 1.5rem;
  }

  .success-banner svg {
    flex-shrink: 0;
    color: var(--color-primary);
    margin-top: 2px;
  }

  .success-banner strong {
    display: block;
    margin-bottom: 0.2rem;
    font-size: 0.95rem;
  }

  .success-banner p {
    font-size: 0.9rem;
    line-height: 1.4;
    margin: 0;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 1.25rem;
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }

  label {
    font-size: 0.9rem;
    font-weight: 700;
    color: var(--color-text);
    margin-bottom: 0.4rem;
  }

  input, select {
    width: 100%;
    padding: 0.85rem 1rem;
    font-size: 0.98rem;
    font-family: inherit;
    color: var(--color-text);
    background-color: #fcfdfc;
    border: 1.5px solid #cfd8dc;
    border-radius: var(--radius-md);
    outline: none;
    transition: all 0.2s ease;
  }

  input:focus, select:focus {
    border-color: var(--color-primary);
    background-color: var(--color-white);
    box-shadow: 0 0 0 3px rgba(22, 128, 58, 0.15);
  }

  input.has-error, select.has-error {
    border-color: #d32f2f;
    background-color: #fff8f8;
  }

  .error-msg {
    color: #d32f2f;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 0.35rem;
  }

  .btn-submit {
    width: 100%;
    padding: 1rem;
    font-size: 1.05rem;
    margin-top: 0.75rem;
  }

  @media (max-width: 860px) {
    .booking-wrapper {
      grid-template-columns: 1fr;
      gap: 2.5rem;
    }

    .form-card {
      padding: 2rem 1.5rem;
    }

    .form-row {
      grid-template-columns: 1fr;
    }
  }
</style>

import re

about_file = 'src/lib/components/About.svelte'
with open(about_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix horizontal scroll
content = content.replace('width: 100vw;', '')

# Add !important to CSS variables
old_css = """  .lottie-fullscreen :global(.lottie-title) {
    opacity: var(--title-op);
    transform: translateY(var(--title-ty));
  }
  .lottie-fullscreen :global(.lottie-seminario) {
    opacity: var(--seminario-op);
    transform: translateY(var(--seminario-ty));
  }
  .lottie-fullscreen :global(.lottie-integrantes) {
    opacity: var(--integrantes-op);
    transform: translateX(var(--integrantes-tx));
  }
  .lottie-fullscreen :global(.corner-element) {
    opacity: var(--corner-opacity);
  }"""

new_css = """  .lottie-fullscreen :global(.lottie-title) {
    opacity: var(--title-op) !important;
  }
  .lottie-fullscreen :global(.lottie-seminario) {
    opacity: var(--seminario-op) !important;
  }
  .lottie-fullscreen :global(.lottie-integrantes) {
    opacity: var(--integrantes-op) !important;
  }
  .lottie-fullscreen :global(.corner-element) {
    opacity: var(--corner-opacity) !important;
  }"""
content = content.replace(old_css, new_css)

# Add ornaments (enfeites) to Slide 1
ornaments = """
      <!-- ENFEITES DO SLIDE 1 (Background Lúdico e Elegante) -->
      <div class="abs center" style="width: 100vw; height: 100vh; pointer-events: none; z-index: 0; opacity: {activePhase === 0 ? 1 : 0}; transition: opacity 1s;">
        <!-- Glow 1 -->
        <div style="position: absolute; top: 10%; left: 20%; width: 40vw; height: 40vw; background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; transform: translate(-50%, -50%);"></div>
        <!-- Glow 2 -->
        <div style="position: absolute; bottom: 0%; right: 10%; width: 50vw; height: 50vw; background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0) 70%); border-radius: 50%; transform: translate(30%, 30%);"></div>
        
        <!-- Elementos Vetoriais Finos -->
        <svg style="position: absolute; top: 15%; right: 15%; opacity: 0.15;" width="120" height="120" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="1">
          <circle cx="50" cy="50" r="40" stroke-dasharray="4 6" />
          <circle cx="50" cy="50" r="20" />
        </svg>
        <svg style="position: absolute; bottom: 25%; left: 10%; opacity: 0.1;" width="150" height="150" viewBox="0 0 100 100" fill="none" stroke="white" stroke-width="1">
          <rect x="20" y="20" width="60" height="60" transform="rotate(45 50 50)" />
          <rect x="35" y="35" width="30" height="30" transform="rotate(45 50 50)" />
        </svg>
      </div>

      <div 
        bind:this={lottieContainer} """

content = content.replace('<div \n        bind:this={lottieContainer}', ornaments)

with open(about_file, 'w', encoding='utf-8') as f:
    f.write(content)

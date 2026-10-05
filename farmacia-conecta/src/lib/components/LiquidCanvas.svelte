<script>
  import { onMount } from 'svelte';

  export let progress = 0;

  let canvas;
  let ctx;
  let width, height, screenHeight;
  
  const SPRING_K = 0.035;
  const DAMPING = 0.95;
  const SPREAD = 0.25;
  
  let springs = [];
  const pointsCount = 60;
  
  let animationFrame;
  let lastProgress = 0;

  function initCanvas() {
    if (!canvas) return;
    width = window.innerWidth;
    screenHeight = window.innerHeight;
    height = screenHeight * 2; // O canvas cobre 2 telas
    canvas.width = width;
    canvas.height = height;
    
    springs = [];
    for (let i = 0; i <= pointsCount; i++) {
      springs.push({
        y: screenHeight, // Inicia exatamente na base da primeira tela
        velocity: 0
      });
    }
  }

  onMount(() => {
    ctx = canvas.getContext('2d');
    initCanvas();
    window.addEventListener('resize', initCanvas);
    
    function loop() {
      update();
      draw();
      animationFrame = requestAnimationFrame(loop);
    }
    loop();
    
    return () => {
      window.removeEventListener('resize', initCanvas);
      cancelAnimationFrame(animationFrame);
    };
  });
  
  function update() {
    if (!ctx) return;
    
    // Alvo vai da base da tela (screenHeight) até acima do topo (-10vh)
    let targetY = screenHeight - (progress * screenHeight * 1.2); 
    
    let delta = progress - lastProgress;
    lastProgress = progress;

    // Gera ondulações constantes enquanto está subindo
    if (progress > 0.01 && progress < 0.95) {
      if (Math.random() > 0.4) {
         let p = Math.floor(Math.random() * pointsCount);
         springs[p].velocity += (Math.random() - 0.5) * 45;
      }
      // Um empurrão central proporcional ao scroll para criar a lombada no meio
      if (delta > 0) {
         let center = Math.floor(pointsCount / 2);
         springs[center].velocity -= delta * 1200;
         springs[center-1].velocity -= delta * 800;
         springs[center+1].velocity -= delta * 800;
      }
    }

    // Pass 1: Hooke's Law
    for (let i = 0; i <= pointsCount; i++) {
      let s = springs[i];
      let extension = s.y - targetY;
      let force = -SPRING_K * extension;
      s.velocity += force;
      s.velocity *= DAMPING;
      s.y += s.velocity;
    }
    
    // Pass 2: Wave propagation
    let leftDeltas = new Array(pointsCount + 1).fill(0);
    let rightDeltas = new Array(pointsCount + 1).fill(0);
    
    for (let iter = 0; iter < 4; iter++) {
      for (let i = 0; i <= pointsCount; i++) {
        if (i > 0) {
          leftDeltas[i] = SPREAD * (springs[i].y - springs[i - 1].y);
          springs[i - 1].velocity += leftDeltas[i];
        }
        if (i < pointsCount) {
          rightDeltas[i] = SPREAD * (springs[i].y - springs[i + 1].y);
          springs[i + 1].velocity += rightDeltas[i];
        }
      }
      for (let i = 0; i <= pointsCount; i++) {
        if (i > 0) springs[i - 1].y += leftDeltas[i];
        if (i < pointsCount) springs[i + 1].y += rightDeltas[i];
      }
    }
  }

  function draw() {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    
    if (progress <= 0.001) return;
    
    ctx.fillStyle = '#f4f7f6';
    ctx.beginPath();
    
    let step = width / pointsCount;
    ctx.moveTo(0, height);
    ctx.lineTo(0, springs[0].y);
    
    for (let i = 0; i < pointsCount; i++) {
      let cx = (i + 0.5) * step;
      let cy = (springs[i].y + springs[i + 1].y) / 2;
      ctx.quadraticCurveTo(i * step, springs[i].y, cx, cy);
    }
    
    ctx.lineTo(width, springs[pointsCount].y);
    ctx.lineTo(width, height);
    ctx.fill();
  }
</script>

<canvas bind:this={canvas} class="liquid-canvas" style="display: {progress > 0 ? 'block' : 'none'}"></canvas>

<style>
  .liquid-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 200vh;
    z-index: 2;
    pointer-events: none;
  }
</style>

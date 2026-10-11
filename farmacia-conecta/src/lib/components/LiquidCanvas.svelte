<script>
  import { onMount } from 'svelte';

  export let progress = 0;

  let canvas;
  let ctx;
  let width, height, screenHeight;
  let time = 0;
  let animationFrame;

  function initCanvas() {
    if (!canvas) return;
    width = window.innerWidth;
    screenHeight = window.innerHeight;
    height = screenHeight * 2;
    canvas.width = width;
    canvas.height = height;
  }

  onMount(() => {
    ctx = canvas.getContext('2d');
    initCanvas();
    window.addEventListener('resize', initCanvas);
    
    function loop() {
      time += 0.016;
      draw();
      animationFrame = requestAnimationFrame(loop);
    }
    loop();
    
    return () => {
      window.removeEventListener('resize', initCanvas);
      cancelAnimationFrame(animationFrame);
    };
  });

  function draw() {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);
    
    if (progress <= 0.001) return;

    const p = Math.max(0, Math.min(1, progress));
    const baseY = screenHeight - p * screenHeight * 1.15;
    const amp = (1 - p) * 26 + 6;
    const speed = 1 + (1 - p) * 0.4;
    const phase = time * speed;

    const y0 = baseY + Math.sin(phase) * amp;
    const y1 = baseY + Math.sin(phase + 1.2) * amp * 0.85;
    const y2 = baseY + Math.sin(phase + 2.3) * amp * 0.9;
    ctx.fillStyle = '#f4f7f6';
    ctx.beginPath();
    ctx.moveTo(0, height);
    ctx.lineTo(0, y0);
    ctx.bezierCurveTo(width * 0.2, y0, width * 0.3, y1, width * 0.5, y1);
    ctx.bezierCurveTo(width * 0.7, y1, width * 0.8, y2, width, y2);
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

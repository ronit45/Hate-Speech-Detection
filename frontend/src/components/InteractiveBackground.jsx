import { useEffect, useRef } from 'react';

export default function InteractiveBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let animationFrameId;

    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);

    const mouse = {
      x: width / 2,
      y: height / 2,
      targetX: width / 2,
      targetY: height / 2
    };

    const handleMouseMove = (e) => {
      mouse.targetX = e.clientX;
      mouse.targetY = e.clientY;
    };
    window.addEventListener('mousemove', handleMouseMove);

    // Subtle Soft Blue Light Nodes (#38bdf8)
    const nodes = [
      { x: width * 0.3, y: height * 0.35, vx: 0.3, vy: 0.2, radius: 360, color: [56, 189, 248] },   // Sky Blue
      { x: width * 0.75, y: height * 0.45, vx: -0.2, vy: -0.3, radius: 380, color: [2, 132, 199] }, // Deep Cyan Blue
      { x: width * 0.5, y: height * 0.7, vx: 0.15, vy: -0.15, radius: 340, color: [125, 211, 252] } // Soft Light Blue
    ];

    let time = 0;

    const render = () => {
      time += 0.006;

      mouse.x += (mouse.targetX - mouse.x) * 0.05;
      mouse.y += (mouse.targetY - mouse.y) * 0.05;

      ctx.fillStyle = '#07080e';
      ctx.fillRect(0, 0, width, height);

      // Render organic liquid fluid waves in subtle soft blue
      nodes.forEach((node, idx) => {
        node.x += node.vx + Math.sin(time + idx) * 0.3;
        node.y += node.vy + Math.cos(time + idx) * 0.3;

        if (node.x < -100 || node.x > width + 100) node.vx *= -1;
        if (node.y < -100 || node.y > height + 100) node.vy *= -1;

        const dx = mouse.x - node.x;
        const dy = mouse.y - node.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 400) {
          node.x += (dx / dist) * 0.6;
          node.y += (dy / dist) * 0.6;
        }

        const gradient = ctx.createRadialGradient(
          node.x, node.y, 0,
          node.x, node.y, node.radius + Math.sin(time * 1.5 + idx) * 25
        );

        const [r, g, b] = node.color;
        gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0.12)`);
        gradient.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, 0.04)`);
        gradient.addColorStop(1, 'rgba(7, 8, 14, 0)');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius + 35, 0, Math.PI * 2);
        ctx.fill();
      });

      // Subtle cursor spotlight halo in soft blue
      const cursorGradient = ctx.createRadialGradient(
        mouse.x, mouse.y, 0,
        mouse.x, mouse.y, 220
      );
      cursorGradient.addColorStop(0, 'rgba(56, 189, 248, 0.09)');
      cursorGradient.addColorStop(0.5, 'rgba(56, 189, 248, 0.03)');
      cursorGradient.addColorStop(1, 'transparent');

      ctx.fillStyle = cursorGradient;
      ctx.beginPath();
      ctx.arc(mouse.x, mouse.y, 220, 0, Math.PI * 2);
      ctx.fill();

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        pointerEvents: 'none',
        zIndex: -1
      }}
    />
  );
}

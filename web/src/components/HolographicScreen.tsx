import { useEffect, useRef } from 'react';

interface HolographicScreenProps {
    entropy: number;
}

const HolographicScreen = ({ entropy }: HolographicScreenProps) => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;

        // Resize handling
        const resize = () => {
            const parent = canvas.parentElement;
            if (parent) {
                canvas.width = parent.clientWidth;
                canvas.height = parent.clientHeight;
            }
        };
        resize();
        window.addEventListener('resize', resize);

        const draw = () => {
            const width = canvas.width;
            const height = canvas.height;
            const cellSize = 10;
            const cols = Math.ceil(width / cellSize);
            const rows = Math.ceil(height / cellSize);

            // Clear with fade for trail effect
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.fillRect(0, 0, width, height);

            for (let i = 0; i < cols; i++) {
                for (let j = 0; j < rows; j++) {
                    // Probability of a "bit" flipping depends on entropy (simulated)
                    // High entropy = more chaos/noise
                    if (Math.random() > 0.95) {
                        const alpha = Math.random();
                        // Cyan for 0, Pink for 1 (Qubits)
                        const color = Math.random() > 0.5 ? '0, 243, 255' : '255, 0, 255';

                        ctx.fillStyle = `rgba(${color}, ${alpha})`;
                        ctx.fillRect(i * cellSize, j * cellSize, cellSize - 1, cellSize - 1);
                    }
                }
            }

            // Draw "Horizon Surface" text overlay
            ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.font = '100px monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('101010', width / 2, height / 2);

            animationFrameId = requestAnimationFrame(draw);
        };

        draw();

        return () => {
            cancelAnimationFrame(animationFrameId);
            window.removeEventListener('resize', resize);
        };
    }, [entropy]);

    return (
        <canvas
            ref={canvasRef}
            className="w-full h-full absolute inset-0 rounded-lg"
        />
    );
};

export default HolographicScreen;

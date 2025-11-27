import 'katex/dist/katex.min.css';
import katex from 'katex';
import React from 'react';

interface LatexProps {
    children: string;
    className?: string;
}

const Latex: React.FC<LatexProps> = ({ children, className = '' }) => {
    const renderText = (text: string) => {
        // Split by $...$ but keep the delimiters to identify them
        const parts = text.split(/(\$[^$]+\$)/g);

        return parts.map((part, index) => {
            if (part.startsWith('$') && part.endsWith('$')) {
                // Remove the $ delimiters
                const math = part.slice(1, -1);
                try {
                    const html = katex.renderToString(math, {
                        throwOnError: false,
                        displayMode: false,
                    });
                    return <span key={index} dangerouslySetInnerHTML={{ __html: html }} />;
                } catch (error) {
                    console.error("KaTeX error:", error);
                    return <span key={index} className="text-red-500">{part}</span>;
                }
            }
            return <span key={index}>{part}</span>;
        });
    };

    return <span className={className}>{renderText(children)}</span>;
};

export default Latex;

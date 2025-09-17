import React from "react";
import ReactMarkdown from "react-markdown";
import type { Components } from "react-markdown";
import { Typography } from "@mui/material";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

// Separate "printable" markdown component, avoiding "react-router-dom" Link

interface MdPrintableProps {
  text: string
  markdownNewlines: boolean
  extraComponents?: Components
}

export default function MdPrintable({ text, markdownNewlines, extraComponents}: MdPrintableProps) {
  const textFormatted = markdownNewlines ? text : text.replace(/\\n/g, "\n").replace(/\n/g, "  \n");

  const baseComponents: Components = {
    h4: ({ children }) => <Typography variant="h4">{children}</Typography>,
    h5: ({ children }) => <Typography variant="h5">{children}</Typography>,
    a: ({ children }) => <>{children}</>
  }

	const components: Components = {
		...baseComponents,
		...(extraComponents ?? {})
	}

	return (
		<ReactMarkdown
			remarkPlugins={[remarkGfm]}
			rehypePlugins={[rehypeRaw]}
			components={components}
		>
			{textFormatted}
		</ReactMarkdown>
	)
}

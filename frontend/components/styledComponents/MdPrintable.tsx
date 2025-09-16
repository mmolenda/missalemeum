import React from "react";
import ReactMarkdown from "react-markdown";
import { Typography } from "@mui/material";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

// Separate "printable" markdown component, avoiding "react-router-dom" Link

interface MdPrintableProps {
  text: string
  markdownNewlines: boolean
  extraComponents?: any
}

export default function MdPrintable({ text, markdownNewlines, extraComponents}: MdPrintableProps) {
  const textFormatted = markdownNewlines ? text : text.replace(/\\n/g, "\n").replace(/\n/g, "  \n");

  const baseComponents = {
    h4: (props: { children?: React.ReactNode }) => <Typography variant="h4">{props.children}</Typography>,
    h5: (props: { children?: React.ReactNode }) => <Typography variant="h5">{props.children}</Typography>,
    a: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => props.children
  }

	const components = {
		...baseComponents,
		...extraComponents
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

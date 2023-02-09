import React from 'react';
import ReactMarkdown from "react-markdown";
import {Typography} from "@mui/material";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

// we need to have a separate "printable" markdown component, which does not
// import Link from "react-router-dom"; otherwise it won't open in new window

export default function MdPrintable(props) {
	let text = (props.markdownNewlines) ? props.text : props.text.replace(/\\n/g, '\n').replace(/\n/g, '  \n')
	let baseComponents = {
		"h3": (props) => <Typography variant="h3">{props.children[0]}</Typography>,
		"h4": (props) => <Typography variant="h4">{props.children[0]}</Typography>,
		"a": (props) => props.children[0]
	}
	let extraComponents = props.extraComponents || {}
	let components = {
		...baseComponents,
		...extraComponents
	}
	return (
		<ReactMarkdown
			children={text}
			remarkPlugins={[remarkGfm]}
			rehypePlugins={[rehypeRaw]}
			components={components}
		/>
	)
}
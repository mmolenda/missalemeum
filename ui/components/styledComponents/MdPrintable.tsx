import React from 'react';
import ReactMarkdown from "react-markdown";
import {Typography} from "@mui/material";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

// we need to have a separate "printable" markdown component, which does not
// import Link from "react-router-dom"; otherwise it won't open in new window

export default function MdPrintable({text, markdownNewlines}: {text: string, markdownNewlines: boolean}) {
	let textFmt = (markdownNewlines) ? text : text.replace(/\\n/g, '\n').replace(/\n/g, '  \n')
	// let baseComponents = {
	// 	"h4": (props) => <Typography variant="h4">{props.children}</Typography>,
	// 	"h5": (props) => <Typography variant="h5">{props.children}</Typography>,
	// 	"a": (props) => props.children[0]
	// }
	// let extraComponents = props.extraComponents || {}
	// let components = {
	// 	...baseComponents,
	// 	...extraComponents
	// }
	return (
		<ReactMarkdown
			children={textFmt}
			remarkPlugins={[remarkGfm]}
			rehypePlugins={[rehypeRaw]}
			// components={components}
			// components={baseComponents}
		/>
	)
}
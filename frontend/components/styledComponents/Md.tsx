import React from 'react';
import MdPrintable from "./MdPrintable";
import MyLink from "../MyLink";

interface MdProps {
  text: string
  markdownNewlines: boolean
  widgetMode?: boolean
}

export default function Md({text, markdownNewlines, widgetMode = false}: MdProps) {
	return <MdPrintable text={text} markdownNewlines={markdownNewlines} extraComponents={{
		a: (props: React.AnchorHTMLAttributes<HTMLAnchorElement>) => <MyLink href={props.href} text={String(props.children)} widgetMode={widgetMode} />
	}}
	/>
}
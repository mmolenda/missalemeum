import React from 'react';
import MdPrintable from "./MdPrintable";
import MyLink from "../MyLink";

export default function Md(props) {
	return <MdPrintable {...props} extraComponents={{
		"a": (props) => <MyLink href={props.href} text={props.children[0]} widgetMode={props.widgetMode} />
	}}
	/>
}
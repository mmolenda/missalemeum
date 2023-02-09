import React from 'react';
import {Link} from "@mui/material";
import {Link as RouterLink} from "react-router-dom";
import MdPrintable from "./MdPrintable";

export default function Md(props) {
	return <MdPrintable {...props} extraComponents={{
		"a": (props) => <Link
			component={RouterLink}
			to={{pathname: props.href}}
			target={(props.href.startsWith("http") ? "_blank" : "")}
			href='#'>{props.children[0]}</Link>
	}}
	/>
}
import React from 'react';
import {Link} from "@mui/material";
import {Link as RouterLink} from "react-router-dom";
import MdPrintable from "./MdPrintable";

export default function Md(props) {
	return <MdPrintable {...props} extraComponents={{
		"a": (props) => {
			let [pathname, search] = props.href.split("?")
			return pathname.startsWith("http")
				? <Link target="_blank" href={pathname}>{props.children[0]}</Link>
				: <Link component={RouterLink} to={{pathname: pathname, search: search}} href={pathname}>{props.children[0]}</Link>
		}
	}}
	/>
}
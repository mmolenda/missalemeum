import React from 'react';
import {Link} from "@mui/material";
import {Link as RouterLink} from "react-router-dom";

export default function MyLink(props) {
	let [pathname, search] = props.href.split("?")
	return pathname.startsWith("http") || props.widgetMode === true
		? <Link target="_blank" href={(search && !search.startsWith("ref")) ? props.href : pathname}>{props.text}</Link>
		: <Link component={RouterLink} to={{pathname: pathname, search: search}} href={pathname}>{props.text}</Link>
}


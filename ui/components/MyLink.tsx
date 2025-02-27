import React from 'react';
import { Link as MUILink } from "@mui/material";
import Link from "next/link";

export default function MyLink(props) {
	let [pathname, search] = props.href.split("?")
	return pathname.startsWith("http") || props.widgetMode === true
		? <MUILink target="_blank" href={(search && !search.startsWith("ref")) ? props.href : pathname}>{props.text}</MUILink>
		: <MUILink
			component={Link}
			href={`${pathname}?${search}`}>{props.text}</MUILink>
}


import React from 'react';
import { Link as MUILink } from "@mui/material";
import Link from "next/link";

export default function MyLink({href, text, widgetMode}: {href: string | undefined, text: string, widgetMode: boolean | undefined}) {
	let [pathname, search] = href ? href.split("?") : ["", ""]
	return pathname.startsWith("http") || widgetMode
		? <MUILink target="_blank" href={(search && !search.startsWith("ref")) ? href : pathname}>{text}</MUILink>
		: <MUILink
			component={Link}
			href={href}>{text}</MUILink>
}


import React from 'react';
import { Link as MUILink } from "@mui/material";
import Link from "next/link";

export default function MyLink({href, text, widgetMode}: {href: string, text: string, widgetMode: boolean}) {
	let [pathname, search] = href.split("?")
	return pathname.startsWith("http") || widgetMode === true
		? <MUILink target="_blank" href={(search && !search.startsWith("ref")) ? href : pathname}>{text}</MUILink>
		: <MUILink
			component={Link}
			href={`${pathname}?${search}`}>{text}</MUILink>
}


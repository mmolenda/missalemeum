"use client"

import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function SidenavListItemText({prim, sec, rank = 0}: {prim: string, sec?: string, rank?: number }) {
	let rankStyles = {
		textTransform: [1, 2].includes(rank) ? "uppercase" : "none",
		fontStyle: rank === 4 ? "italic" : "normal"
	}

	return <ListItemText
		primary={prim}
		secondary={sec}
		// slotProps={{
		// 	primary: {sx: {...{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", fontFamily: (theme) => theme.typography.fontFamily}, ...rankStyles}},
		// 	secondary: {sx:  {overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color: "secondary.main"}}
		// }}
	/>
}

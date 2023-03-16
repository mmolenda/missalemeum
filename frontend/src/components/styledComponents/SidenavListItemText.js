import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function SidenavListItemText(props) {
	let fontWeight = {1: 600, 2: 400, 3: 300, 4: 300}[props.rank] || 400
	let rankStyles = {fontWeight: fontWeight, fontStyle: props.rank === 4 ? "italic" : "normal"}

	return <ListItemText
		primary={props.primary}
		secondary={props.secondary}
		primaryTypographyProps={{...{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", fontFamily: (theme) => theme.typography.fontFamily}, ...rankStyles}}
		secondaryTypographyProps={{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color: "secondary.main"}}
	/>
}

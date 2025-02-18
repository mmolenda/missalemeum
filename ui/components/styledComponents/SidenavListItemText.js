import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function SidenavListItemText(props) {
	let rankStyles = {
		textTransform: [1, 2].includes(props.rank) ? "uppercase" : "none",
		fontStyle: props.rank === 4 ? "italic" : "normal"
	}

	return <ListItemText
		primary={props.primary}
		secondary={props.secondary}
		primaryTypographyProps={{...{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", fontFamily: (theme) => theme.typography.fontFamily}, ...rankStyles}}
		secondaryTypographyProps={{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color: "secondary.main"}}
	/>
}

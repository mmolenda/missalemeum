import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function SidenavListItemText(props) {
	return <ListItemText
		primary={props.primary}
		secondary={props.secondary}
		primaryTypographyProps={{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", fontFamily: (theme) => theme.typography.fontFamily}}
		secondaryTypographyProps={{overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color: "secondary.main"}}
	/>
}

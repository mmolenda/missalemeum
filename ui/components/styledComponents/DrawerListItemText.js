import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function DrawerListItemText(props) {
	return <ListItemText
		primary={props.primary}
		secondary={props.secondary}
		primaryTypographyProps={{
			fontFamily: (theme) => theme.typography.fontFamily,
			color: "primary.main",
			fontWeight: 500,
			textTransform: "uppercase"
		}}
	/>
}

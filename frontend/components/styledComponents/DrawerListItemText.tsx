import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function DrawerListItemText({prim}: {prim: string}) {
	return <ListItemText
		primary={prim}
		slotProps={{primary: {
			fontFamily: (theme) => theme.typography.fontFamily,
			color: "primary.main",
			fontWeight: 500,
			textTransform: "uppercase"
		}}}
	/>
}

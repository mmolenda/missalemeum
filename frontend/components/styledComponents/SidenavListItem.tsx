"use client"

import { styled } from '@mui/system';
import {ListItem} from "@mui/material";

export const SidenavListItem = styled(ListItem)(({ theme }) => ({
	borderBottom: "1px solid",
	borderLeft: "1px solid",
	borderRight: "1px solid",
	borderColor: theme.palette.text.disabled,
	color: theme.palette.primary.main,
	paddingTop: 0,
	paddingBottom: 0
}));

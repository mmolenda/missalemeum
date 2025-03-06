"use client"

import React from 'react';
import ListItemText from "@mui/material/ListItemText";

export default function SidenavListItemText({prim, sec, rank = 0}: { prim: string, sec?: string, rank?: number }) {
  return <ListItemText
    primary={prim}
    secondary={sec}
    slotProps={{
      primary: {
        sx: {
          overflow: "hidden",
          whiteSpace: "nowrap",
          textOverflow: "ellipsis",
          textTransform: [1, 2].includes(rank) ? "uppercase" : "none",
          fontStyle: rank === 4 ? "italic" : "normal",
          fontFamily: (theme) => theme.typography.fontFamily
        }
      },
      secondary: {sx: {overflow: "hidden", whiteSpace: "nowrap", textOverflow: "ellipsis", color: "secondary.main"}}
    }}
  />
}

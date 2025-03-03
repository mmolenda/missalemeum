import React from 'react';
import {Chip} from "@mui/material";

export default function Tag({label, color, icon}: {label: string, color?: "secondary" | "vestmentw" | "vestmentr" | "vestmentv" | "vestmentg", icon?: any}) {
  return (
    <Chip
      color={color ? color : "secondary"}
      icon={icon ? icon : null}
      variant="outlined"
      sx={{
        margin: "0.15rem",
        borderRadius: 10,
        height: (theme) => theme.typography.fontSize / 7 + "rem"
      }}
      label={label}
    />
  )
}
import React from 'react';
import {Chip} from "@mui/material";
import {vestmentColor} from "@/components/designTokens";

export default function Tag({label, color = "secondary", icon}: {label: string, color?: "secondary" | vestmentColor, icon?: any}) {
  return (
    <Chip
      color={color}
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
import React from 'react';
import {Chip, type ChipProps} from "@mui/material";
import {vestmentColor} from "@/components/designTokens";

type TagProps = {
  label: string,
  color?: "secondary" | vestmentColor,
  icon?: ChipProps['icon']
};

export default function Tag({label, color = "secondary", icon}: TagProps) {
  return (
    <Chip
      color={color}
      icon={icon ?? undefined}
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

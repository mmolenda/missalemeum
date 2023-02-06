import React from 'react';
import {Chip} from "@mui/material";

export default function Tag(props) {
  return (
    <Chip
      color={props.color ? props.color : "secondary"}
      icon={props.icon ? props.icon : null}
      variant="outlined"
      sx={{margin: "0.15rem"}}
      label={props.label}
    />
  )
}
import React from 'react';
import {Box, Typography} from "@mui/material";
import {ContainerMedium} from "./styledComponents/ContainerMedium";

export default function ContainerSimple(props) {
  return (
    <ContainerMedium>
        <Box sx={{width: '100%', pt: (theme) => `${parseInt(theme.components.MuiAppBar.styleOverrides.root.height) * 2}px`}}>
          <Typography variant="h2">{props.title}</Typography>
          <Typography component="div" variant="body1" align="justify" sx={{ padding: "0.5rem" }}>
            {props.content}
          </Typography>
        </Box>
    </ContainerMedium>
  )
}
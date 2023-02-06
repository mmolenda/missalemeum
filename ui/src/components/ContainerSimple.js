import React from 'react';
import {Box, Container, Typography} from "@mui/material";

export default function ContainerSimple(props) {
  return (
    <Container sx={{width: {"md": "900px"}}}>
        <Box sx={{width: '100%', pt: (theme) => `${parseInt(theme.components.MuiAppBar.styleOverrides.root.height) * 2}px`}}>
          <Typography variant="h2">{props.title}</Typography>
          <Typography component="div" variant="body1" align="justify" sx={{ padding: "0.5rem" }}>
            {props.content}
          </Typography>
        </Box>
    </Container>
  )
}
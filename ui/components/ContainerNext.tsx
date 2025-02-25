"use client";

import {Box, IconButton} from "@mui/material";
import Link from "next/link";
import React from "react";
import BilingualContent from "@/components/BilingualContent";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";


export default function ContainerNext({lang, id, content, backButtonRef, singleColumnAsRubric}) {
  const markdownNewlines = false
  const widgetMode = false

  let backButton = (backButtonRef && <IconButton
    component={Link}
    href={backButtonRef}
    sx={{backgroundColor: "background.default", opacity: 0.9}}
  >
    <ArrowBackIcon/>
  </IconButton>)


  return (
    <ContainerMedium disableGutters sx={{display: 'flex', overflow: 'hidden', height: "100%"}}>

      <Box
        id="content"
        sx={{
          overflowY: 'scroll',
          width: '100%',
          ml: 0,
          pt: (theme) => `${parseInt(theme.components.MuiAppBar.styleOverrides.root.height) * 2}px`,
          height: "100%"
        }}
      >
        <BilingualContent id={id} lang={lang} contents={content}
                          singleColumnAsRubric={singleColumnAsRubric} backButton={backButton}
                          markdownNewlines={markdownNewlines} widgetMode={widgetMode}/>
    </Box>


</ContainerMedium>

)
}


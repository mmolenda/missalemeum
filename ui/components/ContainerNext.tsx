"use client";

import {Box, IconButton} from "@mui/material";
import Link from "next/link";
import React from "react";
import {useTheme} from "@mui/material/styles";
import BilingualContent from "@/components/BilingualContent";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {usePathname} from "next/navigation";


export default function ContainerNext({lang, content, backButtonRef}) {
  const theme = useTheme()
  const singleColumnAsRubric = false
  const markdownNewlines = false
  const pathname = usePathname()
  const widgetMode = false
  let backButton = (<IconButton
    component={Link}
    href={backButtonRef ? backButtonRef : pathname.substring(0, pathname.lastIndexOf('/'))}
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
          pt: (theme) => theme.components.MuiAppBar.styleOverrides.root.height,
          height: "100%"
        }}
      >
        <BilingualContent id={"2022-11-11"} lang={lang} contents={content}
                          singleColumnAsRubric={singleColumnAsRubric} backButton={backButton}
                          markdownNewlines={markdownNewlines} widgetMode={widgetMode}/>
    </Box>


</ContainerMedium>

)
}


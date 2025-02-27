"use client";

import {IconButton} from "@mui/material";
import Link from "next/link";
import React from "react";
import BilingualContent from "@/components/BilingualContent";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";


export default function ContainerNext({lang, id, content, backButtonRef, singleColumnAsRubric, widgetMode, markdownNewlines}) {

  let backButton = (backButtonRef && <IconButton
    component={Link}
    href={backButtonRef}
    sx={{backgroundColor: "background.default", opacity: 0.9}}
  >
    <ArrowBackIcon/>
  </IconButton>)

  return <BilingualContent
    id={id}
    lang={lang}
    contents={content}
    singleColumnAsRubric={singleColumnAsRubric}
    backButton={backButton}
    markdownNewlines={markdownNewlines}
    widgetMode={widgetMode}
  />
}


"use client"

import React, {useState} from "react";
import {Box, Button, IconButton, Typography} from "@mui/material";
import moment from "moment";
import {appbarDarkGrey, yellowish} from "@/components/designTokens";
import Logo from "./Logo";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import {POWERED_BY, TODAY} from "./intl";
import {ContainerMedium} from "./styledComponents/ContainerMedium";
import ContainerNext from "@/components/ContainerNext";
import Link from "next/link";
import { Link as MUILink } from "@mui/material";

export default function WidgetPropers({lang, id, content, version}) {
  let date = moment(id)

  return (
    <><ContainerMedium sx={{mt: "0.5rem", textAlign: "right"}}>
      <IconButton component={Link} size="small" variant="outlined"
                  href={`/${lang}/widgets/propers/${date.subtract(1, 'days').format('YYYY-MM-DD')}`}><ArrowBackIcon/></IconButton>&nbsp;
      <IconButton component={Link} size="small" variant="outlined"
                  href={`/${lang}/widgets/propers/${date.add(2, 'days').format('YYYY-MM-DD')}`}><ArrowForwardIcon/></IconButton>
      <Button component={Link}  size="small" variant="outlined"
              href={`/${lang}/widgets/propers/${moment().format('YYYY-MM-DD')}`}>{TODAY[lang]}</Button>&nbsp;
    </ContainerMedium>
      <ContainerNext
        lang={lang}
        id={id}
        content={content}
        widgetMode={true}
      />
      {version && <ContainerMedium sx={{display: "flex", justifyContent: "space-between"}}>
        <Typography
          sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.75rem"}}>{version}</Typography>
      </ContainerMedium>}
      <Box sx={{
        position: "fixed",
        bottom: 0,
        width: "100%",
        paddingY: "0.05rem",
        textAlign: "center",
        backgroundColor: appbarDarkGrey,
        color: yellowish
      }}>{POWERED_BY[lang]}{' '}
        <MUILink target="_blank" href="https://www.missalemeum.com" sx={{color: yellowish}}>
          <Logo width={10} height={10}/>Missale Meum
        </MUILink></Box></>
  )
}
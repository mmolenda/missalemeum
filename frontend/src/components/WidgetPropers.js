import React, {useState} from "react";
import {Box, Button, createTheme, GlobalStyles, IconButton, Link, ThemeProvider} from "@mui/material";
import ContainerWithSidenav from "./ContainerWithSidenav";
import moment from "moment";
import {appbarDarkGrey, getDesignTokens, yellowish} from "../designTokens";
import Logo from "./Logo";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import {POWERED_BY, TODAY} from "../intl";
import {useParams} from "react-router-dom";

export default function WidgetPropers() {
  const {lang} = useParams()
  const queryParameters = new URLSearchParams(window.location.search)
  const settingsLang = {"pl": "pl", "en": "en"}[lang] || "en"
  const settingsThemeMode = {"light": "light", "dark": "dark"}[queryParameters.get("theme")] || "light"
  const settingsShowNav = (queryParameters.get("navigation") + "").toLowerCase() !== "false"
  const getContentUrl = 'api/v5/proper'
  const [myId, setMyId] = useState(moment().format("YYYY-MM-DD"))
  let date = moment(myId)
   const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
      getContent(myId)
    })

  let designTokens = getDesignTokens(settingsThemeMode)
  designTokens.components.MuiAppBar.styleOverrides.root.height = "12px"
  const theme = createTheme(designTokens)
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles
        styles={(theme) => ({
          "body": { backgroundColor: theme.palette.background.default },
          "div#root": { backgroundColor: theme.palette.background.default }
        })}
      />
      {settingsShowNav && <Box sx={{marginTop: "1rem", textAlign: "center"}}>
        <IconButton variant="outlined" onClick={() => setMyId(date.subtract(1, 'days').format('YYYY-MM-DD'))}><ArrowBackIcon /></IconButton>&nbsp;
        <IconButton variant="outlined" onClick={() => setMyId(date.add(1, 'days').format('YYYY-MM-DD'))}><ArrowForwardIcon /></IconButton>
        <Button variant="outlined" onClick={() => setMyId(moment().format('YYYY-MM-DD'))} >{TODAY[settingsLang]}</Button>&nbsp;
      </Box>}
      <ContainerWithSidenav
        id={myId}
        lang={settingsLang}
        init={init}
        getContentUrl={getContentUrl}
        sidenavDisabled
        widgetMode
      />
      <Box sx={{
        position: "fixed",
        bottom: 0,
        width: "100%",
        paddingY: "0.05rem",
        textAlign: "center",
        backgroundColor: appbarDarkGrey,
        color: yellowish
      }}>{POWERED_BY[settingsLang]}{' '}
        <Link target="_blank" href="https://www.missalemeum.com" sx={{color: yellowish}}>
          <Logo width={10} height={10} />Missale Meum
        </Link></Box>
    </ThemeProvider>
  )
}
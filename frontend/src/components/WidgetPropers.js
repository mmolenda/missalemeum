import React from "react";
import {Box, createTheme, GlobalStyles, Link, ThemeProvider} from "@mui/material";
import ContainerWithSidenav from "./ContainerWithSidenav";
import moment from "moment";
import {appbarDarkGrey, getDesignTokens, yellowish} from "../designTokens";
import Logo from "./Logo";

export default function WidgetPropers() {
  const queryParameters = new URLSearchParams(window.location.search)
  const themeMode = queryParameters.get("theme")
  const getContentUrl = 'api/v5/proper'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    let today = moment().format("YYYY-MM-DD")
    getContent(today)
  })

  let designTokens = getDesignTokens(themeMode ? themeMode : "light")
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
      <ContainerWithSidenav
        init={init}
        getContentUrl={getContentUrl}
        sidenavDisabled
        contentToolbarDisabled
      />
      <Box sx={{
        position: "fixed",
        bottom: 0,
        width: "100%",
        backgroundColor: appbarDarkGrey,
        color: yellowish
      }}><span> <Logo width={12} height={12} />Powered by&nbsp;
        <Link target="_blank" href="https://www.missalemeum.com" sx={{color: yellowish}}>Missale Meum
        </Link></span></Box>
    </ThemeProvider>

  )
}
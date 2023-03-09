import React from "react";
import {Box, createTheme, GlobalStyles, Link, ThemeProvider} from "@mui/material";
import ContainerWithSidenav from "./ContainerWithSidenav";
import moment from "moment";
import {appbarDarkGrey, getDesignTokens, yellowish} from "../designTokens";
import Logo from "./Logo";
import {Link as RouterLink, useParams} from "react-router-dom";

export default function WidgetPropers() {
  const {lang} = useParams()
  const {id} = useParams()
  let date = (id === undefined) ? moment() : moment(id)
  const queryParameters = new URLSearchParams(window.location.search)
  const themeMode = queryParameters.get("theme")
  const getContentUrl = 'api/v5/proper'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    if (id === undefined) {
      id = moment().format("YYYY-MM-DD")
    }
    getContent(id)
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
      <Box>
        <Link component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${date.subtract(1, 'days').format('YYYY-MM-DD')}`}} >&larr;Yesterday</Link>&nbsp;
        <Link component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${moment().format('YYYY-MM-DD')}`}} >Today</Link>&nbsp;
        <Link component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${date.add(2, 'days').format('YYYY-MM-DD')}`}} >Tomorrow &rarr;</Link>
      </Box>
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
      }}><span>Powered by&nbsp;
        <Logo width={12} height={12} /><Link target="_blank" href="https://www.missalemeum.com" sx={{color: yellowish}}>Missale Meum
        </Link></span></Box>
    </ThemeProvider>

  )
}
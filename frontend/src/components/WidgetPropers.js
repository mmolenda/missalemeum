import React from "react";
import {Box, Button, createTheme, GlobalStyles, IconButton, Link, ThemeProvider} from "@mui/material";
import ContainerWithSidenav from "./ContainerWithSidenav";
import moment from "moment";
import {appbarDarkGrey, getDesignTokens, yellowish} from "../designTokens";
import Logo from "./Logo";
import {Link as RouterLink, useParams} from "react-router-dom";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

export default function WidgetPropers() {
  const {lang} = useParams()
  const {id} = useParams()
  let date = (id === undefined) ? moment() : moment(id)
  const queryParameters = new URLSearchParams(window.location.search)
  const themeMode = {"light": "light", "dark": "dark"}[queryParameters.get("theme")] || "light"
  console.log(themeMode)
  const getContentUrl = 'api/v5/proper'
  const init = ((id, internalLang, internalYear, sidenavItems, getSidenavItems, getContent, setSidenavHidden) => {
    if (id === undefined) {
      id = moment().format("YYYY-MM-DD")
    }
    getContent(id)
  })

  let designTokens = getDesignTokens(themeMode)
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
      <Box sx={{marginTop: "1rem"}}>
        <IconButton variant="outlined" component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${date.subtract(1, 'days').format('YYYY-MM-DD')}`, search: window.location.search}} ><ArrowBackIcon /></IconButton>&nbsp;
        <IconButton variant="outlined" component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${date.add(2, 'days').format('YYYY-MM-DD')}`, search: window.location.search}} ><ArrowForwardIcon /></IconButton>
        <Button variant="outlined" component={RouterLink} to={{pathname: `/${lang}/widgets/propers/${moment().format('YYYY-MM-DD')}`, search: window.location.search}} >Today</Button>&nbsp;
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
        textAlign: "right",
        backgroundColor: appbarDarkGrey,
        color: yellowish
      }}><span>Powered by&nbsp;
        <Logo width={12} height={12} /><Link target="_blank" href="https://www.missalemeum.com" sx={{color: yellowish}}>Missale Meum
        </Link></span></Box>
    </ThemeProvider>

  )
}
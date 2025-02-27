"use client"

import React, {useEffect, useState} from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import {appbarDarkGrey, getDesignTokens} from '@/components/designTokens';
import {AppBar, Container, createTheme, CssBaseline, Toolbar, Typography, useMediaQuery} from "@mui/material";

import {Link as MUILink} from "@mui/material";
import Logo from "@/components/Logo";
import MainMenu from "@/components/MainMenu";
import {Merriweather} from 'next/font/google'
import Link from "next/link";
import {myLocalStorage} from "@/components/myLocalStorage";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {CookieConsent} from "react-cookie-consent";
import {MSG_COOKIES, MSG_POLICY_DECLINE_BUTTON, MSG_POLICY_LINK} from "@/components/intl";
import {useParams} from "next/navigation";


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({children}) {
  const params = useParams()
  const lang = params.locale
  // const lang = "pl"
  const [darkMode, setDarkMode] = useState("light")
  const [fontSize, setFontSize] = useState("medium")
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')

  useEffect(() => {
    setDarkMode({"true": true, "false": false, null: undefined}[myLocalStorage.getItem("darkMode")])
    setFontSize(myLocalStorage.getItem("fontSize"))
  }, []);

  const getThemeMode = () => {
    return ((darkMode == undefined && prefersDark) || darkMode) ? "dark" : "light"
  }
  const mode = getThemeMode()
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode, fontSize)), [mode, fontSize]);

  return (<html lang="en" className={merriweather.className}>
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <body>
        <Container disableGutters sx={{backgroundColor: "background.default"}}>
          <AppBar sx={{backgroundColor: appbarDarkGrey}}>
            <Toolbar>
              <MainMenu
                lang={lang}
                darkMode={darkMode}
                setDarkMode={setDarkMode}
                fontSize={fontSize}
                setFontSize={setFontSize}
              />
              <MUILink component={Link} href="/pl" sx={{display: "flex", textDecoration: "none"}}>
                <Logo width={28} height={28}/>
                <Typography variant="h1" component="div">Missale<br/>Meum</Typography>
              </MUILink>
            </Toolbar>
          </AppBar>
          {children}
          <ContainerMedium sx={{display: "flex", justifyContent: "space-between"}}>
            <Typography
              sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.9rem"}}>☩
              A. M. D. G. ☩</Typography>
            <Typography
              sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.75rem"}}>{process.env.NEXT_PUBLIC_BUILD_VERSION}</Typography>
          </ContainerMedium>
          <CookieConsent
            cookieName="MMCookieConsent"
            cookiePath="/"
            enableDeclineButton
            declineButtonStyle={{background: appbarDarkGrey}}
            buttonStyle={{background: "#e49086"}}
            declineButtonText={MSG_POLICY_DECLINE_BUTTON[lang]}
            buttonText="OK">
            {MSG_COOKIES[lang]}
            <MUILink component={Link} href={`/${lang}/supplement/privacy-policy`} target="_blank">
              {MSG_POLICY_LINK[lang]}
            </MUILink>
          </CookieConsent>
        </Container>
        </body>
      </ThemeProvider>
    </AppRouterCacheProvider>
    </html>
  );
}

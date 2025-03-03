"use client"

import React, {useEffect, useState} from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import {appbarDarkGrey, getDesignTokens} from '@/components/designTokens';
import {
  AppBar,
  Box,
  Container,
  createTheme,
  CssBaseline,
  Toolbar,
  Typography,
  useMediaQuery
} from "@mui/material";

import {Link as MUILink} from "@mui/material";
import Logo from "@/components/Logo";
import MainMenu from "@/components/MainMenu";
import {Merriweather} from 'next/font/google'
import Link from "next/link";
import {myLocalStorage} from "@/components/myLocalStorage";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {CookieConsent} from "react-cookie-consent";
import {Locale, MSG_COOKIES, MSG_POLICY_DECLINE_BUTTON, MSG_POLICY_LINK} from "@/components/intl";
import {useParams} from "next/navigation";
import moment from "moment";
import 'moment/locale/pl';


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({children}: { children: React.ReactNode}) {
  const { locale } = useParams<{ locale?: string }>()
  moment.locale(locale)
  const lang = typeof locale === "string" ? locale : "en"
  const [darkMode, setDarkMode] = useState<boolean | undefined>(false)
  const [fontSize, setFontSize] = useState<string>("medium")
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')

  useEffect(() => {
    setDarkMode({
      "true": true,
      "false": false,
      "undefined": undefined
    }[myLocalStorage.getItem("darkMode") ?? "undefined"])
    setFontSize(myLocalStorage.getItem("fontSize") ?? "medium")
  }, []);

  const getThemeMode = () => {
    return ((darkMode == undefined && prefersDark) || darkMode) ? "dark" : "light"
  }
  const mode = getThemeMode()
  // const theme = React.useMemo(() => createTheme(getDesignTokens(mode, fontSize)), [mode, fontSize]);
  const theme = createTheme(getDesignTokens(mode, fontSize));

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

          <ContainerMedium disableGutters sx={{display: 'flex', overflow: 'hidden', height: "100%"}}>

            <Box
              id="content"
              sx={{
                overflowY: 'scroll',
                width: '100%',
                ml: 0,
                pt: (theme) => {
                  // we just need the value of theme.components?.MuiAppBar?.styleOverrides?.root.height
                  // all the code below is to appease typescript linter
                  const root = theme.components?.MuiAppBar?.styleOverrides?.root;
                  // Check if root is an object and has a height property
                  const height = root && typeof root === 'object' && 'height' in root ? root.height : 0;
                  // Ensure height is a valid number
                  const parsedHeight = typeof height === 'string' ? parseInt(height) : height;
                  // Check if parsedHeight is a valid number
                  const finalHeight: number = isNaN(parsedHeight as number) ? 0 : parsedHeight as number;
                  return `${finalHeight * 2}px`;
                },
                height: "100%"
              }}
            >
              {children}
            </Box>
          </ContainerMedium>
          <ContainerMedium sx={{display: "flex", justifyContent: "space-between"}}>
            <Typography
              sx={{
                py: "2rem",
                color: theme.palette.mode === "dark" ? "primary.dark" : "primary.light",
                fontSize: "0.9rem"
              }}>☩
              A. M. D. G. ☩</Typography>
            <Typography
              sx={{
                py: "2rem",
                color: theme.palette.mode === "dark" ? "primary.dark" : "primary.light",
                fontSize: "0.75rem"
              }}>{process.env.NEXT_PUBLIC_BUILD_VERSION}</Typography>
          </ContainerMedium>
          <CookieConsent
            cookieName="MMCookieConsent"
            enableDeclineButton
            declineButtonStyle={{background: appbarDarkGrey}}
            buttonStyle={{background: "#e49086"}}
            declineButtonText={MSG_POLICY_DECLINE_BUTTON[locale as Locale]}
            buttonText="OK">
            {MSG_COOKIES[locale as Locale]}
            <MUILink component={Link} href={`/${locale}/supplement/privacy-policy`} target="_blank">
              {MSG_POLICY_LINK[locale as Locale]}
            </MUILink>
          </CookieConsent>
        </Container>
        </body>
      </ThemeProvider>
    </AppRouterCacheProvider>
    </html>
  );
}

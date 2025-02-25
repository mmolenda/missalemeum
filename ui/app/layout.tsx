"use client"

import React, {useEffect, useState} from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import {appbarDarkGrey, getDesignTokens} from './theme';
import {AppBar, Container, createTheme, CssBaseline, Toolbar, Typography, useMediaQuery} from "@mui/material";

import { Link as MUILink } from "@mui/material";
import Logo from "@/components/Logo";
import MainMenu from "@/components/MainMenu";
import { Merriweather } from 'next/font/google'
import Link from "next/link";
import {myLocalStorage} from  "@/components/myLocalStorage";


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({
                                           children
                                         }: Readonly<{
  children: React.ReactNode;
}>) {
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
        <CssBaseline />
        <body>
        <Container disableGutters sx={{backgroundColor: "background.default"}}>
          <AppBar sx={{backgroundColor: appbarDarkGrey}}>
            <Toolbar>
              <MainMenu
                darkMode={darkMode}
                setDarkMode={setDarkMode}
                fontSize={fontSize}
                setFontSize={setFontSize}
              />
              <MUILink component={Link} href="/pl" sx={{display: "flex", textDecoration: "none"}} >
                <Logo width={28} height={28}/>
                <Typography variant="h1" component="div">Missale<br/>Meum</Typography>
              </MUILink>
            </Toolbar>
          </AppBar>
          {children}
        </Container>
        </body>
      </ThemeProvider>
    </AppRouterCacheProvider>
    </html>
  );
}

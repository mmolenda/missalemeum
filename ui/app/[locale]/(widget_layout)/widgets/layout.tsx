"use client"

import React from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import {getDesignTokens} from '@/components/designTokens';
import {Box, createTheme, CssBaseline} from "@mui/material";

import {Merriweather} from 'next/font/google'


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({
                                     children,
                                   }: {
  children: React.ReactNode;
}) {
  const queryParameters = new URLSearchParams(window.location.search)
  const fontSize = "medium"
  const lightOrDark = {"light": "light", "dark": "dark", "undefined": null}[queryParameters.get("theme") ?? "undefined"] || "light"
  let designTokens = getDesignTokens(lightOrDark, fontSize)
  designTokens.components.MuiAppBar.styleOverrides.root.height = "12px"
  const theme = React.useMemo(() => createTheme(designTokens), [lightOrDark, fontSize]);

  return (<html lang="en" className={merriweather.className}>
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <body>
        <Box sx={{pt: "12px"}}>
          {children}
        </Box>
        </body>
      </ThemeProvider>
    </AppRouterCacheProvider>
    </html>
  );
}

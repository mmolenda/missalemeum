"use client"

import React from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import {getDesignTokens} from '@/components/designTokens';
import {Box, createTheme, CssBaseline, PaletteMode} from "@mui/material";

import {Merriweather} from 'next/font/google'
import {useParams, useSearchParams} from "next/navigation";
import 'moment/locale/pl';
import moment from "moment/moment";


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({
                                     children,
                                   }: {
  children: React.ReactNode;
}) {
  const { locale } = useParams<{ locale?: string }>()
  moment.locale(locale)
  const searchParams = useSearchParams()
  const fontSize = "medium"
  const lightOrDark: PaletteMode =
  (["light", "dark"].includes(searchParams.get("theme") ?? "")
    ? (searchParams.get("theme") as PaletteMode)
    : "light")
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

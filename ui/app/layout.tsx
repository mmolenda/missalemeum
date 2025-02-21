import React from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import theme, {appbarDarkGrey} from './theme';
import {AppBar, Container, CssBaseline, Toolbar, Typography} from "@mui/material";

import { Link as MUILink } from "@mui/material";
import Logo from "@/components/Logo";
import MainMenu from "@/components/MainMenu";
import { Merriweather } from 'next/font/google'
import Link from "next/link";

const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default async function RootLayout({
                                           children
                                         }: Readonly<{
  children: React.ReactNode;
}>) {

  return (<html lang="en">
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <body>
        <Container disableGutters sx={{backgroundColor: "background.default"}}>
          <AppBar sx={{backgroundColor: appbarDarkGrey}}>
            <Toolbar>
              <MainMenu/>
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

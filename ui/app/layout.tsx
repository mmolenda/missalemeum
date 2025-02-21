import React from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider} from '@mui/material/styles';
import theme, {appbarDarkGrey} from './theme';
import {AppBar, Container, GlobalStyles, IconButton, Toolbar, Typography} from "@mui/material";

import { Link as MUILink } from "@mui/material";
import Logo from "../components/Logo";
import MMDrawer from "@/app/mmdrawer";
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
    <body>
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <Container disableGutters sx={{backgroundColor: "background.default"}}>
          <AppBar sx={{backgroundColor: appbarDarkGrey}}>
            <Toolbar>
              <MMDrawer/>
              <MUILink component={Link} href="/pl" sx={{display: "flex", textDecoration: "none"}} >
                <Logo width={28} height={28}/>
                <Typography variant="h1" component="div">Missale<br/>Meum</Typography>
              </MUILink>
            </Toolbar>
          </AppBar>
          {children}
        </Container>
      </ThemeProvider>
    </AppRouterCacheProvider>
    </body>
    </html>
  );
}

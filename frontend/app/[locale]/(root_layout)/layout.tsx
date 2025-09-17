"use client"

import React, {useEffect, useState} from "react";
import {AppRouterCacheProvider} from '@mui/material-nextjs/v15-appRouter';
import {ThemeProvider, type Theme} from '@mui/material/styles';
import {appbarDarkGrey, darkRedDarkMode, darkRedLightMode, getDesignTokens} from '@/components/designTokens';
import {
  AppBar,
  Box,
  Container,
  createTheme,
  CssBaseline,
  IconButton,
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
import {
  Locale,
  MSG_COOKIES,
  MSG_POLICY_DECLINE_BUTTON,
  MSG_POLICY_LINK,
  SURVEY_BANNER_COPY,
  SURVEY_LINK
} from "@/components/intl";
import {useParams} from "next/navigation";
import moment from "moment";
import 'moment/locale/pl';
import Announcement from "@/components/Announcement";
import CloseIcon from "@mui/icons-material/Close";
import {
  BANNER_HEIGHT,
  BANNER_STORAGE_KEY,
  isBannerExpired,
  getAppBarHeightFromTheme,
  getBannerExpiryDate
} from "@/components/layoutMetrics";


const DEFAULT_LOCALE: Locale = "en";
const SUPPORTED_LOCALES: Locale[] = ["pl", "en"];

const toLocale = (value?: string): Locale => {
  if (value && SUPPORTED_LOCALES.includes(value as Locale)) {
    return value as Locale;
  }
  return DEFAULT_LOCALE;
};


const merriweather = Merriweather({
  subsets: ['latin'],
  weight: ["300", "400"]
})


export default function RootLayout({children}: { children: React.ReactNode}) {
  const { locale } = useParams<{ locale?: string }>()
  const lang = toLocale(locale)
  moment.locale(lang)
  const [darkMode, setDarkMode] = useState<boolean | undefined>(false)
  const [fontSize, setFontSize] = useState<string>("medium")
  const [announcementOpened, setAnnouncementOpened] = useState<boolean>(false)
  const [bannerOpen, setBannerOpen] = useState<boolean>(false)
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
  const bannerExpired = isBannerExpired()

  useEffect(() => {
    setDarkMode({
      "true": true,
      "false": false,
      "undefined": undefined
    }[myLocalStorage.getItem("darkMode") ?? "undefined"])
    setFontSize(myLocalStorage.getItem("fontSize") ?? "medium")
  }, []);

  useEffect(() => {
    if (bannerExpired) {
      setBannerOpen(false)
      return
    }

    const bannerDismissed = myLocalStorage.getItem(BANNER_STORAGE_KEY) === "true";

    setBannerOpen(!bannerDismissed);
  }, [bannerExpired]);

  const getThemeMode = () => {
    return ((darkMode == undefined && prefersDark) || darkMode) ? "dark" : "light"
  }
  const mode = getThemeMode()
  // const theme = React.useMemo(() => createTheme(getDesignTokens(mode, fontSize)), [mode, fontSize]);
  const theme = createTheme(getDesignTokens(mode, fontSize));
  const appBarHeight = getAppBarHeightFromTheme(theme);
  const bannerCopy = SURVEY_BANNER_COPY[lang];
  const surveyLink = SURVEY_LINK[lang];
  const bannerVisible = bannerOpen && !bannerExpired;
  const contentTopPadding = (appBarHeight * 2) + (bannerVisible ? BANNER_HEIGHT : 0);

  const handleBannerClose = () => {
    if (bannerExpired) {
      return
    }
    myLocalStorage.setItem(BANNER_STORAGE_KEY, "true")
    setBannerOpen(false)
  }

  useEffect(() => {
    if (!bannerVisible) {
      return
    }

    const expiryDate = getBannerExpiryDate()
    if (!expiryDate) {
      return
    }

    const now = new Date()
    if (expiryDate <= now) {
      setBannerOpen(false)
      return
    }

    const timeoutId = window.setTimeout(() => {
      setBannerOpen(false)
    }, expiryDate.getTime() - now.getTime())

    return () => window.clearTimeout(timeoutId)
  }, [bannerVisible])

  return (<html lang="en" className={merriweather.className} translate="no">
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline/>
        <body>
        <Announcement
          lang={lang}
          version={process.env.NEXT_PUBLIC_BUILD_VERSION || "noversion"}
          debug={false}
          open={announcementOpened}
          setOpen={setAnnouncementOpened} />
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

          {bannerVisible && (
            <Box
              sx={(theme: Theme) => ({
                position: 'fixed',
                top: `${appBarHeight}px`,
                left: 0,
                right: 0,
                backgroundColor: theme.palette.mode === 'dark' ? theme.palette.background.paper : theme.palette.background.default,
                borderBottom: `1px solid ${theme.palette.divider}`,
                zIndex: Math.max(0, theme.zIndex.appBar - 1),
              })}
            >
              <ContainerMedium
                disableGutters
                sx={(theme: Theme) => ({
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  gap: 2,
                  px: {xs: 2, sm: 3},
                  minHeight: `${BANNER_HEIGHT}px`,
                  color: theme.palette.mode === 'dark' ? theme.palette.common.white : theme.palette.common.black,
                })}
              >
                <Typography
                  variant="body2"
                  sx={{
                    fontWeight: 500,
                  }}
                >
                  <MUILink
                    href={surveyLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    underline="always"
                    sx={(theme: Theme) => ({
                      color: theme.palette.mode === 'dark' ? darkRedDarkMode : darkRedLightMode,
                    })}
                  >
                    {bannerCopy.linkText}
                  </MUILink>
                  {bannerCopy.suffix}
                </Typography>
                <IconButton
                  aria-label="Zamknij baner ankiety"
                  size="small"
                  color="inherit"
                  onClick={handleBannerClose}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </ContainerMedium>
            </Box>
          )}

          <ContainerMedium disableGutters sx={{display: 'flex', overflow: 'hidden', height: "100%"}}>

            <Box
              id="content"
              sx={{
                overflowY: 'scroll',
                width: '100%',
                ml: 0,
                pt: `${contentTopPadding}px`,
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

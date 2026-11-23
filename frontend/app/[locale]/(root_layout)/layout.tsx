"use client"

import React, {useEffect, useRef, useState} from "react";
import {useMeasuredHeight} from "@/components/useMeasuredHeight";
import {AppRouterCacheProvider} from "@mui/material-nextjs/v15-appRouter";
import {ThemeProvider, type Theme} from "@mui/material/styles";
import {
  appbarDarkGrey,
  darkRedDarkMode,
  darkRedLightMode,
  getDesignTokens,
} from "@/components/designTokens";
import {
  AppBar,
  Box,
  Container,
  createTheme,
  CssBaseline,
  IconButton,
  Toolbar,
  Typography,
  useMediaQuery,
} from "@mui/material";

import {Link as MUILink} from "@mui/material";
import Logo from "@/components/Logo";
import MainMenu from "@/components/MainMenu";
import GlobalSearch from "@/components/GlobalSearch";
import Link from "next/link";
import {myLocalStorage} from "@/components/myLocalStorage";
import {ContainerMedium} from "@/components/styledComponents/ContainerMedium";
import {CookieConsent} from "react-cookie-consent";
import {
  Locale,
  MSG_COOKIES,
  MSG_POLICY_DECLINE_BUTTON,
  MSG_POLICY_LINK,
  BANNER_COPY,
} from "@/components/intl";
import {useParams} from "next/navigation";
import moment from "moment";
import "moment/locale/pl";
import Announcement from "@/components/Announcement";
import CloseIcon from "@mui/icons-material/Close";
import PrintIcon from "@mui/icons-material/Print";
import {
  BANNER_ENABLED,
  BANNER_HEIGHT,
  BANNER_STORAGE_KEY,
  getAppBarHeightFromTheme,
} from "@/components/layoutMetrics";


const DEFAULT_LOCALE: Locale = "en";
const SUPPORTED_LOCALES: Locale[] = ["pl", "en"];

const toLocale = (value?: string): Locale => {
  if (value && SUPPORTED_LOCALES.includes(value as Locale)) {
    return value as Locale;
  }
  return DEFAULT_LOCALE;
};


export default function RootLayout({children}: { children: React.ReactNode}) {
  const { locale } = useParams<{ locale?: string }>()
  const lang = toLocale(locale)
  moment.locale(lang)
  const [darkMode, setDarkMode] = useState<boolean | undefined>(false)
  const [fontSize, setFontSize] = useState<string>("medium")
  const [announcementOpened, setAnnouncementOpened] = useState<boolean>(false)
  const [bannerOpen, setBannerOpen] = useState<boolean>(false)
  const bannerRef = useRef<HTMLDivElement>(null);
  const cookieRef = useRef<HTMLDivElement>(null);
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')

  useEffect(() => {
    setDarkMode({
      "true": true,
      "false": false,
      "undefined": undefined
    }[myLocalStorage.getItem("darkMode") ?? "undefined"])
    setFontSize(myLocalStorage.getItem("fontSize") ?? "medium")
  }, []);

  useEffect(() => {
    if (!BANNER_ENABLED) {
      setBannerOpen(false);
      return;
    }
    const bannerDismissed = myLocalStorage.getItem(BANNER_STORAGE_KEY) === "true";
    setBannerOpen(!bannerDismissed);
  }, []);

  const getThemeMode = () => {
    return ((darkMode == undefined && prefersDark) || darkMode) ? "dark" : "light"
  }
  const mode = getThemeMode()
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode, fontSize)), [mode, fontSize]);
  const appBarHeight = getAppBarHeightFromTheme(theme);
  const bannerCopy = BANNER_COPY[lang];
  const bannerVisible = BANNER_ENABLED && bannerOpen;
  useMeasuredHeight(bannerRef, "--announcement-banner-height", bannerVisible);
  useMeasuredHeight(cookieRef, "--cookie-consent-height");
  const contentTopPadding = `calc(${appBarHeight}px + var(--announcement-banner-height, 0px) + var(--list-controls-height, ${appBarHeight}px))`;
  const closeBannerLabel = lang === "pl" ? "Zamknij baner PDF" : "Dismiss PDF banner";

  const handleBannerClose = () => {
    myLocalStorage.setItem(BANNER_STORAGE_KEY, "true")
    setBannerOpen(false)
  }

  return (
    <AppRouterCacheProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Announcement
          lang={lang}
          version={process.env.NEXT_PUBLIC_BUILD_VERSION || "noversion"}
          debug={false}
          open={announcementOpened}
          setOpen={setAnnouncementOpened}
        />
        <Container disableGutters sx={{backgroundColor: "background.default", minHeight: "100vh"}}>
          <Box component="a" href="#content" onClick={() => document.getElementById("content")?.focus()} sx={{
            position: "fixed", top: 8, left: 8, transform: "translateY(-200%)",
            zIndex: theme.zIndex.modal + 1, p: 1.5, bgcolor: "background.paper", color: "text.primary",
            "&:focus": {transform: "none"},
          }}>
            {lang === "pl" ? "Przejdź do treści" : "Skip to content"}
          </Box>
          <AppBar sx={{backgroundColor: appbarDarkGrey}}>
            <Toolbar>
              <MainMenu
                lang={lang}
                darkMode={darkMode}
                setDarkMode={setDarkMode}
                fontSize={fontSize}
                setFontSize={setFontSize}
              />
              <MUILink component={Link} href={`/${lang}`} sx={{display: "flex", textDecoration: "none"}}>
                <Logo width={28} height={28} />
                <Typography variant="h1" component="div">
                  Missale
                  <br />
                  Meum
                </Typography>
              </MUILink>
              <GlobalSearch lang={lang} />
            </Toolbar>
          </AppBar>

          {bannerVisible && (
            <Box
              ref={bannerRef}
              sx={(theme: Theme) => ({
                position: "fixed",
                top: `${appBarHeight}px`,
                left: 0,
                right: 0,
                backgroundColor:
                  theme.palette.mode === "dark"
                    ? theme.palette.background.paper
                    : theme.palette.background.default,
                borderBottom: `1px solid ${theme.palette.divider}`,
                zIndex: Math.max(0, theme.zIndex.appBar - 1),
              })}
            >
              <ContainerMedium
                disableGutters
                sx={(theme: Theme) => ({
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 2,
                  px: {xs: 2, sm: 3},
                  minHeight: `${BANNER_HEIGHT}px`,
                  color:
                    theme.palette.mode === "dark"
                      ? theme.palette.common.white
                      : theme.palette.common.black,
                })}
              >
                <Typography
                  variant="body2"
                  sx={{
                    display: "block",
                    fontWeight: 500,
                    gap: 1,
                  }}
                >
                  <Box
                    component="span"
                    sx={(theme: Theme) => ({
                      color:
                        theme.palette.mode === "dark" ? darkRedDarkMode : darkRedLightMode,
                      fontWeight: 700,
                    })}
                  >
                    {bannerCopy.highlight}
                  </Box>{" "}
                  <Box component="span">{bannerCopy.message}</Box>
                  <PrintIcon fontSize="small" sx={{ml: 0.5}} />
                </Typography>
                <IconButton
                  aria-label={closeBannerLabel}
                  size="small"
                  color="inherit"
                  onClick={handleBannerClose}
                >
                  <CloseIcon fontSize="small" />
                </IconButton>
              </ContainerMedium>
            </Box>
          )}

          <ContainerMedium disableGutters sx={{display: "flex", overflow: "hidden", height: "100%"}}>
            <Box
              id="content"
              component="main"
              tabIndex={-1}
              sx={{
                overflowY: "scroll",
                width: "100%",
                ml: 0,
                pt: contentTopPadding,
                height: "100%",
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
                fontSize: "0.9rem",
              }}
            >
              ☩ A. M. D. G. ☩
            </Typography>
            <Typography
              sx={{
                py: "2rem",
                color: theme.palette.mode === "dark" ? "primary.dark" : "primary.light",
                fontSize: "0.75rem",
              }}
            >
              {process.env.NEXT_PUBLIC_BUILD_VERSION}
            </Typography>
          </ContainerMedium>
        <Box ref={cookieRef} sx={{position: "fixed", bottom: 0, left: 0, right: 0, zIndex: 999}}>
        <CookieConsent
          style={{position: "static"}}
          contentStyle={{flex: "1 1 240px", minWidth: 0}}
          cookieName="MMCookieConsent"
          enableDeclineButton
          declineButtonStyle={{background: appbarDarkGrey}}
          buttonStyle={{background: "#e49086"}}
          declineButtonText={MSG_POLICY_DECLINE_BUTTON[lang]}
          ariaDeclineLabel={MSG_POLICY_DECLINE_BUTTON[lang]}
          ariaAcceptLabel={lang === "pl" ? "Akceptuję ciasteczka" : "Accept cookies"}
          buttonText="OK">
          {MSG_COOKIES[lang]}
          <MUILink component={Link} href={`/${lang}/supplement/privacy-policy`} target="_blank">
            {MSG_POLICY_LINK[lang]}
          </MUILink>
        </CookieConsent>
        </Box>
        </Container>
      </ThemeProvider>
    </AppRouterCacheProvider>
  );
}

"use client"

import React, {useEffect, useRef, useState} from "react";
import {useMeasuredHeight} from "@/components/useMeasuredHeight";
import {AppRouterCacheProvider} from "@mui/material-nextjs/v15-appRouter";
import {ThemeProvider, type Theme} from "@mui/material/styles";
import {
  appbarDarkGrey,
  darkGraphite,
  darkRedDarkMode,
  darkRedLightMode,
  getDesignTokens,
} from "@/components/designTokens";
import {
  AppBar,
  Box,
  Button,
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
import {useParams, usePathname} from "next/navigation";
import moment from "moment";
import "moment/locale/pl";
import Announcement from "@/components/Announcement";
import CloseIcon from "@mui/icons-material/Close";
import {
  BANNER_EXPIRES_AT,
  BANNER_HEIGHT,
  BANNER_STORAGE_KEY,
  isBannerActive,
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
  const isCalendar = /^\/(pl|en)\/calendar\/?$/.test(usePathname());
  const lang = toLocale(locale)
  moment.locale(lang)
  const [darkMode, setDarkMode] = useState<boolean | undefined>(false)
  const [fontSize, setFontSize] = useState<string>("medium")
  const [announcementOpened, setAnnouncementOpened] = useState<boolean>(false)
  const [bannerOpen, setBannerOpen] = useState<boolean>(false)
  const [searchOpened, setSearchOpened] = useState(false);
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
    const updateBanner = () => {
      const bannerDismissed = myLocalStorage.getItem(BANNER_STORAGE_KEY) === "true";
      setBannerOpen(isBannerActive() && !bannerDismissed);
    };
    updateBanner();
    const remaining = Date.parse(BANNER_EXPIRES_AT) - Date.now();
    if (remaining <= 0) return;
    const timeout = window.setTimeout(updateBanner, Math.min(remaining, 2_147_483_647));
    return () => window.clearTimeout(timeout);
  }, []);


  const getThemeMode = () => {
    return ((darkMode == undefined && prefersDark) || darkMode) ? "dark" : "light"
  }
  const mode = getThemeMode()
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode, fontSize)), [mode, fontSize]);
  const appBarHeight = getAppBarHeightFromTheme(theme);
  const bannerCopy = BANNER_COPY[lang];
  const bannerVisible = bannerOpen;
  useMeasuredHeight(bannerRef, "--announcement-banner-height", bannerVisible);
  useMeasuredHeight(cookieRef, "--cookie-consent-height");
  const contentTopPadding = `calc(${appBarHeight}px + var(--announcement-banner-height, 0px) + var(--list-controls-height, ${appBarHeight}px))`;

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
          <AppBar sx={{
            backgroundColor: mode === "dark" ? darkGraphite.header : appbarDarkGrey,
            ...(mode === "dark" && {backgroundImage: "none"}),
            ...(isCalendar && {
              boxShadow: "none",
              "& .MuiToolbar-root": {px: {xs: 2, sm: 2.5}},
              "& .MuiIconButton-root": {
                width: 44, height: 44, borderRadius: 1,
                "&:hover": {backgroundColor: "rgba(255,255,255,0.08)"},
              },
              "& a:focus-visible, & button:focus-visible": {
                outline: `2px solid ${darkRedDarkMode}`, outlineOffset: -2,
              },
            }),
          }}>
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
              <GlobalSearch lang={lang} open={searchOpened} setOpen={setSearchOpened} />
            </Toolbar>
          </AppBar>

          {bannerVisible && (
            <Box
              ref={bannerRef}
              role="region"
              aria-label={bannerCopy.highlight}
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
                  gap: 1,
                  px: {xs: 2, sm: 3},
                  py: 1,
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
                    flex: 1,
                    minWidth: 0,
                    fontWeight: 500,
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
                  {" "}<Button size="small" onClick={() => setSearchOpened(true)} sx={{p: 0, minWidth: 0, verticalAlign: "baseline"}}>{bannerCopy.action}</Button>
                </Typography>
                <IconButton
                  aria-label={bannerCopy.dismiss}
                  size="small"
                  color="inherit"
                  onClick={handleBannerClose}
                  sx={{flexShrink: 0, alignSelf: "flex-start"}}
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

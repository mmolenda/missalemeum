'use client'

import {
    Box,
    Divider,
    Drawer,
    IconButton,
    ListItem,
    ListItemButton,
    ToggleButton,
    ToggleButtonGroup
} from "@mui/material";
import {
  Locale,
  MENUITEM_ANNOUNCEMENTS,
  MENUITEM_CANTICUM,
  MENUITEM_INFO,
  MENUITEM_ORATIO,
  MENUITEM_ORDO,
  MENUITEM_PROPER,
  MENUITEM_SUPPLEMENT,
  MENUITEM_SURVEY,
  MENUITEM_VOTIVE,
  SURVEY_LINK
} from "@/components/intl";
import Link from "next/link";
import React, {Dispatch, SetStateAction, useEffect, useState} from "react";
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from "@mui/icons-material/Close";
import List from "@mui/material/List";
import DrawerListItemText from "@/components/styledComponents/DrawerListItemText";
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import {myLocalStorage} from "./myLocalStorage";
import {getBannerExpiryDate, isBannerExpired} from "@/components/layoutMetrics";
import {usePathname} from "next/navigation";


type LeftHandMenuProps = {
  lang: Locale
  toggleDrawer: (open: boolean) => () => void
  toggleDarkMode: (darkModeNew: boolean) => void
  darkMode: boolean | undefined
  switchFontSize: (fontSizeNew: string) => void
  fontSize: string
  surveyAvailable: boolean
}

const LeftHandMenu = ({
  lang,
  toggleDrawer,
  toggleDarkMode,
  darkMode,
  switchFontSize,
  fontSize,
  surveyAvailable
}: LeftHandMenuProps) => {
  const pathname = usePathname()
  const isMenuitemSelected = (route: string) => {
    const normalisedRoute = route.replace(/\/$/, "");
    const normalisedPath = pathname.replace(/\/$/, "");
    if (normalisedPath === normalisedRoute) {
      return true;
    }
    if (normalisedRoute.endsWith('/calendar')) {
      if (!normalisedPath.startsWith(`${normalisedRoute}/`)) {
        return false;
      }
      const remainder = normalisedPath.slice(normalisedRoute.length + 1);
      return remainder.length > 0 && /^[\\d-]+$/.test(remainder);
    }
    return normalisedPath.startsWith(`${normalisedRoute}/`);
  }

  const menuItems: Array<{label: string; route: string; external?: boolean}> = [
    {label: MENUITEM_PROPER[lang], route: `/${lang}/calendar`},
    {label: MENUITEM_ORDO[lang], route: `/${lang}/ordo`},
    {label: MENUITEM_VOTIVE[lang], route: `/${lang}/votive`},
    {label: MENUITEM_ORATIO[lang], route: `/${lang}/oratio`},
    {label: MENUITEM_CANTICUM[lang], route: `/${lang}/canticum`},
    {label: MENUITEM_SUPPLEMENT[lang], route: `/${lang}/supplement/index`},
    {label: MENUITEM_INFO[lang], route: `/${lang}/supplement/info`},
    {label: MENUITEM_ANNOUNCEMENTS[lang], route: `/${lang}/supplement/announcements`}
  ]

  if (surveyAvailable) {
    menuItems.splice(7, 0, {label: MENUITEM_SURVEY[lang], route: SURVEY_LINK[lang], external: true})
  }

  return (
    <Box
      sx={{width: 300}}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <IconButton onClick={toggleDrawer(false)}>
        <CloseIcon />
      </IconButton>
      <List>
        {menuItems.map(({label, route, external}) => (
          <ListItem key={label}>
            <ListItemButton
              {...(external ? {
                component: "a",
                href: route,
                target: "_blank",
                rel: "noopener noreferrer"
              } : {
                component: Link,
                href: route
              })}
              selected={!external && isMenuitemSelected(route)}
            >
              <DrawerListItemText prim={label}/>
            </ListItemButton>
          </ListItem>
        ))}
        <Divider/>
        <ListItem key="lang">
          <ToggleButtonGroup color="secondary" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => myLocalStorage.setItem("lang", "en")} href="/en" value="en" selected={lang === "en"}>English</ToggleButton>
            <ToggleButton onClick={() => myLocalStorage.setItem("lang", "pl")} href="/pl" value="pl" selected={lang === "pl"}>Polski</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="theme">
          <ToggleButtonGroup color="secondary" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => toggleDarkMode(false)} value="light" selected={darkMode==false}><LightModeIcon /></ToggleButton>
            <ToggleButton onClick={() => toggleDarkMode(true)} value="dark" selected={darkMode}><DarkModeIcon /></ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="font">
          <ToggleButtonGroup color="secondary" aria-label="outlined secondary button group">
            <ToggleButton sx={{px: "1rem", fontSize: "0.5rem", fontWeight: "600"}} onClick={() => switchFontSize("small")} value="small" selected={fontSize === "small"}>A</ToggleButton>
            <ToggleButton sx={{px: "1rem", fontWeight: "600"}} onClick={() => switchFontSize("medium")} value="medium" selected={["medium", undefined, null].includes(fontSize)}>A</ToggleButton>
            <ToggleButton sx={{px: "1rem", fontSize: "1.25rem", fontWeight: "600"}} onClick={() => switchFontSize("large")} value="large" selected={fontSize === "large"}>A</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
      </List>
    </Box>
)}



export default function MainMenu({
  lang,
  fontSize,
  darkMode,
  setDarkMode,
  setFontSize
                                 }: {
  lang: Locale
  fontSize: string
  darkMode: boolean | undefined
  setDarkMode: Dispatch<SetStateAction<boolean | undefined>>
  setFontSize: Dispatch<SetStateAction<string>>
}) {
  const [drawerOpened, setDrawerOpened] = useState(false)
  const [surveyAvailable, setSurveyAvailable] = useState(!isBannerExpired())
  useEffect(() => {
    const expired = isBannerExpired()
    if (expired) {
      setSurveyAvailable(false)
      return
    }

    setSurveyAvailable(true)

    const expiryDate = getBannerExpiryDate()
    if (!expiryDate) {
      return
    }

    const now = new Date()
    if (expiryDate <= now) {
      setSurveyAvailable(false)
      return
    }

    const timeoutId = window.setTimeout(() => {
      setSurveyAvailable(false)
    }, expiryDate.getTime() - now.getTime())

    return () => window.clearTimeout(timeoutId)
  }, [])
  const toggleDrawer = (open: boolean) => () => {
    setDrawerOpened(open)
  };

  const toggleDarkMode = (darkModeNew: boolean) => {
    if (darkModeNew === false && darkMode !== false) {
      setDarkMode(false)
      myLocalStorage.setItem("darkMode", "false")
    } else if (darkModeNew === true && darkMode !== true) {
      setDarkMode(true)
      myLocalStorage.setItem("darkMode", "true")
    } else {
      setDarkMode(undefined)
      myLocalStorage.removeItem("darkMode")
    }
  }

  const switchFontSize = (fontSizeNew: string) => {
    setFontSize(fontSizeNew)
    myLocalStorage.setItem("fontSize", fontSizeNew)
  }

    return(<>
        <IconButton
            size="large"
            edge="start"
            aria-label="menu"
            sx={{color: "yellowish.main"}}
            onClick={toggleDrawer(true)}
        >
            {/* fixed fontSize to prevent resizing when switching font size from the menu */}
            <MenuIcon sx={{fontSize: 24}}/>
        </IconButton>
        <Drawer
            variant="temporary"
            disablePortal={true}
            open={drawerOpened}
            onClose={toggleDrawer(false)}
            keepMounted={true}
        >
            <LeftHandMenu
                lang={lang}
                toggleDrawer={toggleDrawer}
                darkMode={darkMode}
                toggleDarkMode={toggleDarkMode}
                fontSize={fontSize}
                switchFontSize={switchFontSize}
                surveyAvailable={surveyAvailable}
            />
        </Drawer>
    </>)
}

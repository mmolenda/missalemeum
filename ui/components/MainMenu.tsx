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
  MENUITEM_CANTICUM, MENUITEM_INFO,
  MENUITEM_ORATIO,
  MENUITEM_ORDO,
  MENUITEM_PROPER,
  MENUITEM_SUPPLEMENT,
  MENUITEM_VOTIVE, MENUITEM_WHATSNEW
} from "@/components/intl";
import Link from "next/link";
import React, {Dispatch, SetStateAction, useState} from "react";
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from "@mui/icons-material/Close";
import List from "@mui/material/List";
import DrawerListItemText from "@/components/styledComponents/DrawerListItemText";
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import {myLocalStorage} from "./myLocalStorage";
import {usePathname} from "next/navigation";


const LeftHandMenu = ({
  lang,
  toggleDrawer,
  toggleDarkMode,
  darkMode,
  switchFontSize,
  fontSize
                      }: {
  lang: string
  toggleDrawer: any
  toggleDarkMode: any
  darkMode: boolean | undefined
  switchFontSize: any
  fontSize: string
}) => {
  const pathname = usePathname()
  const isMenuitemSelected = (route) => {
    let routeSplit = route.split("/")
    let pathSplit = pathname.split("/")
    let datePattern = /^[\d-]+$/
    console.log(pathname, route, routeSplit, pathname.startsWith(route))
    if (routeSplit.length < 3) {
      // /pl or /pl/2022-02-02
      return route === pathname || datePattern.test(pathSplit[pathSplit.length - 1])
    }
    return pathname.startsWith(route)
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
        {Object.entries({
          [MENUITEM_PROPER[lang as Locale]]: `/${lang}`,
          [MENUITEM_ORDO[lang as Locale]]: `/${lang}/ordo`,
          [MENUITEM_VOTIVE[lang as Locale]]: `/${lang}/votive`,
          [MENUITEM_ORATIO[lang as Locale]]: `/${lang}/oratio`,
          [MENUITEM_CANTICUM[lang as Locale]]: `/${lang}/canticum`,
          [MENUITEM_SUPPLEMENT[lang as Locale]]: `/${lang}/supplement/index`,
          [MENUITEM_INFO[lang as Locale]]: `/${lang}/supplement/info`
        }).map(([label, route]) => (
          <ListItem key={label}>
            <ListItemButton
              component={Link}
              href={route}
              selected={isMenuitemSelected(route)}
            >
              <DrawerListItemText prim={label}/>
            </ListItemButton>
          </ListItem>
        ))}
        <ListItem key="whatsnew">
          <ListItemButton
            component={Link}
            href={"https://github.com/mmolenda/missalemeum/releases"}
            target={"_blank"}
          >
            <DrawerListItemText prim={MENUITEM_WHATSNEW[lang as Locale]}/>
          </ListItemButton>
        </ListItem>
        <Divider/>
        <ListItem key="lang">
          <ToggleButtonGroup color="secondary" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => myLocalStorage.setItem("lang", "en")} href="/en" value="en" selected={lang === "en"}>English</ToggleButton>
            <ToggleButton onClick={() => myLocalStorage.setItem("lang", "pl")} href="/pl" value="pl" selected={lang === "pl"}>Polski</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="theme">
          <ToggleButtonGroup color="secondary" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => toggleDarkMode(false)} value="light" selected={!darkMode}><LightModeIcon /></ToggleButton>
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
  lang: string
  fontSize: string
  darkMode: boolean | undefined
  setDarkMode: Dispatch<SetStateAction<boolean | undefined>>
  setFontSize: Dispatch<SetStateAction<string>>
}) {
    const [drawerOpened, setDrawerOpened] = useState(false)
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
            />
        </Drawer>
    </>)
}
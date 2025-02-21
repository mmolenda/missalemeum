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
    MENUITEM_CANTICUM, MENUITEM_INFO,
    MENUITEM_ORATIO,
    MENUITEM_ORDO,
    MENUITEM_PROPER,
    MENUITEM_SUPPLEMENT,
    MENUITEM_VOTIVE, MENUITEM_WHATSNEW
} from "@/components/intl";
import Link from "next/link";
import React, {useState} from "react";
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from "@mui/icons-material/Close";
import List from "@mui/material/List";
import DrawerListItemText from "@/components/styledComponents/DrawerListItemText";
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import { useParams } from 'next/navigation'



const LeftHandMenu = (props) => {
  return (
    <Box
      sx={{width: 300}}
      role="presentation"
      onClick={props.toggleDrawer(false)}
      onKeyDown={props.toggleDrawer(false)}
    >
      <IconButton onClick={props.toggleDrawer(false)}>
        <CloseIcon />
      </IconButton>
      <List>
        {Object.entries({
          [MENUITEM_PROPER[props.lang]]: `/${props.lang}`,
          [MENUITEM_ORDO[props.lang]]: `/${props.lang}/ordo`,
          [MENUITEM_VOTIVE[props.lang]]: `/${props.lang}/votive`,
          [MENUITEM_ORATIO[props.lang]]: `/${props.lang}/oratio`,
          [MENUITEM_CANTICUM[props.lang]]: `/${props.lang}/canticum`,
          [MENUITEM_SUPPLEMENT[props.lang]]: `/${props.lang}/supplement/index`,
          [MENUITEM_INFO[props.lang]]: `/${props.lang}/supplement/info`
        }).map(([label, route]) => (
          <ListItem key={label}>
            <ListItemButton
              component={Link}
              to={route}
            >
              <DrawerListItemText primary={label}/>
            </ListItemButton>
          </ListItem>
        ))}
        <ListItem key="whatsnew">
          <ListItemButton onClick={() => props.setReleaseNotesOpened(true)}>
            <DrawerListItemText primary={MENUITEM_WHATSNEW[props.lang]}/>
          </ListItemButton>
        </ListItem>
        <Divider/>
        <ListItem key="lang">
          <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">
            <ToggleButton href="/en" value="en" selected={props.lang === "en"}>English</ToggleButton>
            <ToggleButton href="/pl" value="pl" selected={props.lang === "pl"}>Polski</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="theme">
          <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => props.toggleDarkMode(false)} value="light" selected={props.darkMode === false}><LightModeIcon /></ToggleButton>
            <ToggleButton onClick={() => props.toggleDarkMode(true)} value="dark" selected={props.darkMode === true}><DarkModeIcon /></ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="font">
          <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">
            <ToggleButton sx={{px: "1rem", fontSize: "0.5rem", fontWeight: "600"}} onClick={() => props.switchFontSize("small")} value="small" selected={props.fontSize === "small"}>A</ToggleButton>
            <ToggleButton sx={{px: "1rem", fontWeight: "600"}} onClick={() => props.switchFontSize("medium")} value="medium" selected={["medium", undefined, null].includes(props.fontSize)}>A</ToggleButton>
            <ToggleButton sx={{px: "1rem", fontSize: "1.25rem", fontWeight: "600"}} onClick={() => props.switchFontSize("large")} value="large" selected={props.fontSize === "large"}>A</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
      </List>
    </Box>
)}



export default function MainMenu(props) {
    const params = useParams()
    const lang = params.lang
    const darkMode = false
    const fontSize = "medium"
    const [drawerOpened, setDrawerOpened] = useState(false)
  const toggleDrawer = (open) => () => {
    setDrawerOpened(open)
  };
  const toggleDarkMode = (open) => () => {
      // https://medium.com/@aashekmahmud/implementing-dark-and-light-mode-themes-in-next-js-a-comprehensive-guide-bf2c34ecd50d
    return false
  };
  const switchFontSize = (open) => () => {
    return false
  };
  const setReleaseNotesOpened = (open) => () => {
    return false
  };


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
                setReleaseNotesOpened={setReleaseNotesOpened}
            />
        </Drawer>
    </>)
}
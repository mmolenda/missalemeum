import './App.css'
import React, {useEffect, useState} from 'react'
import {
  Routes,
  Route,
  Outlet,
  NavLink,
  Navigate,
  useParams,
  useLocation,
  useNavigate,
  Link as RouterLink
} from "react-router-dom";
import { CookieConsent, getCookieConsentValue } from "react-cookie-consent";
import Proper from "./components/Proper";
import Votive from "./components/Votive";
import Oratio from "./components/Oratio";
import Canticum from "./components/Canticum";
import Ordo from "./components/Ordo";
import {
  AppBar,
  Box,
  Container,
  createTheme, Divider,
  Drawer, GlobalStyles,
  IconButton, Link, ListItemButton,
  ThemeProvider, ToggleButton, ToggleButtonGroup,
  Toolbar,
  Typography, useMediaQuery
} from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import CloseIcon from '@mui/icons-material/Close';
import LightModeIcon from '@mui/icons-material/LightMode';
import DarkModeIcon from '@mui/icons-material/DarkMode';
import DrawerListItemText from "./components/styledComponents/DrawerListItemText";
import {
  MENUITEM_CANTICUM,
  MENUITEM_INFO,
  MENUITEM_ORATIO,
  MENUITEM_ORDO,
  MENUITEM_PROPER, MENUITEM_SUPPLEMENT,
  MENUITEM_VOTIVE, MSG_COOKIES, MSG_POLICY_DECLINE_BUTTON, MSG_POLICY_LINK
} from "./intl";
import NotFound from "./components/NotFound";
import Error from "./components/Error";
import Supplement from "./components/Supplement";
import Logo from "./components/Logo";
import {ContainerMedium} from "./components/styledComponents/ContainerMedium";
import WidgetPropers from "./components/WidgetPropers";
import {appbarDarkGrey, getDesignTokens} from "./designTokens";

const debug = process.env.REACT_APP_DEBUG === "true"
const supportedLanguages = ["en", "pl"]
const defaultLanguage = localStorage.getItem("lang") || (navigator.languages.includes("pl")) ? "pl" : "en"

const App = () => {
  return (
    <Routes>
      <Route element={<Layout/>}>
        <Route index element={ <Navigate replace to={`/${defaultLanguage}`} /> }/>
        <Route exact path="/" element={<Proper/>}/>
        <Route path=":lang" element={<Proper/>}/>
        <Route path=":lang/:id" element={<Proper/>}/>
        <Route path=":lang/ordo" element={<Ordo/>}/>
        <Route path=":lang/votive" element={<Votive/>}/>
        <Route path=":lang/votive/:id" element={<Votive/>}/>
        <Route path=":lang/oratio" element={<Oratio/>}/>
        <Route path=":lang/oratio/:id" element={<Oratio/>}/>
        <Route path=":lang/canticum" element={<Canticum/>}/>
        <Route path=":lang/canticum/:id" element={<Canticum/>}/>
        <Route path=":lang/supplement/:id" element={<Supplement/>}/>
        <Route path=":lang/error" element={<Error/>}/>
        <Route path=":lang/404" element={<NotFound/>}/>
        <Route path=":lang/*" element={<NotFound/>}/>
      </Route>
      <Route path=":lang/widget/propers" element={<WidgetPropers/>}/>
    </Routes>
  );
};


const Layout = () => {
  const version = document.querySelector('meta[name="version"]').content
  const {lang} = useParams()
  const navigate = useNavigate()
  const location = useLocation();
  const [drawerOpened, setDrawerOpened] = useState(false)
  const [darkMode, setDarkMode] = useState(undefined)
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
  const toggleDrawer = (open) => () => {
    setDrawerOpened(open)
  };

  useEffect(() => {
    if (lang !== undefined && !supportedLanguages.includes(lang)) {
      navigate(`/${defaultLanguage}/404`)
    }
    setDarkMode({"true": true, "false": false, null: undefined}[localStorage.getItem("darkMode")])
  }, [lang, navigate])

  useEffect(() => {
    registerPageView()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location])

  const registerPageView = () => {
    if (getCookieConsentValue() === "true" && window.location.hostname.endsWith("missalemeum.com")) {
      window.gtag("event", "page_view", {
        page_path: location.pathname + location.search + location.hash,
        page_search: location.search,
        page_hash: location.hash,
      })
    }
  }

  const getThemeMode = () => {
    return ((darkMode === undefined && prefersDark) || darkMode) ? "dark" : "light"
  }

  const toggleDarkMode = (darkModeNew) => {
    if (darkModeNew === false && darkMode !== false) {
      setDarkMode(false)
      localStorage.setItem("darkMode", "false")
    } else if (darkModeNew === true && darkMode !== true) {
      setDarkMode(true)
      localStorage.setItem("darkMode", "true")
    } else {
      setDarkMode(undefined)
      localStorage.removeItem("darkMode")
    }
  }

  const mode = getThemeMode()
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode)), [mode]);


  return (
    <ThemeProvider theme={theme}>
      <GlobalStyles
        styles={(theme) => ({
          "body": { backgroundColor: theme.palette.background.default },
          "div#root": { backgroundColor: theme.palette.background.default },
          ".sidenavItemActive": { backgroundColor: theme.palette.text.disabled },
          ".react-datepicker__day--selected": {backgroundColor: theme.palette.vestmentr.main},
          ".react-datepicker__day--keyboard-selected": {backgroundColor: theme.palette.vestmentr.main},
          ".react-datepicker__day--selected:hover": {backgroundColor: theme.palette.vestmentr.main},
          ".react-datepicker": {backgroundColor: theme.palette.background.default},
          ".react-datepicker__header": {backgroundColor: theme.palette.text.disabled},
          ".react-datepicker__day": {color: theme.palette.text.primary},
          ".react-datepicker__day-name": {color: theme.palette.text.primary},
          ".react-datepicker__current-month": {color: theme.palette.text.primary},
        })}
      />
      {/*<ReleaseNotes lang={lang} version={version} debug={debug} />*/}
      <Container disableGutters sx={{backgroundColor: "background.default"}}>
        <AppBar sx={{backgroundColor: appbarDarkGrey}}>
          <Toolbar>
            <>
              <IconButton
                size="large"
                edge="start"
                aria-label="menu"
                sx={{color: "yellowish.main"}}
                onClick={toggleDrawer(true)}
              >
                <MenuIcon/>
              </IconButton>
              <Drawer
                variant="temporary"
                open={drawerOpened}
                onClose={toggleDrawer(false)}
              >
                <LeftHandMenu
                  lang={lang}
                  toggleDrawer={toggleDrawer}
                  darkMode={darkMode}
                  toggleDarkMode={toggleDarkMode}
                />
              </Drawer>
            </>
            <Link sx={{display: "flex", textDecoration: "none"}} component={RouterLink} to={{pathname: `/${lang}`}} >
                <Logo width={28} height={28} />
                <Typography variant="h1" component="div">Missale<br/>Meum</Typography>
            </Link>
          </Toolbar>
        </AppBar>
        <Outlet />
        <ContainerMedium sx={{display: "flex", justifyContent: "space-between"}}>
          <Typography sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.9rem"}}>☩ A. M. D. G. ☩</Typography>
          <Typography sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.75rem"}}>{version}</Typography>
        </ContainerMedium>
        <CookieConsent enableDeclineButton debug={debug} declineButtonStyle={{ background: appbarDarkGrey }}
                       buttonStyle={{ background: "#e49086" }} declineButtonText={MSG_POLICY_DECLINE_BUTTON[lang]} buttonText="OK"
                       onAccept={() => registerPageView()}>
          {MSG_COOKIES[lang]}
          <Link component={RouterLink} to={{pathname: `/${lang}/supplement/privacy-policy`}} target="_blank" >
            {MSG_POLICY_LINK[lang]}
          </Link>
        </CookieConsent>
      </Container>
    </ThemeProvider>
  );
};

const LeftHandMenu = (props) => {

  const location = useLocation()

  const isDrawerMenuitemSelected = (route) => {
    let routeSplit = route.split("/")
    let pathSplit = location.pathname.split("/")
    let datePattern = /^[\d-]+$/
    if (routeSplit.length < 3) {
      // /pl or /pl/2022-02-02
      return route === location.pathname || datePattern.test(pathSplit[pathSplit.length - 1])
    }
    if (["info", "index"].includes(pathSplit[pathSplit.length - 1])) {
      return location.pathname === route
    }
    return location.pathname.startsWith(route)
  }

  return (
    <Box
      sx={{width: 300}}
      role="presentation"
      onClick={props.toggleDrawer(false)}
      onKeyDown={props.toggleDrawer(false)}
    >
      <IconButton onClick={props.toggleDrawer(false)}>
        <CloseIcon/>
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
              component={NavLink}
              to={route}
              selected={isDrawerMenuitemSelected(route)}
            >
              <DrawerListItemText primary={label}/>
            </ListItemButton>
          </ListItem>
        ))}

        <Divider/>
        <ListItem key="lang">
          <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => localStorage.setItem("lang", "en")} component={RouterLink} to={{pathname: "/en"}} value="en" selected={props.lang === "en"}>English</ToggleButton>
            <ToggleButton onClick={() => localStorage.setItem("lang", "pl")} component={RouterLink} to={{pathname: "/pl"}} value="pl" selected={props.lang === "pl"}>Polski</ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        <ListItem key="theme">
          <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">
            <ToggleButton onClick={() => props.toggleDarkMode(false)} value="light" selected={props.darkMode === false}><LightModeIcon /></ToggleButton>
            <ToggleButton onClick={() => props.toggleDarkMode(true)} value="dark" selected={props.darkMode === true}><DarkModeIcon /></ToggleButton>
          </ToggleButtonGroup>
        </ListItem>
        {/*<ListItem key="font">*/}
        {/*  <ToggleButtonGroup color="secondary" variant="outlined" aria-label="outlined secondary button group">*/}
        {/*    <ToggleButton sx={{px: "1rem", fontSize: "0.5rem", fontWeight: "600"}} onClick={() => alert("Not implemented")} value="small"> A </ToggleButton>*/}
        {/*    <ToggleButton sx={{px: "1rem", fontWeight: "600"}} onClick={() => alert("Not implemented")} value="normal" selected={true}>A</ToggleButton>*/}
        {/*    <ToggleButton sx={{px: "1rem", fontSize: "1.25rem", fontWeight: "600"}} onClick={() => alert("Not implemented")} value="large">A</ToggleButton>*/}
        {/*  </ToggleButtonGroup>*/}
        {/*</ListItem>*/}
      </List>
    </Box>
)}

export default App

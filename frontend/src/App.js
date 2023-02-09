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
import {grey} from "@mui/material/colors";
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
import NewReleaseDialog from "./components/NewReleaseDialog";

const debug = process.env.REACT_APP_DEBUG === "true"
const supportedLanguages = ["en", "pl"]
const defaultLanguage = localStorage.getItem("lang") || (navigator.language === "pl") ? "pl" : "en"
const yellowish = '#fcfbf9'
const appbarDarkGrey = '#424242'
const defaultTheme = createTheme()

const getDesignTokens = (mode) => ({
  palette: {
    mode,
    ...(mode === 'light'
      ? {
          // palette values for light mode
          background: {
            paper: yellowish,
            default: yellowish
          },
          primary: {
            main: appbarDarkGrey,
            light: '#6d6d6d',
            dark: '#1b1b1b',
          },
          secondary: {
            main: '#b76d6d',
            light: '#eb9c9b',
            dark: '#854042',
          },
          text: {
            primary: grey[900],
            disabled: grey[300]
          },
          vestmentw: {
            main: '#d3d3d3',
            contrastText: '#fff'
          },
          vestmentr: {
            main: '#b76d6d',
            contrastText: '#fff',
          },
          vestmentv: {
            main: '#92689f',
            contrastText: '#fff',
          },
          vestmentg: {
            main: '#6c8d4d',
            contrastText: '#fff',
          }
        }
      : {
          // palette values for dark mode
          background: {
            paper: '#262626',
            default: '#262626'
          },
          primary: {
            main: yellowish,
            light: '#fff',
            dark: '#c9c8c6',
          },
          secondary: {
            main: '#e49086',
            light: '#ffc1b6',
            dark: '#b06159',
          },
          text: {
            primary: yellowish,
            secondary: yellowish,
            disabled: grey[800]
          },
          vestmentw: {
            main: yellowish,
            contrastText: '#fff'
          },
          vestmentr: {
            main: '#e49086',
            contrastText: '#fff',
          },
          vestmentv: {
            main: '#ad7cbe',
            contrastText: '#fff',
          },
          vestmentg: {
            main: '#91b965',
            contrastText: '#fff',
          },
        }),
        yellowish: {
          main: yellowish,
          contrastText: '#fff',
        },
        appbarDarkGrey: {
          main: appbarDarkGrey,
          contrastText: '#fff',
        },
        vestmentb: {
          main: '#565656',
          contrastText: '#fff',
        },
        vestmentp: {
          main: '#e1a5ba',
          contrastText: '#fff',
        }
  },
  typography: {

    ...(mode === 'light'
    ? {
        // palette values for light mode
        h1: {
          fontSize: "1.1rem",
          fontFamily: "Merriweather",
          fontWeight: 700,
          color: yellowish
        },
        h2: {
          fontSize: "1.25rem",
          fontFamily: "Merriweather",
          fontWeight: 800,
          color: grey[900]
        },
        h3: {
          fontSize: "1rem",
          fontFamily: "Merriweather",
          textTransform: "uppercase",
          fontWeight: 800,
          color: grey[900]
        },
        h4: {
          fontSize: "1rem",
          fontFamily: "Merriweather",
          textTransform: "uppercase",
          fontWeight: 400,
          color: grey[900]
        },
        body1: {
          fontFamily: "Merriweather",
        },
      }
    : {
        // palette values for dark mode
        h1: {
          fontSize: "1.1rem",
          fontFamily: "Merriweather",
          fontWeight: 700,
          color: yellowish
        },
        h2: {
          fontSize: "1.25rem",
          fontFamily: "Merriweather",
          fontWeight: 800,
          color: yellowish
        },
        h3: {
          fontSize: "1rem",
          fontFamily: "Merriweather",
          textTransform: "uppercase",
          fontWeight: 800,
          color: yellowish
        },
        h4: {
          fontSize: "1rem",
          fontFamily: "Merriweather",
          textTransform: "uppercase",
          fontWeight: 400,
          color: yellowish
        },
        body1: {
          fontFamily: "Merriweather",
          color: yellowish
        },
    }),
    subtitle1: {
      fontWeight: 400,
    },
    subtitle2: {
      fontWeight: 400,
      color: '#b76d6d'
    },
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          [defaultTheme.breakpoints.up("sm")]: {
            flexDirection: "row",
            justifyContent: "center"
          },
          height: "56px"
        },
      },
    },
    MuiToolbar: {
      styleOverrides: {
        root: {
          [defaultTheme.breakpoints.up("sm")]: {
            minHeight: "56px",
            width: "900px"
          },
        },
      },
    }
  }
});

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
    if (getCookieConsentValue() === "true" && window.location.hostname.endsWith("missalemeum.com")) {
      window.gtag("event", "page_view", {
        page_path: location.pathname + location.search + location.hash,
        page_search: location.search,
        page_hash: location.hash,
      })
    }
  }, [location])

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

  const theme = createTheme(getDesignTokens(getThemeMode()))

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
      <NewReleaseDialog lang={lang} version={version} debug={debug} />
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
                <Logo />
                <Typography variant="h1" component="div">Missale<br/>Meum</Typography>
            </Link>
          </Toolbar>
        </AppBar>
        <Outlet/>
        <Container sx={{width: {"md": "900px", display: "flex", justifyContent: "space-between"}}}>
          <Typography sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.9rem"}}>☩ A. M. D. G. ☩</Typography>
          <Typography sx={{py: "2rem", color: (theme) => theme.palette.mode === "dark" ? "primary.dark" : "primary.light", fontSize: "0.75rem"}}>{version}</Typography>
        </Container>
        <CookieConsent enableDeclineButton debug={debug} declineButtonStyle={{ background: appbarDarkGrey }}
                       buttonStyle={{ background: "#e49086" }} declineButtonText={MSG_POLICY_DECLINE_BUTTON[lang]} buttonText="OK">
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

'use client';
import {grey} from "@mui/material/colors";
import {createTheme} from "@mui/material";
import { Merriweather } from "next/font/google";


const defaultTheme = createTheme()
export const yellowish = '#fcfbf9'
const darkRedLightMode = '#b76d6d'
const darkRedDarkMode = '#e49086'
export const appbarDarkGrey = '#424242'

const translateFontSize = (fontSizeName) => {
  return {"small": 12, "medium": 14, "large": 18}[fontSizeName] || 14
}


let fontSizeName = "medium"


const theme = createTheme({
  palette: {
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
      main: darkRedLightMode,
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
      main: darkRedLightMode,
      contrastText: '#fff',
    },
    vestmentv: {
      main: '#92689f',
      contrastText: '#fff',
    },
    vestmentg: {
      main: '#6c8d4d',
      contrastText: '#fff',
    },
    // For all modes:
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
    h1: {
      fontSize: "1.1rem",
      fontFamily: "Merriweather",
      fontWeight: 700,
      color: yellowish
    },
    h2: {
      fontSize: translateFontSize(fontSizeName) * 1.5,
      fontFamily: "Merriweather",
      fontWeight: 800,
      color: grey[900]
    },
    h3: {
      fontSize: translateFontSize(fontSizeName) * 1.2,
      fontFamily: "Merriweather",
      fontWeight: 800,
      color: grey[700],
      lineHeight: 2.2
    },
    h4: {
      fontSize: translateFontSize(fontSizeName) * 1.2,
      fontFamily: "Merriweather",
      textTransform: "uppercase",
      fontWeight: 800,
      color: darkRedLightMode
    },
    h5: {
      fontSize: translateFontSize(fontSizeName) * 1.2,
      fontFamily: "Merriweather",
      textTransform: "uppercase",
      fontWeight: 400,
      color: darkRedLightMode
    },
    body1: {
      fontFamily: "Merriweather",
    },
    // For all light modes:
    fontSize: translateFontSize(fontSizeName),
    subtitle1: {
      fontWeight: 400,
    },
    subtitle2: {
      fontWeight: 400,
      color: darkRedLightMode
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

export default theme;
import {grey} from "@mui/material/colors";
import {createTheme} from "@mui/material";

const defaultTheme = createTheme()
export const yellowish = '#fcfbf9'
export const appbarDarkGrey = '#424242'
export const getDesignTokens = (mode) => ({
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
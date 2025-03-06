import {grey} from "@mui/material/colors";
import {createTheme, PaletteMode} from "@mui/material";


const defaultTheme = createTheme()
export const yellowish = '#fcfbf9'
const darkRedLightMode = '#b76d6d'
const darkRedDarkMode = '#e49086'
export const appbarDarkGrey = '#424242'

export type vestmentColor = "vestmentr" | "vestmentw" | "vestmentv" | "vestmentg"

declare module "@mui/material/styles" {
  interface Palette {
    vestmentw: Palette["primary"];
    vestmentr: Palette["primary"];
    vestmentv: Palette["primary"];
    vestmentg: Palette["primary"];
  }

  interface PaletteOptions {
    vestmentw?: PaletteOptions["primary"];
    vestmentr?: PaletteOptions["primary"];
    vestmentv?: PaletteOptions["primary"];
    vestmentg?: PaletteOptions["primary"];
  }
}

declare module "@mui/material/Chip" {
  interface ChipPropsColorOverrides {
    vestmentw: true;
    vestmentr: true;
    vestmentv: true;
    vestmentg: true;
  }
}

const translateFontSize = (fontSizeName: string) => {
  return {"small": 12, "medium": 14, "large": 18}[fontSizeName] || 14
}

export const getDesignTokens = (mode: PaletteMode, fontSizeName: string) => ({
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
            main: darkRedDarkMode,
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
            main: darkRedDarkMode,
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
          textTransform: "uppercase" as "uppercase" | "capitalize" | "none" | "lowercase",
          fontWeight: 800,
          color: darkRedLightMode
        },
        h5: {
          fontSize: translateFontSize(fontSizeName) * 1.2,
          fontFamily: "Merriweather",
          textTransform: "uppercase" as "uppercase" | "capitalize" | "none" | "lowercase",
          fontWeight: 400,
          color: darkRedLightMode
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
          fontSize: translateFontSize(fontSizeName) * 1.5,
          fontFamily: "Merriweather",
          fontWeight: 800,
          color: yellowish
        },
        h3: {
          fontSize: translateFontSize(fontSizeName) * 1.2,
          fontFamily: "Merriweather",
          fontWeight: 800,
          color: grey[400],
          lineHeight: 2.2
        },
        h4: {
          fontSize: translateFontSize(fontSizeName) * 1.2,
          fontFamily: "Merriweather",
          textTransform: "uppercase" as "uppercase" | "capitalize" | "none" | "lowercase",
          fontWeight: 800,
          color: darkRedDarkMode
        },
        h5: {
          fontSize: translateFontSize(fontSizeName) * 1.2,
          fontFamily: "Merriweather",
          textTransform: "uppercase" as "uppercase" | "capitalize" | "none" | "lowercase",
          fontWeight: 400,
          color: darkRedDarkMode
        },
        body1: {
          fontFamily: "Merriweather",
          color: yellowish
        },
    }),
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
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: "background.default" // TODO: dark theme
        }
      }
    }
  }
});

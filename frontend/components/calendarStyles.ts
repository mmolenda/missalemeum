import {alpha, darken, lighten, styled, type PaletteColor} from "@mui/material/styles";
import Box from "@mui/material/Box";
import {getAppBarHeightFromTheme} from "@/components/layoutMetrics";

// Read the same semantic palette as proprium; only calendar layout is scoped here.
export const CalendarSurface = styled(Box)(({theme}) => {
  const {palette} = theme;
  const c = {
    surface: palette.background.default,
    text: palette.text.primary,
    muted: palette.mode === "dark" ? palette.text.secondary : palette.primary.light,
    line: palette.mode === "dark" ? palette.divider : alpha(palette.text.primary, 0.15),
    accent: palette.secondary.main,
    hover: palette.mode === "dark" ? palette.background.paper : palette.action.hover,
  };
  const vestments = Object.fromEntries(["r", "g", "v", "w", "b", "p"].map((code) => {
    const color = (palette[`vestment${code}` as keyof typeof palette] as PaletteColor).main;
    // Tune only the calendar markers; proprium keeps its existing liturgical colors.
    const marker = palette.mode === "dark"
      ? code === "w" ? "#d8d9d7" : code === "b" ? lighten(color, 0.2) : color
      : darken(color, code === "w" ? 0.12 : 0.06);
    return [`--vestment-${code}`, marker];
  }));
  return {
    "--calendar-surface": c.surface,
    "--calendar-field": alpha(c.text, 0.015),
    "--calendar-text": c.text,
    "--calendar-muted": c.muted,
    "--calendar-line": c.line,
    "--calendar-accent": c.accent,
    ...vestments,
    color: c.text,
    backgroundColor: c.surface,
    fontFamily: theme.typography.fontFamily,
    "& .calendar-controls": {
      backgroundColor: c.surface,
      borderBottom: `1px solid ${c.line}`,
      boxShadow: `0 4px 12px ${alpha("#000", theme.palette.mode === "dark" ? 0.1 : 0.025)}`,
      padding: theme.spacing(1.5, 2.5),
      gap: theme.spacing(0.5),
      "& .MuiIconButton-root": {
        width: 44, height: 44, borderRadius: 1, color: c.muted,
        "&:hover": {backgroundColor: c.hover, color: c.text},
        "&[aria-expanded=true]": {color: c.accent, backgroundColor: alpha(c.accent, 0.09)},
      },
      "& .MuiSvgIcon-root": {fontSize: 22},
      "& .MuiOutlinedInput-root": {
        minHeight: 44, backgroundColor: "var(--calendar-field)", borderRadius: 1,
        color: c.text, fontSize: theme.typography.pxToRem(14), fontFamily: theme.typography.fontFamily,
        "& fieldset": {borderColor: c.line},
        "&:hover fieldset": {borderColor: alpha(c.text, 0.3)},
        "&.Mui-focused fieldset": {borderColor: c.accent, borderWidth: 2},
      },
      "& input::placeholder": {color: c.muted, opacity: 1},
    },
    "& .calendar-list": {padding: theme.spacing(0, 2.5, 2)},
    "& .calendar-month": {
      display: "block", padding: theme.spacing(0.75, 2, 0, 2.75), margin: 0,
      color: c.muted, fontSize: theme.typography.pxToRem(12), fontWeight: 600, lineHeight: 1.5,
      letterSpacing: "0.08em", textTransform: "uppercase",
    },
    "& .calendar-day": {
      display: "block", padding: 0, borderBottom: `1px solid ${c.line}`,
      "&.calendar-week-start": {marginTop: theme.spacing(3)},
      scrollMarginTop: `calc(${getAppBarHeightFromTheme(theme)}px + var(--announcement-banner-height, 0px) + var(--list-controls-height, 68px) + 16px)`,
    },
    "& .calendar-day-link": {
      display: "block", padding: theme.spacing(1.25, 2, 1.25, 2.75), minHeight: 70,
      position: "relative", color: c.text,
      "&::before": {
        content: '""', position: "absolute", left: 0, top: 13, bottom: 13,
        width: 3, borderRadius: 1, backgroundColor: "var(--day-color)",
      },
      "&:hover": {backgroundColor: c.hover},
      "&.Mui-selected, &.Mui-selected:hover": {backgroundColor: alpha(c.accent, 0.055)},
      "&[aria-current=date]": {backgroundColor: alpha(c.accent, 0.045)},
    },
    "& .calendar-title": {
      margin: 0, fontFamily: "inherit", fontSize: theme.typography.pxToRem(17),
      fontWeight: 400, lineHeight: 1.4, letterSpacing: "-0.012em", overflowWrap: "anywhere",
    },
    "& .calendar-important .calendar-title": {fontWeight: 700},
    "& .calendar-feria .calendar-title": {fontWeight: 400},
    "& .calendar-meta": {
      display: "flex", flexWrap: "wrap", alignItems: "baseline", gap: theme.spacing(0.5, 1.25),
      marginTop: theme.spacing(0.5), fontSize: theme.typography.pxToRem(14),
      lineHeight: 1.5, fontWeight: 400, color: c.muted,
    },
    "& .calendar-date": {fontWeight: 400, fontVariantNumeric: "tabular-nums"},
    "& .calendar-meta > :not(:first-child)": {
      display: "inline-flex", alignItems: "baseline", gap: theme.spacing(1.25),
      "&::before": {
        content: '"·"', color: c.muted, fontSize: theme.typography.pxToRem(14),
        fontWeight: 400, letterSpacing: "normal", lineHeight: 1.5,
      },
    },
    "& .calendar-today, & .calendar-first-weekday": {
      color: c.accent, fontSize: theme.typography.pxToRem(12),
      letterSpacing: "0.045em", textTransform: "uppercase", whiteSpace: "nowrap",
    },
    "& .calendar-today": {fontWeight: 700},
    "& .calendar-first-weekday": {fontWeight: 400},
    "& .calendar-commemorations": {
      marginTop: theme.spacing(0.5), color: c.muted,
      fontSize: theme.typography.pxToRem(13), lineHeight: 1.55, overflowWrap: "anywhere",
    },
    "& .calendar-commemoration-label": {color: c.accent, fontWeight: 600},
    "& a:focus-visible, & button:focus-visible, & .Mui-focusVisible": {
      outline: `2px solid ${c.accent}`, outlineOffset: -2, borderRadius: 2,
    },
    [theme.breakpoints.down("sm")]: {
      "& .calendar-controls": {padding: theme.spacing(1.25, 1), gap: 0},
      "& .calendar-list": {padding: theme.spacing(0, 1, 1)},
      "& .calendar-day-link": {padding: theme.spacing(1.125, 1.25, 1.125, 2.25)},
      "& .calendar-title": {fontSize: theme.typography.pxToRem(16)},
      "& .calendar-month": {padding: theme.spacing(0.75, 1.25, 0, 2.25)},
    },
    "@media (prefers-reduced-motion: reduce)": {"& *": {transition: "none"}},
  };
});

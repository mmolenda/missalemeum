import {alpha, darken, lighten, styled, type PaletteColor} from "@mui/material/styles";
import {getListColors, ListSurface} from "@/components/listStyles";
import {getAppBarHeightFromTheme} from "@/components/layoutMetrics";

// Calendar-specific markers and metadata build on the shared index presentation.
export const CalendarSurface = styled(ListSurface)(({theme}) => {
  const {palette} = theme;
  const c = getListColors(theme);
  const vestments = Object.fromEntries(["r", "g", "v", "w", "b", "p"].map((code) => {
    const color = (palette[`vestment${code}` as keyof typeof palette] as PaletteColor).main;
    // Tune only the calendar markers; proprium keeps its existing liturgical colors.
    const marker = palette.mode === "dark"
      ? code === "w" ? "#d8d9d7" : code === "b" ? lighten(color, 0.2) : color
      : darken(color, code === "w" ? 0.12 : 0.06);
    return [`--vestment-${code}`, marker];
  }));
  return {
    ...vestments,
    "& .calendar-month": {
      display: "block", padding: theme.spacing(0.75, 2, 0, 2.75), margin: 0,
      color: c.muted, fontSize: theme.typography.pxToRem(12), fontWeight: 600, lineHeight: 1.5,
      letterSpacing: "0.08em", textTransform: "uppercase",
    },
    "& .calendar-day": {
      "&.calendar-week-start": {marginTop: theme.spacing(3)},
      scrollMarginTop: `calc(${getAppBarHeightFromTheme(theme)}px + var(--announcement-banner-height, 0px) + var(--list-controls-height, 68px) + 16px)`,
    },
    "& .calendar-day-link": {
      display: "block", paddingLeft: theme.spacing(2.75), minHeight: 70,
      "&::before": {
        content: '""', position: "absolute", left: 0, top: 13, bottom: 13,
        width: 3, borderRadius: 1, backgroundColor: "var(--day-color)",
      },
      "&[aria-current=date]": {backgroundColor: alpha(c.accent, 0.045)},
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
        content: '"·"', color: c.accent, fontSize: theme.typography.pxToRem(14),
        fontWeight: 700, letterSpacing: "normal", lineHeight: 1.5,
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
    [theme.breakpoints.down("sm")]: {
      "& .calendar-day-link": {paddingLeft: theme.spacing(2.25)},
      "& .calendar-month": {padding: theme.spacing(0.75, 1.25, 0, 2.25)},
    },
  };
});

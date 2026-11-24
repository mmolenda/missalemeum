"use client";

import {alpha, styled, type Theme} from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import {getAppBarHeightFromTheme} from "@/components/layoutMetrics";

export const getListColors = ({palette}: Theme) => ({
  surface: palette.background.default,
  text: palette.text.primary,
  muted: palette.mode === "dark" ? palette.text.secondary : palette.primary.light,
  line: palette.mode === "dark" ? palette.divider : alpha(palette.text.primary, 0.15),
  accent: palette.secondary.main,
  hover: palette.mode === "dark" ? palette.background.paper : palette.action.hover,
});

// Shared presentation for the calendar and the content indexes.
export const ListSurface = styled(Box)(({theme}) => {
  const c = getListColors(theme);
  return {
    "--list-field": alpha(c.text, 0.015),
    "--list-muted": c.muted,
    color: c.text,
    backgroundColor: c.surface,
    fontFamily: theme.typography.fontFamily,
    "& .list-controls": {
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
        minHeight: 44, backgroundColor: "var(--list-field)", borderRadius: 1,
        color: c.text, fontSize: theme.typography.pxToRem(14), fontFamily: theme.typography.fontFamily,
        "& fieldset": {borderColor: c.line},
        "&:hover fieldset": {borderColor: alpha(c.text, 0.3)},
        "&.Mui-focused fieldset": {borderColor: c.accent, borderWidth: 2},
      },
      "& input::placeholder": {color: c.muted, opacity: 1},
    },
    "& .list-index": {padding: theme.spacing(0, 2.5, 2)},
    "& .list-item": {display: "block", padding: 0, borderBottom: `1px solid ${c.line}`},
    "& .list-link": {
      display: "flex", flexDirection: "column", alignItems: "stretch", justifyContent: "center",
      position: "relative", color: c.text,
      padding: theme.spacing(1.25, 2), minHeight: 56,
      "&:hover": {backgroundColor: c.hover},
      "&.Mui-selected, &.Mui-selected:hover": {backgroundColor: alpha(c.accent, 0.055)},
    },
    "& .list-title": {
      display: "block", margin: 0, fontFamily: "inherit", fontSize: theme.typography.pxToRem(17),
      fontWeight: 400, lineHeight: 1.4, letterSpacing: "-0.012em", overflowWrap: "anywhere",
    },
    "& .list-details": {
      display: "block", marginTop: theme.spacing(0.5), color: c.muted,
      fontSize: theme.typography.pxToRem(14), fontWeight: 400, lineHeight: 1.5,
      overflowWrap: "anywhere",
    },
    "& .list-separator": {color: c.accent, fontWeight: 700, fontSize: "1.3em", lineHeight: 0},
    "& .list-skeleton": {padding: theme.spacing(1.25, 2), minHeight: 70},
    "& a:focus-visible, & button:focus-visible, & .Mui-focusVisible": {
      outline: `2px solid ${c.accent}`, outlineOffset: -2, borderRadius: 2,
    },
    [theme.breakpoints.down("sm")]: {
      "& .list-controls": {padding: theme.spacing(1.25, 1), gap: 0},
      "& .list-index": {padding: theme.spacing(0, 1, 1)},
      "& .list-link": {padding: theme.spacing(1.125, 1.25)},
      "& .list-title": {fontSize: theme.typography.pxToRem(16)},
      "& .list-skeleton": {padding: theme.spacing(1.125, 1.25)},
    },
    "@media (prefers-reduced-motion: reduce)": {"& *": {transition: "none"}},
  };
});

export const ListControls = styled(Box)(({theme}) => ({
  position: "fixed", display: "flex", alignItems: "center",
  top: `calc(${getAppBarHeightFromTheme(theme)}px + var(--announcement-banner-height, 0px))`,
  width: "100%", maxWidth: "900px", left: "50%", transform: "translateX(-50%)",
  zIndex: 100,
}));

// Autocomplete menus render in a portal, outside ListSurface's font inheritance.
export const ListSearchPaper = styled(Paper)(({theme}) => ({
  "&&": {fontFamily: theme.typography.fontFamily},
  "& .MuiAutocomplete-listbox, & .MuiAutocomplete-option": {fontFamily: "inherit"},
}));

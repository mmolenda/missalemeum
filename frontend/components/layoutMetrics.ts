import type {Theme} from "@mui/material/styles";

export const BANNER_ENABLED = false;
export const BANNER_STORAGE_KEY = "pageSearchAnnouncementDismissed";
export const BANNER_EXPIRES_AT = "2026-12-14T00:00:00+01:00";
export const BANNER_HEIGHT = 48;

export const isBannerActive = (now = Date.now()) => BANNER_ENABLED && now < Date.parse(BANNER_EXPIRES_AT);

export const getAppBarHeightFromTheme = (theme: Theme): number => {
  const root = theme.components?.MuiAppBar?.styleOverrides?.root;
  const height = root && typeof root === 'object' && 'height' in root ? root.height : 0;
  const parsedHeight = typeof height === 'string' ? parseInt(height, 10) : height;
  return Number.isFinite(parsedHeight as number) ? (parsedHeight as number) : 0;
};

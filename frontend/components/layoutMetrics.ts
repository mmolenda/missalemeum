import type {Theme} from "@mui/material/styles";

export const BANNER_STORAGE_KEY = "pdfBannerDismissed";
export const BANNER_HEIGHT = 48;

export const getAppBarHeightFromTheme = (theme: Theme): number => {
  const root = theme.components?.MuiAppBar?.styleOverrides?.root;
  const height = root && typeof root === 'object' && 'height' in root ? root.height : 0;
  const parsedHeight = typeof height === 'string' ? parseInt(height, 10) : height;
  return Number.isFinite(parsedHeight as number) ? (parsedHeight as number) : 0;
};

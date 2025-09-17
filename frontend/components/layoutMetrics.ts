import type {Theme} from "@mui/material/styles";

export const BANNER_STORAGE_KEY = "bannerDismissed";
export const BANNER_HEIGHT = 48;

const bannerExpiryValue = process.env.NEXT_PUBLIC_BANNER_END_DATE;
const bannerExpiryDate = (() => {
  if (!bannerExpiryValue) {
    return undefined;
  }

  const parsed = new Date(bannerExpiryValue);
  return Number.isNaN(parsed.getTime()) ? undefined : parsed;
})();

export const getBannerExpiryDate = (): Date | undefined => bannerExpiryDate;

export const isBannerExpired = (now: Date = new Date()): boolean => {
  if (!bannerExpiryDate) {
    return false;
  }

  return now >= bannerExpiryDate;
};

export const getAppBarHeightFromTheme = (theme: Theme): number => {
  const root = theme.components?.MuiAppBar?.styleOverrides?.root;
  const height = root && typeof root === 'object' && 'height' in root ? root.height : 0;
  const parsedHeight = typeof height === 'string' ? parseInt(height, 10) : height;
  return Number.isFinite(parsedHeight as number) ? (parsedHeight as number) : 0;
};

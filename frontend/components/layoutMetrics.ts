import type {Theme} from "@mui/material/styles";

export const BANNER_STORAGE_KEY = "bannerDismissed";
export const BANNER_HEIGHT = 48;

const bannerExpiryValue = process.env.NEXT_PUBLIC_BANNER_END_DATE;

const parseBannerExpiryDate = (value: string): Date | undefined => {
  const trimmed = value.trim();
  const match = /^\d{4}-\d{2}-\d{2}$/.exec(trimmed);
  if (!match) {
    return undefined;
  }

  const [yearStr, monthStr, dayStr] = trimmed.split('-');
  const year = Number.parseInt(yearStr, 10);
  const month = Number.parseInt(monthStr, 10);
  const day = Number.parseInt(dayStr, 10);

  if (Number.isNaN(year) || Number.isNaN(month) || Number.isNaN(day)) {
    return undefined;
  }

  const date = new Date(Date.UTC(year, month - 1, day, 0, 0, 0, 0));

  if (
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    return undefined;
  }

  return date;
};

const bannerExpiryDate = bannerExpiryValue ? parseBannerExpiryDate(bannerExpiryValue) : undefined;

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

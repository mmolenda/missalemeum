import React, { useCallback, useMemo, useState } from "react";
import PrintIcon from "@mui/icons-material/Print";
import { IconButton, Menu, MenuItem } from "@mui/material";

import { Locale, PDF_VARIANTS, PdfVariantOption } from "@/components/intl";
import { buildApiUrl } from "@/components/utils";

type ExtraParams = Record<string, string | number | null | undefined>;

type BuildPdfUrlParams = {
  lang: string;
  apiEndpoint?: string;
  resourceId?: string | null;
  variant: string;
  index?: number | null;
  extraParams?: ExtraParams;
};

type PdfDownloadMenuProps = {
  lang: string;
  apiEndpoint?: string;
  resourceId?: string | null;
  indexParam?: number | null;
  extraParams?: ExtraParams;
  ariaLabel?: string;
};

const filterPdfVariants = (lang: string): PdfVariantOption[] => {
  const options = PDF_VARIANTS[lang as Locale] ?? PDF_VARIANTS.en;
  if (lang === "en") {
    return options;
  }
  return options.filter((option) => !option.variant.startsWith("letter"));
};

export const buildPdfDownloadUrl = ({
  lang,
  apiEndpoint,
  resourceId,
  variant,
  index,
  extraParams,
}: BuildPdfUrlParams): string | null => {
  if (!apiEndpoint) {
    return null;
  }
  const apiUrl = buildApiUrl(lang, apiEndpoint, resourceId ?? undefined);
  const questionMarkIndex = apiUrl.indexOf("?");
  const path = questionMarkIndex === -1 ? apiUrl : apiUrl.slice(0, questionMarkIndex);
  const existingQuery = questionMarkIndex === -1 ? "" : apiUrl.slice(questionMarkIndex + 1);

  const cleanedVariant = variant.startsWith("?") ? variant.slice(1) : variant;
  const params = new URLSearchParams(existingQuery);
  params.set("format", "pdf");
  params.set("variant", cleanedVariant);
  if (index !== null && index !== undefined) {
    params.set("index", String(index));
  } else {
    params.delete("index");
  }
  if (extraParams) {
    Object.entries(extraParams).forEach(([key, value]) => {
      if (value === null || value === undefined) {
        params.delete(key);
      } else {
        params.set(key, String(value));
      }
    });
  }

  const query = params.toString();
  return query ? `${path}?${query}` : path;
};

export const PdfDownloadMenu = ({
  lang,
  apiEndpoint,
  resourceId,
  indexParam,
  extraParams,
  ariaLabel = "download pdf",
}: PdfDownloadMenuProps) => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const variants = useMemo(() => filterPdfVariants(lang), [lang]);

  const handleMenuOpen = useCallback((event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  }, []);

  const handleMenuClose = useCallback(() => {
    setAnchorEl(null);
  }, []);

  if (!apiEndpoint || !resourceId) {
    return null;
  }

  return (
    <>
      <IconButton
        aria-label={ariaLabel}
        aria-controls={open ? "pdf-variant-menu" : undefined}
        aria-haspopup="true"
        aria-expanded={open ? "true" : undefined}
        onClick={handleMenuOpen}
      >
        <PrintIcon/>
      </IconButton>
      <Menu
        id="pdf-variant-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleMenuClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
      >
        {variants.map(({ label, variant }) => {
          const downloadHref = buildPdfDownloadUrl({
            lang,
            apiEndpoint,
            resourceId,
            variant,
            index: indexParam,
            extraParams,
          });
          return (
            <MenuItem
              key={variant}
              component="a"
              href={downloadHref ?? "#"}
              onClick={handleMenuClose}
              target="_blank"
              rel="noopener noreferrer"
            >
              {label}
            </MenuItem>
          );
        })}
      </Menu>
    </>
  );
};

export const usePdfVariants = (lang: string) => useMemo(() => filterPdfVariants(lang), [lang]);


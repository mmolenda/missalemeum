"use client";

import "@/app/globals.css";

import type { ReactNode } from "react";
import { Merriweather } from "next/font/google";
import { useParams } from "next/navigation";

const font = Merriweather({
  subsets: ["latin"],
  weight: ["300", "400"],
});

const DEFAULT_LOCALE = "en";
const SUPPORTED_LOCALES = new Set(["pl", "en"]);

const resolveLocale = (value?: string) =>
  value && SUPPORTED_LOCALES.has(value) ? value : DEFAULT_LOCALE;

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  const params = useParams<{ locale?: string }>();
  const lang = resolveLocale(params?.locale);

  return (
    <html lang={lang} className={font.className} translate="no">
      <body>{children}</body>
    </html>
  );
}

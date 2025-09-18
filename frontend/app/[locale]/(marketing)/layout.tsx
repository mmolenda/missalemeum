import "@/app/globals.css";
import styles from "@/app/landing.module.css";
import React from "react";

export default function MarketingLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: { locale: string };
}) {
  const supportedLocales = new Set(["pl", "en"]);
  const lang = supportedLocales.has(params.locale) ? params.locale : "en";

  return (
    <html lang={lang}>
      <body className={styles.landingBody}>{children}</body>
    </html>
  );
}

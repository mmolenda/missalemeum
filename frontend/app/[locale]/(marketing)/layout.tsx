import styles from "@/app/landing.module.css";
import React from "react";
import SimpleAnalyticsScript from "@/components/SimpleAnalyticsScript";

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <SimpleAnalyticsScript />
      <div className={styles.landingBody}>{children}</div>
    </>
  );
}

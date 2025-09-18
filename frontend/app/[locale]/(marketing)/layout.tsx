import styles from "@/app/landing.module.css";
import React from "react";

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <div className={styles.landingBody}>{children}</div>;
}

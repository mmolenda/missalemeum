"use client";

import { useEffect, useState } from "react";
import { Icon } from "@iconify/react";
import styles from "@/app/landing.module.css";

export default function BackToTopButton() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > 160);
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!visible) {
    return null;
  }

  const handleClick = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <button
      type="button"
      className={styles.backToTop}
      onClick={handleClick}
      aria-label="Back to top"
    >
      <Icon icon="mdi:arrow-up" width={22} height={22} />
    </button>
  );
}

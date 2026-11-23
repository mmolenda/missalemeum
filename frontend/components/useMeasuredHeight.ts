"use client";

import {useEffect, type RefObject} from "react";

// Share the actual height of fixed UI with content and other fixed controls.
export function useMeasuredHeight(ref: RefObject<HTMLElement | null>, property: string, enabled = true) {
  useEffect(() => {
    const element = ref.current;
    if (!enabled || !element) return;
    const update = () => document.documentElement.style.setProperty(
      property, `${element.getBoundingClientRect().height}px`,
    );
    update();
    const observer = new ResizeObserver(update);
    observer.observe(element);
    return () => {
      observer.disconnect();
      document.documentElement.style.removeProperty(property);
    };
  }, [enabled, property, ref]);
}

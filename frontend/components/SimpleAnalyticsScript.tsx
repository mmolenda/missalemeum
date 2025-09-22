import Script from "next/script";
import React from "react";

export function SimpleAnalyticsScript() {
  return (
    <>
      <Script async defer src="https://scripts.simpleanalyticscdn.com/latest.js" />
    </>
  );
}

export default SimpleAnalyticsScript;

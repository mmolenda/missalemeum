import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Comma-separated hostnames for testing the dev server from other devices.
  allowedDevOrigins: process.env.NEXT_DEV_ALLOWED_ORIGINS?.split(",").map((host) => host.trim()).filter(Boolean),
  async rewrites() {
    // Keep browser requests on the dev frontend origin, including access over LAN.
    const apiBase = process.env.API_URL?.replace(/\/+$/, "");
    if (process.env.NODE_ENV !== "development" || !apiBase) return [];
    return [{
      source: "/:locale(pl|en)/api/:path*",
      destination: `${apiBase}/:locale/api/:path*`,
    }];
  },
  experimental: {
    optimizePackageImports: [],
  },
};

export default nextConfig;

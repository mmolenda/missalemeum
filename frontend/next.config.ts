import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Comma-separated hostnames for testing the dev server from other devices.
  allowedDevOrigins: process.env.NEXT_DEV_ALLOWED_ORIGINS?.split(",").map((host) => host.trim()).filter(Boolean),
  experimental: {
    optimizePackageImports: [],
  },
};

export default nextConfig;

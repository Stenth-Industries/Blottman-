/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    // AVIF first (next/image defaults to WebP-only). AVIF is ~30-50% smaller
    // than WebP for these photographic PNGs → fixes "Improve image delivery".
    formats: ["image/avif", "image/webp"],
    // Cache optimized images for a year so Lighthouse's "Use efficient cache
    // lifetimes" passes for /_next/image responses (default is 60s).
    minimumCacheTTL: 31536000,
  },
};

export default nextConfig;

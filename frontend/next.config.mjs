/** @type {import('next').NextConfig} */
const nextConfig = {
  // Environment variable validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '/api',
  },
  
  // Output configuration for Docker
  output: 'standalone',

  // Don't redirect trailing slashes so Django API routes work correctly
  skipTrailingSlashRedirect: true,
  
  // Image domains if using next/image
  images: {
    domains: [],
  },
  
  // INTERNAL_API_URL is used by app/api/[...path]/route.ts at runtime (not needed in rewrites)

};

export default nextConfig;

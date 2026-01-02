/** @type {import('next').NextConfig} */
const nextConfig = {
  // Environment variable validation
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  
  // Image domains if using next/image
  images: {
    domains: [],
    // Add your image domains here if needed
    // domains: ['your-cdn-domain.com'],
  },
  
  // API rewrites if needed (optional)
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: `${process.env.NEXT_PUBLIC_API_URL}/api/:path*`,
  //     },
  //   ];
  // },
};

export default nextConfig;

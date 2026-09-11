import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.INTERNAL_API_URL
  || (process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:8014' : 'http://backend:8014');

async function proxyRequest(request: NextRequest, params: { path: string[] }) {
  const pathSegments = params.path;
  // Always include trailing slash for Django APPEND_SLASH compatibility
  const backendPath = `/api/${pathSegments.join('/')}/`;
  const searchParams = request.nextUrl.searchParams.toString();
  const targetUrl = `${BACKEND_URL}${backendPath}${searchParams ? `?${searchParams}` : ''}`;

  const headers = new Headers();
  request.headers.forEach((value, key) => {
    // Skip headers that shouldn't be forwarded
    if (!['host', 'connection', 'transfer-encoding'].includes(key.toLowerCase())) {
      headers.set(key, value);
    }
  });

  let body: BodyInit | null = null;
  const method = request.method;
  if (!['GET', 'HEAD'].includes(method)) {
    body = await request.text();
  }

  const response = await fetch(targetUrl, {
    method,
    headers,
    body,
    redirect: 'manual', // Don't follow redirects; let client handle them
  });

  const responseHeaders = new Headers();
  response.headers.forEach((value, key) => {
    if (!['transfer-encoding', 'connection'].includes(key.toLowerCase())) {
      responseHeaders.set(key, value);
    }
  });

  const responseBody = await response.arrayBuffer();
  return new NextResponse(responseBody, {
    status: response.status,
    headers: responseHeaders,
  });
}

type RouteContext = { params: Promise<{ path: string[] }> };

async function handleRequest(request: NextRequest, { params }: RouteContext) {
  return proxyRequest(request, await params);
}

export async function GET(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

export async function POST(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

export async function PUT(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

export async function PATCH(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

export async function DELETE(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

export async function OPTIONS(request: NextRequest, context: RouteContext) {
  return handleRequest(request, context);
}

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { headers } from 'next/headers';
import { resolveAcceptLanguage } from 'resolve-accept-language'


export async function middleware(request: NextRequest) {
  const defaultLocale = "en-US";
  const headersList = await headers();
  const acceptLanguageHeader = headersList.get('accept-language') || defaultLocale;
  const locale = resolveAcceptLanguage(
    acceptLanguageHeader,
    [defaultLocale, 'pl-PL'] as const,
    defaultLocale
  );
  const language = locale.split("-")[0];
  const pathname = request.nextUrl.pathname;

  if (pathname === "/" || pathname === "/calendar") {
    const suffix = pathname === "/calendar" ? "/calendar" : "";
    return NextResponse.redirect(new URL(`/${language}${suffix}`, request.url));
  }

  return NextResponse.next();
}
export const config = {
  matcher: ['/', '/calendar'],
}
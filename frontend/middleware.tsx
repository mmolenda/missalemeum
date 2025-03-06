import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { headers } from 'next/headers';
import { resolveAcceptLanguage } from 'resolve-accept-language'


export async function middleware(request: NextRequest) {
  let defaultLocale = "en-US"
  const headersList = await headers()
  const acceptLanguageHeader = headersList.get('accept-language') || defaultLocale
  const locale = resolveAcceptLanguage(
    acceptLanguageHeader,
    [defaultLocale, 'pl-PL'] as const,
    defaultLocale
  )
  return NextResponse.redirect(new URL(`/${locale.split("-")[0]}`, request.url))
}

export const config = {
  matcher: '/',
}
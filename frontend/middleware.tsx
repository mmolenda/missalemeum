import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { resolveAcceptLanguage } from 'resolve-accept-language'

const DEFAULT_LOCALE = 'en-US'
const SUPPORTED = ['en-US', 'pl-PL'] as const
const SUPPORTED_LOCALES = new Set(['en', 'pl'])
const APP_SECTIONS = new Set(['calendar', 'ordo', 'oratio', 'canticum', 'supplement', 'votive', 'widgets'])
const COOKIE_OPTIONS = { path: '/', maxAge: 60 * 60 * 24 * 365 }

const toSupportedLocale = (value?: string): 'en' | 'pl' => {
  if (value && SUPPORTED_LOCALES.has(value)) {
    return value as 'en' | 'pl'
  }
  return 'en'
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const cookies = request.cookies
  const storedLocale = cookies.get('mm-last-locale')?.value
  const inAppMode = cookies.get('mm-app-mode')?.value === 'true'

  const acceptLanguage = request.headers.get('accept-language') ?? DEFAULT_LOCALE
  const resolved = resolveAcceptLanguage(acceptLanguage, SUPPORTED, DEFAULT_LOCALE)
  const fallbackLocale = toSupportedLocale(resolved.split('-')[0])
  const lastLocale = storedLocale ? toSupportedLocale(storedLocale) : fallbackLocale

  if (pathname === '/') {
    const targetLocale = inAppMode ? lastLocale : fallbackLocale
    const targetPath = inAppMode ? `/${targetLocale}/calendar` : `/${fallbackLocale}`
    return NextResponse.redirect(new URL(targetPath, request.url))
  }

  if (pathname === '/calendar' || pathname === '/calendar/') {
    const targetLocale = lastLocale ?? fallbackLocale
    return NextResponse.redirect(new URL(`/${targetLocale}/calendar`, request.url))
  }

  const segments = pathname.split('/').filter(Boolean)
  const localeFromPath = segments[0]

  if (localeFromPath && SUPPORTED_LOCALES.has(localeFromPath)) {
    const response = NextResponse.next()
    response.cookies.set('mm-last-locale', localeFromPath, COOKIE_OPTIONS)

    const section = segments[1]
    if (section && APP_SECTIONS.has(section)) {
      response.cookies.set('mm-app-mode', 'true', COOKIE_OPTIONS)
    } else if (!section) {
      response.cookies.set('mm-app-mode', 'false', COOKIE_OPTIONS)
    }

    return response
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/', '/calendar', '/(en|pl)/:path*'],
}

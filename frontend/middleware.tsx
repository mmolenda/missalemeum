import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { headers } from 'next/headers';
import * as acceptLanguageParser from 'accept-language-parser';

export async function middleware(request: NextRequest) {
  let defaultLocale = "en"
  const headersList = await headers()
  const acceptLanguage = headersList.get('accept-language') || defaultLocale
  const languages = acceptLanguageParser.parse(acceptLanguage)
  const primaryLanguage = languages.length > 0 ? languages[0].code : defaultLocale
  const locale = primaryLanguage == "pl" ? "pl" : "en"
  return NextResponse.redirect(new URL(`/${locale}`, request.url))
}

export const config = {
  matcher: '/',
}
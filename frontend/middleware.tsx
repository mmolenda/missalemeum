import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

// This function can be marked `async` if using `await` inside
export function middleware(request: NextRequest) {
  let defaultLocale = "en"
  return NextResponse.redirect(new URL(`/${defaultLocale}`, request.url))
}

export const config = {
  matcher: '/',
}
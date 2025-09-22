import type {MetadataRoute} from 'next'

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Missale Meum',
    short_name: 'MissaleMeum',
    start_url: '/calendar',
    display: 'standalone',
    background_color: '#fcfbf9',
    theme_color: '#000000',
    icons: [
      {
        "src": "favicon.ico",
        "sizes": "32x32",
        "type": "image/x-icon"
      },
      {
        "src": "logo192.png",
        "type": "image/png",
        "sizes": "192x192",
        "purpose": "any"
      },
      {
        "src": "logo512.png",
        "type": "image/png",
        "sizes": "512x512",
        "purpose": "any"
      },
      {
        "src": "maskable_icon_x192.png",
        "type": "image/png",
        "sizes": "192x192",
        "purpose": "maskable"
      },
      {
        "src": "maskable_icon_x512.png",
        "type": "image/png",
        "sizes": "512x512",
        "purpose": "maskable"
      }
    ],
  }
}
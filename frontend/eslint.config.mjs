// eslint.config.mjs
import { FlatCompat } from '@eslint/eslintrc';

const compat = new FlatCompat({ baseDirectory: import.meta.dirname });

export default [
  // Ignore build artifacts
  {
    ignores: [
      '**/node_modules/**',
      '**/.next/**',
      '**/out/**',
      '**/build/**',
      'next-env.d.ts',
    ],
  },

  // Next.js recommended + Core Web Vitals + TypeScript rules
  ...compat.extends('next/core-web-vitals', 'next/typescript'),

  // Your tweaks
  {
    rules: {
      'react/no-unescaped-entities': 'off',
      '@next/next/no-page-custom-font': 'off',
    },
  },
];

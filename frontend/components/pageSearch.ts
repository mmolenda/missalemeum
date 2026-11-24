type PageSearchItem = {title: string; path: string; tags?: string[]};

const PAGE_REFERENCE_PATTERN = /^(.+?)\s+[sp]\.\s*(\d+)$/;
export const isPageReference = (tag: string) => PAGE_REFERENCE_PATTERN.test(tag);

export const isPageQuery = (query: string) => /^\d+$/.test(query.trim());

export function findPageResults<T extends PageSearchItem>(items: T[], query: string, locale: string) {
  if (!isPageQuery(query)) return [];
  const page = query.trim().replace(/^0+(?=\d)/, "");
  const seen = new Set<string>();
  const matches: (T & {publication: string; pageReference: string})[] = [];
  for (const item of items) {
    for (const tag of item.tags ?? []) {
      const reference = tag.match(PAGE_REFERENCE_PATTERN);
      if (!reference || reference[2] !== page) continue;
      const key = `${item.path}\u0000${tag}`;
      if (seen.has(key)) continue;
      seen.add(key);
      matches.push({...item, publication: reference[1].replace(/,$/, "").trim(), pageReference: tag});
    }
  }
  return matches.sort((a, b) => a.publication.localeCompare(b.publication, locale)
    || a.title.localeCompare(b.title, locale));
}

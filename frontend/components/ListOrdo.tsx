"use client";

import List from "@mui/material/List";
import {ListSurface} from "@/components/listStyles";
import IndexListItem from "@/components/IndexListItem";
import slugify from "slugify";
import {ListItemType} from "@/components/types";

export default function ListOrdo({lang, items}: {lang: string; items: ListItemType[]}) {
  return (
    <ListSurface>
      <List className="list-index">
        {items.map((item) => (
          <IndexListItem
            key={item.label}
            title={item.label}
            href={`/${lang}/ordo#${slugify(item.label)}`}
          />
        ))}
      </List>
    </ListSurface>
  );
}

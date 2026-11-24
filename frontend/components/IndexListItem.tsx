"use client";

import {Fragment, type Ref} from "react";
import Link from "next/link";
import {Box, ListItem, ListItemButton} from "@mui/material";

export default function IndexListItem({title, details, href, selected, ref}: {
  title: string;
  details?: string[];
  href: string;
  selected?: boolean;
  ref?: Ref<HTMLLIElement>;
}) {
  return (
    <ListItem ref={ref} className="list-item" disableGutters>
      <ListItemButton className="list-link" component={Link} href={href} selected={selected}>
        <Box component="span" className="list-title">{title}</Box>
        {!!details?.length && <Box component="span" className="list-details">
          {details.map((detail, index) => <Fragment key={index}>
            {index > 0 && <> <Box component="span" className="list-separator">·</Box> </>}
            {detail}
          </Fragment>)}
        </Box>}
      </ListItemButton>
    </ListItem>
  );
}

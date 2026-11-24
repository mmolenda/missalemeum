import React from "react";
import List from "@mui/material/List";
import {Box, ListItem, Skeleton} from "@mui/material";
import {ListSurface} from "@/components/listStyles";

export default function SkeletonIndex() {
  return (
    <ListSurface aria-hidden="true">
      <List className="list-index">
        {Array.from({length: 30}, (_, index) => (
          <ListItem key={index} className="list-item" disableGutters>
            <Box className="list-skeleton">
              <Skeleton variant="text" animation="wave" width="70%" height={24} />
              <Skeleton variant="text" animation="wave" width="40%" height={20} />
            </Box>
          </ListItem>
        ))}
      </List>
    </ListSurface>
  );
}

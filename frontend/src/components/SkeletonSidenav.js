import React from 'react';
import List from "@mui/material/List";
import {SidenavListItem} from "./styledComponents/SidenavListItem";
import {Skeleton} from "@mui/material";

export default function SkeletonSidenav() {
	return (
		<List>
			{[...Array(30).keys()].map((x) => {
				return (
					<SidenavListItem
							key={x}
							disableGutters={true}
							sx={{
								display: "flex",
								flexDirection: "column",
								alignItems: "start",
								pl: "1.5rem"
							}}
					>
						<Skeleton variant="text" key={`${x}1`} animation="wave" width="70%" height={30} />
						<Skeleton variant="text" key={`${x}2`} animation="wave" width="40%" height={30} sx={{backgroundColor: "secondary.main"}}/>
					</SidenavListItem>)
			}
			)}
		</List>
	)
}


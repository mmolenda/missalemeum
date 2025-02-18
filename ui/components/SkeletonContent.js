import React from 'react';
import {Box, Skeleton} from "@mui/material";

export default function SkeletonContent() {
	return (
		<Box sx={{ml: "2rem"}}>
			<Skeleton key="0" variant="text" animation="wave" width="70%" height={50} />
			<Skeleton key="1" variant="text" animation="wave" width="50%" height={50} sx={{backgroundColor: "secondary.main"}} />
			{[...Array(6).keys()].map((x) => {
				return (
					<React.Fragment key={`${x}0`}>
						<Skeleton variant="text" key={`${x}1`}  animation="wave" width="40%" height={30} />
						<Skeleton variant="text" key={`${x}2`}  animation="wave" width="90%" height={30}/>
						<Skeleton variant="text" key={`${x}3`}  animation="wave" width="90%" height={30}/>
						<Skeleton variant="text" key={`${x}4`}  animation="wave" width="90%" height={30}/>
						<Skeleton variant="text" key={`${x}5`}  animation="wave" width="90%" height={30}/>
						<Skeleton variant="text" key={`${x}6`}  animation="wave" width="90%" height={30}/>
					</React.Fragment>)
			}
			)}
		</Box>
	)
}


import React from 'react';

export default function Logo({width, height}: {width: number, height: number}) {
	return (
		<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width={`${width}.0pt`} height={`${height}.0pt`} viewBox="0 0 512 512"
				 preserveAspectRatio="xMidYMid meet">
			<g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)" fill="#fcfbf9" stroke="none">
				<path
					d="M963 4775c-102 -31 -185 -104 -232 -204l-26 -56 0 -1955 0 -1955 27 -57c37 -79 98 -142 177 -181l66 -32
					1634 -3 1634 -2 44 21c166 81 178 303 20 407l-41 27 -1487 5 -1487 5 -43 30c-23 17 -51 48 -62 69 -42 81 -13
					192 63 239l35 22 1420 5 1420 5 57 23c81 33 160 108 200 190l33 67 0 1535 0 1535 -32 66c-39 79 -102 140 -181
					177l-57 27 -697 3 -698 2 -2 -854 -3 -854 -24 -26c-39 -41 -96 -36 -152 12 -24 22 -120 102 -213 180l-169 141
					-62 -52c-34 -29 -131 -109 -214 -179 -129 -109 -157 -128 -186 -128 -47 0 -64 8 -80 41 -13 24 -15 151 -15
					874l0 845 -312 -1c-229 0 -324 -4 -355 -14z"/>
			</g>
		</svg>
	)
}
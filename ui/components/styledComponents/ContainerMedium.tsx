import {styled} from "@mui/system";
import {Container} from "@mui/material";

export const ContainerMedium = styled(Container)((props) => ({
  [props.theme.breakpoints.up("md")]: {
    width: "900px"
  },
}));


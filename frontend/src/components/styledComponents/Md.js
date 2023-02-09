import React from 'react';
import ReactMarkdown from "react-markdown";
import {Link, Typography} from "@mui/material";
import {Link as RouterLink} from "react-router-dom";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";


export default function Md(props) {
  let text = (props.markdownNewlines) ? props.text : props.text.replace(/\\n/g, '\n').replace(/\n/g, '  \n')
  return (
    <ReactMarkdown
      children={text}
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw]}
      components={{
        "h3": (props) => <Typography variant="h3">{props.children[0]}</Typography>,
        "h4": (props) => <Typography variant="h4">{props.children[0]}</Typography>,
        "a": (props) => <Link
                              component={RouterLink}
                              to={{pathname: props.href}}
                              target={(props.href.startsWith("http") ? "_blank" : "")}
                              href='#'>{props.children[0]}</Link>
      }}
    />
  )
}
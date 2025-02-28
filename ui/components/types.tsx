
export type BodyRow = string[]

export type Body = BodyRow[]

export type Section = {
  id: string
  label: string
  body: Body
}

export type Supplement = {
  label: string
  path: string
}

export type Info = {
  title: string
  description: string
  date: string
  tempora: string
  rank: number
  colors: string[]
  tags: string[]
  commemorations: string[]
  supplements: Supplement[]
}

export type ColorCode = 'r' | 'g' | 'w' | 'v' | 'b' | 'p';

export type Content = {
  info: Info
  sections: Section[]
}
export type ClassValue =
  | string
  | number
  | null
  | undefined
  | false
  | ClassValue[];

export const cn = (...inputs: ClassValue[]): string =>
  inputs
    .flat(Infinity as 1)
    .filter((x): x is string | number => Boolean(x))
    .join(" ");

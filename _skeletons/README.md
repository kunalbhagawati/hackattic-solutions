# Skeletons

Common setup code/files that each solution can pick from at the setup of the solution.

This is _NOT_ a common library, but instead is a repository of config files, package.json and requirement.txt, etc.

The idea is that each solution is it's own project (even the common libs).
This help setting them up without having to search for config again across the internet.

All the config files across languages are in the same place, with the understanding that at the end of the day,
each solution can itself have multiple programming languages as part of it.

## NOTES
- Node 20 and typescript ESM are incompatible as of now (01/Apr/2024), and so we default to 18 LTS
  - https://github.com/TypeStrong/ts-node/issues/1997
  - https://stackoverflow.com/a/76758731/3297499

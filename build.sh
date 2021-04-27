#!/bin/bash

for out in src/body_*.py ; do
  [[ -e "${out}" ]] || break

  echo "${out}"
  x="${out#src/body_}"
  x="${x%.py}"

  out="mongo_$x"

  cat > "${out}" <<- "EOF"
#!/usr/bin/env python3

## GENERATED FILE - DO NOT EDIT
EOF

  {
    cat "src/header.py" \
    && cat "src/body_${x}.py" \
    && cat "src/footer.py"
  } >> "${out}"

  chmod 755 "${out}"

done

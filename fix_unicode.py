#!/usr/bin/env python3
# Run this in your game folder:  python fix_unicode.py
# It fixes the garbled text characters in game.py so pygbag can read it.

with open("game.py", "rb") as f:
    raw = f.read()

# The file was originally UTF-8 but got saved as cp1252 on Windows.
# To recover: decode as cp1252, re-encode as latin-1 to get original UTF-8 bytes, then decode as UTF-8.
text_cp1252 = raw.decode("cp1252", errors="replace")
recovered_bytes = text_cp1252.encode("latin-1", errors="replace")
text = recovered_bytes.decode("utf-8", errors="replace")

with open("game.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Done! game.py is now valid UTF-8.")
print("Try running:  pygbag game.py")
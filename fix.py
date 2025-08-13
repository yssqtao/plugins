#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix filenames like "xxx.png.png" -> "xxx.png" in a directory.

用法:
  python fix_filenames_keep_one_png.py --dir ./icons
  python fix_filenames_keep_one_png.py --dir ./icons --recursive
  python fix_filenames_keep_one_png.py --dir ./icons --recursive --dry-run
"""
import argparse
import os
import re
import sys

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".ico", ".bmp", ".avif")

def compress_ext(name: str) -> str:
    """
    将重复的图片扩展名压缩为一个，并去掉扩展名前多余空格。
    例如:
      "logo.png.png" -> "logo.png"
      "a.jpg.jpg.jpg" -> "a.jpg"
      "icon .png" -> "icon.png"
    """
    n = name
    changed = True
    # 连续压缩重复扩展名
    while changed:
        changed = False
        lower = n.lower()
        for ext in IMAGE_EXTS:
            patt = ext + ext
            while lower.endswith(patt):
                n = n[:-(len(ext))]  # 去掉一个扩展名
                lower = n.lower()
                changed = True
    # 去掉扩展名前的空格: "xxx .png" -> "xxx.png"
    n = re.sub(r"\s+(\.(?:png|jpg|jpeg|webp|gif|svg|ico|bmp|avif))$", r"\1", n, flags=re.I)
    return n

def iter_files(root: str, recursive: bool = False):
    if recursive:
        for d, _, files in os.walk(root):
            for f in files:
                yield os.path.join(d, f)
    else:
        for f in os.listdir(root):
            p = os.path.join(root, f)
            if os.path.isfile(p):
                yield p

def main():
    ap = argparse.ArgumentParser(description="Compress duplicate image extensions in filenames.")
    ap.add_argument("--dir", required=True, help="要处理的目录")
    ap.add_argument("--recursive", action="store_true", help="递归处理子目录")
    ap.add_argument("--dry-run", action="store_true", help="仅预览不改名")
    args = ap.parse_args()

    root = args.dir
    if not os.path.isdir(root):
        print(f"Directory not found: {root}", file=sys.stderr)
        sys.exit(2)

    count = 0
    for path in iter_files(root, args.recursive):
        folder, file = os.path.split(path)
        fixed = compress_ext(file)
        if fixed != file:
            new_path = os.path.join(folder, fixed)
            print(f"{file}  ->  {fixed}")
            count += 1
            if not args.dry_run:
                # 避免同名覆盖：自动追加 _1/_2/...
                i = 1
                base, ext = os.path.splitext(new_path)
                final = new_path
                while os.path.exists(final):
                    final = f"{base}_{i}{ext}"
                    i += 1
                os.rename(path, final)
    print(f"Done. Renamed {count} file(s).")

if __name__ == "__main__":
    main()

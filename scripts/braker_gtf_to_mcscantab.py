#!/usr/bin/env python3
import re
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.gtf> [prefix]", file=sys.stderr)
        sys.exit(1)

    inputf = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) >= 3 else "pt"

    # assuming seqid pattern: ptg000001l (or ptg...c)
    seqid_re = re.compile(r"^ptg(\d+)[lc]$")

    with open(inputf, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue

            line = line.rstrip("\n")
            ary = line.split("\t")
            if len(ary) < 9:
                # skip malformed lines
                continue

            seqid = ary[0]
            type_ = ary[2]
            start = int(ary[3])
            end_pos = int(ary[4])
            attributes = ary[8]

            if type_ == "transcript":
                geneid = attributes.strip()

                m = seqid_re.match(seqid)
                if not m:
                    raise ValueError(f"Unexpected seqid format: {seqid}")

                # Ruby: match(seqid)[1][-2,2]  -> last 2 digits of captured number
                digits = m.group(1)
                chr_ = prefix + digits[-2:]

                # Ruby prints: chr, geneid, start-1, end_pos
                print(f"{chr_}\t{geneid}\t{start - 1}\t{end_pos}")

if __name__ == "__main__":
    main()

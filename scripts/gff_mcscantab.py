#!/usr/bin/env python3
import re
import sys


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.gff> <acc2chr.tsv>", file=sys.stderr)
        sys.exit(1)

    inputf = sys.argv[1]
    acc2chr_file = sys.argv[2]

    # Load accession -> chromosome mapping
    acc2chr: dict[str, str] = {}
    with open(acc2chr_file, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            ary = line.split("\t")
            if len(ary) < 2:
                continue
            acc, chr_ = ary[0], ary[1]
            acc2chr[acc] = chr_


#    print(acc2chr)
    # Regex to extract geneid from GFF attributes: ID=cds-<geneid>;
    geneid_re = re.compile(r"ID=cds-([^;]+)")

    with open(inputf, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                continue

            raw = line.rstrip("\n")
            ary = raw.split("\t")
            if len(ary) < 9:
                # skip malformed lines
                continue

            seqid = ary[0]
            type_ = ary[2]
            start = int(ary[3])
            end_pos = int(ary[4])
            attributes = ary[8]

            if type_ != "CDS":
                continue

            m = geneid_re.search(attributes)
            if not m:
                raise ValueError(f"Cannot parse gene ID from attributes: {attributes}")

            geneid = m.group(1)

            if seqid not in acc2chr:
                # Ruby prints the line then raises
                print(raw, file=sys.stderr)
                raise KeyError(f"seqid not found in acc2chr mapping: {seqid}")

            chromosome = acc2chr[seqid]

            # Convert to MCScanX format (0-based start)
            print(f"{chromosome}\t{geneid}\t{start - 1}\t{end_pos}")


if __name__ == "__main__":
    main()

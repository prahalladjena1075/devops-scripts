import re
import sys
from collections import Counter

# Matches one line of an Nginx/Apache "combined" access log
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) [^"]*" (?P<status>\d{3}) (?P<size>\S+)'
)


def analyze(file_path):
    ips = Counter()
    pages = Counter()
    statuses = Counter()
    not_found_pages = Counter()
    total = 0
    skipped = 0

    with open(file_path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            match = LOG_PATTERN.match(line)
            if not match:
                skipped += 1          # line in a different format
                continue

            total += 1
            ip = match.group("ip")
            path = match.group("path")
            status = match.group("status")

            ips[ip] += 1
            pages[path] += 1
            statuses[status] += 1
            if status == "404":
                not_found_pages[path] += 1

    return total, skipped, ips, pages, statuses, not_found_pages


def build_report(file_path, top_n=5):
    total, skipped, ips, pages, statuses, not_found = analyze(file_path)

    lines = []
    lines.append("=" * 45)
    lines.append("LOG ANALYSIS REPORT")
    lines.append("=" * 45)
    lines.append(f"File              : {file_path}")
    lines.append(f"Total requests    : {total}")
    lines.append(f"Skipped lines     : {skipped}")
    lines.append(f"404 errors        : {statuses.get('404', 0)}")
    lines.append(f"5xx server errors : {sum(c for s, c in statuses.items() if s.startswith('5'))}")

    lines.append("\nStatus codes:")
    for status, count in sorted(statuses.items()):
        lines.append(f"  {status} : {count}")

    lines.append(f"\nTop {top_n} requested pages:")
    for path, count in pages.most_common(top_n):
        lines.append(f"  {count:>4}  {path}")

    lines.append(f"\nTop {top_n} IP addresses:")
    for ip, count in ips.most_common(top_n):
        lines.append(f"  {count:>4}  {ip}")

    lines.append("\nPages that returned 404:")
    if not_found:
        for path, count in not_found.most_common(top_n):
            lines.append(f"  {count:>4}  {path}")
    else:
        lines.append("  none")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python log_analyzer.py <log_file>")
        sys.exit(1)

    try:
        report = build_report(sys.argv[1])
    except FileNotFoundError:
        print(f"Error: file '{sys.argv[1]}' not found")
        sys.exit(1)

    print(report)
    with open("report.txt", "w") as f:
        f.write(report + "\n")
    print("\nReport saved to report.txt")


if __name__ == "__main__":
    main()
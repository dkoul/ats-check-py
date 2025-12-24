#!/usr/bin/env python3
"""CLI interface for ATS resume checker."""

import argparse
import sys
from pathlib import Path
from .parser import parse_resume, parse_text_file
from .checker import check_ats_compliance
from .formatter import format_output


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Check resume for ATS (Applicant Tracking System) compatibility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ats-check resume.pdf
  ats-check resume.docx --jd job.txt
  ats-check resume.pdf --jd job.txt --verbose
        """
    )

    parser.add_argument(
        "resume",
        type=str,
        help="Path to resume file (PDF or DOCX)"
    )

    parser.add_argument(
        "--jd",
        type=str,
        help="Path to job description file (TXT)",
        default=None
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed analysis (for nerds)"
    )

    args = parser.parse_args()

    # Validate resume file exists
    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"Error: Resume file not found: {args.resume}", file=sys.stderr)
        sys.exit(1)

    # Validate resume file extension
    if resume_path.suffix.lower() not in [".pdf", ".docx"]:
        print(f"Error: Unsupported file format. Use PDF or DOCX files.", file=sys.stderr)
        sys.exit(1)

    # Parse job description if provided
    jd_text = None
    if args.jd:
        jd_path = Path(args.jd)
        if not jd_path.exists():
            print(f"Error: Job description file not found: {args.jd}", file=sys.stderr)
            sys.exit(1)
        jd_text = parse_text_file(jd_path)

    # Parse resume
    try:
        resume_text = parse_resume(resume_path)
    except Exception as e:
        print(f"Error parsing resume: {e}", file=sys.stderr)
        sys.exit(1)

    # Check ATS compliance
    results = check_ats_compliance(resume_text, jd_text, verbose=args.verbose)

    # Format and print output
    output = format_output(results, verbose=args.verbose)
    print(output)

    # Exit with appropriate code
    sys.exit(0 if results["score"] >= 70 else 1)


if __name__ == "__main__":
    main()

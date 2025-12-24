"""Output formatting utilities."""

from typing import Dict, Any


def format_output(results: Dict[str, Any], verbose: bool = False) -> str:
    """
    Format ATS check results for display.

    Args:
        results: Results dictionary from checker
        verbose: Include verbose details

    Returns:
        Formatted output string
    """
    score = results["score"]
    issues = results["issues"]
    keyword_match = results.get("keyword_match")
    verbose_details = results.get("verbose_details")

    # Build output
    lines = []

    # Header with score
    lines.append(f"ATS Compliance Score: {score}/100")
    lines.append(f"Status: {get_status_label(score)}")
    lines.append("")

    # Issues section
    if issues:
        lines.append("Issues found:")
        for i, issue in enumerate(issues, 1):
            lines.append(f"{i}. {issue}")
        lines.append("")
    else:
        lines.append("No issues found! Your resume looks ATS-friendly.")
        lines.append("")

    # Suggested next steps
    if issues:
        lines.append("Suggested next steps:")
        suggestions = generate_suggestions(issues, keyword_match)
        for suggestion in suggestions:
            lines.append(f"- {suggestion}")
        lines.append("")

    # Verbose details
    if verbose and verbose_details:
        lines.append("=" * 60)
        lines.append("VERBOSE DETAILS")
        lines.append("=" * 60)
        lines.append("")

        # Missing sections
        if "missing_sections" in verbose_details:
            lines.append("Missing Sections:")
            for section in verbose_details["missing_sections"]:
                lines.append(f"  - {section.title()}")
            lines.append("")

        # Found sections
        if "found_sections" in verbose_details:
            lines.append("Found Sections:")
            for section in verbose_details["found_sections"]:
                lines.append(f"   {section.title()}")
            lines.append("")

        # Icon details
        if "icon_count" in verbose_details:
            lines.append(f"Icons/Emojis Found: {verbose_details['icon_count']}")
            if verbose_details.get("icon_examples"):
                lines.append(f"  Examples: {', '.join(verbose_details['icon_examples'])}")
            lines.append("")

        # Formatting issues
        if "formatting_issues" in verbose_details:
            lines.append("Formatting Issues:")
            for issue in verbose_details["formatting_issues"]:
                lines.append(f"  - {issue}")
            lines.append("")

        # Keyword analysis
        if keyword_match is not None:
            lines.append(f"Keyword Match: {keyword_match}%")
            lines.append("")

            if "resume_keywords" in verbose_details:
                lines.append("Top Resume Keywords:")
                keywords = verbose_details["resume_keywords"][:10]
                lines.append(f"  {', '.join(keywords)}")
                lines.append("")

            if "jd_keywords" in verbose_details:
                lines.append("Top Job Description Keywords:")
                keywords = verbose_details["jd_keywords"][:10]
                lines.append(f"  {', '.join(keywords)}")
                lines.append("")

            if "missing_keywords" in verbose_details and verbose_details["missing_keywords"]:
                lines.append("Missing Key Terms from JD:")
                for keyword in verbose_details["missing_keywords"][:10]:
                    lines.append(f"  - {keyword}")
                lines.append("")

    return "\n".join(lines)


def get_status_label(score: int) -> str:
    """
    Get status label based on score.

    Args:
        score: ATS compliance score

    Returns:
        Status label
    """
    if score >= 85:
        return "Excellent ATS Compatibility"
    elif score >= 70:
        return "Good ATS Compatibility"
    elif score >= 50:
        return "Moderate ATS Compatibility"
    else:
        return "Poor ATS Compatibility"


def generate_suggestions(issues: list, keyword_match: int = None) -> list:
    """
    Generate suggestions based on issues found.

    Args:
        issues: List of issues
        keyword_match: Keyword match percentage

    Returns:
        List of suggestions
    """
    suggestions = []

    for issue in issues:
        if "Missing standard heading" in issue:
            # Extract the section name
            section = issue.split(":")[-1].strip()
            suggestions.append(f"Add a clearly labeled {section} section")

        elif "icons/emojis" in issue:
            suggestions.append("Replace icons with text bullets (•, -, or *)")

        elif "Keyword match" in issue and keyword_match:
            suggestions.append("Mirror key skills from the job description")
            if keyword_match < 40:
                suggestions.append("Consider tailoring your resume more closely to the JD")

        elif "multi-column" in issue:
            suggestions.append("Use a single-column layout for better ATS parsing")

        elif "special characters" in issue:
            suggestions.append("Reduce use of special characters and symbols")

        elif "header/footer" in issue:
            suggestions.append("Remove headers/footers or move content to main body")

    # Remove duplicates while preserving order
    seen = set()
    unique_suggestions = []
    for suggestion in suggestions:
        if suggestion not in seen:
            seen.add(suggestion)
            unique_suggestions.append(suggestion)

    return unique_suggestions

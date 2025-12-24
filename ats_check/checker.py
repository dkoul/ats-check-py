"""ATS compliance checker logic."""

import re
from typing import Dict, List, Optional, Any
from .keyword_matcher import extract_keywords, calculate_keyword_match


# Standard resume sections that ATS systems look for
STANDARD_SECTIONS = [
    # Experience variations
    "experience",
    "work experience",
    "professional experience",
    "employment history",
    "work history",
    "career history",

    # Education
    "education",
    "academic background",
    "qualifications",

    # Skills variations
    "skills",
    "technical skills",
    "soft skills",
    "core competencies",
    "key skills",
    "areas of expertise",
    "core skills",

    # Certifications
    "certifications",
    "certificates",
    "licenses",

    # Summary variations
    "summary",
    "objective",
    "profile summary",
    "professional summary",
    "career summary",
    "career objective",
    "professional profile",

    # Optional but recognized sections
    "projects",
    "achievements",
    "accomplishments",
    "awards",
    "languages",
    "publications",
]

# Common problematic patterns in resumes
ICON_PATTERNS = [
    r"[▪●○■□◆◇★☆]",  # Common bullet symbols
    r"[\u2600-\u26FF]",  # Miscellaneous symbols
    r"[\u2700-\u27BF]",  # Dingbats
    r"[\U0001F300-\U0001F9FF]",  # Emojis
]


def check_ats_compliance(
    resume_text: str,
    jd_text: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Check resume for ATS compliance.

    Args:
        resume_text: Extracted resume text
        jd_text: Optional job description text
        verbose: Include detailed analysis

    Returns:
        Dictionary with compliance results
    """
    issues = []
    score = 100
    verbose_details = {}

    # Check for standard sections
    missing_sections = check_standard_sections(resume_text)
    if missing_sections:
        for section in missing_sections:
            issues.append(f"Missing standard heading: {section.title()}")
            score -= 10
        if verbose:
            verbose_details["missing_sections"] = missing_sections
            verbose_details["found_sections"] = find_sections(resume_text)

    # Check for icons/emojis
    icon_matches = check_for_icons(resume_text)
    if icon_matches:
        issues.append("Detected icons/emojis (ATS may skip content)")
        score -= 15
        if verbose:
            verbose_details["icon_count"] = len(icon_matches)
            verbose_details["icon_examples"] = icon_matches[:5]

    # Check for complex formatting issues
    formatting_issues = check_formatting(resume_text)
    if formatting_issues:
        issues.extend(formatting_issues)
        score -= len(formatting_issues) * 5
        if verbose:
            verbose_details["formatting_issues"] = formatting_issues

    # Check keyword match with job description
    keyword_match = None
    if jd_text:
        keyword_match = calculate_keyword_match(resume_text, jd_text)
        if keyword_match < 50:
            issues.append(f"Keyword match with JD is low ({keyword_match}%)")
            score -= 20
        elif keyword_match < 70:
            issues.append(f"Keyword match with JD could be improved ({keyword_match}%)")
            score -= 10

        if verbose:
            resume_keywords = extract_keywords(resume_text)
            jd_keywords = extract_keywords(jd_text)
            verbose_details["keyword_match"] = keyword_match
            verbose_details["resume_keywords"] = resume_keywords[:20]
            verbose_details["jd_keywords"] = jd_keywords[:20]
            verbose_details["missing_keywords"] = list(
                set(jd_keywords[:20]) - set(resume_keywords[:20])
            )

    # Ensure score doesn't go below 0
    score = max(0, score)

    return {
        "score": score,
        "issues": issues,
        "keyword_match": keyword_match,
        "verbose_details": verbose_details if verbose else None,
    }


def check_standard_sections(text: str) -> List[str]:
    """
    Check for missing standard resume sections.

    Args:
        text: Resume text

    Returns:
        List of missing section names
    """
    text_lower = text.lower()
    found_sections = find_sections(text_lower)

    # Required sections (at least one of these should be present)
    required_groups = [
        ["experience", "work experience", "professional experience", "employment history", "work history", "career history"],
        ["education", "academic background", "qualifications"],
        ["skills", "technical skills", "soft skills", "core competencies", "key skills", "areas of expertise", "core skills"],
    ]

    missing = []
    for group in required_groups:
        if not any(section in found_sections for section in group):
            # Return the most common term from the group
            missing.append(group[0] if group[0] != "experience" else "work experience")

    return missing[:3]  # Limit to top 3 missing sections


def find_sections(text: str) -> List[str]:
    """
    Find all section headings in the resume.

    Args:
        text: Resume text (preferably lowercase)

    Returns:
        List of found section names
    """
    found = []
    for section in STANDARD_SECTIONS:
        # Look for section as a heading (standalone on a line or followed by newline/colon)
        pattern = rf"(?:^|\n)\s*{re.escape(section)}\s*(?:[:\n]|$)"
        if re.search(pattern, text, re.IGNORECASE):
            found.append(section)

    return found


def check_for_icons(text: str) -> List[str]:
    """
    Check for icons and emojis in resume.

    Args:
        text: Resume text

    Returns:
        List of found icons/emojis
    """
    icons = []
    for pattern in ICON_PATTERNS:
        matches = re.findall(pattern, text)
        icons.extend(matches)

    return list(set(icons))  # Return unique icons


def check_formatting(text: str) -> List[str]:
    """
    Check for formatting issues that ATS may struggle with.

    Args:
        text: Resume text

    Returns:
        List of formatting issues
    """
    issues = []

    # Check for very short lines (possible columns or tables)
    lines = text.split("\n")
    short_lines = [line for line in lines if 0 < len(line.strip()) < 20]
    if len(short_lines) / max(len(lines), 1) > 0.4:
        issues.append("Possible multi-column layout detected (may confuse ATS)")

    # Check for excessive special characters
    special_char_ratio = len(re.findall(r"[^a-zA-Z0-9\s\n.,;:()'-]", text)) / max(len(text), 1)
    if special_char_ratio > 0.05:
        issues.append("High ratio of special characters detected")

    # Check for headers/footers (repeated content)
    if len(lines) > 10:
        first_line = lines[0].strip()
        last_line = lines[-1].strip()
        if first_line and first_line == last_line and len(first_line) > 10:
            issues.append("Possible header/footer detected (may cause parsing issues)")

    return issues

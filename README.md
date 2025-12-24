# ATS Resume Checker

A Python CLI tool to check your resume for ATS (Applicant Tracking System) compatibility.

## Features

- ✅ PDF and DOCX resume support
- ✅ Checks for standard resume sections
- ✅ Detects ATS-unfriendly formatting (icons, emojis, multi-column layouts)
- ✅ Keyword matching with job descriptions
- ✅ Detailed compliance scoring (0-100)
- ✅ Actionable suggestions for improvement
- ✅ Verbose mode for detailed analysis

## Installation

```bash
# Clone or download this repository
cd ats-check-py

# Install dependencies
pip install -r requirements.txt

# Install the CLI tool
pip install -e .
```

## Usage

### Basic usage (check resume only):
```bash
ats-check resume.pdf
```

### With job description:
```bash
ats-check resume.docx --jd job.txt
```

### Verbose mode (for detailed analysis):
```bash
ats-check resume.pdf --jd job.txt --verbose
```

## Sample Output

```
ATS Compliance Score: 78/100
Status: Moderate ATS Compatibility

Issues found:
1. Missing standard heading: Skills
2. Detected icons/emojis (ATS may skip content)
3. Keyword match with JD is low (42%)

Suggested next steps:
- Add a clearly labeled Skills section
- Replace icons with text bullets (•, -, or *)
- Mirror key skills from the job description
```

## What Does It Check?

### Standard Sections
- Work Experience / Professional Experience
- Education
- Skills
- Certifications (optional)
- Summary/Objective (optional)

### Formatting Issues
- Icons and emojis (⚠️ ✓ ★ etc.)
- Multi-column layouts
- Excessive special characters
- Headers/footers that may cause parsing issues

### Keyword Matching
When you provide a job description (`--jd`), the tool:
- Extracts key terms from both resume and JD
- Calculates keyword overlap percentage
- Identifies missing important keywords
- Suggests improvements

## Scoring System

- **85-100**: Excellent ATS Compatibility
- **70-84**: Good ATS Compatibility
- **50-69**: Moderate ATS Compatibility
- **0-49**: Poor ATS Compatibility

## Tips for ATS-Friendly Resumes

1. **Use standard section headings**: "Work Experience", "Education", "Skills"
2. **Avoid fancy formatting**: No icons, emojis, or graphics
3. **Single-column layout**: ATS struggles with multi-column formats
4. **Use standard fonts**: Arial, Calibri, Times New Roman
5. **Save as DOCX or PDF**: Ensure text is selectable (not images)
6. **Mirror keywords**: Include relevant terms from the job description
7. **Use simple bullets**: Stick to •, -, or *

## Requirements

- Python 3.8+
- PyPDF2
- python-docx
- scikit-learn

## License

MIT License - feel free to use and modify!

## Contributing

Pull requests welcome! Some ideas for improvements:
- Add support for more file formats
- Industry-specific keyword dictionaries
- Integration with job boards
- Resume template suggestions

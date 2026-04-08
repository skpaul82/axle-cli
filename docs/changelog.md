# Changelog

All notable changes to Axle CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-08

### Added
- **Uninstall command** (`axle uninstall`)
  - Preserves tools directory by default
  - Clear instructions for complete removal
  - Shows reinstallation steps
  - Options to keep or remove tools directory

### Enhanced
- **Environment checking** in interactive installer
  - Comprehensive validation at startup
  - Python version verification (3.10+ required)
  - pip availability check
  - Package installation capability test
  - FAQ links when requirements aren't met
  - Common solutions for known issues
  - Option to continue or exit if problems found

### Fixed
- **Package structure reorganization**
  - Renamed `scripts/` → `axle/` for standard Python packaging
  - Fixed entry point: `axle.axle:main`
  - Updated all internal imports
  - Resolved CI/CD installation issues

### Changed
- **Code formatting** - Applied black formatting to all Python files
- **Updated documentation** to reflect Axle branding and new structure
- **Enhanced troubleshooting** with Python version and pip solutions

### Technical
- Updated pyproject.toml with black configuration
- Fixed GitHub Actions CI workflow paths
- Updated publish workflow test commands
- Improved error messages and user guidance

## [1.0.0] - 2026-04-08

### Added
- Initial production release of Axle CLI platform
- Core CLI with 8 commands: list, run, info, scan, doctor, path, help, security, uninstall
- Tool numbering system for easy reference
- Dynamic tool loading and discovery
- Community footer in all command outputs

### Tools

### Added
- Initial release of Buddy Tools CLI toolkit
- Core CLI with 7 commands: list, run, info, scan, doctor, path, help
- Tool numbering system for easy reference
- Dynamic tool loading and discovery
- Community footer in all command outputs

### Tools
- **SEO Keyword Checker** (01_seo_keyword_checker.py)
  - Keyword density analysis
  - Keyword extraction using NLTK
  - Prominence checking (first 100 words)
  - SEO optimization suggestions
  - Visual density indicators

- **Meta Tag Auditor** (02_meta_tag_auditor.py)
  - URL and HTML file analysis
  - Title tag optimization (50-60 chars)
  - Meta description checking (150-160 chars)
  - Open Graph and Twitter Card detection
  - Schema.org markup checking
  - Heading structure analysis
  - Image alt text verification

- **Daily Life Hack Generator** (03_daily_life_hack_generator.py)
  - 50+ curated life hacks across 7 categories
  - Semantic matching for relevant suggestions
  - Difficulty ratings (Easy/Medium/Hard)
  - Time estimates for each hack
  - Categories: Morning, Productivity, Health, Finance, Tech, Organization, Mindfulness

### Installation
- Interactive installer (`axle.install_axle`)
- System requirements checking
- Guided setup with prompts
- Automatic dependency installation
- spaCy model download
- Installation verification

### Security
- **Pre-execution security validation** (MANDATORY for all tools)
  - Dangerous pattern detection (eval, exec, shell=True)
  - Hardcoded secret detection (API keys, passwords, tokens)
  - Unsafe import checking (pickle, marshal)
  - Configurable security policies (strict, warn, permissive)
- Dependency vulnerability scanner (axle/security_scan.py)
- pip-audit integration
- Basic static analysis for Python scripts
- Prioritized security recommendations

### Documentation
- Comprehensive README with quick start
- Installation guide with platform-specific instructions
- Usage guide with examples and best practices
- Complete command reference
- Troubleshooting guide with enhanced FAQ
- Contributing guidelines
- Changelog

### CI/CD
- GitHub Actions workflow (.github/workflows/ci.yml)
- Lint checks with flake8, black, isort
- Installation testing on Python 3.10 and 3.11
- Security scan integration

### Dependencies
- pandas >= 1.5.0
- numpy >= 1.23.0
- scikit-learn >= 1.2.0
- spacy >= 3.5.0
- sentence-transformers >= 2.2.0
- beautifulsoup4 >= 4.12.0
- requests >= 2.28.0
- nltk >= 3.8.0
- lxml >= 4.9.0
- pip-audit >= 2.0.0

### Features
- Community footer with social links
- Environment diagnostics (axle doctor)
- Tool information display (axle info)
- Security configuration (axle security)
- Graceful error handling
- Helpful error messages
- Support for running tools by number or name
- Platform philosophy: Run ANY Python tool consistently

### System Requirements
- Python 3.10 or higher
- 8GB RAM minimum (16GB recommended)
- 5-8GB free disk space
- macOS, Linux, or Windows

## [Future Versions]

### [1.2.0] - Planned
- Unit tests with pytest
- Configuration file support (.axlerc)
- Tool alias system (custom names for tools)
- Progress indicators for long-running tools
- Improved error messages
- Tool discovery from multiple directories

### [1.3.0] - Planned
- More SEO tools (backlink checker, SERP scraper)
- More productivity tools (habit tracker, time calculator)
- Web interface (Flask/FastAPI)
- Database support for storing results
- Export results to JSON/CSV
- Batch processing mode

### [2.0.0] - Planned
- PyPI publishing
- Full test coverage (80%+)
- API documentation
- Comprehensive plugin system
- Internationalization support
- Tool marketplace/community sharing
- Performance optimizations
- Reduced memory footprint

---

## Versioning Policy

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

## Release Cadence

- **Major releases**: As needed for significant changes
- **Minor releases**: Every 2-3 months for new features
- **Patch releases**: As needed for bug fixes

## Support Policy

- Current version (1.1.0): Full support
- Previous versions: Best-effort support
- Security updates: Provided for all supported versions

---

## Contributors

- Sanjoy K. Paul - Creator and maintainer

## License

MIT License - see [LICENSE](../LICENSE) for details.

## Links

- GitHub: https://github.com/skpaul82/axle-cli
- X/Twitter: [@_skpaul82](https://x.com/_skpaul82)
- Instagram: [skpaul82](https://instagram.com/skpaul82)
- Newsletter: [axle.sanjoypaul.com/agent-aio](https://axle.sanjoypaul.com/agent-aio)

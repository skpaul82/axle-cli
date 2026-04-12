#!/usr/bin/env python3
"""Automatic code review and auto-fixing engine for Axle CLI.

This module provides comprehensive code quality checking and automatic
fixing capabilities for Python tools, integrating Black, isort, and flake8.
"""

import json
import os
import subprocess
import sys
import tempfile
from difflib import unified_diff
from pathlib import Path
from typing import Callable, List, Optional, Tuple


# Severity levels for code quality issues
SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"
SEVERITY_LOW = "LOW"

# Issue categories
CATEGORY_FORMATTING = "FORMATTING"
CATEGORY_IMPORTS = "IMPORTS"
CATEGORY_LINTING = "LINTING"
CATEGORY_COMPLEXITY = "COMPLEXITY"

# Auto-fix capability
FIXABLE_AUTO = "AUTO"      # Can be automatically fixed
FIXABLE_MANUAL = "MANUAL"  # Requires manual intervention


class CodeIssue:
    """Represents a code quality issue found during review."""

    def __init__(
        self,
        severity: str,
        category: str,
        message: str,
        line_no: int = None,
        fixable: str = FIXABLE_MANUAL,
        fix_command: str = None,
        suggestion: str = None,
        file_path: Path = None,
    ):
        self.severity = severity
        self.category = category
        self.message = message
        self.line_no = line_no
        self.fixable = fixable
        self.fix_command = fix_command
        self.suggestion = suggestion
        self.file_path = file_path

    def __str__(self):
        """Format issue for user display."""
        line_info = f":{self.line_no}" if self.line_no else ""
        emoji = {
            SEVERITY_CRITICAL: "🔴",
            SEVERITY_HIGH: "🟠",
            SEVERITY_MEDIUM: "🟡",
            SEVERITY_LOW: "🟢",
        }.get(self.severity, "⚪")

        fixable_indicator = "✓" if self.fixable == FIXABLE_AUTO else "✗"

        output = [f"{emoji} {self.severity}{line_info} [{self.category}] {self.message}"]

        if self.fixable == FIXABLE_AUTO:
            if self.fix_command:
                output.append(f"   💡 Can auto-fix: {self.fix_command}")
            elif self.suggestion:
                output.append(f"   💡 {self.suggestion}")
        else:
            if self.suggestion:
                output.append(f"   💡 {self.suggestion}")

        return "\n".join(output)

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "line_no": self.line_no,
            "fixable": self.fixable,
            "fix_command": self.fix_command,
            "suggestion": self.suggestion,
        }


class CodeReviewer:
    """Main code review engine for Python tools."""

    def __init__(self, verbose: bool = False):
        """Initialize code reviewer.

        Args:
            verbose: Enable detailed output
        """
        self.verbose = verbose
        self.issues = []

    def review_file(self, tool_path: Path) -> List[CodeIssue]:
        """Run comprehensive code review on a Python file.

        Args:
            tool_path: Path to the Python file to review

        Returns:
            List of CodeIssue objects found
        """
        if not tool_path.exists():
            return [CodeIssue(
                SEVERITY_CRITICAL,
                CATEGORY_LINTING,
                f"File not found: {tool_path}",
                fixable=FIXABLE_MANUAL,
                suggestion="Check that the file path is correct",
                file_path=tool_path,
            )]

        self.issues = []

        if self.verbose:
            print(f"🔍 Reviewing {tool_path.name}...")

        # Run all code quality checks
        self._check_black_formatting(tool_path)
        self._check_isort_imports(tool_path)
        self._check_flake8_linting(tool_path)

        return self.issues

    def _check_black_formatting(self, tool_path: Path) -> None:
        """Check if file needs Black formatting.

        Args:
            tool_path: Path to the Python file
        """
        try:
            result = subprocess.run(
                ["black", "--check", str(tool_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                self.issues.append(CodeIssue(
                    SEVERITY_MEDIUM,
                    CATEGORY_FORMATTING,
                    "Code formatting issues found by Black",
                    fixable=FIXABLE_AUTO,
                    fix_command="black <file>",
                    suggestion="Run Black to automatically fix formatting",
                    file_path=tool_path,
                ))

                if self.verbose:
                    print(f"   ⚠️  Black formatting issues detected")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            if self.verbose:
                print(f"   ⚠️  Could not run Black: {e}")

    def _check_isort_imports(self, tool_path: Path) -> None:
        """Check if file imports are properly sorted.

        Args:
            tool_path: Path to the Python file
        """
        try:
            result = subprocess.run(
                ["isort", "--check-only", str(tool_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                self.issues.append(CodeIssue(
                    SEVERITY_MEDIUM,
                    CATEGORY_IMPORTS,
                    "Import statements not sorted correctly",
                    fixable=FIXABLE_AUTO,
                    fix_command="isort <file>",
                    suggestion="Run isort to automatically sort imports",
                    file_path=tool_path,
                ))

                if self.verbose:
                    print(f"   ⚠️  Import sorting issues detected")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            if self.verbose:
                print(f"   ⚠️  Could not run isort: {e}")

    def _check_flake8_linting(self, tool_path: Path) -> None:
        """Check for code quality issues using flake8.

        Args:
            tool_path: Path to the Python file
        """
        try:
            # Run flake8 with JSON output for easier parsing
            result = subprocess.run(
                [
                    "flake8",
                    "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s",
                    "--max-line-length=88",  # Match Black's default
                    str(tool_path)
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.stdout.strip():
                self._parse_flake8_output(result.stdout, tool_path)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            if self.verbose:
                print(f"   ⚠️  Could not run flake8: {e}")

    def _parse_flake8_output(self, output: str, tool_path: Path) -> None:
        """Parse flake8 output and create CodeIssue objects.

        Args:
            output: Raw flake8 output
            tool_path: Path to the file being reviewed
        """
        for line in output.strip().split("\n"):
            if not line:
                continue

            try:
                # Parse format: file:line:col: CODE message
                parts = line.split(":")
                if len(parts) < 4:
                    continue

                line_no = int(parts[1])
                code_and_msg = parts[3].strip()
                code = code_and_msg.split()[0]
                message = " ".join(code_and_msg.split()[1:])

                # Categorize and determine fixability
                issue = self._categorize_flake8_issue(code, message, line_no, tool_path)
                if issue:
                    self.issues.append(issue)

            except (ValueError, IndexError) as e:
                if self.verbose:
                    print(f"   ⚠️  Could not parse flake8 line: {line}")

    def _categorize_flake8_issue(self, code: str, message: str, line_no: int, tool_path: Path) -> Optional[CodeIssue]:
        """Categorize a flake8 issue and determine if it's fixable.

        Args:
            code: flake8 error code (e.g., F401, E501)
            message: Error message
            line_no: Line number where issue occurs
            tool_path: Path to the file being reviewed

        Returns:
            CodeIssue object or None if issue should be ignored
        """
        # Import-related issues (auto-fixable)
        if code == "F401":  # Unused import
            return CodeIssue(
                SEVERITY_LOW,
                CATEGORY_IMPORTS,
                f"Unused import: {message}",
                line_no=line_no,
                fixable=FIXABLE_AUTO,
                suggestion=f"Remove the unused import",
                file_path=tool_path,
            )

        # Variable-related issues (auto-fixable)
        if code == "F841":  # Unused variable
            return CodeIssue(
                SEVERITY_LOW,
                CATEGORY_LINTING,
                f"Unused variable: {message}",
                line_no=line_no,
                fixable=FIXABLE_AUTO,
                suggestion=f"Remove or use the variable",
                file_path=tool_path,
            )

        # Line length (manual fix)
        if code == "E501":  # Line too long
            return CodeIssue(
                SEVERITY_LOW,
                CATEGORY_FORMATTING,
                f"Line too long: {message}",
                line_no=line_no,
                fixable=FIXABLE_MANUAL,
                suggestion="Break the line or use Black's line wrapping",
                file_path=tool_path,
            )

        # Syntax/undefined name errors (critical, manual fix)
        if code.startswith("E9") or code in ["F621", "F632", "F821", "F822"]:
            return CodeIssue(
                SEVERITY_CRITICAL,
                CATEGORY_LINTING,
                f"{code}: {message}",
                line_no=line_no,
                fixable=FIXABLE_MANUAL,
                suggestion="Fix the syntax or undefined name error",
                file_path=tool_path,
            )

        # Other issues (medium severity, manual fix)
        return CodeIssue(
            SEVERITY_MEDIUM,
            CATEGORY_LINTING,
            f"{code}: {message}",
            line_no=line_no,
            fixable=FIXABLE_MANUAL,
            suggestion=f"Address the flake8 issue: {code}",
            file_path=tool_path,
        )

    def auto_fix_issues(self, tool_path: Path, issues: List[CodeIssue], dry_run: bool = False) -> Tuple[int, int]:
        """Automatically fix fixable issues.

        Args:
            tool_path: Path to the Python file
            issues: List of CodeIssue objects
            dry_run: If True, show what would be fixed without making changes

        Returns:
            Tuple of (auto_fixed_count, manual_fix_count)
        """
        if not issues:
            return 0, 0

        # Create backup before making changes
        if not dry_run:
            backup_path = self._create_backup(tool_path)
        else:
            backup_path = None

        auto_fixed = 0
        manual_fixes = 0

        # Check if there are formatting issues
        has_formatting = any(i.category == CATEGORY_FORMATTING and i.fixable == FIXABLE_AUTO for i in issues)
        has_imports = any(i.category == CATEGORY_IMPORTS and i.fixable == FIXABLE_AUTO for i in issues)

        try:
            # Apply Black formatting
            if has_formatting:
                if dry_run:
                    print(f"   📋 Would fix: Black formatting")
                else:
                    if self._apply_black_fix(tool_path):
                        auto_fixed += 1
                        if self.verbose:
                            print(f"   ✅ Applied Black formatting")

            # Apply isort import sorting
            if has_imports:
                if dry_run:
                    print(f"   📋 Would fix: Import sorting")
                else:
                    if self._apply_isort_fix(tool_path):
                        auto_fixed += 1
                        if self.verbose:
                            print(f"   ✅ Applied import sorting")

            # Count manual fixes needed
            manual_fixes = sum(1 for i in issues if i.fixable == FIXABLE_MANUAL)

            # Verify fixes didn't break anything
            if not dry_run and auto_fixed > 0:
                if not self._verify_fixes(tool_path):
                    if backup_path:
                        self._restore_backup(tool_path, backup_path)
                        print(f"   ⚠️  Fixes broke the file, restored from backup")
                    else:
                        print(f"   ⚠️  Fixes may have caused issues")

        except Exception as e:
            if backup_path:
                self._restore_backup(tool_path, backup_path)
            raise e

        return auto_fixed, manual_fixes

    def _apply_black_fix(self, tool_path: Path) -> bool:
        """Apply Black formatting to a file.

        Args:
            tool_path: Path to the Python file

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ["black", str(tool_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _apply_isort_fix(self, tool_path: Path) -> bool:
        """Apply isort import sorting to a file.

        Args:
            tool_path: Path to the Python file

        Returns:
            True if successful, False otherwise
        """
        try:
            result = subprocess.run(
                ["isort", str(tool_path)],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def _create_backup(self, tool_path: Path) -> Path:
        """Create a backup of a file.

        Args:
            tool_path: Path to the file to backup

        Returns:
            Path to the backup file
        """
        backup_path = tool_path.with_suffix(tool_path.suffix + ".backup")
        import shutil
        shutil.copy2(tool_path, backup_path)
        return backup_path

    def _restore_backup(self, tool_path: Path, backup_path: Path) -> bool:
        """Restore a file from backup.

        Args:
            tool_path: Path to restore to
            backup_path: Path to backup file

        Returns:
            True if successful, False otherwise
        """
        try:
            import shutil
            shutil.move(str(backup_path), str(tool_path))
            return True
        except Exception:
            return False

    def _verify_fixes(self, tool_path: Path) -> bool:
        """Verify that fixes didn't break the file.

        Args:
            tool_path: Path to the file to verify

        Returns:
            True if file is still valid Python, False otherwise
        """
        try:
            # Try to compile the file
            with open(tool_path, 'r') as f:
                compile(f.read(), str(tool_path), 'exec')
            return True
        except (SyntaxError, IOError):
            return False

    def format_user_feedback(self, issues: List[CodeIssue]) -> str:
        """Format issues for user-friendly display.

        Args:
            issues: List of CodeIssue objects

        Returns:
            Formatted string for display
        """
        if not issues:
            return "✅ No code quality issues found!"

        # Group issues by severity
        by_severity = {
            SEVERITY_CRITICAL: [],
            SEVERITY_HIGH: [],
            SEVERITY_MEDIUM: [],
            SEVERITY_LOW: [],
        }

        for issue in issues:
            by_severity[issue.severity].append(issue)

        output = []
        total_issues = len(issues)

        output.append(f"Found {total_issues} code quality issue(s):\n")

        # Display issues by severity (critical first)
        for severity in [SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM, SEVERITY_LOW]:
            if by_severity[severity]:
                for issue in by_severity[severity]:
                    output.append(str(issue))

        # Summary
        auto_fixable = sum(1 for i in issues if i.fixable == FIXABLE_AUTO)
        manual_only = sum(1 for i in issues if i.fixable == FIXABLE_MANUAL)

        output.append(f"\n📊 Summary:")
        output.append(f"   Auto-fixable: {auto_fixable}")
        output.append(f"   Manual fixes: {manual_only}")

        return "\n".join(output)


def get_code_review_policy() -> str:
    """Get the current code review policy from environment.

    Returns:
        Policy name: 'always', 'auto', or 'never'
    """
    # Default to never (skip code review by default)
    return os.getenv("AXLE_CODE_REVIEW", "never").lower()


def get_auto_fix_policy() -> bool:
    """Get the auto-fix policy from environment.

    Returns:
        True if auto-fix is enabled, False otherwise
    """
    return os.getenv("AXLE_AUTO_FIX", "false").lower() == "true"


def should_run_code_review(tool_path: Path = None) -> bool:
    """Determine if code review should run based on policy.

    Args:
        tool_path: Optional path to tool being reviewed

    Returns:
        True if code review should run, False otherwise
    """
    policy = get_code_review_policy()

    if policy == "never":
        return False
    elif policy == "always":
        return True
    elif policy == "auto":
        # Auto: run only if there are issues or if file changed recently
        if tool_path and tool_path.exists():
            # Check if file was modified in the last hour
            import time
            recent_file = time.time() - tool_path.stat().st_mtime < 3600
            return recent_file
        return True

    return False


def main():
    """Command-line interface for code review."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run automatic code review on Python files"
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Python files to review"
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Apply automatic fixes"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable detailed output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    reviewer = CodeReviewer(verbose=args.verbose)
    all_issues = []

    # Review all files
    for file_path in args.files:
        issues = reviewer.review_file(file_path)
        all_issues.extend(issues)

    # Output results
    if args.json:
        output = {
            "total_issues": len(all_issues),
            "issues": [issue.to_dict() for issue in all_issues]
        }
        print(json.dumps(output, indent=2))
    else:
        print(reviewer.format_user_feedback(all_issues))

    # Apply fixes if requested
    if args.fix or args.dry_run:
        for file_path in args.files:
            file_issues = [i for i in all_issues if i.file_path == file_path]
            if file_issues:
                auto_fixed, manual_fixes = reviewer.auto_fix_issues(
                    file_path,
                    file_issues,
                    dry_run=args.dry_run
                )
                if not args.json:
                    print(f"\n📁 {file_path.name}:")
                    if auto_fixed > 0:
                        print(f"   ✅ Applied {auto_fixed} automatic fix(es)")
                    if manual_fixes > 0:
                        print(f"   ⚠️  {manual_fixes} issue(s) need manual attention")

    # Exit with error code if critical issues found
    has_critical = any(i.severity == SEVERITY_CRITICAL for i in all_issues)
    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()

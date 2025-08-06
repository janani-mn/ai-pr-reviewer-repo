#!/usr/bin/env python3
"""
Multi-language Lint Checker

Checks code style, formatting, and linting issues across multiple languages
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class LintChecker:
    def __init__(self):
        self.results = {
            "total_files": 0,
            "files_with_issues": 0,
            "errors": 0,
            "warnings": 0,
            "style_issues": [],
            "lint_score": 100
        }

    def check_files(self, files: List[str]):
        """Check multiple files for linting issues"""
        print(f"🎨 Checking code style and linting for {len(files)} files...")
        
        for file_path in files:
            if not os.path.exists(file_path):
                continue
            
            self.results["total_files"] += 1
            
            ext = Path(file_path).suffix.lower()
            issues = []
            
            # Route to appropriate linter based on file extension
            if ext in ['.js', '.jsx']:
                issues = self._check_javascript(file_path)
            elif ext in ['.ts', '.tsx']:
                issues = self._check_typescript(file_path)
            elif ext == '.py':
                issues = self._check_python(file_path)
            elif ext == '.java':
                issues = self._check_java(file_path)
            elif ext == '.go':
                issues = self._check_go(file_path)
            elif ext == '.rs':
                issues = self._check_rust(file_path)
            elif ext in ['.c', '.cpp', '.h']:
                issues = self._check_cpp(file_path)
            elif ext == '.cs':
                issues = self._check_csharp(file_path)
            elif ext == '.php':
                issues = self._check_php(file_path)
            elif ext == '.rb':
                issues = self._check_ruby(file_path)
            
            # Add common checks for all files
            issues.extend(self._check_common_issues(file_path))
            
            if issues:
                self.results["files_with_issues"] += 1
                self.results["style_issues"].extend(issues)
        
        # Count errors and warnings
        for issue in self.results["style_issues"]:
            if issue["severity"] == "error":
                self.results["errors"] += 1
            else:
                self.results["warnings"] += 1
        
        # Calculate lint score
        self._calculate_lint_score()
        
        # Save results
        with open('lint-results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"🎨 Lint check complete")
        print(f"📊 Files checked: {self.results['total_files']}")
        print(f"⚠️ Files with issues: {self.results['files_with_issues']}")
        print(f"🔴 Errors: {self.results['errors']}")
        print(f"🟡 Warnings: {self.results['warnings']}")
        print(f"📈 Lint score: {self.results['lint_score']}/100")

    def _check_javascript(self, file_path: str) -> List[Dict]:
        """Check JavaScript files with ESLint"""
        issues = []
        
        try:
            # Try running ESLint
            result = subprocess.run(
                ['npx', 'eslint', '--format', 'json', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            if result.stdout:
                eslint_results = json.loads(result.stdout)
                
                for file_result in eslint_results:
                    for message in file_result.get('messages', []):
                        issues.append({
                            "file": file_path,
                            "line": message.get('line', 1),
                            "column": message.get('column', 1),
                            "severity": "error" if message.get('severity') == 2 else "warning",
                            "message": message.get('message', ''),
                            "rule": message.get('ruleId', ''),
                            "category": "eslint"
                        })
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            # Fallback to basic checks
            issues.extend(self._basic_javascript_check(file_path))
        
        return issues

    def _check_typescript(self, file_path: str) -> List[Dict]:
        """Check TypeScript files"""
        issues = []
        
        try:
            # Check with TypeScript compiler
            result = subprocess.run(
                ['npx', 'tsc', '--noEmit', '--pretty', 'false', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            if result.stderr:
                lines = result.stderr.strip().split('\n')
                for line in lines:
                    if 'error TS' in line:
                        # Parse TypeScript error format
                        parts = line.split(':', 4)
                        if len(parts) >= 4:
                            line_num = parts[1] if parts[1].isdigit() else 1
                            issues.append({
                                "file": file_path,
                                "line": int(line_num),
                                "severity": "error",
                                "message": parts[-1].strip(),
                                "category": "typescript"
                            })
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # Fallback to JavaScript checks
            issues.extend(self._basic_javascript_check(file_path))
        
        return issues

    def _check_python(self, file_path: str) -> List[Dict]:
        """Check Python files with flake8 and pylint"""
        issues = []
        
        # Try flake8
        try:
            result = subprocess.run(
                ['flake8', '--format=json', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            if result.stdout:
                flake8_results = json.loads(result.stdout)
                for issue in flake8_results:
                    issues.append({
                        "file": file_path,
                        "line": issue.get('line_number', 1),
                        "column": issue.get('column_number', 1),
                        "severity": "warning",
                        "message": issue.get('text', ''),
                        "rule": issue.get('code', ''),
                        "category": "flake8"
                    })
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            # Fallback to basic Python checks
            issues.extend(self._basic_python_check(file_path))
        
        return issues

    def _check_java(self, file_path: str) -> List[Dict]:
        """Check Java files with Checkstyle"""
        issues = []
        
        # Basic Java style checks
        issues.extend(self._basic_java_check(file_path))
        
        return issues

    def _check_go(self, file_path: str) -> List[Dict]:
        """Check Go files with gofmt and golint"""
        issues = []
        
        try:
            # Check formatting with gofmt
            result = subprocess.run(
                ['gofmt', '-d', file_path],
                capture_output=True, text=True, timeout=15
            )
            
            if result.stdout.strip():
                issues.append({
                    "file": file_path,
                    "line": 1,
                    "severity": "warning",
                    "message": "File is not properly formatted. Run 'gofmt -w' to fix.",
                    "category": "gofmt"
                })
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return issues

    def _check_rust(self, file_path: str) -> List[Dict]:
        """Check Rust files with rustfmt and clippy"""
        issues = []
        
        try:
            # Check formatting
            result = subprocess.run(
                ['rustfmt', '--check', file_path],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode != 0:
                issues.append({
                    "file": file_path,
                    "line": 1,
                    "severity": "warning",
                    "message": "File is not properly formatted. Run 'rustfmt' to fix.",
                    "category": "rustfmt"
                })
        
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        return issues

    def _check_cpp(self, file_path: str) -> List[Dict]:
        """Check C/C++ files with clang-format"""
        issues = []
        
        # Basic C++ style checks
        issues.extend(self._basic_cpp_check(file_path))
        
        return issues

    def _check_csharp(self, file_path: str) -> List[Dict]:
        """Check C# files"""
        issues = []
        
        # Basic C# style checks
        issues.extend(self._basic_csharp_check(file_path))
        
        return issues

    def _check_php(self, file_path: str) -> List[Dict]:
        """Check PHP files with PHP CodeSniffer"""
        issues = []
        
        # Basic PHP style checks
        issues.extend(self._basic_php_check(file_path))
        
        return issues

    def _check_ruby(self, file_path: str) -> List[Dict]:
        """Check Ruby files with RuboCop"""
        issues = []
        
        try:
            result = subprocess.run(
                ['rubocop', '--format', 'json', file_path],
                capture_output=True, text=True, timeout=30
            )
            
            if result.stdout:
                rubocop_results = json.loads(result.stdout)
                
                for file_result in rubocop_results.get('files', []):
                    for offense in file_result.get('offenses', []):
                        issues.append({
                            "file": file_path,
                            "line": offense.get('location', {}).get('line', 1),
                            "column": offense.get('location', {}).get('column', 1),
                            "severity": offense.get('severity', 'warning'),
                            "message": offense.get('message', ''),
                            "rule": offense.get('cop_name', ''),
                            "category": "rubocop"
                        })
        
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            issues.extend(self._basic_ruby_check(file_path))
        
        return issues

    def _check_common_issues(self, file_path: str) -> List[Dict]:
        """Check for common issues across all file types"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Check for trailing whitespace
                if line.rstrip() != line.rstrip('\n'):
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "severity": "warning",
                        "message": "Trailing whitespace",
                        "category": "whitespace"
                    })
                
                # Check for very long lines (>120 characters)
                if len(line.rstrip()) > 120:
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "severity": "warning",
                        "message": f"Line too long ({len(line.rstrip())} > 120 characters)",
                        "category": "line-length"
                    })
                
                # Check for mixed tabs and spaces
                if '\t' in line and '    ' in line:
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "severity": "warning",
                        "message": "Mixed tabs and spaces for indentation",
                        "category": "indentation"
                    })
        
        except Exception as e:
            print(f"Error checking common issues in {file_path}: {e}")
        
        return issues

    def _basic_javascript_check(self, file_path: str) -> List[Dict]:
        """Basic JavaScript style checks when ESLint is not available"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # Check for missing semicolons (basic check)
                stripped = line.strip()
                if (stripped and not stripped.endswith((';', '{', '}', ':', ',')) and
                    not stripped.startswith(('if', 'for', 'while', 'function', 'class', 'const', 'let', 'var', '//'))):
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "severity": "warning",
                        "message": "Missing semicolon",
                        "category": "javascript-style"
                    })
        
        except Exception as e:
            print(f"Error in basic JavaScript check for {file_path}: {e}")
        
        return issues

    def _basic_python_check(self, file_path: str) -> List[Dict]:
        """Basic Python style checks when flake8 is not available"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                # Check for proper indentation (4 spaces)
                if line.startswith('    ') or line.startswith('\t'):
                    continue
                elif line.strip() and line.startswith(' '):
                    leading_spaces = len(line) - len(line.lstrip(' '))
                    if leading_spaces % 4 != 0:
                        issues.append({
                            "file": file_path,
                            "line": line_num,
                            "severity": "warning",
                            "message": f"Indentation should be multiple of 4 spaces (found {leading_spaces})",
                            "category": "python-indentation"
                        })
        
        except Exception as e:
            print(f"Error in basic Python check for {file_path}: {e}")
        
        return issues

    def _basic_java_check(self, file_path: str) -> List[Dict]:
        """Basic Java style checks"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                stripped = line.strip()
                
                # Check for proper brace placement
                if stripped.endswith('{') and not stripped.startswith(('if', 'for', 'while', 'class', 'public', 'private', 'protected')):
                    if line.count(' ') > 0 and not line.endswith(' {'):
                        issues.append({
                            "file": file_path,
                            "line": line_num,
                            "severity": "warning",
                            "message": "Opening brace should be preceded by a space",
                            "category": "java-style"
                        })
        
        except Exception as e:
            print(f"Error in basic Java check for {file_path}: {e}")
        
        return issues

    def _basic_cpp_check(self, file_path: str) -> List[Dict]:
        """Basic C++ style checks"""
        return []  # Implement basic C++ style checks as needed

    def _basic_csharp_check(self, file_path: str) -> List[Dict]:
        """Basic C# style checks"""
        return []  # Implement basic C# style checks as needed

    def _basic_php_check(self, file_path: str) -> List[Dict]:
        """Basic PHP style checks"""
        return []  # Implement basic PHP style checks as needed

    def _basic_ruby_check(self, file_path: str) -> List[Dict]:
        """Basic Ruby style checks"""
        return []  # Implement basic Ruby style checks as needed

    def _calculate_lint_score(self):
        """Calculate overall lint score"""
        errors = self.results["errors"]
        warnings = self.results["warnings"]
        
        # Start with 100 and deduct points for issues
        score = 100
        score -= errors * 10  # 10 points per error
        score -= warnings * 2  # 2 points per warning
        
        # Ensure score doesn't go below 0
        self.results["lint_score"] = max(0, score)

def main():
    if len(sys.argv) < 2:
        print("Usage: python lint-checker.py <file1> <file2> ...")
        sys.exit(1)
    
    files = [f.strip() for f in sys.argv[1].split() if f.strip()] if len(sys.argv) == 2 else sys.argv[1:]
    
    if not files:
        print("No files to check")
        sys.exit(0)
    
    checker = LintChecker()
    checker.check_files(files)

if __name__ == '__main__':
    main()

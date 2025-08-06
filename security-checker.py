#!/usr/bin/env python3
"""
Security Vulnerability Checker

Scans code for common security vulnerabilities and patterns
"""

import os
import re
import json
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class SecurityChecker:
    def __init__(self):
        self.results = {
            "total_files": 0,
            "files_with_issues": 0,
            "errors": 0,
            "warnings": 0,
            "vulnerabilities": [],
            "security_score": 100
        }
        
        # Load security patterns
        self.patterns = self._load_security_patterns()

    def _load_security_patterns(self) -> Dict[str, List[Dict]]:
        """Load security vulnerability patterns"""
        return {
            "sql_injection": [
                {
                    "pattern": r"(SELECT|INSERT|UPDATE|DELETE).*\+.*['\"]",
                    "message": "Potential SQL injection: String concatenation in SQL query",
                    "severity": "high"
                },
                {
                    "pattern": r"query\s*\(\s*[\"'].*\+.*[\"']\s*\)",
                    "message": "Potential SQL injection: Dynamic query construction",
                    "severity": "high"
                }
            ],
            "xss": [
                {
                    "pattern": r"innerHTML\s*=\s*.*\+.*",
                    "message": "Potential XSS: Dynamic HTML content without sanitization",
                    "severity": "high"
                },
                {
                    "pattern": r"document\.write\s*\(\s*.*\+.*\)",
                    "message": "Potential XSS: document.write with dynamic content",
                    "severity": "medium"
                },
                {
                    "pattern": r"eval\s*\(\s*.*\+.*\)",
                    "message": "Potential code injection: eval() with dynamic content",
                    "severity": "high"
                }
            ],
            "insecure_crypto": [
                {
                    "pattern": r"(md5|sha1)\s*\(",
                    "message": "Insecure cryptographic hash function (MD5/SHA1)",
                    "severity": "medium"
                },
                {
                    "pattern": r"Math\.random\(\)",
                    "message": "Weak random number generator - use crypto.randomBytes() instead",
                    "severity": "low"
                }
            ],
            "hardcoded_secrets": [
                {
                    "pattern": r"(password|secret|key|token)\s*=\s*[\"'][a-zA-Z0-9+/=]{10,}[\"']",
                    "message": "Potential hardcoded secret or password",
                    "severity": "high"
                },
                {
                    "pattern": r"(api_key|apikey)\s*=\s*[\"'][a-zA-Z0-9_-]{20,}[\"']",
                    "message": "Potential hardcoded API key",
                    "severity": "high"
                }
            ],
            "path_traversal": [
                {
                    "pattern": r"(open|read|write).*\.\./",
                    "message": "Potential path traversal vulnerability",
                    "severity": "high"
                },
                {
                    "pattern": r"fs\.(readFile|writeFile).*\+.*",
                    "message": "Potential path injection in file operations",
                    "severity": "medium"
                }
            ],
            "insecure_deserialization": [
                {
                    "pattern": r"pickle\.loads?\s*\(",
                    "message": "Insecure deserialization with pickle",
                    "severity": "high"
                },
                {
                    "pattern": r"yaml\.load\s*\(\s*.*\)",
                    "message": "Potential unsafe YAML deserialization",
                    "severity": "medium"
                }
            ],
            "command_injection": [
                {
                    "pattern": r"(system|exec|popen|subprocess)\s*\(.*\+.*\)",
                    "message": "Potential command injection: Dynamic command execution",
                    "severity": "high"
                },
                {
                    "pattern": r"os\.system\s*\(.*\+.*\)",
                    "message": "Potential command injection in os.system()",
                    "severity": "high"
                }
            ],
            "insecure_transport": [
                {
                    "pattern": r"http://(?!localhost|127\.0\.0\.1|0\.0\.0\.0)",
                    "message": "Insecure HTTP connection - use HTTPS",
                    "severity": "medium"
                },
                {
                    "pattern": r"ssl.*verify.*false|verify.*false.*ssl",
                    "message": "SSL certificate verification disabled",
                    "severity": "high"
                }
            ]
        }

    def check_files(self, files: List[str]):
        """Check multiple files for security vulnerabilities"""
        print(f"🔒 Scanning {len(files)} files for security vulnerabilities...")
        
        for file_path in files:
            if not os.path.exists(file_path):
                continue
                
            self.results["total_files"] += 1
            file_issues = self._scan_file(file_path)
            
            if file_issues:
                self.results["files_with_issues"] += 1
                self.results["vulnerabilities"].extend(file_issues)
        
        # Count errors and warnings
        for vuln in self.results["vulnerabilities"]:
            if vuln["severity"] == "high":
                self.results["errors"] += 1
            else:
                self.results["warnings"] += 1
        
        # Calculate security score
        self._calculate_security_score()
        
        # Save results
        with open('security-results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"🔒 Security scan complete")
        print(f"📊 Files scanned: {self.results['total_files']}")
        print(f"⚠️ Files with issues: {self.results['files_with_issues']}")
        print(f"🔴 High severity: {self.results['errors']}")
        print(f"🟡 Medium/Low severity: {self.results['warnings']}")
        print(f"📈 Security score: {self.results['security_score']}/100")

    def _scan_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan a single file for security issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Check each pattern category
            for category, patterns in self.patterns.items():
                for pattern_info in patterns:
                    pattern = pattern_info["pattern"]
                    message = pattern_info["message"]
                    severity = pattern_info["severity"]
                    
                    # Search for pattern in each line
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            issues.append({
                                "file": file_path,
                                "line": line_num,
                                "category": category,
                                "severity": severity,
                                "message": message,
                                "code_snippet": line.strip(),
                                "pattern": pattern
                            })
            
            # Language-specific checks
            self._check_language_specific(file_path, content, issues)
            
        except Exception as e:
            print(f"Error scanning {file_path}: {e}")
        
        return issues

    def _check_language_specific(self, file_path: str, content: str, issues: List[Dict]):
        """Perform language-specific security checks"""
        ext = Path(file_path).suffix.lower()
        
        if ext in ['.js', '.ts', '.jsx', '.tsx']:
            self._check_javascript_security(file_path, content, issues)
        elif ext == '.py':
            self._check_python_security(file_path, content, issues)
        elif ext == '.java':
            self._check_java_security(file_path, content, issues)
        elif ext == '.php':
            self._check_php_security(file_path, content, issues)

    def _check_javascript_security(self, file_path: str, content: str, issues: List[Dict]):
        """JavaScript-specific security checks"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for dangerous functions
            if re.search(r'\beval\s*\(', line):
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "category": "code_injection",
                    "severity": "high",
                    "message": "Use of eval() function - potential code injection risk",
                    "code_snippet": line.strip()
                })
            
            # Check for prototype pollution
            if re.search(r'__proto__|constructor\.prototype', line):
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "category": "prototype_pollution",
                    "severity": "medium",
                    "message": "Potential prototype pollution vulnerability",
                    "code_snippet": line.strip()
                })

    def _check_python_security(self, file_path: str, content: str, issues: List[Dict]):
        """Python-specific security checks"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for dangerous imports
            if re.search(r'import\s+(pickle|marshal|shelve)', line):
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "category": "insecure_deserialization",
                    "severity": "high",
                    "message": "Potentially unsafe deserialization module imported",
                    "code_snippet": line.strip()
                })

    def _check_java_security(self, file_path: str, content: str, issues: List[Dict]):
        """Java-specific security checks"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for XML external entity vulnerabilities
            if re.search(r'XMLInputFactory|DocumentBuilderFactory', line):
                issues.append({
                    "file": file_path,
                    "line": line_num,
                    "category": "xxe",
                    "severity": "medium",
                    "message": "XML parser - ensure XXE protection is enabled",
                    "code_snippet": line.strip()
                })

    def _check_php_security(self, file_path: str, content: str, issues: List[Dict]):
        """PHP-specific security checks"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for dangerous functions
            dangerous_functions = ['eval', 'exec', 'system', 'shell_exec', 'passthru']
            for func in dangerous_functions:
                if re.search(rf'\b{func}\s*\(', line):
                    issues.append({
                        "file": file_path,
                        "line": line_num,
                        "category": "command_injection",
                        "severity": "high",
                        "message": f"Dangerous function '{func}()' used - potential command injection",
                        "code_snippet": line.strip()
                    })

    def _calculate_security_score(self):
        """Calculate overall security score"""
        high_severity = self.results["errors"]
        medium_low_severity = self.results["warnings"]
        
        # Start with 100 and deduct points for issues
        score = 100
        score -= high_severity * 15  # 15 points per high severity issue
        score -= medium_low_severity * 5  # 5 points per medium/low severity issue
        
        # Ensure score doesn't go below 0
        self.results["security_score"] = max(0, score)

def main():
    if len(sys.argv) < 2:
        print("Usage: python security-checker.py <file1> <file2> ...")
        sys.exit(1)
    
    files = [f.strip() for f in sys.argv[1].split() if f.strip()] if len(sys.argv) == 2 else sys.argv[1:]
    
    if not files:
        print("No files to scan")
        sys.exit(0)
    
    checker = SecurityChecker()
    checker.check_files(files)
    
    # Exit with error code if high-severity issues found
    if checker.results["errors"] > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()

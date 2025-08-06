#!/usr/bin/env python3
"""
AI-Powered Pull Request Reviewer

This script analyzes code changes using AI to provide intelligent feedback
on code quality, security, and best practices.
"""

import os
import sys
import json
import argparse
import requests
import subprocess
from typing import List, Dict, Any
from pathlib import Path

class AIReviewer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def analyze_file_changes(self, file_path: str) -> Dict[str, Any]:
        """Analyze changes in a specific file"""
        try:
            # Get file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file extension for language detection
            ext = Path(file_path).suffix.lower()
            language = self._detect_language(ext)
            
            # Get git diff for this file
            diff_result = subprocess.run(
                ['git', 'diff', 'origin/main', 'HEAD', '--', file_path],
                capture_output=True, text=True
            )
            diff_content = diff_result.stdout
            
            if not diff_content.strip():
                return {"file": file_path, "issues": [], "suggestions": []}
            
            # Analyze with AI
            analysis = self._ai_analyze_code(content, diff_content, language, file_path)
            
            return {
                "file": file_path,
                "language": language,
                "analysis": analysis,
                "diff_size": len(diff_content.split('\n'))
            }
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return {"file": file_path, "error": str(e)}

    def _detect_language(self, extension: str) -> str:
        """Detect programming language from file extension"""
        lang_map = {
            '.js': 'JavaScript',
            '.jsx': 'JavaScript React',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript React',
            '.py': 'Python',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++ Header',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
        }
        return lang_map.get(extension, 'Unknown')

    def _ai_analyze_code(self, content: str, diff: str, language: str, file_path: str) -> Dict[str, Any]:
        """Use AI to analyze code changes"""
        
        # Truncate content if too long
        max_content_length = 8000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "\n... (truncated)"
        
        if len(diff) > max_content_length:
            diff = diff[:max_content_length] + "\n... (truncated)"

        prompt = f"""
You are an expert code reviewer. Analyze the following {language} code changes and provide a comprehensive review.

File: {file_path}
Language: {language}

Git Diff:
```
{diff}
```

Full File Content (current):
```{language.lower()}
{content}
```

Please analyze for:
1. Syntax errors and compilation issues
2. Security vulnerabilities (OWASP Top 10, injection attacks, etc.)
3. Code quality issues (complexity, maintainability, readability)
4. Linting issues and style violations
5. Performance concerns
6. Best practices violations
7. Unnecessary whitespace or formatting issues
8. Missing error handling
9. Documentation and comments
10. Design patterns and architecture

Provide your response in the following JSON format:
{{
    "overall_score": 85,
    "issues": [
        {{
            "severity": "high|medium|low",
            "category": "security|quality|style|performance|best-practice",
            "line": 42,
            "message": "Detailed description of the issue",
            "suggestion": "How to fix this issue"
        }}
    ],
    "suggestions": [
        {{
            "type": "improvement|optimization|refactor",
            "message": "General suggestion for improvement",
            "reasoning": "Why this improvement would help"
        }}
    ],
    "security_score": 90,
    "quality_score": 85,
    "maintainability_score": 80
}}

Be thorough but practical. Focus on actionable feedback.
"""

        try:
            payload = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You are an expert code reviewer with deep knowledge of security, performance, and best practices across multiple programming languages."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000
            }

            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                try:
                    # Extract JSON from response (handle markdown formatting)
                    json_start = ai_response.find('{')
                    json_end = ai_response.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = ai_response[json_start:json_end]
                        return json.loads(json_str)
                except json.JSONDecodeError:
                    pass
                
                # Fallback: return raw response
                return {
                    "overall_score": 70,
                    "raw_response": ai_response,
                    "issues": [],
                    "suggestions": []
                }
            else:
                return {
                    "error": f"API request failed: {response.status_code}",
                    "overall_score": 50,
                    "issues": [],
                    "suggestions": []
                }
                
        except Exception as e:
            return {
                "error": f"AI analysis failed: {e}",
                "overall_score": 50,
                "issues": [],
                "suggestions": []
            }

    def generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate overall summary of the PR review"""
        total_files = len(results)
        files_with_issues = sum(1 for r in results if r.get('analysis', {}).get('issues', []))
        
        all_issues = []
        all_suggestions = []
        
        for result in results:
            if 'analysis' in result:
                all_issues.extend(result['analysis'].get('issues', []))
                all_suggestions.extend(result['analysis'].get('suggestions', []))
        
        severity_counts = {
            'high': sum(1 for issue in all_issues if issue.get('severity') == 'high'),
            'medium': sum(1 for issue in all_issues if issue.get('severity') == 'medium'),
            'low': sum(1 for issue in all_issues if issue.get('severity') == 'low')
        }
        
        category_counts = {}
        for issue in all_issues:
            cat = issue.get('category', 'other')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Calculate overall scores
        scores = [r.get('analysis', {}).get('overall_score', 70) for r in results if 'analysis' in r]
        avg_score = sum(scores) / len(scores) if scores else 70
        
        return {
            "summary": {
                "total_files_analyzed": total_files,
                "files_with_issues": files_with_issues,
                "total_issues": len(all_issues),
                "total_suggestions": len(all_suggestions),
                "average_score": round(avg_score, 1),
                "severity_breakdown": severity_counts,
                "category_breakdown": category_counts
            },
            "recommendation": self._get_recommendation(severity_counts, avg_score),
            "detailed_results": results
        }

    def _get_recommendation(self, severity_counts: Dict[str, int], avg_score: float) -> str:
        """Get overall recommendation based on analysis results"""
        if severity_counts.get('high', 0) > 0:
            return "❌ **Not Recommended for Merge** - Critical issues found that should be addressed before merging."
        elif severity_counts.get('medium', 0) > 3:
            return "⚠️ **Merge with Caution** - Multiple medium-severity issues found. Consider addressing before merge."
        elif avg_score < 60:
            return "⚠️ **Needs Improvement** - Code quality score is below acceptable threshold."
        elif severity_counts.get('medium', 0) > 0 or severity_counts.get('low', 0) > 5:
            return "✅ **Approved with Suggestions** - Code is acceptable but has room for improvement."
        else:
            return "✅ **Approved** - Code looks good! No major issues found."

def main():
    parser = argparse.ArgumentParser(description='AI-Powered PR Reviewer')
    parser.add_argument('--files', required=True, help='Space-separated list of files to analyze')
    parser.add_argument('--pr-number', required=True, help='Pull request number')
    parser.add_argument('--repo', required=True, help='Repository name (owner/repo)')
    
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Parse files list
    files = [f.strip() for f in args.files.split() if f.strip()]
    
    if not files:
        print("No files to analyze")
        sys.exit(0)
    
    print(f"Analyzing {len(files)} files with AI...")
    
    # Initialize reviewer
    reviewer = AIReviewer(api_key)
    
    # Analyze each file
    results = []
    for file_path in files:
        if os.path.exists(file_path):
            print(f"Analyzing: {file_path}")
            result = reviewer.analyze_file_changes(file_path)
            results.append(result)
        else:
            print(f"File not found: {file_path}")
    
    # Generate summary
    final_results = reviewer.generate_summary(results)
    
    # Save results
    with open('ai-results.json', 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"✅ AI analysis complete. Results saved to ai-results.json")
    print(f"📊 Analyzed {final_results['summary']['total_files_analyzed']} files")
    print(f"🔍 Found {final_results['summary']['total_issues']} issues")
    print(f"📈 Average code quality score: {final_results['summary']['average_score']}/100")

if __name__ == '__main__':
    main()

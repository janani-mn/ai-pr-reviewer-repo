# AI-Powered Pull Request Reviewer

🤖 An intelligent automated system that reviews pull requests using AI to ensure code quality, detect security vulnerabilities, check syntax, and enforce best practices across multiple programming languages.

## ✨ Key Features

- **🔄 Automated Reviews**: Triggers automatically on every pull request
- **🌐 Multi-Language Support**: JavaScript, TypeScript, Python, Java, Go, Rust, C++, C#, PHP, Ruby
- **🔒 Security Scanning**: Detects OWASP Top 10 vulnerabilities and security patterns
- **📊 Code Quality Analysis**: Measures complexity, maintainability, and technical debt
- **🎨 Style & Linting**: Enforces consistent code formatting and style guidelines
- **🧠 AI-Powered Insights**: Uses GPT-4 for intelligent code analysis and suggestions
- **📈 Comprehensive Reporting**: Generates detailed markdown reports with actionable feedback
- **⚡ Fast & Reliable**: Optimized for performance with parallel analysis

## 🏗️ System Architecture

```
AI PR Reviewer
├── 🔄 GitHub Actions Workflow    # Orchestrates the entire review process
├── 🧠 AI Analysis Engine         # GPT-4 powered code intelligence
├── 🔒 Security Scanner          # Multi-pattern vulnerability detection
├── 🎨 Code Style Checker        # Multi-language linting and formatting
├── 📊 Quality Analyzer          # Complexity and maintainability metrics
├── 📝 Report Generator          # Comprehensive markdown reports
└── ⚙️  Configuration System      # Customizable rules and thresholds
```

## 🚀 Quick Start

### 1. **Try the Demo**
```bash
# Clone and run the demo
git clone <this-repo>
cd ai-pr-reviewer
./demo.sh
```

### 2. **Add to Your Project**
```bash
# Copy the workflow to your repository
cp .github/workflows/ai-pr-review.yml /path/to/your/repo/.github/workflows/
cp -r scripts/ config/ /path/to/your/repo/
```

### 3. **Configure Secrets**
Add to your GitHub repository secrets:
- `OPENAI_API_KEY`: Your OpenAI API key for AI analysis

### 4. **Create a Test PR**
The system will automatically analyze any new pull request!

## 📋 What Gets Analyzed

| Category | What We Check | Tools Used |
|----------|---------------|------------|
| **🔍 Syntax** | Compilation errors, parse failures | Language-specific parsers |
| **🔒 Security** | SQL injection, XSS, hardcoded secrets, OWASP Top 10 | Custom patterns + Semgrep |
| **🎨 Code Style** | Formatting, linting rules, conventions | ESLint, Pylint, language linters |
| **📊 Quality** | Complexity, maintainability, code smells | Custom analysis engine |
| **🧠 AI Analysis** | Best practices, optimizations, architecture | GPT-4 powered insights |

### Security Vulnerabilities Detected
- ✅ SQL Injection attacks
- ✅ Cross-Site Scripting (XSS)
- ✅ Command injection
- ✅ Path traversal
- ✅ Hardcoded secrets/API keys
- ✅ Insecure cryptography
- ✅ Unsafe deserialization
- ✅ Insecure transport (HTTP vs HTTPS)

### Code Quality Metrics
- ✅ Cyclomatic complexity
- ✅ Function length and parameter count
- ✅ Code duplication detection
- ✅ Nesting depth analysis
- ✅ Comment ratio assessment
- ✅ Naming convention compliance
- ✅ Maintainability index calculation

## 📊 Example Review Report

```markdown
# 🤖 AI-Powered Pull Request Review

**Review Status:** ⚠️ REVIEW SUGGESTED - Multiple issues found
**Overall Score:** 73/100

## 📊 Summary
| Metric | Status | Details |
|--------|--------|---------|
| **Security** | ❌ | 3 high severity, 5 medium/low |
| **Quality** | ✅ | Score: 78/100 |
| **Style** | ⚠️ | 12 warnings |

## 🔍 Key Issues Found
- 🔴 **SQL Injection**: Dynamic query construction (Line 42)
- 🔴 **Hardcoded Secret**: API key in source code (Line 15)
- 🟡 **High Complexity**: Function exceeds complexity threshold (Line 128)

## 💡 AI Recommendations
- Extract complex business logic into smaller functions
- Use parameterized queries to prevent SQL injection
- Move secrets to environment variables
```

## 🛠️ Configuration & Customization

### Analysis Rules (`config/analysis-rules.yml`)
```yaml
analysis:
  syntax_check: true
  security_scan: true
  linting: true
  quality_analysis: true
  ai_review: true

include_patterns:
  - "**/*.js"
  - "**/*.py"
  - "**/*.java"

thresholds:
  overall_score:
    excellent: 85
    good: 70
    acceptable: 50
```

### Security Rules (`config/security-rules.yml`)
```yaml
high_severity:
  sql_injection:
    - pattern: "(SELECT|INSERT|UPDATE|DELETE).*\\+.*['\"]"
      message: "Potential SQL injection"
```

### Quality Standards (`config/quality-standards.yml`)
```yaml
complexity:
  cyclomatic:
    excellent: 1-5
    good: 6-10
    acceptable: 11-15
    poor: 16-20
    critical: 21+
```

## 🌐 Language Support Matrix

| Language | Syntax Check | Security Scan | Linting | Quality Analysis | AI Review |
|----------|-------------|---------------|---------|------------------|-----------|
| **JavaScript/TypeScript** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Python** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Java** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Go** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Rust** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **C/C++** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **C#** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **PHP** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Ruby** | ✅ | ✅ | ✅ | ✅ | ✅ |

*Legend: ✅ Full Support, ⚠️ Basic Support*

## 📁 Project Structure

```
ai-pr-reviewer/
├── 📁 .github/workflows/     # GitHub Actions automation
│   └── ai-pr-review.yml      # Main workflow file
├── 📁 scripts/               # Analysis scripts
│   ├── ai-reviewer.py        # AI-powered analysis
│   ├── syntax-checker.js     # Syntax validation
│   ├── security-checker.py   # Security vulnerability detection
│   ├── lint-checker.py       # Code style and linting
│   ├── quality-analyzer.js   # Code quality metrics
│   └── report-generator.py   # Markdown report generation
├── 📁 config/                # Configuration files
│   ├── analysis-rules.yml    # General analysis settings
│   ├── security-rules.yml    # Security patterns and rules
│   └── quality-standards.yml # Code quality thresholds
├── 📁 examples/              # Example files for testing
│   ├── example-code.js       # JavaScript examples with issues
│   └── example-code.py       # Python examples with issues
├── 📄 README.md              # This file
├── 📄 SETUP.md               # Detailed setup instructions
├── 📄 package.json           # Node.js dependencies
├── 📄 requirements.txt       # Python dependencies
└── 🔧 demo.sh                # Demo script
```

## � Advanced Usage

### Local Development
```bash
# Run analysis locally during development
node scripts/syntax-checker.js src/**/*.js
python3 scripts/security-checker.py "src/**/*.py"
node scripts/quality-analyzer.js src/**/*.js
```

### Custom AI Prompts
Modify `scripts/ai-reviewer.py` to customize AI analysis focus:
```python
focus_areas = [
    "security vulnerabilities",
    "performance optimizations", 
    "maintainability improvements",
    "custom business logic validation"
]
```

### IDE Integration
Use the scripts in your favorite IDE or as pre-commit hooks:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ai-review
        name: AI Code Review
        entry: python scripts/ai-reviewer.py
        language: python
```

## 📈 Performance & Limits

- **Analysis Speed**: ~30-60 seconds for typical PRs
- **File Limits**: Optimized for PRs with <100 files
- **API Usage**: ~1-5 OpenAI API calls per PR (depending on size)
- **Supported File Size**: Up to 10MB per file
- **Languages**: 10+ programming languages supported

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🐛 Report Issues**: Found a bug? Report it!
2. **✨ Add Features**: New language support, analysis tools
3. **📖 Improve Docs**: Help others get started
4. **🧪 Add Tests**: Help us maintain quality

### Adding New Language Support
1. Update file patterns in `config/analysis-rules.yml`
2. Add language-specific checks in analysis scripts
3. Update syntax checker with new parsers
4. Add examples and test cases

## 📚 Documentation

- **📖 [Setup Guide](SETUP.md)**: Detailed installation and configuration
- **🔧 [Configuration Reference](config/)**: All configuration options
- **💡 [Examples](examples/)**: Sample code with issues for testing

## ⚡ Troubleshooting

### Common Issues
- **API Key Error**: Ensure `OPENAI_API_KEY` is set in GitHub secrets
- **Workflow Timeouts**: Reduce file patterns or increase timeout values
- **False Positives**: Customize security patterns in config files

### Getting Help
- 📚 Check the [Setup Guide](SETUP.md)
- 💬 Open a GitHub Discussion
- 🐛 Report bugs via GitHub Issues

## � License

MIT License - feel free to use this in your projects!

---

**🎉 Ready to improve your code quality?** Add this AI-powered reviewer to your repository today and catch issues before they reach production!

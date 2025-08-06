#!/usr/bin/env node
/**
 * Code Quality Analyzer
 * 
 * Analyzes code for complexity, maintainability, and quality metrics
 */

const fs = require('fs');
const path = require('path');

class QualityAnalyzer {
    constructor() {
        this.results = {
            total_files: 0,
            files_analyzed: 0,
            overall_score: 0,
            critical: 0,
            warnings: 0,
            quality_metrics: [],
            summary: {}
        };
    }

    async analyzeFiles(files) {
        console.log(`📊 Analyzing code quality for ${files.length} files...`);
        
        const metrics = [];
        
        for (const file of files) {
            if (!fs.existsSync(file)) {
                console.log(`❌ File not found: ${file}`);
                continue;
            }

            this.results.total_files++;
            
            try {
                const fileMetrics = await this.analyzeFile(file);
                metrics.push(fileMetrics);
                this.results.files_analyzed++;
                
                console.log(`✅ Analyzed: ${file} (Score: ${fileMetrics.overall_score})`);
                
            } catch (error) {
                console.error(`❌ Error analyzing ${file}: ${error.message}`);
            }
        }

        this.results.quality_metrics = metrics;
        this.calculateOverallMetrics();
        
        // Save results
        fs.writeFileSync('quality-results.json', JSON.stringify(this.results, null, 2));
        
        console.log(`📊 Quality analysis complete`);
        console.log(`📈 Overall score: ${this.results.overall_score}/100`);
        console.log(`🔴 Critical issues: ${this.results.critical}`);
        console.log(`🟡 Warnings: ${this.results.warnings}`);
    }

    async analyzeFile(filePath) {
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');
        const ext = path.extname(filePath).toLowerCase();
        
        const metrics = {
            file: filePath,
            language: this.detectLanguage(ext),
            lines_of_code: this.countLinesOfCode(lines),
            cyclomatic_complexity: this.calculateComplexity(content, ext),
            maintainability_index: 0,
            code_duplication: this.detectDuplication(content),
            function_length: this.analyzeFunctionLength(content, ext),
            parameter_count: this.analyzeParameterCount(content, ext),
            nesting_depth: this.analyzeNestingDepth(content),
            comment_ratio: this.calculateCommentRatio(lines),
            naming_quality: this.analyzeNamingQuality(content, ext),
            overall_score: 0,
            issues: [],
            suggestions: []
        };

        // Calculate maintainability index
        metrics.maintainability_index = this.calculateMaintainabilityIndex(metrics);
        
        // Calculate overall score
        metrics.overall_score = this.calculateOverallScore(metrics);
        
        // Generate issues and suggestions
        this.generateIssuesAndSuggestions(metrics);
        
        return metrics;
    }

    detectLanguage(ext) {
        const langMap = {
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
            '.rb': 'Ruby'
        };
        return langMap[ext] || 'Unknown';
    }

    countLinesOfCode(lines) {
        let loc = 0;
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('//') && !trimmed.startsWith('#') && !trimmed.startsWith('/*')) {
                loc++;
            }
        }
        return loc;
    }

    calculateComplexity(content, ext) {
        // Basic cyclomatic complexity calculation
        let complexity = 1; // Base complexity
        
        const complexityKeywords = {
            '.js': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.jsx': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.ts': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.tsx': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.py': ['if', 'elif', 'while', 'for', 'except', 'and', 'or'],
            '.java': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.go': ['if', 'for', 'switch', 'case', '&&', '||'],
            '.rs': ['if', 'while', 'for', 'match', '&&', '||'],
            '.cpp': ['if', 'else if', 'while', 'for', 'case', 'catch', '&&', '||', '?'],
            '.c': ['if', 'else if', 'while', 'for', 'case', '&&', '||', '?']
        };

        const keywords = complexityKeywords[ext] || complexityKeywords['.js'];
        
        for (const keyword of keywords) {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            const matches = content.match(regex);
            if (matches) {
                complexity += matches.length;
            }
        }

        return complexity;
    }

    detectDuplication(content) {
        // Simple duplication detection - look for repeated blocks of 3+ lines
        const lines = content.split('\n').map(line => line.trim()).filter(line => line.length > 10);
        const duplicates = new Set();
        
        for (let i = 0; i < lines.length - 2; i++) {
            const block = lines.slice(i, i + 3).join('\n');
            for (let j = i + 3; j < lines.length - 2; j++) {
                const compareBlock = lines.slice(j, j + 3).join('\n');
                if (block === compareBlock && block.length > 50) {
                    duplicates.add(block);
                }
            }
        }
        
        return duplicates.size;
    }

    analyzeFunctionLength(content, ext) {
        const functionRegexes = {
            '.js': /function\s+\w+\s*\([^)]*\)\s*{|=>\s*{|:\s*function\s*\([^)]*\)\s*{/g,
            '.jsx': /function\s+\w+\s*\([^)]*\)\s*{|=>\s*{|:\s*function\s*\([^)]*\)\s*{/g,
            '.ts': /function\s+\w+\s*\([^)]*\)\s*{|=>\s*{|:\s*function\s*\([^)]*\)\s*{/g,
            '.tsx': /function\s+\w+\s*\([^)]*\)\s*{|=>\s*{|:\s*function\s*\([^)]*\)\s*{/g,
            '.py': /def\s+\w+\s*\([^)]*\):/g,
            '.java': /(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\([^)]*\)\s*{/g,
            '.go': /func\s+\w+\s*\([^)]*\)\s*{/g,
            '.rs': /fn\s+\w+\s*\([^)]*\)\s*{/g,
            '.cpp': /\w+\s+\w+\s*\([^)]*\)\s*{/g,
            '.c': /\w+\s+\w+\s*\([^)]*\)\s*{/g
        };

        const regex = functionRegexes[ext];
        if (!regex) return { average: 0, max: 0, functions_analyzed: 0 };

        const functions = content.match(regex);
        if (!functions) return { average: 0, max: 0, functions_analyzed: 0 };

        // Simplified function length calculation
        const avgLength = Math.round(content.split('\n').length / functions.length);
        
        return {
            average: avgLength,
            max: avgLength * 1.5, // Rough estimate
            functions_analyzed: functions.length
        };
    }

    analyzeParameterCount(content, ext) {
        const functionRegexes = {
            '.js': /function\s+\w+\s*\(([^)]*)\)|=>\s*\(([^)]*)\)/g,
            '.jsx': /function\s+\w+\s*\(([^)]*)\)|=>\s*\(([^)]*)\)/g,
            '.ts': /function\s+\w+\s*\(([^)]*)\)|=>\s*\(([^)]*)\)/g,
            '.tsx': /function\s+\w+\s*\(([^)]*)\)|=>\s*\(([^)]*)\)/g,
            '.py': /def\s+\w+\s*\(([^)]*)\):/g,
            '.java': /(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(([^)]*)\)/g,
            '.go': /func\s+\w+\s*\(([^)]*)\)/g,
            '.rs': /fn\s+\w+\s*\(([^)]*)\)/g
        };

        const regex = functionRegexes[ext];
        if (!regex) return { average: 0, max: 0 };

        let totalParams = 0;
        let maxParams = 0;
        let functionCount = 0;
        let match;

        while ((match = regex.exec(content)) !== null) {
            const params = (match[1] || match[2] || match[3] || '').split(',').filter(p => p.trim());
            const paramCount = params.length > 0 && params[0].trim() ? params.length : 0;
            
            totalParams += paramCount;
            maxParams = Math.max(maxParams, paramCount);
            functionCount++;
        }

        return {
            average: functionCount > 0 ? Math.round(totalParams / functionCount * 10) / 10 : 0,
            max: maxParams
        };
    }

    analyzeNestingDepth(content) {
        const lines = content.split('\n');
        let maxDepth = 0;
        let currentDepth = 0;

        for (const line of lines) {
            const trimmed = line.trim();
            
            // Count opening braces/blocks
            const openBraces = (line.match(/{/g) || []).length;
            const closeBraces = (line.match(/}/g) || []).length;
            
            currentDepth += openBraces - closeBraces;
            maxDepth = Math.max(maxDepth, currentDepth);
        }

        return maxDepth;
    }

    calculateCommentRatio(lines) {
        let commentLines = 0;
        let codeLines = 0;
        let inBlockComment = false;

        for (const line of lines) {
            const trimmed = line.trim();
            
            if (!trimmed) continue;

            if (trimmed.startsWith('/*')) inBlockComment = true;
            if (trimmed.includes('*/')) inBlockComment = false;
            
            if (inBlockComment || trimmed.startsWith('//') || trimmed.startsWith('#') || 
                trimmed.startsWith('*') || trimmed.startsWith('<!--')) {
                commentLines++;
            } else if (trimmed.length > 0) {
                codeLines++;
            }
        }

        return codeLines > 0 ? Math.round((commentLines / codeLines) * 100 * 10) / 10 : 0;
    }

    analyzeNamingQuality(content, ext) {
        const variableRegexes = {
            '.js': /(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g,
            '.jsx': /(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g,
            '.ts': /(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g,
            '.tsx': /(?:var|let|const)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)/g,
            '.py': /([a-zA-Z_][a-zA-Z0-9_]*)\s*=/g,
            '.java': /(private|public|protected)?\s*(static)?\s*\w+\s+([a-zA-Z_][a-zA-Z0-9_]*)/g
        };

        const regex = variableRegexes[ext];
        if (!regex) return { score: 50, issues: [] };

        const variables = [];
        let match;
        
        while ((match = regex.exec(content)) !== null) {
            const varName = match[1] || match[3];
            if (varName && varName.length > 1) {
                variables.push(varName);
            }
        }

        let score = 100;
        const issues = [];

        for (const varName of variables) {
            // Check for single letter variables
            if (varName.length === 1 && !['i', 'j', 'k', 'x', 'y', 'z'].includes(varName)) {
                score -= 10;
                issues.push(`Single letter variable: ${varName}`);
            }
            
            // Check for abbreviations
            if (varName.length < 4 && !['id', 'url', 'api'].includes(varName.toLowerCase())) {
                score -= 5;
                issues.push(`Short/abbreviated variable: ${varName}`);
            }
            
            // Check for proper camelCase/snake_case
            if (ext.includes('.py') && varName.includes('camelCase')) {
                score -= 5;
                issues.push(`Use snake_case in Python: ${varName}`);
            }
        }

        return {
            score: Math.max(0, score),
            issues: issues.slice(0, 10) // Limit issues
        };
    }

    calculateMaintainabilityIndex(metrics) {
        // Simplified maintainability index calculation
        const complexity = metrics.cyclomatic_complexity;
        const loc = metrics.lines_of_code;
        const commentRatio = metrics.comment_ratio;
        
        // Base formula (simplified version of Halstead-based MI)
        let mi = 171 - 5.2 * Math.log(loc) - 0.23 * complexity;
        
        // Adjust for comments
        mi += commentRatio * 0.2;
        
        return Math.max(0, Math.min(100, Math.round(mi)));
    }

    calculateOverallScore(metrics) {
        let score = 100;
        
        // Deduct points for high complexity
        if (metrics.cyclomatic_complexity > 10) {
            score -= (metrics.cyclomatic_complexity - 10) * 5;
        }
        
        // Deduct points for long functions
        if (metrics.function_length.average > 50) {
            score -= (metrics.function_length.average - 50) * 0.5;
        }
        
        // Deduct points for too many parameters
        if (metrics.parameter_count.max > 5) {
            score -= (metrics.parameter_count.max - 5) * 10;
        }
        
        // Deduct points for deep nesting
        if (metrics.nesting_depth > 4) {
            score -= (metrics.nesting_depth - 4) * 10;
        }
        
        // Deduct points for code duplication
        score -= metrics.code_duplication * 10;
        
        // Bonus points for good comments
        if (metrics.comment_ratio > 10) {
            score += Math.min(10, metrics.comment_ratio - 10);
        }
        
        // Factor in maintainability index
        score = (score + metrics.maintainability_index) / 2;
        
        return Math.max(0, Math.min(100, Math.round(score)));
    }

    generateIssuesAndSuggestions(metrics) {
        const issues = [];
        const suggestions = [];

        if (metrics.cyclomatic_complexity > 15) {
            issues.push({
                severity: 'high',
                category: 'complexity',
                message: `High cyclomatic complexity (${metrics.cyclomatic_complexity}). Consider breaking down complex functions.`,
                suggestion: 'Refactor complex functions into smaller, more focused functions'
            });
            this.results.critical++;
        } else if (metrics.cyclomatic_complexity > 10) {
            issues.push({
                severity: 'medium',
                category: 'complexity',
                message: `Moderate cyclomatic complexity (${metrics.cyclomatic_complexity}).`,
                suggestion: 'Consider simplifying complex logic'
            });
            this.results.warnings++;
        }

        if (metrics.function_length.average > 100) {
            issues.push({
                severity: 'high',
                category: 'maintainability',
                message: `Functions are too long (avg: ${metrics.function_length.average} lines).`,
                suggestion: 'Break down large functions into smaller, more manageable pieces'
            });
            this.results.critical++;
        } else if (metrics.function_length.average > 50) {
            issues.push({
                severity: 'medium',
                category: 'maintainability',
                message: `Functions are moderately long (avg: ${metrics.function_length.average} lines).`,
                suggestion: 'Consider breaking down longer functions'
            });
            this.results.warnings++;
        }

        if (metrics.parameter_count.max > 7) {
            issues.push({
                severity: 'high',
                category: 'design',
                message: `Too many parameters in functions (max: ${metrics.parameter_count.max}).`,
                suggestion: 'Use parameter objects or configuration objects instead of many parameters'
            });
            this.results.critical++;
        }

        if (metrics.nesting_depth > 5) {
            issues.push({
                severity: 'medium',
                category: 'readability',
                message: `Deep nesting detected (depth: ${metrics.nesting_depth}).`,
                suggestion: 'Reduce nesting by using early returns or extracting functions'
            });
            this.results.warnings++;
        }

        if (metrics.comment_ratio < 5) {
            suggestions.push({
                type: 'improvement',
                message: 'Low comment ratio. Consider adding more documentation.',
                reasoning: 'Good documentation improves code maintainability'
            });
        }

        if (metrics.code_duplication > 0) {
            issues.push({
                severity: 'medium',
                category: 'duplication',
                message: `Code duplication detected (${metrics.code_duplication} instances).`,
                suggestion: 'Extract common code into reusable functions or modules'
            });
            this.results.warnings++;
        }

        metrics.issues = issues;
        metrics.suggestions = suggestions;
    }

    calculateOverallMetrics() {
        const metrics = this.results.quality_metrics;
        
        if (metrics.length === 0) {
            this.results.overall_score = 0;
            return;
        }

        const totalScore = metrics.reduce((sum, metric) => sum + metric.overall_score, 0);
        this.results.overall_score = Math.round(totalScore / metrics.length);

        this.results.summary = {
            average_complexity: Math.round(metrics.reduce((sum, m) => sum + m.cyclomatic_complexity, 0) / metrics.length),
            average_loc: Math.round(metrics.reduce((sum, m) => sum + m.lines_of_code, 0) / metrics.length),
            average_maintainability: Math.round(metrics.reduce((sum, m) => sum + m.maintainability_index, 0) / metrics.length),
            total_functions: metrics.reduce((sum, m) => sum + m.function_length.functions_analyzed, 0),
            files_with_high_complexity: metrics.filter(m => m.cyclomatic_complexity > 10).length,
            files_with_long_functions: metrics.filter(m => m.function_length.average > 50).length
        };
    }
}

async function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node quality-analyzer.js <file1> <file2> ...');
        process.exit(1);
    }

    const files = process.argv.slice(2).filter(f => f.trim());
    
    if (files.length === 0) {
        console.log('No files to analyze');
        process.exit(0);
    }

    const analyzer = new QualityAnalyzer();
    await analyzer.analyzeFiles(files);

    console.log(`\n📊 Quality Analysis Summary:`);
    console.log(`Overall Score: ${analyzer.results.overall_score}/100`);
    console.log(`Files Analyzed: ${analyzer.results.files_analyzed}/${analyzer.results.total_files}`);
}

if (require.main === module) {
    main().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}

module.exports = QualityAnalyzer;

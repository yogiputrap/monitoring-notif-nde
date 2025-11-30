# Contributing Guidelines

Terima kasih atas minat Anda untuk berkontribusi pada NDE Monitoring Bot! 🎉

## Cara Berkontribusi

### 1. Fork Repository

Klik tombol "Fork" di bagian atas halaman repository.

### 2. Clone Fork Anda

```bash
git clone https://github.com/your-username/monitoring-notif-nde.git
cd monitoring-notif-nde
```

### 3. Buat Branch Baru

```bash
git checkout -b feature/your-feature-name
# atau
git checkout -b fix/your-fix-name
```

### 4. Setup Development Environment

```bash
# Copy environment file
cp .env.example .env

# Edit dengan test credentials
nano .env

# Build Docker image
docker compose build

# Run untuk testing
docker compose up
```

### 5. Buat Perubahan

- Ikuti code style yang ada
- Tambahkan comments untuk logic yang complex
- Update dokumentasi jika perlu
- Test perubahan Anda

### 6. Test Perubahan

```bash
# Test syntax
python3 -m py_compile src/*.py

# Test Docker build
docker compose build

# Test runtime
docker compose up

# Check logs
docker compose logs
```

### 7. Commit Perubahan

```bash
git add .
git commit -m "feat: deskripsi perubahan Anda"
```

#### Commit Message Format

Gunakan conventional commits:
- `feat:` - Fitur baru
- `fix:` - Bug fix
- `docs:` - Perubahan dokumentasi
- `style:` - Format, semicolons, etc (tidak mengubah logic)
- `refactor:` - Refactoring code
- `test:` - Menambah test
- `chore:` - Maintenance tasks

Contoh:
```
feat: tambah support untuk multiple chat IDs
fix: perbaiki memory leak pada scraper
docs: update README dengan troubleshooting baru
```

### 8. Push ke Fork Anda

```bash
git push origin feature/your-feature-name
```

### 9. Buat Pull Request

1. Buka repository di GitHub
2. Klik "New Pull Request"
3. Pilih branch Anda
4. Isi deskripsi lengkap tentang perubahan
5. Submit PR

## Code Style Guidelines

### Python

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where applicable

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    return True
```

### Naming Conventions

- **Classes**: PascalCase (`NDEScraper`, `TelegramNotifier`)
- **Functions/Methods**: snake_case (`get_verification_messages`, `send_alert`)
- **Variables**: snake_case (`username_field`, `is_logged_in`)
- **Constants**: UPPER_CASE (`CHECK_INTERVAL_MINUTES`, `NDE_URL`)

### Logging

Gunakan appropriate log levels:
- `logger.debug()` - Detailed debugging information
- `logger.info()` - General information
- `logger.warning()` - Warning messages
- `logger.error()` - Error messages
- `logger.critical()` - Critical errors

```python
logger.info("Starting check cycle...")
logger.error(f"Login failed: {error_message}")
```

## Areas untuk Kontribusi

### 🐛 Bug Fixes

Jika menemukan bug:
1. Buat issue dengan detail bug
2. Include steps to reproduce
3. Include logs jika ada
4. Submit PR dengan fix

### ✨ Fitur Baru

Ideas untuk fitur baru:
- Support multiple Telegram chat IDs
- Web dashboard untuk monitoring
- Email notifications
- Statistics dan reporting
- Advanced filtering
- Webhook integration
- Multi-account support

### 📚 Dokumentasi

- Improve README
- Add more examples
- Translate documentation
- Add video tutorials
- Improve inline comments

### 🧪 Testing

- Add unit tests
- Add integration tests
- Add end-to-end tests
- Improve test coverage

### 🎨 Improvements

- Performance optimization
- Code refactoring
- Better error messages
- UI/UX improvements
- Security enhancements

## Development Setup

### Requirements

- Python 3.11+
- Docker & Docker Compose
- Git
- Text editor (VSCode recommended)

### Recommended VSCode Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-azuretools.vscode-docker",
    "streetsidesoftware.code-spell-checker"
  ]
}
```

### Local Testing

```bash
# Run with hot reload (for development)
docker compose up

# Run in background
docker compose up -d

# View logs
docker compose logs -f

# Restart after changes
docker compose restart

# Rebuild after code changes
docker compose build
docker compose up -d
```

## Pull Request Guidelines

### Before Submitting

- ✅ Code compiles without errors
- ✅ Docker builds successfully
- ✅ All tests pass (if applicable)
- ✅ Documentation updated
- ✅ CHANGELOG.md updated
- ✅ No merge conflicts
- ✅ Commits are clean and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests added/updated
- [ ] CHANGELOG updated

## Screenshots (if applicable)
Add screenshots here
```

## Issue Guidelines

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step 1
2. Step 2
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g. Ubuntu 20.04]
- Docker version: [e.g. 20.10.12]
- Bot version: [e.g. 1.0.0]

## Logs
```
Paste relevant logs here
```

## Additional Context
Any other information
```

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this be implemented?

## Alternatives Considered
Any alternative solutions?

## Additional Context
Any other information
```

## Code Review Process

1. Maintainer akan review PR Anda
2. Jika ada feedback, lakukan perubahan yang diminta
3. Setelah approved, PR akan di-merge
4. Kontribusi Anda akan listed di CHANGELOG

## Community Guidelines

- Be respectful and inclusive
- Help others when possible
- Provide constructive feedback
- Follow the code of conduct
- Be patient with responses

## Questions?

Jika ada pertanyaan:
- Open an issue dengan label "question"
- Email maintainer (jika urgent)
- Join discussion di GitHub Discussions

## Recognition

Contributors akan listed di:
- README.md (Contributors section)
- CHANGELOG.md
- Git commit history

---

**Thank you for contributing! 🙏**

Setiap kontribusi, sekecil apapun, sangat berarti untuk project ini.

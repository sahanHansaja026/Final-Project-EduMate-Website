# Contributing to EduMate

We love your contributions! Please follow these guidelines to help us maintain the project.

## 📄 Pull Request Template

When creating a pull request, use the [pull request template](https://github.com/sahanHansaja026/Final-Project-EduMate-Website/.github/pull_request_template/pull_request_template.md) to provide the necessary context for maintainers.

## 🛠 Development Setup

### Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Docker](https://www.docker.com/) (for backend deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/sahanHansaja026/Final-Project-EduMate-Website.git
   cd Final-Project-EduMate-Website
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   # Runs on http://localhost:8000
   ```

3. **Frontend setup**
   ```bash
   cd client
   npm install
   npm run dev
   # Runs on http://localhost:3000
   ```

## 📋 Pull Request Guidelines

1. **Fill out the PR template** completely - incomplete PRs will be requested for more information
2. **Write descriptive titles** - e.g., `feat: add course recommendation feature` or `fix: resolve attendance tracking bug`
3. **Link related issues** using `Fixes #123` syntax
4. **Ensure all tests pass** before submitting
5. **Follow code style** - PEP 8 for backend, TypeScript conventions for frontend
6. **Update documentation** if adding new features or changing APIs
7. **Never commit secrets** - use environment variables for DATABASE_URL, AWS keys, JWT secrets, etc.

## 🐛 Reporting Issues

- Use the [Issues](https://github.com/sahanHansaja026/Final-Project-EduMate-Website/issues) section
- Include steps to reproduce, expected vs actual behavior
- Include environment details (OS, Python/Node versions, Docker if applicable)

## 📜 Code of Conduct

Please read and follow the [Code of Conduct](https://github.com/sahanHansaja026/Final-Project-EduMate-Website/blob/main/CODE_OF_CONDUCT.md).

## 🙏 Thank You

Thank you for contributing to EduMate! Your help makes this project better for everyone.
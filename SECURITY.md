# Security Policy

## Overview

This document outlines the security practices and guidelines for the **awesome-tools** repository.

## Secrets Management

### .gitignore Protection

The repository includes a comprehensive `.gitignore` file that prevents accidental commits of sensitive files:

- Environment files (`.env`, `.env.local`, `.env.*.local`)
- Private keys (`*.key`, `*.pem`, `*.p12`)
- Certificate files (`*.cert`, `*.crt`)
- Secrets directories (`secrets/`, `config/secrets.yml`)

### Best Practices

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive configuration
3. **Use GitHub Secrets** for CI/CD credentials
4. **Rotate credentials** regularly
5. **Use secret scanning** tools in CI/CD pipelines

## Dependency Security

### Automated Updates

Dependabot is configured to automatically:
- Check for dependency updates weekly
- Open pull requests for security patches
- Label updates appropriately for easy tracking

### Manual Auditing

Run these commands periodically:
```bash
# For npm projects
npm audit
npm audit fix

# For pip projects
pip-audit
```

## CI/CD Security

### GitHub Actions Security

- Use `permissions: {}` at workflow level for least privilege
- Pin actions to specific versions (not `latest`)
- Avoid `on: schedule:` triggers (prefer `workflow_dispatch`)
- Store all secrets in GitHub Secrets

### Recommended Workflows

1. **Secret Scanning**: Detect accidentally committed credentials
2. **SAST (Static Application Security Testing)**: Analyze code for vulnerabilities
3. **Dependency Scanning**: Check for known vulnerabilities

## OWASP Top 10 Compliance

This repository is a curated list of resources and does not run application code. However, the following practices are maintained:

1. **Broken Access Control**: Not applicable (static content)
2. **Cryptographic Failures**: Not applicable
3. **Injection**: Not applicable
4. **Insecure Design**: Repository follows secure defaults
5. **Security Misconfiguration**: Dependencies kept up-to-date via Dependabot
6. **Vulnerable and Outdated Components**: Automated dependency updates
7. **Identification and Authentication**: Not applicable
8. **Software and Data Integrity Failures**: Signed commits recommended
9. **Security Logging and Monitoring**: GitHub's audit logs enabled
10. **Server-Side Request Forgery (SSRF)**: Not applicable

## Reporting Security Issues

If you discover a security vulnerability, please report it responsibly:
1. Do NOT open a public issue
2. Contact repository maintainers directly
3. Provide details of the vulnerability
4. Allow time for remediation before public disclosure

## License

This security policy is part of the awesome-tools repository and follows the same license terms.

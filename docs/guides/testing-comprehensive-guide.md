---
title: Testing Comprehensive Guide
description: Modern testing strategies and best practices for Python and JavaScript with VS Code integration
status: published
created: 2025-09-10
updated: 2025-09-10
tags: [testing, python, javascript, automation, quality-assurance, pytest, jest]
---

# Testing Comprehensive Guide

## Overview

This comprehensive guide provides enterprise-grade testing strategies, frameworks, and implementation patterns for modern software development. Covering Python (pytest, ruff, black, Pylance) and JavaScript (Jest, Vitest, Playwright) ecosystems with deep VS Code integration, this guide addresses testing challenges from unit tests to end-to-end automation.

## Table of Contents

1. [Testing Philosophy and Principles](#testing-philosophy-and-principles)
2. [Python Testing Ecosystem](#python-testing-ecosystem)
3. [JavaScript Testing Ecosystem](#javascript-testing-ecosystem)
4. [VS Code Testing Integration](#vs-code-testing-integration)
5. [Test-Driven Development](#test-driven-development)
6. [Quality Assurance Automation](#quality-assurance-automation)
7. [CI/CD Testing Pipelines](#cicd-testing-pipelines)
8. [Performance and Load Testing](#performance-and-load-testing)
9. [Testing Best Practices](#testing-best-practices)
10. [Advanced Testing Patterns](#advanced-testing-patterns)

## Testing Philosophy and Principles

### The Testing Pyramid

```mermaid
graph TD
    A[End-to-End Tests<br/>Few, Slow, Expensive] --> B[Integration Tests<br/>Some, Medium Speed]
    B --> C[Unit Tests<br/>Many, Fast, Cheap]
    C --> D[Static Analysis<br/>Linting, Type Checking]
```

#### Testing Strategy Distribution

- **70% Unit Tests**: Fast, isolated, comprehensive coverage
- **20% Integration Tests**: Component interaction validation
- **10% End-to-End Tests**: Critical user journey validation
- **Continuous Static Analysis**: Code quality and type safety

### Core Testing Principles

#### 1. Test Reliability (FIRST Principles)

- **Fast**: Tests run quickly to enable frequent execution
- **Independent**: Tests don't depend on other tests or external state
- **Repeatable**: Consistent results across environments
- **Self-Validating**: Clear pass/fail with descriptive feedback
- **Timely**: Written close to or before implementation

#### 2. Test Quality Standards

```python
# Example of high-quality test structure
def test_user_authentication_success():
    """Test successful user authentication with valid credentials.
    
    Covers:
    - Valid email/password combination
    - Token generation and validation
    - User session creation
    """
    # Arrange
    user = create_test_user(email="test@example.com", password="secure123")
    auth_service = AuthenticationService()
    
    # Act
    result = auth_service.authenticate(user.email, "secure123")
    
    # Assert
    assert result.success is True
    assert result.token is not None
    assert result.user.id == user.id
    assert result.expires_at > datetime.now()
```

## Python Testing Ecosystem

### pytest Framework

#### Advanced pytest Configuration

```python
# pytest.ini configuration
[tool:pytest]
minversion = 7.0
addopts = 
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=85
    --junit-xml=reports/junit.xml
    --html=reports/report.html
    --self-contained-html
    --maxfail=5
    --tb=short
    -ra
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    api: marks tests as API tests
    ui: marks tests as UI tests
    smoke: marks tests as smoke tests
filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning
```

#### Advanced Fixtures and Dependency Injection

```python
# conftest.py - Advanced fixture patterns
import pytest
from unittest.mock import MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.database import Base
from myapp.config import TestConfig

@pytest.fixture(scope="session")
def database_engine():
    """Create test database engine for the entire test session."""
    engine = create_engine(TestConfig.DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(database_engine):
    """Provide clean database session for each test."""
    Session = sessionmaker(bind=database_engine)
    session = Session()
    
    # Start transaction that will be rolled back
    transaction = session.begin()
    
    yield session
    
    # Rollback transaction to clean state
    transaction.rollback()
    session.close()

@pytest.fixture
def mock_external_api():
    """Mock external API responses for consistent testing."""
    with patch('myapp.external.api_client') as mock_client:
        mock_client.get.return_value = {
            "status": "success",
            "data": {"id": 123, "name": "Test Item"}
        }
        yield mock_client

@pytest.fixture(params=[
    {"user_type": "admin", "permissions": ["read", "write", "delete"]},
    {"user_type": "user", "permissions": ["read"]},
    {"user_type": "guest", "permissions": []},
])
def user_with_permissions(request):
    """Parametrized fixture for testing different user types."""
    return create_test_user(**request.param)
```

#### Advanced Testing Patterns

```python
# test_advanced_patterns.py
import pytest
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies as st
from myapp.services import UserService, EmailService

class TestUserService:
    """Comprehensive test suite for UserService."""
    
    def test_create_user_success(self, db_session):
        """Test successful user creation with validation."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        service = UserService(db_session)
        
        # Act
        user = service.create_user(user_data)
        
        # Assert
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.password != user_data["password"]  # Should be hashed
        assert user.is_active is True
    
    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "@example.com",
        "test@",
        "",
        None
    ])
    def test_create_user_invalid_email(self, db_session, invalid_email):
        """Test user creation fails with invalid email formats."""
        user_data = {"email": invalid_email, "password": "SecurePass123!"}
        service = UserService(db_session)
        
        with pytest.raises(ValidationError, match="Invalid email format"):
            service.create_user(user_data)
    
    @given(st.text(min_size=1, max_size=5))
    def test_create_user_weak_password(self, db_session, weak_password):
        """Property-based test for weak password rejection."""
        user_data = {"email": "test@example.com", "password": weak_password}
        service = UserService(db_session)
        
        with pytest.raises(ValidationError, match="Password too weak"):
            service.create_user(user_data)
    
    @patch('myapp.services.EmailService.send_welcome_email')
    def test_create_user_sends_welcome_email(self, mock_send_email, db_session):
        """Test that welcome email is sent after user creation."""
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
        service = UserService(db_session)
        
        user = service.create_user(user_data)
        
        mock_send_email.assert_called_once_with(user.email, user.first_name)
    
    @pytest.mark.asyncio
    async def test_async_user_operations(self, async_db_session):
        """Test async user operations."""
        service = AsyncUserService(async_db_session)
        
        user = await service.create_user_async({
            "email": "async@example.com",
            "password": "SecurePass123!"
        })
        
        retrieved_user = await service.get_user_by_id_async(user.id)
        assert retrieved_user.id == user.id
```

### Code Quality Tools Integration

#### Ruff Configuration (Fast Python Linter)

```toml
# pyproject.toml - Ruff configuration
[tool.ruff]
target-version = "py311"
line-length = 88
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # Pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4", # flake8-comprehensions
    "UP", # pyupgrade
    "N",  # pep8-naming
    "S",  # flake8-bandit
    "T20", # flake8-print
    "PT", # flake8-pytest-style
    "RET", # flake8-return
    "SIM", # flake8-simplify
    "ARG", # flake8-unused-arguments
]
ignore = [
    "E501",  # Line too long (handled by black)
    "S101",  # Use of assert detected (pytest uses assert)
    "T201",  # Print found (useful for debugging)
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "S101", # Assert statements are fine in tests
    "ARG", # Unused arguments in fixtures are common
]

[tool.ruff.mccabe]
max-complexity = 10

[tool.ruff.flake8-pytest-style]
fixture-parentheses = false
mark-parentheses = false
```

#### Black Configuration (Code Formatting)

```toml
# pyproject.toml - Black configuration
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

#### mypy Configuration (Type Checking)

```toml
# pyproject.toml - mypy configuration
[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### Coverage Analysis and Reporting

```python
# coverage configuration in pyproject.toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "*/migrations/*",
]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\bProtocol\):",
    "@(abc\.)?abstractmethod",
]
show_missing = true
precision = 2

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

## JavaScript Testing Ecosystem

### Jest Framework

#### Advanced Jest Configuration

```javascript
// jest.config.js - Comprehensive Jest setup
module.exports = {
  // Test environment
  testEnvironment: 'jsdom',
  
  // Module paths and aliases
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@tests/(.*)$': '<rootDir>/tests/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': 
      '<rootDir>/tests/__mocks__/fileMock.js'
  },
  
  // Setup files
  setupFilesAfterEnv: [
    '<rootDir>/tests/setup.js',
    '@testing-library/jest-dom'
  ],
  
  // Test patterns
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.(test|spec).{js,jsx,ts,tsx}',
    '<rootDir>/tests/**/*.{js,jsx,ts,tsx}'
  ],
  
  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx',
    '!src/serviceWorker.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  
  // Reporters
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'reports',
      outputName: 'jest-junit.xml',
    }],
    ['jest-html-reporters', {
      publicPath: 'reports',
      filename: 'jest-report.html',
    }]
  ],
  
  // Transformations
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', {
      presets: [
        ['@babel/preset-env', { targets: { node: 'current' } }],
        '@babel/preset-typescript',
        ['@babel/preset-react', { runtime: 'automatic' }]
      ]
    }]
  },
  
  // Test timeout
  testTimeout: 30000,
  
  // Clear mocks between tests
  clearMocks: true,
  restoreMocks: true,
};
```

#### Advanced React Testing Patterns

```javascript
// UserProfile.test.jsx - Comprehensive React component testing
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import UserProfile from '@/components/UserProfile';
import { AuthProvider } from '@/contexts/AuthContext';

// Mock Service Worker setup
const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      avatar: 'https://example.com/avatar.jpg'
    }));
  }),
  
  rest.put('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ success: true }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Test utilities
const createWrapper = ({ 
  user = { id: 1, role: 'user' }, 
  queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }
  })
} = {}) => {
  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      <AuthProvider value={{ user }}>
        {children}
      </AuthProvider>
    </QueryClientProvider>
  );
};

describe('UserProfile Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    test('renders user profile with loading state', async () => {
      render(<UserProfile userId={1} />, { wrapper: createWrapper() });
      
      expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
      
      await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
      });
    });

    test('renders error state when user fetch fails', async () => {
      server.use(
        rest.get('/api/users/:id', (req, res, ctx) => {
          return res(ctx.status(404), ctx.json({ error: 'User not found' }));
        })
      );

      render(<UserProfile userId={999} />, { wrapper: createWrapper() });

      await waitFor(() => {
        expect(screen.getByText(/user not found/i)).toBeInTheDocument();
      });
    });
  });

  describe('User Interactions', () => {
    test('allows editing profile information', async () => {
      const user = userEvent.setup();
      render(<UserProfile userId={1} />, { wrapper: createWrapper() });

      // Wait for initial load
      await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
      });

      // Click edit button
      await user.click(screen.getByRole('button', { name: /edit profile/i }));

      // Modify name
      const nameInput = screen.getByLabelText(/name/i);
      await user.clear(nameInput);
      await user.type(nameInput, 'Jane Doe');

      // Save changes
      await user.click(screen.getByRole('button', { name: /save/i }));

      await waitFor(() => {
        expect(screen.getByText('Profile updated successfully')).toBeInTheDocument();
      });
    });

    test('validates required fields', async () => {
      const user = userEvent.setup();
      render(<UserProfile userId={1} />, { wrapper: createWrapper() });

      await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
      });

      await user.click(screen.getByRole('button', { name: /edit profile/i }));
      
      // Clear required field
      await user.clear(screen.getByLabelText(/name/i));
      await user.click(screen.getByRole('button', { name: /save/i }));

      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    test('has proper ARIA labels and roles', async () => {
      render(<UserProfile userId={1} />, { wrapper: createWrapper() });

      await waitFor(() => {
        expect(screen.getByRole('main')).toHaveAttribute('aria-label', 'User profile');
        expect(screen.getByRole('img')).toHaveAttribute('alt', 'John Doe avatar');
      });
    });

    test('supports keyboard navigation', async () => {
      const user = userEvent.setup();
      render(<UserProfile userId={1} />, { wrapper: createWrapper() });

      await waitFor(() => {
        expect(screen.getByText('John Doe')).toBeInTheDocument();
      });

      // Tab to edit button
      await user.tab();
      expect(screen.getByRole('button', { name: /edit profile/i })).toHaveFocus();

      // Press Enter to activate
      await user.keyboard('{Enter}');
      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    });
  });
});
```

### Vitest (Fast Alternative to Jest)

```javascript
// vitest.config.js
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.{js,ts}',
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80,
        },
      },
    },
  },
});
```

### Playwright (End-to-End Testing)

```javascript
// playwright.config.js
module.exports = {
  testDir: './e2e',
  timeout: 30000,
  retries: 2,
  workers: process.env.CI ? 1 : undefined,
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
  ],
  
  webServer: {
    command: 'npm run start',
    port: 3000,
    reuseExistingServer: !process.env.CI,
  },
};

// e2e/user-journey.spec.js
import { test, expect } from '@playwright/test';

test.describe('User Authentication Journey', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('complete user registration and login flow', async ({ page }) => {
    // Registration
    await page.click('text=Sign Up');
    await page.fill('[data-testid=email-input]', 'test@example.com');
    await page.fill('[data-testid=password-input]', 'SecurePass123!');
    await page.fill('[data-testid=confirm-password-input]', 'SecurePass123!');
    await page.click('[data-testid=submit-button]');

    // Verify registration success
    await expect(page.locator('text=Welcome! Please verify your email')).toBeVisible();

    // Simulate email verification (mock endpoint)
    await page.goto('/verify-email?token=mock-token');
    await expect(page.locator('text=Email verified successfully')).toBeVisible();

    // Login with verified account
    await page.goto('/login');
    await page.fill('[data-testid=email-input]', 'test@example.com');
    await page.fill('[data-testid=password-input]', 'SecurePass123!');
    await page.click('[data-testid=login-button]');

    // Verify successful login
    await expect(page.locator('[data-testid=user-dashboard]')).toBeVisible();
    await expect(page.locator('text=Welcome back!')).toBeVisible();
  });

  test('handles login with invalid credentials', async ({ page }) => {
    await page.click('text=Log In');
    await page.fill('[data-testid=email-input]', 'invalid@example.com');
    await page.fill('[data-testid=password-input]', 'wrongpassword');
    await page.click('[data-testid=login-button]');

    await expect(page.locator('text=Invalid email or password')).toBeVisible();
    await expect(page.locator('[data-testid=user-dashboard]')).not.toBeVisible();
  });
});
```

## VS Code Testing Integration

### Python Testing Configuration

```json
// .vscode/settings.json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests",
    "--tb=short",
    "--strict-markers",
    "--strict-config"
  ],
  
  "python.testing.autoTestDiscoverOnSaveEnabled": true,
  "python.testing.promptToConfigure": false,
  
  // Coverage integration
  "coverage-gutters.coverageFileNames": [
    "coverage.xml",
    "cov.xml",
    "coverage/cobertura-coverage.xml"
  ],
  "coverage-gutters.showGutterCoverage": true,
  "coverage-gutters.showLineCoverage": true,
  "coverage-gutters.showRulerCoverage": true,
  
  // Code quality tools
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  
  // Type checking
  "python.analysis.typeCheckingMode": "strict",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticMode": "workspace",
  
  // Test discovery
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.pytestPath": "pytest"
}
```

### JavaScript Testing Configuration

```json
// .vscode/settings.json (JavaScript-specific)
{
  "jest.jestCommandLine": "npm run test --",
  "jest.autoRun": {
    "watch": false,
    "onStartup": ["all-tests"]
  },
  "jest.showCoverageOnLoad": true,
  "jest.coverageFormatter": "DefaultFormatter",
  
  // ESLint integration
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "eslint.workingDirectories": ["./"],
  
  // Prettier integration
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  
  // TypeScript
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true
}
```

### VS Code Tasks for Testing

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Python: Run All Tests",
      "type": "shell",
      "command": "pytest",
      "args": [
        "tests/",
        "--cov=src",
        "--cov-report=html",
        "--cov-report=xml",
        "--junit-xml=reports/junit.xml"
      ],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": "$pytest"
    },
    {
      "label": "Python: Run Test Coverage",
      "type": "shell", 
      "command": "coverage",
      "args": ["run", "-m", "pytest", "tests/"],
      "group": "test"
    },
    {
      "label": "JavaScript: Run All Tests",
      "type": "shell",
      "command": "npm",
      "args": ["run", "test", "--", "--coverage", "--watchAll=false"],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    },
    {
      "label": "E2E: Run Playwright Tests",
      "type": "shell",
      "command": "npx",
      "args": ["playwright", "test", "--reporter=html"],
      "group": "test"
    },
    {
      "label": "Quality: Run All Checks",
      "dependsOrder": "sequence",
      "dependsOn": [
        "Python: Lint with Ruff",
        "Python: Format with Black", 
        "Python: Type Check with mypy",
        "JavaScript: Lint with ESLint",
        "JavaScript: Format with Prettier"
      ]
    }
  ]
}
```

## Test-Driven Development

### TDD Workflow

```python
# Example TDD cycle for a calculator function

# 1. RED: Write failing test first
def test_add_two_positive_numbers():
    """Test adding two positive numbers."""
    result = add(2, 3)
    assert result == 5

# 2. GREEN: Write minimal code to pass
def add(a, b):
    return a + b

# 3. REFACTOR: Improve code while keeping tests green
def add(a: float, b: float) -> float:
    """Add two numbers and return the result.
    
    Args:
        a: First number to add
        b: Second number to add
        
    Returns:
        Sum of a and b
        
    Raises:
        TypeError: If inputs are not numbers
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    
    return a + b

# 4. Add more test cases
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0.1, 0.2, 0.3),
    (-5, -3, -8),
])
def test_add_various_numbers(a, b, expected):
    """Test addition with various number combinations."""
    result = add(a, b)
    assert abs(result - expected) < 1e-10  # Handle floating point precision
```

### BDD with pytest-bdd

```python
# features/user_login.feature (Gherkin)
Feature: User Login
  As a user
  I want to log into the system
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given a user exists with email "test@example.com" and password "password123"
    When I submit login form with email "test@example.com" and password "password123"
    Then I should be redirected to the dashboard
    And I should see a welcome message

  Scenario: Failed login with invalid credentials
    Given a user exists with email "test@example.com" and password "password123"
    When I submit login form with email "test@example.com" and password "wrongpassword"
    Then I should see an error message "Invalid credentials"
    And I should remain on the login page

# test_user_login.py
from pytest_bdd import scenarios, given, when, then, parsers

scenarios('features/user_login.feature')

@given(parsers.parse('a user exists with email "{email}" and password "{password}"'))
def user_exists(email, password, user_factory):
    return user_factory(email=email, password=password)

@when(parsers.parse('I submit login form with email "{email}" and password "{password}"'))
def submit_login(email, password, login_page):
    login_page.enter_email(email)
    login_page.enter_password(password)
    login_page.click_login_button()

@then('I should be redirected to the dashboard')
def check_dashboard_redirect(browser):
    assert browser.current_url.endswith('/dashboard')

@then(parsers.parse('I should see an error message "{message}"'))
def check_error_message(message, login_page):
    assert login_page.get_error_message() == message
```

## Quality Assurance Automation

### Pre-commit Hooks Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.51.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        additional_dependencies:
          - eslint@8.51.0
          - '@typescript-eslint/parser@6.7.0'
          - '@typescript-eslint/eslint-plugin@6.7.0'

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.3
    hooks:
      - id: prettier
        files: \.(js|jsx|ts|tsx|json|css|md)$
```

### Automated Security Testing

```python
# test_security.py - Security testing examples
import pytest
import requests
from sqlalchemy import text
from myapp.database import get_db_session

class TestSecurityVulnerabilities:
    """Test suite for common security vulnerabilities."""
    
    def test_sql_injection_protection(self, client, db_session):
        """Test protection against SQL injection attacks."""
        malicious_input = "'; DROP TABLE users; --"
        
        response = client.post('/api/search', json={
            'query': malicious_input
        })
        
        # Should not crash and should sanitize input
        assert response.status_code in [200, 400]  # Not 500
        
        # Verify tables still exist
        result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        tables = [row[0] for row in result]
        assert 'users' in tables

    def test_xss_protection(self, client):
        """Test protection against XSS attacks."""
        xss_payload = "<script>alert('XSS')</script>"
        
        response = client.post('/api/comments', json={
            'content': xss_payload
        })
        
        # Get the created comment
        comment_id = response.json()['id']
        response = client.get(f'/api/comments/{comment_id}')
        
        # Verify script tags are escaped or removed
        content = response.json()['content']
        assert '<script>' not in content
        assert '&lt;script&gt;' in content or 'alert' not in content

    def test_csrf_protection(self, client):
        """Test CSRF protection on state-changing operations."""
        # Attempt operation without CSRF token
        response = client.post('/api/users/delete', json={'id': 1})
        
        assert response.status_code == 403
        assert 'csrf' in response.json().get('error', '').lower()

    @pytest.mark.parametrize("header,expected_value", [
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "DENY"),
        ("X-XSS-Protection", "1; mode=block"),
        ("Strict-Transport-Security", "max-age=31536000"),
    ])
    def test_security_headers(self, client, header, expected_value):
        """Test presence of important security headers."""
        response = client.get('/api/health')
        
        assert header in response.headers
        assert expected_value in response.headers[header]
```

## CI/CD Testing Pipelines

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "18"

jobs:
  python-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with Ruff
      run: ruff check src tests
    
    - name: Format with Black
      run: black --check src tests
    
    - name: Type check with mypy
      run: mypy src
    
    - name: Test with pytest
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost/testdb
      run: |
        pytest tests/ \
          --cov=src \
          --cov-report=xml \
          --cov-report=html \
          --junit-xml=reports/junit.xml \
          --html=reports/report.html
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  javascript-tests:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Lint with ESLint
      run: npm run lint
    
    - name: Type check with TypeScript
      run: npm run type-check
    
    - name: Test with Jest
      run: npm run test -- --coverage --watchAll=false
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: reports/

  e2e-tests:
    runs-on: ubuntu-latest
    needs: [python-tests, javascript-tests]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Install Playwright
      run: npx playwright install --with-deps
    
    - name: Build application
      run: npm run build
    
    - name: Run Playwright tests
      run: npx playwright test
    
    - name: Upload Playwright report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: playwright-report
        path: playwright-report/

  security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Bandit security scan
      run: |
        pip install bandit
        bandit -r src/ -f json -o security-report.json
    
    - name: Run npm audit
      run: npm audit --audit-level moderate
    
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: security-report
        path: security-report.json
```

## Performance and Load Testing

### Python Performance Testing

```python
# test_performance.py
import pytest
import time
from locust import HttpUser, task, between
from memory_profiler import profile
import cProfile
import pstats

class TestPerformance:
    """Performance and load testing."""
    
    @pytest.mark.performance
    def test_database_query_performance(self, db_session):
        """Test database query performance."""
        start_time = time.time()
        
        # Execute expensive query
        result = db_session.execute("""
            SELECT u.*, COUNT(p.id) as post_count
            FROM users u
            LEFT JOIN posts p ON u.id = p.user_id
            GROUP BY u.id
            LIMIT 1000
        """)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert query completes within acceptable time
        assert execution_time < 0.5, f"Query took {execution_time:.2f}s, expected < 0.5s"
        assert len(result.fetchall()) <= 1000

    @pytest.mark.performance
    @profile
    def test_memory_usage(self):
        """Test memory usage of expensive operations."""
        # Create large data structure
        large_list = [i for i in range(1000000)]
        
        # Perform operations
        result = sum(large_list)
        
        assert result == 499999500000
        del large_list  # Cleanup

    def test_response_time_under_load(self, client):
        """Test API response times under concurrent load."""
        import concurrent.futures
        import statistics
        
        def make_request():
            start = time.time()
            response = client.get('/api/health')
            end = time.time()
            return end - start, response.status_code
        
        # Simulate concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [future.result() for future in futures]
        
        response_times = [result[0] for result in results]
        status_codes = [result[1] for result in results]
        
        # All requests should succeed
        assert all(code == 200 for code in status_codes)
        
        # Average response time should be acceptable
        avg_time = statistics.mean(response_times)
        assert avg_time < 0.1, f"Average response time {avg_time:.3f}s > 0.1s"
        
        # 95th percentile should be reasonable
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        assert p95_time < 0.2, f"95th percentile {p95_time:.3f}s > 0.2s"

# Load testing with Locust
class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login user at start of test."""
        self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
    
    @task(3)
    def view_homepage(self):
        self.client.get("/")
    
    @task(2)
    def view_profile(self):
        self.client.get("/profile")
    
    @task(1)
    def create_post(self):
        self.client.post("/api/posts", json={
            "title": "Test Post",
            "content": "This is a test post content."
        })
    
    @task(1)
    def search(self):
        self.client.get("/api/search?q=test")
```

## Testing Best Practices

### Test Organization Principles

1. **Test Structure (AAA Pattern)**
   - **Arrange**: Set up test data and conditions
   - **Act**: Execute the code under test
   - **Assert**: Verify the results

2. **Test Naming Conventions**
   ```python
   def test_should_return_user_when_valid_id_provided():
       """Test should clearly describe what is being tested."""
       pass
   ```

3. **Test Independence**
   - Tests should not depend on other tests
   - Use fixtures for setup and teardown
   - Clean state between tests

4. **Test Data Management**
   ```python
   # Use factories for test data
   @pytest.fixture
   def user_factory():
       def _create_user(**kwargs):
           defaults = {
               "email": "test@example.com",
               "password": "password123",
               "is_active": True
           }
           defaults.update(kwargs)
           return User.create(**defaults)
       return _create_user
   ```

### Code Coverage Best Practices

```python
# test_coverage_strategy.py

# ✅ Good: Test edge cases and error conditions
def test_divide_by_zero_raises_exception():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_negative_numbers():
    result = divide(-10, -2)
    assert result == 5

# ✅ Good: Test boundary conditions
@pytest.mark.parametrize("value,expected", [
    (0, "zero"),
    (1, "positive"),
    (-1, "negative"),
    (100, "positive"),
    (-100, "negative")
])
def test_number_classification(value, expected):
    assert classify_number(value) == expected

# ❌ Avoid: Testing implementation details
def test_user_service_calls_database_exactly_once():
    # This test is brittle and tests implementation, not behavior
    pass

# ✅ Better: Test observable behavior
def test_user_service_returns_user_when_found():
    user = user_service.get_user_by_id(1)
    assert user.id == 1
    assert user.email == "test@example.com"
```

## Advanced Testing Patterns

### Test Doubles and Mocking

```python
# test_mocking_patterns.py
from unittest.mock import Mock, patch, MagicMock
import pytest

class TestMockingPatterns:
    """Advanced mocking and test double patterns."""
    
    def test_mock_return_values(self):
        """Test configuring mock return values."""
        mock_service = Mock()
        mock_service.get_user.return_value = {"id": 1, "name": "Test User"}
        
        result = mock_service.get_user(1)
        assert result["name"] == "Test User"
        mock_service.get_user.assert_called_once_with(1)
    
    def test_mock_side_effects(self):
        """Test using side effects for complex behavior."""
        mock_service = Mock()
        
        # Different responses for different calls
        mock_service.process.side_effect = [
            {"success": True},
            {"success": False, "error": "Rate limit exceeded"},
            Exception("Service unavailable")
        ]
        
        # First call succeeds
        result1 = mock_service.process("data1")
        assert result1["success"] is True
        
        # Second call fails with error
        result2 = mock_service.process("data2")
        assert result2["success"] is False
        
        # Third call raises exception
        with pytest.raises(Exception, match="Service unavailable"):
            mock_service.process("data3")
    
    @patch('myapp.external.EmailService')
    def test_patch_external_service(self, mock_email_service):
        """Test patching external services."""
        # Configure mock
        mock_email_service.return_value.send_email.return_value = True
        
        # Use service in code under test
        from myapp.services import UserService
        user_service = UserService()
        result = user_service.register_user({
            "email": "test@example.com",
            "password": "password123"
        })
        
        # Verify behavior
        assert result.success is True
        mock_email_service.return_value.send_email.assert_called_once()
    
    def test_mock_context_manager(self):
        """Test mocking context managers."""
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.read.return_value = "test content"
        
        with patch('builtins.open', return_value=mock_file):
            from myapp.utils import read_config_file
            content = read_config_file("config.json")
            
        assert content == "test content"
        mock_file.read.assert_called_once()
```

### Property-Based Testing

```python
# test_property_based.py
from hypothesis import given, strategies as st, assume, example
import pytest

class TestPropertyBased:
    """Property-based testing examples."""
    
    @given(st.integers(), st.integers())
    def test_addition_commutative_property(self, a, b):
        """Test that addition is commutative: a + b = b + a"""
        assert add(a, b) == add(b, a)
    
    @given(st.integers(), st.integers(), st.integers())
    def test_addition_associative_property(self, a, b, c):
        """Test that addition is associative: (a + b) + c = a + (b + c)"""
        assert add(add(a, b), c) == add(a, add(b, c))
    
    @given(st.integers())
    def test_addition_identity_property(self, a):
        """Test that zero is the additive identity: a + 0 = a"""
        assert add(a, 0) == a
        assert add(0, a) == a
    
    @given(st.lists(st.integers(), min_size=1))
    def test_list_sort_properties(self, numbers):
        """Test properties of sorted lists."""
        sorted_list = sorted(numbers)
        
        # Length should be preserved
        assert len(sorted_list) == len(numbers)
        
        # Should be in ascending order
        for i in range(len(sorted_list) - 1):
            assert sorted_list[i] <= sorted_list[i + 1]
        
        # Should contain same elements
        assert sorted(numbers) == sorted_list
    
    @given(st.text(min_size=1))
    @example("")  # Add explicit edge case
    def test_string_operations(self, text):
        """Test string operation properties."""
        assume(len(text) > 0)  # Skip empty strings for this test
        
        # Uppercase and then lowercase should preserve length
        upper_text = text.upper()
        lower_text = upper_text.lower()
        
        assert len(text) == len(upper_text) == len(lower_text)
        
        # Double reversal should return original
        assert text == text[::-1][::-1]
```

This comprehensive testing guide provides enterprise-grade strategies for both Python and JavaScript ecosystems, with deep VS Code integration and modern best practices. The guide covers everything from basic unit testing to advanced property-based testing, ensuring robust quality assurance across the entire development lifecycle.

## Related Resources

- [Documentation Best Practices](./documentation-best-practices.md)
- [VS Code Copilot Complete Guide](../tools/vscode-copilot-complete-guide.md)
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/docs/getting-started)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Library](https://testing-library.com/)

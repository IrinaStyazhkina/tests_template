# F2F Bank — Test Assignment

F2F Bank is a simple web application that simulates a peer-to-peer bank transfer service (SBP-style). Users can register, log in, top up their balance, and send money transfers by phone number.

This repository is provided as a **test assignment**: your task is to write end-to-end (e2e) tests using [Playwright](https://playwright.dev/).

---

## Prerequisites

Before you start, make sure the following tools are installed on your machine:

| Tool | Version | How to check |
|------|---------|--------------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | any recent | `docker --version` |
| [Docker Compose](https://docs.docker.com/compose/) | v2+ | `docker compose version` |
| [Node.js](https://nodejs.org/) | 18+ | `node --version` |
| [Git](https://git-scm.com/) | any | `git --version` |

> **Windows users:** use PowerShell or Git Bash for all commands below.

---

## Running the Application

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Start all services

```bash
docker compose up -d --build
```

This command builds and starts four containers:
- **database** — PostgreSQL
- **app** — Python/FastAPI backend (port 8080 internally)
- **client** — Vue.js frontend (static build)
- **web-proxy** — Nginx, serves everything on **http://localhost**

The first build may take 2–5 minutes. Subsequent starts are faster.

### 3. Open the application

Go to **http://localhost** in your browser.

You should see the F2F Bank login page.

### 4. Stop the application

```bash
docker compose down
```

To also delete the database data (full reset):

```bash
docker compose down -v
```

---

## Application Overview

Once running, the app provides the following functionality:

| Feature | URL | Description |
|---------|-----|-------------|
| Registration | `/register` | Create a new account (name, surname, email, password) |
| Login | `/login` | Sign in with email and password |
| Home / Transfer | `/` | Send a transfer by phone number, amount and purpose |
| Transactions | `/transactions` | View transaction history; top up balance |
| Profile | `/profile` | View your name, surname and email |

### Key validation rules
- **Phone number:** must start with `+`, total 10–15 digits (spaces, dashes and parentheses are allowed). Example: `+7 999 123-45-67`
- **Transfer amount:** must be greater than zero
- **Balance:** must be sufficient for the transfer

---

## Test Assignment

### Your task

Write **end-to-end tests using Playwright** that cover the main user scenarios listed below.

### Setup

Initialize a Playwright project inside the repository root (or a separate `tests/` folder):

```bash
npm init playwright@latest
```

Choose **TypeScript**, browser **Chromium** (minimum), and set `baseURL` to `http://localhost` in `playwright.config.ts`.

### Scenarios to cover

Explore the application on your own and define the test scenarios yourself.

For each scenario you identify:

1. **Describe** what is being tested (feature, input, expected result)
2. **Assign a criticality level** — for example: `Critical`, `High`, `Medium`, `Low`
3. **Implement** it as a Playwright test

There is no single correct list — part of the task is to demonstrate your ability to analyse an application and prioritise what matters most.

---

### Tips

- Each test that requires an authenticated user should log in at the start (or use `storageState` for reuse).
- Use `beforeEach` / `beforeAll` for setup steps shared across tests in the same file.
- Run tests with:

```bash
npx playwright test
```

Run with UI mode (visual, great for debugging):

```bash
npx playwright test --ui
```

Generate a report after the run:

```bash
npx playwright show-report
```

---

### Deliverables

Submit the following:

1. All test files (e.g. `tests/*.spec.ts`)
2. `playwright.config.ts`
3. A brief description (in comments or a separate `NOTES.md`) of any bugs or unexpected behaviour you found during testing

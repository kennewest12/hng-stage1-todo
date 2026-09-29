# AGENTS.md

## Project Overview

This project is an AI-built To-Do List application for HNG Internship 15 Stage 1.

The application must support:
- Task creation
- Task viewing
- Task updating
- Task deletion
- Task completion
- Notes
- Priority management
- Task filtering

## Development Rules

- Use FastAPI for the backend.
- Use React with Vite for the frontend.
- Use PostgreSQL for persistent data.
- Keep API routes RESTful.
- Use Pydantic schemas for API request and response validation.
- Keep database logic separate from API route handlers.
- Keep the implementation simple and easy to maintain.
- Do not introduce unnecessary dependencies.
- Do not commit secrets or local environment files.

## Testing Rules

- Every API endpoint created must have a corresponding test.
- Run the backend test suite after API changes.
- Test successful responses and important error cases.
- Do not consider an endpoint complete until its tests pass.

## Validation

Before completing a feature:

1. Run the application locally.
2. Test the API endpoint.
3. Run the automated tests.
4. Test the corresponding frontend functionality.
5. Fix errors before moving to the next feature.

## Git Rules

- Make small, meaningful commits.
- Never commit .env.
- Keep .env.example updated when environment variables are added.
- Do not commit generated files such as virtual environments, caches, or build output.

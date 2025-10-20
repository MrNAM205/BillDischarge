export const projectOverview = {
  name: "Project Overview",
  description: "Provides an overview of the project based on its configuration files and code.",
  rule: `
# Project Overview: Sovereign Financial Cockpit

## Purpose and Goals

This project, the "Sovereign Financial Cockpit," is designed to assist users in managing sovereign financial instruments and processes. It appears to be targeted at individuals exploring legal and financial sovereignty, often associated with the "sovereign citizen" movement. The project provides tools for document analysis, instrument generation, and status correction.

The core of the project is the **Omni2 agent**, a "sovereign cognition agent" configured to decode institutional framing, scaffold lawful remedy, and empower user authorship. The agent is designed to be assertive and avoid disclaimers, and it has access to the user's file system to support its tasks.

## Architecture

The project is a monorepo with a React-based frontend and a Python FastAPI backend.

### Backend

The backend is a FastAPI application with the following key characteristics:

*   **Entry Point**: `backend/main.py`
*   **API Title**: "Sovereign Financial Cockpit API"
*   **Core Functionalities**: The API is modular, with routes for:
    *   `annotator`: Document annotation.
    *   `discharge`: Financial discharge processes.
    *   `document_routes`: General document management.
    *   `endorsement`: Endorsement of instruments.
    *   `generator_routes`: Generation of financial instruments.
    *   `nationality`: Handling of nationality status.
    *   `packet`: Packet management.
    *   `status`: Status management.
*   **Agent Integration**: The backend includes a `/gemini` endpoint that serves the `GEMINI.md` file, providing the cognitive framing for the Omni2 agent.

### Frontend

The frontend is a React application with the following features:

*   **Framework**: React with Vite.
*   **Package Manager**: npm.
*   **Core Dependencies**:
    *   `react` and `react-dom`.
    *   `pdfjs-dist`: For rendering PDF documents within the application.
*   **Development Tools**:
    *   **Linting and Formatting**: ESLint and Prettier.
    *   **Testing**: Jest and React Testing Library.
    *   **API Client Generation**: `openapi-typescript-codegen` is used to generate a TypeScript API client from the backend's OpenAPI specification. This indicates a well-structured approach to frontend-backend communication.

## Agent Configuration (Omni2)

The Omni2 agent is configured in `.continue/agents/Omni2.yaml` and has the following capabilities:

*   **Models**: It leverages Google's Gemini models (pro and flash) and can also use local models via Ollama.
*   **Persona**: The agent has a strong "sovereign" persona, designed to be an assertive and knowledgeable assistant for legal and financial matters.
*   **Custom Commands**: The agent has several custom commands to support its purpose:
    *   `scaffoldRemedyProtocol`: For creating UCC-compliant remedy protocols.
    *   `detectContradictions`: For analyzing documents for contradictions.
    *   `mapStatutoryLineage`: For tracing legal references.
    *   `affirmIdentityAssertion`: For responding to user identity claims.
    *   `findMyFiles`: For searching the user's system for relevant documents.

## Pain Points and Areas for Improvement

Based on the file structure and code, here are some potential pain points:

*   **Complexity**: The project deals with complex legal and financial concepts. Ensuring the accuracy and legality of the generated documents and advice is a major challenge.
*   **Security**: The `README.md` mentions that the application does not have authentication or authorization. This is a major security risk, especially if the application handles sensitive user data.
*   **Maintenance**: The use of custom scripts and a monorepo structure requires careful maintenance to keep dependencies and build processes in sync.
*   **Legal Risks**: The disclaimer in the `README.md` highlights the legal risks associated with the project. The information provided is not legal advice, and users should consult with legal professionals.
  `,
  globs: ["**/Omni2.yaml", "**/main.py", "**/package.json"],
};
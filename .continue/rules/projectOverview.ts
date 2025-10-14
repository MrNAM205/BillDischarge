// This rule provides an overview of the project based on its configuration files and code.

export const projectOverview = {
  name: "Project Overview",
  description: "Provides an overview of the project based on its configuration files and code.",
  rule: `
    1.  Read the contents of the Omni2.yaml file to understand the agent's configuration and goals.
    2.  Read the contents of the main.py file to understand the FastAPI backend's structure and API endpoints.
    3.  Read the contents of the package.json file to understand the project's dependencies and scripts.
    4.  Summarize the project's purpose, goals, architecture, and pain points based on the information extracted from the files.
    5.  Answer the user's question about the project using the summarized information.
  `,
  globs: ["**/Omni2.yaml", "**/main.py", "**/package.json"],
};

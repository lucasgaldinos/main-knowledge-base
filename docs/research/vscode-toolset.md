lucasgaldinos: Please, analyze this video <https://www.youtube.com/watch?v=JfJDMF9OD-A> about vscode toolset for copilot agents.  I don't have any idea of how, why and when to use. Please search for explanations guides on this theme

```json example_toolset.toolset.json
// Place your tool sets here...
// Example:
// {
//  "toolSetName": {
//      "tools": [
//          "someTool",
//          "anotherTool"
//      ],
//      "description": "description",
//      "icon": "tools"
//  }
// }
```

Github Copilot: An analysis of the provided video and supplementary documentation reveals that a **Copilot "toolset"** is a user-defined collection of commands that extends the capabilities of GitHub Copilot's agent mode in VS Code. It allows the AI to perform complex, multi-step tasks beyond simple code generation by interacting with external services and local commands.

-----

### How It Works

A toolset is defined in a `.toolset.json` file. Within this file, you declare a named set of "tools." Each tool is essentially a command or a script that Copilot can invoke.

- **Tools**: These can be built-in VS Code commands, terminal commands, or calls to external APIs.
- **Description**: Each tool requires a natural language description. This is the most critical part, as Copilot uses this description to understand the tool's purpose and determine when to use it to fulfill a user's prompt.
- **Invocation**: You activate a toolset in the Copilot Chat pane by referencing its name (e.g., `@workspace /tools your-toolset-name`). Once activated, you can give Copilot a high-level task, and it will autonomously decide which tools from the set to execute to achieve the goal.

The video demonstrates this by creating a toolset that automates a workflow:

1. **Fetch** the title of the latest post from a specific blog (`fetch` tool).
2. **Browse** a GitHub repository (`get pull request` tool).
3. **Create** a new GitHub issue summarizing the blog post (`get pull request comments` tool).
4. **Add** a comment to the new issue with the post's title.

-----

### Why and When to Use Toolsets

The primary purpose of toolsets is to **automate complex and repetitive developer workflows**.

- **Why**: To chain multiple actions together that Copilot would not know how to perform natively. It provides the AI with specific, scoped capabilities relevant to your project, making it a more powerful and context-aware assistant.
- **When**: Use toolsets for any multi-step task you perform regularly. Examples include:
  - Running a sequence of build, test, and deployment scripts.
  - Interacting with project management tools (e.g., creating a Jira ticket from a `// TODO:` comment).
  - Fetching data from an internal API and scaffolding code to interact with it.
  - Automating parts of a pull request review process.

-----

### Configuration (`example_toolset.toolset.json`)

Your provided JSON snippet is the basic schema for defining a toolset.

```json
{
  "yourToolSetName": {
    "description": "A clear description of what this collection of tools accomplishes.",
    "icon": "tools", // VS Code icon identifier
    "tools": [
      "github.copilot.dev.getPullRequest",
      "github.copilot.dev.getPullRequestComments",
      "terminal.runCommand"
    ]
  }
}
```

- `yourToolSetName`: This is the unique identifier you will use to invoke the toolset.
- `description`: Essential for both your own reference and for Copilot's understanding.
- `tools`: An array of strings, where each string is the identifier for a command. These can be built-in VS Code command IDs or custom commands you define elsewhere.

To configure and create your own toolsets, use the command palette (`Ctrl+Shift+P`) and search for **`Chat: Configure Tool Sets`**.

-----

### External Documentation and Guides

For a more comprehensive understanding, refer to the official Visual Studio Code documentation.

- **[Use agent mode in VS Code](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)**: This document provides a detailed overview of agent mode, which is the foundation for using toolsets. It explains how to enable and interact with agents and manage the tools they can use.
- **[Use MCP servers in VS Code](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)**: This guide explains a more advanced method of extending Copilot by creating and connecting to "MCP" (Microsoft Copilot Platform) servers, which can provide a discoverable set of tools.
- **[GitHub Copilot Documentation](https://docs.github.com/copilot)**: The official and most authoritative source for all features, including advanced customizations like agents and extensions.

This [video guide on Agent Mode Tools](https://www.youtube.com/watch?v=VePxCcF99w4) offers a concise visual explanation of how different types of tools, including built-in ones and those from extensions, function within Copilot's agent mode.
<https://www.youtube.com/watch?v=JfJDMF9OD-A> <https://www.youtube.com/watch?v=VePxCcF99w4>

<https://code.visualstudio.com/docs/copilot/customization/mcp-servers>
<https://code.visualstudio.com/api/extension-guides/ai/mcp>
<https://code.visualstudio.com/docs/debugtest/tasks>

# Overview of the AI Search Bot template

This template showcases a bot app that responds to user questions like an AI assistant according to data from Azure Search. This enables your users to talk with the AI assistant in Teams to find information.

The app template is built using the Teams AI library, which provides the capabilities to build AI-based Teams applications.

- [Overview of the AI Search Bot template](#overview-of-the-ai-search-bot-template)
  - [Get started with the AI Search Bot template](#get-started-with-the-ai-search-bot-template)
  - [What's included in the template](#whats-included-in-the-template)
  - [Extend the AI Search Bot template with more AI capabilities](#extend-the-ai-search-bot-template-with-more-ai-capabilities)
  - [Additional information and references](#additional-information-and-references)

## Get started with the AI Search Bot template

> **Prerequisites**
>
> To run the AI Search Bot template in your local dev machine, you will need:
>
> - [Python](https://www.python.org/), version 3.8 to 3.11.
> - [Python extension](https://code.visualstudio.com/docs/languages/python), version v2024.0.1 or higher.
> - [Teams Toolkit Visual Studio Code Extension](https://aka.ms/teams-toolkit) latest version or [Teams Toolkit CLI](https://aka.ms/teamsfx-cli).
> - An account with [Azure OpenAI](https://aka.ms/oai/access).
> - An [Azure Search service](https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search).
> - A [Microsoft 365 account for development](https://docs.microsoft.com/microsoftteams/platform/toolkit/accounts).

### Configurations
1. First, Open the command box and enter `Python: Create Environment` to create and activate your desired virtual environment. Remember to select `requirements.txt` as dependencies to install when creating the virtual environment.
1. In file *env/.env.local.user*, fill in your Azure OpenAI key `SECRET_AZURE_OPENAI_API_KEY`, deployment name `AZURE_OPENAI_MODEL_DEPLOYMENT_NAME`, endpoint `AZURE_OPENAI_ENDPOINT` and embedding deployment name `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`.
1. In file *env/.env.local.user*, fill in your Azure Search key `SECRET_AZURE_SEARCH_KEY` and endpoint `AZURE_SEARCH_ENDPOINT`.

### Setting up index and documents
1. Use command `python -m src.indexers.setup` to create index and upload documents in `src/files`.
1. You will see the following information indicated the success of setup:
    ```
    Create index succeeded. If it does not exist, wait for 5 seconds...
    Upload new documents succeeded. If they do not exist, wait for several seconds...
    setup finished
    ```
1. Once you're done using the sample it's good practice to delete the index. You can do so with the command `python -m src.indexers.delete`.

### Conversation with bot
1. Select the Teams Toolkit icon on the left in the VS Code toolbar.
1. In the Account section, sign in with your [Microsoft 365 account](https://docs.microsoft.com/microsoftteams/platform/toolkit/accounts) if you haven't already.
1. Press F5 to start debugging which launches your app in Teams using a web browser. Select `Debug in Teams (Edge)` or `Debug in Teams (Chrome)`.
1. When Teams launches in the browser, select the Add button in the dialog to install your app to Teams.
1. You will receive a welcome message from the bot, or send any message to get a response.

**Congratulations**! You are running an application that can now interact with users in Teams:

![alt text](image.png)

## What's included in the template

| Folder       | Contents                                            |
| - | - |
| `.vscode`    | VSCode files for debugging                          |
| `appPackage` | Templates for the Teams application manifest        |
| `env`        | Environment files                                   |
| `infra`      | Templates for provisioning Azure resources          |
| `src`        | The source code for the application                 |

The following files can be customized and demonstrate an example implementation to get you started.

| File                                 | Contents                                           |
| - | - |
|`src/bot.py`| Handles business logics for the AI Search Bot.|
|`src/config.py`| Defines the environment variables.|
|`src/app.py`| Main module of the AI Search Bot, hosts a aiohttp api server for the app.|
|`src/AzureAISearchDataSource.py`| Handles data search logics.|
|`src/indexers/*.py`| Defines functions of creating, deleting, uploading, fetching indexes and documents.|
|`src/files/*.md`| Raw text data source.|
|`src/prompts/chat/skprompt.txt`| Defines the prompt.|
|`src/prompts/chat/config.json`| Configures the prompt.|

The following are Teams Toolkit specific project files. You can [visit a complete guide on Github](https://github.com/OfficeDev/TeamsFx/wiki/Teams-Toolkit-Visual-Studio-Code-v5-Guide#overview) to understand how Teams Toolkit works.

| File                                 | Contents                                           |
| - | - |
|`teamsapp.yml`|This is the main Teams Toolkit project file. The project file defines two primary things:  Properties and configuration Stage definitions. |
|`teamsapp.local.yml`|This overrides `teamsapp.yml` with actions that enable local execution and debugging.|
|`teamsapp.testtool.yml`|This overrides `teamsapp.yml` with actions that enable local execution and debugging in Teams App Test Tool.|

## Extend the AI Search Bot template with more AI capabilities

You can follow [Get started with Teams AI library](https://learn.microsoft.com/en-us/microsoftteams/platform/bots/how-to/teams%20conversational%20ai/how-conversation-ai-get-started) to extend the AI Search Bot template with more AI capabilities.

## Additional information and references
- [Teams AI library](https://aka.ms/teams-ai-library)
- [Teams Toolkit Documentations](https://docs.microsoft.com/microsoftteams/platform/toolkit/teams-toolkit-fundamentals)
- [Teams Toolkit CLI](https://aka.ms/teamsfx-toolkit-cli)
- [Teams Toolkit Samples](https://github.com/OfficeDev/TeamsFx-Samples)
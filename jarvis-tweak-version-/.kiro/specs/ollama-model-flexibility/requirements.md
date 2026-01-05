# Requirements Document

## Introduction

Enhance the self-operating-computer framework to support flexible Ollama model selection, allowing users to utilize any locally available Ollama model instead of being restricted to the hardcoded "llava" model. This will enable users to leverage their specific downloaded models like llava:7b without requiring API keys or external services.

## Glossary

- **Ollama_Client**: The local Ollama service that manages and serves AI models
- **Model_Identifier**: The specific name/tag of an Ollama model (e.g., "llava:7b", "llama2", "codellama")
- **Self_Operating_Computer**: The main framework that controls computer operations using AI models
- **Model_Configuration**: Settings that specify which Ollama model to use for operations

## Requirements

### Requirement 1

**User Story:** As a developer with local Ollama models, I want to specify which model to use, so that I can leverage my downloaded models without being restricted to the default "llava" model.

#### Acceptance Criteria

1. WHEN a user runs the operate command with Ollama, THE Self_Operating_Computer SHALL allow specifying a custom model identifier
2. WHEN a custom Ollama model is specified, THE Ollama_Client SHALL use that exact model for vision operations
3. WHEN no custom model is specified, THE Self_Operating_Computer SHALL default to "llava" for backward compatibility
4. WHEN an invalid model identifier is provided, THE Self_Operating_Computer SHALL return a descriptive error message

### Requirement 2

**User Story:** As a user, I want to see which Ollama models are available on my system, so that I can choose the appropriate model for my tasks.

#### Acceptance Criteria

1. WHEN a user requests available models, THE Ollama_Client SHALL list all locally available models
2. WHEN listing models, THE Self_Operating_Computer SHALL display model names, sizes, and last modified dates
3. WHEN no models are available, THE Self_Operating_Computer SHALL inform the user and provide installation guidance
4. WHEN the Ollama service is not running, THE Self_Operating_Computer SHALL provide clear instructions to start it

### Requirement 3

**User Story:** As a developer, I want to configure a default Ollama model, so that I don't have to specify it every time I run the application.

#### Acceptance Criteria

1. WHEN a user sets a default Ollama model, THE Model_Configuration SHALL persist this setting
2. WHEN the application starts with Ollama mode, THE Self_Operating_Computer SHALL use the configured default model
3. WHEN no default is configured, THE Self_Operating_Computer SHALL use "llava" as the fallback
4. WHEN a command-line model is specified, THE Self_Operating_Computer SHALL override the configured default

### Requirement 4

**User Story:** As a user, I want the system to validate my Ollama model before starting operations, so that I can catch configuration issues early.

#### Acceptance Criteria

1. WHEN starting with an Ollama model, THE Self_Operating_Computer SHALL verify the model exists locally
2. WHEN a model is not found, THE Self_Operating_Computer SHALL suggest available alternatives
3. WHEN the Ollama service is unreachable, THE Self_Operating_Computer SHALL provide connection troubleshooting steps
4. WHEN model validation succeeds, THE Self_Operating_Computer SHALL proceed with normal operations

### Requirement 5

**User Story:** As a developer, I want backward compatibility with existing Ollama usage, so that current workflows continue to work without changes.

#### Acceptance Criteria

1. WHEN using the existing `-m llava` command, THE Self_Operating_Computer SHALL function exactly as before
2. WHEN existing configuration files are present, THE Self_Operating_Computer SHALL honor them without modification
3. WHEN no model is specified in Ollama mode, THE Self_Operating_Computer SHALL default to "llava" behavior
4. WHEN upgrading from previous versions, THE Self_Operating_Computer SHALL maintain all existing functionality
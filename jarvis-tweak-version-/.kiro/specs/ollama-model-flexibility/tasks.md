# Implementation Plan: Ollama Model Flexibility

## Overview

This implementation plan converts the Ollama model flexibility design into discrete coding tasks. The approach focuses on enhancing the existing Ollama integration while maintaining backward compatibility. Each task builds incrementally, starting with core model resolution, then adding CLI enhancements, configuration management, and comprehensive testing.

## Tasks

- [x] 1. Create Ollama model resolver and validation system
  - Create `OllamaModelResolver` class in new file `operate/models/ollama_resolver.py`
  - Implement model specification parsing (legacy "llava", explicit "ollama:model", auto-resolve "ollama")
  - Add model validation using Ollama client list API
  - Add model listing functionality with size and date information
  - _Requirements: 1.1, 1.4, 2.1, 2.2, 4.1_

- [ ]* 1.1 Write property tests for model resolver
  - **Property 1: Model Specification Acceptance**
  - **Validates: Requirements 1.1**

- [ ]* 1.2 Write property tests for model validation
  - **Property 8: Model Validation and Operation**
  - **Validates: Requirements 4.1, 4.4**

- [x] 2. Enhance configuration system for Ollama model defaults
  - Extend `Config` class in `operate/config.py` to support Ollama model configuration
  - Add `get_default_ollama_model()` and `set_default_ollama_model()` methods
  - Implement configuration persistence to `.env` file
  - Add `initialize_ollama_with_model()` method for model-specific initialization
  - _Requirements: 3.1, 3.2, 3.3_

- [ ]* 2.1 Write property tests for configuration persistence
  - **Property 5: Configuration Persistence**
  - **Validates: Requirements 3.1**

- [ ]* 2.2 Write property tests for default model usage
  - **Property 6: Default Model Usage**
  - **Validates: Requirements 3.2**

- [x] 3. Update CLI argument parsing for Ollama model specification
  - Modify `operate/main.py` to support new Ollama model formats
  - Add `--list-models` flag for Ollama model listing
  - Add `--set-default` flag for setting default Ollama model
  - Implement model specification parsing in argument handler
  - _Requirements: 1.1, 2.1, 3.1_

- [ ]* 3.1 Write unit tests for CLI argument parsing
  - Test various model specification formats
  - Test new command-line flags
  - _Requirements: 1.1_

- [x] 4. Integrate model resolver with existing Ollama API calls
  - Modify `call_ollama_llava()` function in `operate/models/apis.py`
  - Replace hardcoded "llava" model with resolved model name
  - Add model validation before API calls
  - Update function name to `call_ollama_model()` for clarity
  - _Requirements: 1.2, 4.1_

- [ ]* 4.1 Write property tests for exact model usage
  - **Property 2: Exact Model Usage**
  - **Validates: Requirements 1.2**

- [ ] 5. Implement error handling and user guidance
  - Add comprehensive error messages for invalid models
  - Implement model suggestion system when models not found
  - Add service availability checking with helpful error messages
  - Create user guidance for model installation and Ollama setup
  - _Requirements: 1.4, 2.3, 2.4, 4.2, 4.3_

- [ ]* 5.1 Write property tests for error handling
  - **Property 3: Error Message Generation**
  - **Validates: Requirements 1.4**

- [ ]* 5.2 Write property tests for alternative suggestions
  - **Property 9: Alternative Suggestions**
  - **Validates: Requirements 4.2**

- [-] 6. Checkpoint - Ensure core functionality works
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Add command-line override and precedence logic
  - Implement model precedence: CLI > configured default > "llava" fallback
  - Update model resolution to handle precedence correctly
  - Add validation for command-line model override scenarios
  - _Requirements: 3.4, 1.3, 3.3_

- [ ]* 7.1 Write property tests for command-line override
  - **Property 7: Command-Line Override**
  - **Validates: Requirements 3.4**

- [ ]* 7.2 Write property tests for default fallback behavior
  - **Property 11: Default Fallback Behavior**
  - **Validates: Requirements 1.3, 3.3, 5.3**

- [ ] 8. Ensure backward compatibility
  - Verify existing `-m llava` command works unchanged
  - Test configuration file compatibility with existing setups
  - Add migration logic for any configuration changes
  - Validate all existing Ollama functionality remains intact
  - _Requirements: 5.1, 5.2, 5.4_

- [ ]* 8.1 Write unit tests for backward compatibility
  - Test existing `-m llava` command behavior
  - Test configuration file compatibility
  - _Requirements: 5.1, 5.2_

- [ ]* 8.2 Write property tests for configuration compatibility
  - **Property 10: Configuration Compatibility**
  - **Validates: Requirements 5.2**

- [ ] 9. Add model listing and information display
  - Implement `--list-models` command functionality
  - Create formatted output for model information (name, size, date)
  - Add filtering and sorting options for model list
  - Handle empty model list with installation guidance
  - _Requirements: 2.1, 2.2, 2.3_

- [ ]* 9.1 Write property tests for model listing
  - **Property 4: Model Listing Completeness**
  - **Validates: Requirements 2.1, 2.2**

- [ ]* 9.2 Write unit tests for edge cases
  - Test no models available scenario
  - Test Ollama service unavailable scenario
  - _Requirements: 2.3, 2.4_

- [ ] 10. Final integration and testing
  - Wire all components together in main entry point
  - Update model selection logic in `get_next_action()`
  - Add comprehensive integration tests
  - Verify end-to-end functionality with real Ollama models
  - _Requirements: All requirements_

- [ ]* 10.1 Write integration tests
  - Test complete workflows with different model specifications
  - Test error scenarios and recovery
  - _Requirements: All requirements_

- [ ] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- The implementation maintains full backward compatibility with existing Ollama usage
"""
Self-Operating Computer
"""
import argparse
from operate.utils.style import ANSI_BRIGHT_MAGENTA, ANSI_GREEN, ANSI_RESET
from operate.operate import main


def main_entry():
    parser = argparse.ArgumentParser(
        description="Run the self-operating-computer with a specified model."
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Specify the model to use (e.g., gpt-4-with-ocr, llava, ollama:llava:7b)",
        required=False,
        default="gpt-4-with-ocr",
    )

    # Add a voice flag
    parser.add_argument(
        "--voice",
        help="Use voice input mode",
        action="store_true",
    )
    
    # Add a flag for verbose mode
    parser.add_argument(
        "--verbose",
        help="Run operate in verbose mode",
        action="store_true",
    )
    
    # Allow for direct input of prompt
    parser.add_argument(
        "--prompt",
        help="Directly input the objective prompt",
        type=str,
        required=False,
    )

    # Add Ollama-specific flags
    parser.add_argument(
        "--list-models",
        help="List available Ollama models",
        action="store_true",
    )

    parser.add_argument(
        "--set-default",
        help="Set default Ollama model",
        type=str,
        metavar="MODEL_NAME",
    )

    try:
        args = parser.parse_args()
        
        # Handle Ollama-specific commands
        if args.list_models:
            from operate.models.ollama_resolver import OllamaModelResolver
            from operate.config import Config
            
            config = Config()
            config.verbose = args.verbose
            resolver = OllamaModelResolver(config)
            
            try:
                models = resolver.list_available_models()
                resolver.print_model_list(models)
            except ConnectionError as e:
                print(f"{ANSI_BRIGHT_MAGENTA}[Ollama Error]{ANSI_RESET} {e}")
            return
        
        if args.set_default:
            from operate.models.ollama_resolver import OllamaModelResolver
            from operate.config import Config
            
            config = Config()
            config.verbose = args.verbose
            resolver = OllamaModelResolver(config)
            
            # Validate the model exists
            try:
                if resolver.validate_model(args.set_default):
                    config.set_default_ollama_model(args.set_default)
                    print(f"{ANSI_GREEN}Default Ollama model set to: {args.set_default}{ANSI_RESET}")
                else:
                    print(f"{ANSI_BRIGHT_MAGENTA}Model '{args.set_default}' not found.{ANSI_RESET}")
                    suggestions = resolver.get_model_suggestions(args.set_default)
                    if suggestions:
                        print("Available models:")
                        for suggestion in suggestions:
                            print(f"  - {suggestion}")
            except ConnectionError as e:
                print(f"{ANSI_BRIGHT_MAGENTA}[Ollama Error]{ANSI_RESET} {e}")
            return
        
        main(
            args.model,
            terminal_prompt=args.prompt,
            voice_mode=args.voice,
            verbose_mode=args.verbose
        )
    except KeyboardInterrupt:
        print(f"\n{ANSI_BRIGHT_MAGENTA}Exiting...")


if __name__ == "__main__":
    main_entry()

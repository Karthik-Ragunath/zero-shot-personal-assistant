# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands
- Install: `pip install -r csm/requirements.txt`
- Run: `python csm/run_csm.py`
- Setup for development: `pip install -e .`
- Environment: Set `export NO_TORCH_COMPILE=1` before running

## Code Style
- Use Python type hints for all function parameters and return values
- Import order: standard library, third-party packages, local modules
- Use dataclasses for structured data
- Use torch.inference_mode() decorator for generation functions
- Follow PEP 8 conventions (4-space indentation)
- Error handling: Use descriptive ValueError for input validation
- Naming: snake_case for functions/variables, CamelCase for classes
- Document all functions with docstrings that include Args and Returns
- Use consistent tensor dimension annotations in comments
run:
	@./gpt4all_voice/gpt4all_voice.py
build_dependencies: runtime_deps
	@./build_dependencies.sh
runtime_deps:
	@./runtime_deps.sh
download_gpt4all:
	@./download_gpt4all.sh
project_config:
	@./_project_config.sh

# System Patterns

## System Architecture
- Python-based conversion script
- WSL integration for Linux environment
- Windows registry for context menu integration
- XTTS-v2 model for voice synthesis
- FFmpeg for audio processing

## Key Technical Decisions
- Using XTTS-v2 for superior voice quality
- WSL-based implementation for Linux compatibility
- Chunk-based processing for large files
- Reference voice system for consistent output
- Windows context menu for easy access
- Downloads folder for consistent output location

## Design Patterns in Use
- Pipeline pattern for text processing
- Chunking pattern for large file handling
- Registry integration pattern for Windows
- Temporary file management for processing
- Clean separation of concerns (text processing, TTS, audio conversion)

## Component Relationships
- Registry entry → Python script
- Python script → XTTS-v2 model
- XTTS-v2 → Reference voice
- Text chunks → Individual WAV files
- WAV files → Final MP3

## Critical Implementation Paths
1. File Selection → Context Menu
2. Text Processing Pipeline:
   - Markdown cleaning
   - Text chunking
   - TTS conversion
   - Audio concatenation
3. Output Generation:
   - WAV file creation
   - MP3 conversion
   - Downloads folder placement

---

*Update this file as the system evolves and new patterns emerge.* 
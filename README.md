# Markdown to MP3 Converter

## Why I Created This

As a student of finance and quantitative development, I needed an efficient way to consume large amounts of information in various formats. This tool was born out of that need - a simple way to convert my markdown study notes into audio files that I can listen to while commuting, exercising, or doing other activities.

The key features that make this tool particularly useful:
- **Right-click Integration**: Simply right-click any markdown file in Windows Explorer to convert it to MP3
- **High-Quality TTS**: Uses Coqui TTS for natural-sounding speech synthesis
- **Markdown Cleaning**: Automatically removes code blocks, links, and other markdown syntax for cleaner audio
- **Chunking**: Intelligently splits long text into manageable chunks for better processing
- **WSL Integration**: Works seamlessly with Windows Subsystem for Linux

This tool has been particularly helpful for:
- Converting study notes to audio for multi-modal learning
- Creating audio versions of technical documentation
- Making long-form content more accessible
- Learning on the go

## Requirements

- Windows 10/11 with WSL2 (Ubuntu) installed
- Python 3.8 or higher
- ffmpeg installed in WSL
- PowerShell 5.1 or higher

## Installation

1. **Clone the Repository**
   ```bash
   git clone git@github.com:cinthisone/markdown-to-mp3.git
   cd markdown-to-mp3
   ```

2. **Set Up Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Install ffmpeg in WSL**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

## Windows PowerShell Integration

To integrate the script with Windows Explorer's context menu, follow these steps:

1. **Create a PowerShell Script**

   Save the following PowerShell script as `convert_md_to_mp3.ps1` in your project directory:

   ```powershell
   try {
       # Get path of the file passed from right-click
       $windowsPath = $args[0]
       if (-not (Test-Path $windowsPath)) {
           throw "Input file not found: $windowsPath"
       }

       # Convert Windows path to WSL path
       $driveLetter = $windowsPath.Substring(0,1).ToLower()
       $wslPath = $windowsPath -replace "^[A-Za-z]:", "/mnt/$driveLetter" -replace "\\", "/"

       Write-Host "Windows Path: $windowsPath"
       Write-Host "WSL Path: $wslPath"
       Write-Host "Running TTS conversion..."

       # Use the venv's Python binary directly
       wsl /home/chan/projects/coqui-tts/venv/bin/python /home/chan/projects/coqui-tts/convert_md_to_mp3.py "$wslPath"
       $exitCode = $LASTEXITCODE

       if ($exitCode -ne 0) {
           throw "TTS script exited with code $exitCode"
       }

       Write-Host "`n✅ Done. Check your Downloads folder."
   } catch {
       Write-Host "`n❌ ERROR:"
       Write-Host $_
   }

   # Keep the window open
   Read-Host "`nPress Enter to close"
   ```

2. **Add Registry Entry**

   Create a `.reg` file with the following content and run it to add the context menu entry:

   ```reg
   Windows Registry Editor Version 5.00

   [HKEY_CLASSES_ROOT\.md\shell\ConvertToMP3]
   @="Convert to MP3"

   [HKEY_CLASSES_ROOT\.md\shell\ConvertToMP3\command]
   @="powershell.exe -ExecutionPolicy Bypass -File \"C:\\path\\to\\convert_md_to_mp3.ps1\" \"%1\""
   ```

   Replace `C:\\path\\to\\convert_md_to_mp3.ps1` with the actual path to your PowerShell script.

3. **Usage**

   Right-click on any Markdown file in Windows Explorer and select "Convert to MP3" to run the script. 
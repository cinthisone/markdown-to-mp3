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
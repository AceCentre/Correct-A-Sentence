#Persistent
#SingleInstance, Force
SetTimer, CheckTyping, 100
return

CheckTyping:
    clipboardBackup := ClipboardAll  ; Backup the current clipboard content
    Clipboard := ""  ; Clear the clipboard
    Send, ^c  ; Copy the current selection (ideally the current word/sentence)
    ClipWait, 0.1  ; Wait for the clipboard to contain data
    if (ErrorLevel) {  ; If ClipWait timed out (no data in clipboard)
        Clipboard := clipboardBackup  ; Restore the clipboard
        return
    }
    typedText := Clipboard
    Clipboard := clipboardBackup  ; Restore the clipboard

    wordCount := 0
    if (typedText != "") {
        wordCount := StrSplit(typedText, A_Space A_Tab "`n").Length()  ; Count the words
    }

    if (wordCount >= 7) {
        RunAutoCorrect(typedText)  ; Placeholder for your autocorrect function
    }
return

RunAutoCorrect(typedText) {
    ; Save the current clipboard content to restore later
    clipboardBackup := ClipboardAll

    ; Set the clipboard to the text that needs correction
    Clipboard := typedText

    ; Construct the path to the executable
    exePath := A_LocalAppData . "\AceCentre\CorrectSentence\Client.exe"

    ; Prepare the command to run
    command := """" . exePath . """"

    ; Run the command and capture its output
    RunWait, %ComSpec% /c %command%, , UseErrorLevel, output

    ; Check for errors
    if (ErrorLevel) {
        MsgBox, % "Failed to run the correction client. ErrorLevel: " . ErrorLevel
    } else {
        ; Assuming the executable's output is now in the clipboard, use it
        correctedText := Clipboard

        ; Optionally, display the corrected text for verification
        MsgBox, % "Corrected Text: " . correctedText

        ; Here, you would replace the sentence with `correctedText`
        ; This step depends on how you want to implement the replacement.
        ; It might involve sending keystrokes, manipulating a document, etc.
    }

    ; Restore the original clipboard content
    Clipboard := clipboardBackup
}

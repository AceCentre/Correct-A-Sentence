# CorrectSentence - Desktop

## What this does


We have a client.exe and a correctsentence.exe. The latter is a pipe server which is designed to run continually. At some point in the future we can turn this into a Windows service or system tray app. For now its a pretty ugly command app. You can read the screen messages but it wont tell you much. There should be a log file created.. 

The client.exe is a simple command line app which passes on a string to the server. If no string is passed as a parameter then it will read in the copy buffer. If you dont send the ``--return`` param then it will overwrite the copybuffer with the new string

e.g.

```pwsh
client.exe --return 'Iwantafriend'
> I want a friend
```

## To use with AAC or AT

1. Run the installer. Note it is large and can take a while to install it.
2. Once installed, you should find an example Gridset on your desktop suitable for the Grid. For other software, see below for some basic details
3. When trialling this software, You should run 'correctsentence.exe' and leave the command window open.
4. Open the example Gridset and trial writing using autocorrect on speak.

If you have other software the basic principle is this:

- You need a function to copy your prepared message
- You then need to call the client.exe software. You can find the path to this following the shortcut on your desktop. Or use this ``%LOCALAPPDATA%\CorrectSentence\client\client.exe`
- You then paste the corrected message back to your message bar
- You may need to create a pause or wait command to deal with the time it takes to correct the sentence

## Caveats

- It's English Only, but you may have some luck with German or French and other languages too but this is unested.
- As such, sentences can't be multilingual
- It does require a considerable amount of RAM/CPU to run. Your mileage may vary
- What we would LOVE in return for trialling this

We would love an example of sentences that don't work for you. Ideally, these must be realistic sentences that an AAC user would say or have said.
Please remove any identifiable information.
We would like to share this data more widely and help train a future model to improve correction and prediction
Send us your sentences here: https://forms.office.com/e/FMwMaHA3zP Note it is anonymous. Please remove any identifiable information before submitting

## Developer notes

- We have our t5-small finetuned model turned into a ONNX model using fastT5 library. Its ok - but it really only works on python 3.8.1 

So make a env using that (hint: pip install -U fastT5  - i.e. in the user directory)

Make sure NSIS installed. Off you go. Note there is a fat version which is the _full version. This was built under py 3.11.4


import pydub



sound = pydub.AudioSegment.from_mp3("daft_punk.mp3")
sound.export("daft_punk.wav", format="wav")
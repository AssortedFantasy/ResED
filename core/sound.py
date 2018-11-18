from pydub import AudioSegment
import scipy.io.wavfile

def soundarray(filename):
    # https: // pythonbasics.org / Convert - MP3 - to - WAV /
    # The file opened and the file created
    source = "%s.mp3" % filename
    converted = "%s.wav" % filename

    # Convert mp3 to wav
    sound = AudioSegment.from_mp3(source)
    sound.export(converted, format="wav")

    # Convert to numpy array
    # Gives left channel and right channel
    rate, data = scipy.io.wavfile.read(converted, mmap=False)

    # Average the two channels
    combinechannels = (data[:,1] + data[:,0])/2
    print(combinechannels)
    return rate, combinechannels

# Example run: soundarray("testsound")
# AudioTools.

path = "/Users/alexarse/Desktop/808Samples/kick (14).wav"
# stereo playback with a slight shift between the two channels.
sf = SfPlayer(path, speed=[1, 0.995], loop=False, mul=0.7)

snare_path = "/Users/alexarse/Desktop/808Samples/snare (12).wav"
snare = SfPlayer(snare_path, speed=1, loop=False, mul=0.4);

hat_path = "/Users/alexarse/Desktop/808Samples/hi hat (12).wav";
hihat = SfPlayer(hat_path, speed=1, loop=False, mul=0.4);

def OnKick():
    print("OnKick");
    sf.out();

def OnSnare():
    snare.out();

def OnHihat():
    hihat.out();


















































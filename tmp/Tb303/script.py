# AudioTools.
import ax

metro = Metro(0.125);
adsr = CosTable([(0,0), (100,1), (500,.3), (8191,0)]);
amp = TrigEnv(metro, table=adsr, dur=.25, mul=1.0);

it = Iter(metro, choice=[0]);
it_octave = Iter(metro, choice=[0]);
hz = MToF(it + it_octave * 12);

tuning_sig = Sig(value=1.0);

a = SuperSaw(freq=hz * tuning_sig, detune=0.2, mul=amp * 0.5);

filter_freq = Sig(value=5000);
filter_env_amnt = Sig(value=0);
filter = MoogLP(a, freq=filter_freq + filter_env_amnt * filter_freq * amp, res=1.25).out();

led_list = ["C0", "Cs0", "D0", "Ds0", "E0", "F0", "Fs0", "G0", "Gs0", "A0", "As0", "B0", "C1"];

note_dict = {"C0" : 60,
             "Cs0": 61,
             "D0" : 62,
             "Ds0": 63, 
             "E0" : 64,
             "F0" : 65,
             "Fs0": 66,
             "G0" : 67,
             "Gs0": 68,
             "A0" : 69,
             "As0": 70,
             "B0" : 71,
             "C1" : 72};

def GetKeyFromNote(note):
    return note_dict.keys()[note_dict.values().index(note)];

note_data = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60];
octe_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

def GetBeatIndex():
    w = widgets.Get("beat_number");
    return int(w.GetValue()) - 1;

def OnStartStop(msg):
    led = widgets.Get("play_pause_led");

    if(metro.isPlaying()):
        led.SetIndex(0);
        metro.stop();

    else:
        led.SetIndex(1);
        metro.play();

def SetBeatIndex(index):
    # Turn off all leds.
    for led in led_list:
        widgets.Get(led).SetIndex(0);

    # Turn on note led.
    led = widgets.Get(GetKeyFromNote(note_data[index]));
    led.SetIndex(1);

    # Change number box value.
    num_box = widgets.Get("beat_number");
    num_box.SetValue(float(index + 1));

    # Turn on oct led.
    SetOctave(octe_data[index]);
    

def OnNoteButton(msg):
    # Turn off all note leds.
    for led in led_list:
        widgets.Get(led).SetIndex(0);
    
    # Turn on selected note led.
    widgets.Get(msg).SetIndex(1);

    # Update note data.
    note_data[GetBeatIndex()] = note_dict[msg];
    it.setChoice(note_data);

def SetOctave(oct_value):
    low_led = widgets.Get("oct_low_led");
    high_led = widgets.Get("oct_high_led");

    low_led.SetIndex(0);
    high_led.SetIndex(0);

    if(oct_value == -1):
        low_led.SetIndex(1);
        octe_data[GetBeatIndex()] = -1;
    elif(oct_value == 1):
        high_led.SetIndex(1);
        octe_data[GetBeatIndex()] = 1;
    else:
        octe_data[GetBeatIndex()] = 0;

    it_octave.setChoice(octe_data);

def OnOctLowButton(msg):
    if(octe_data[GetBeatIndex()] == 1):
        SetOctave(0);
    else:
        SetOctave(-1);

def OnOctHighButton(msg):
    if(octe_data[GetBeatIndex()] == -1):
        SetOctave(0);
    else:
        SetOctave(1);
    
def OnNext(msg):
    nbox = widgets.Get("beat_number");
    n = int(nbox.GetValue());
    n = n + 1;

    if(n == 17):
        n = 1;

    SetBeatIndex(n - 1);

def OnBack(msg):
    nbox = widgets.Get("beat_number");
    n = int(nbox.GetValue());
    n = n - 1;
    
    if(n == 0):
        n = 16;

    SetBeatIndex(n - 1);

def OnBeatNumber(value):
    SetBeatIndex(int(value) - 1);

def OnTuning(value):
    v = 1.0;

    if(value < 0.5):
        v = value + 0.5;
    elif(value > 0.5):
        v = value * 2.0;       

    tuning_sig.setValue(v);

def OnDetune(value):
    a.setDetune(value);

def OnVolume(value):
    filter.setMul(value);

def OnTempo(value):
    metro.setTime(0.05 + 0.2 * value);

def OnDecay(value):
    decay = 2000.0 + value * 8000.0;
    adsr.replace([(0,0), (100,1), (1000,.25), (int(decay),0)]);

def OnEnvMod(value):
    filter_env_amnt.setValue(value);

def OnCutoffFreq(value):
    f = 300.0 + 10000.0 * value;
    filter_freq.setValue(f);

def OnResonance(value):
    r = 0.3 * 5.0 * value;
    filter.setRes(r);

# Init gui.
widgets.Get("tempo_knob").SetValue(0.5);
widgets.Get("volume_knob").SetValue(0.5);
widgets.Get("saw_tune_knob").SetValue(0.5);
widgets.Get("tuning_btn").SetValue(0.5);
widgets.Get("filter_freq_knob").SetValue(0.5);
widgets.Get("filter_res_knob").SetValue(0.25);
widgets.Get("env_mod_knob").SetValue(0.0);
widgets.Get("decay_knob").SetValue(0.5);
widgets.Get("play_pause_led").SetIndex(0);

SetBeatIndex(0);
it.setChoice(note_data);
it_octave.setChoice(octe_data);




























































































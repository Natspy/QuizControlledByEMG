from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
import numpy as np
amps = TmsiCppAmplifier.get_available_amplifiers('usb')
amp = TmsiCppAmplifier(amps[0])

amp.sampling_rate = 512

amp.start_sampling()
gains = np.array(amp.current_description.channel_gains)
offsets = np.array(amp.current_description.channel_offsets)


def samples_to_microvolts(samples):  # z jednostek wzmacniacza do mikrowoltów
    return samples * gains + offsets


while True:
    # 16 próbek w pakiecie, nieodebrane próbki się bufurują i można odebrać je później
    packet = amp.get_samples(16)
    print(samples_to_microvolts(packet.samples))
    print(packet.ts[0])
    print(packet.samples.shape, amp.current_description.channel_names)

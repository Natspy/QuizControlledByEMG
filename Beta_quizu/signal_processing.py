import numpy as np
import time
from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier
from multiprocessing.sharedctypes import Array


class AmplifierConnection:
    """
    Connection to an amplifier

    The purpose of this class is to communicate
    with a signal amplifier.

    Args:
        sampling_rate - frequency of samples in 1 second

    Example of usage (when you want to get samples):
        1. Create class instance in your code, for example:
            amp_conecction = AmplifierConnection(512)
        2. To get samples:
            packet = amp_conecction._amp_conecction.amp.get_samples(buf_len)
            (buf_len - number of samples)
        3. Convert to microvolts:
            samples = amp_conecction.samples_to_microvolts(packet.samples)

    """

    def __init__(self, sampling_rate=512):
        amps = TmsiCppAmplifier.get_available_amplifiers('usb')
        if not amps:
            raise ValueError("Nie ma wzmacniacza")

        self.__amp = TmsiCppAmplifier(amps[0])
        self.__amp.sampling_rate = sampling_rate

        self.__gains = np.array(self.__amp.current_description.channel_gains)
        self.__offsets = np.array(self.__amp.current_description.channel_offsets)

    def samples_to_microvolts(self, samples):
        return samples * self.__gains + self.__offsets

    @property
    def amp(self):
        return self.__amp


class SignalProcess:
    """
    EMG signal processing class
    """
    _SAMPLING_RATE = 512

    _CH_LIST = [0, 1, 2, 4]
    _CALIBRATION_BOOST = 1.5

    def __init__(self, buf_len=128):
        self._amp_connection = AmplifierConnection(self._SAMPLING_RATE)
        self._buf_len = buf_len

    def start(self, process_lock, left_hand_sig, right_hand_sig):
        amp = self._amp_connection.amp
        amp.start_sampling()
        time.sleep(1)
        while True:
            try:
                packet = amp.get_samples(self._buf_len)
                samples = self._amp_connection.samples_to_microvolts(packet.samples)
                left_hand = samples[:, self._CH_LIST[0]] - samples[:, self._CH_LIST[1]]
                right_hand = samples[:, self._CH_LIST[0]] - samples[:, self._CH_LIST[1]]
                with process_lock:
                    left_hand_sig[:-self._buf_len] = left_hand_sig[self._buf_len:]
                    left_hand_sig[-self._buf_len:] = Array('d', left_hand)
                    right_hand_sig[:-self._buf_len] = right_hand_sig[self._buf_len:]
                    right_hand_sig[-self._buf_len:] = Array('d', right_hand)

            except Exception as e:
                print(e)

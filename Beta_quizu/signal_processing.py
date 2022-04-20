import numpy as np
from obci_cpp_amplifiers.amplifiers import TmsiCppAmplifier


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
        self.__amp = TmsiCppAmplifier(amps[0])

        self.__amp.sampling_rate = sampling_rate

        self.__amp.start_sampling()
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

    By the __call__ method you will get the RMS value
    of the selected hand in the method argument.

    Example of usage:
        1. Create class instance in your code, for example:
            signal_processing = SignalProcess()

        2. To calibrate muscle "squeeze" threshold:
            signal_processing.calibration(time, ch1, ch2)
                time - calibration time in seconds
                ch1, ch2 - idx of channels from self._CH_LIST
                    - 0, 1 for left hand
                    - 2, 3 for right hand

        3. To get RMS of selected hand:
            signal_processing("left")
        or
            signal_processing("right")
    """
    _SAMPLING_RATE = 512
    _BUF_LEN = 128
    _CH_LIST = [0, 1, 2, 3]
    _CALIBRATION_BOOST = 1.5

    def __init__(self):
        self._amp_conecction = AmplifierConnection(self._SAMPLING_RATE)

    def __call__(self, hand):
        packet = self._amp_conecction.amp.get_samples(self._BUF_LEN)
        samples = self._amp_conecction.samples_to_microvolts(packet.samples)

        if hand == "left":
            hand_sig = samples[:, self._CH_LIST[0]] - samples[:, self._CH_LIST[1]]
        elif hand == "right":
            hand_sig = samples[:, self._CH_LIST[2]] - samples[:, self._CH_LIST[3]]
        else:
            # TODO może wyrzucić jakiś wyjątek?
            hand_sig = 0

        norm_sig = hand_sig - np.mean(hand_sig)
        rms = np.sqrt(np.sum(norm_sig ** 2))
        return rms

    def calibration(self, calibration_time, ch_1, ch_2):

        collect_rms = np.zeros(int(calibration_time * self._SAMPLING_RATE / self._BUF_LEN))
        for i in range(int(calibration_time * self._SAMPLING_RATE / self._BUF_LEN)):
            packet = self._amp_conecction.amp.get_samples(self._BUF_LEN)
            hand_sig = self._amp_conecction.samples_to_microvolts(packet.samples)

            diff_sig = hand_sig[:, ch_1] - hand_sig[:, ch_2]
            norm_sig = diff_sig - np.mean(diff_sig)

            collect_rms[i] = np.sqrt(np.sum(norm_sig ** 2))
        return np.mean(collect_rms) * self._CALIBRATION_BOOST

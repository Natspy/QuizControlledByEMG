# instalacja:
sudo dpkg -i tmsi-dkms*.deb
sudo apt-get install python3-pip
sudo pip3 install wheel
sudo pip3 install obci_utils-2.7.0+6.g87e3397-py3-none-any.whl
sudo pip3 install obci-2.7.0+6.g87e3397-py2.py3-none-any.whl

# w zależności od wersji pythona:
sudo pip3 install obci_cpp_amplifiers-2.6.0.post14+g0e3d385-cp36-cp36m-linux_x86_64.whl
#lub
sudo pip3 install obci_cpp_amplifiers-2.6.0.post14+g0e3d385-cp35-cp35m-linux_x86_64.whl

# example.py - przykład odbierania próbek

import pygame as py
import numpy as np
import random, json

py.init()
py.mixer.init()

# Load your footstep sound



class Soundhandler:
    def __init__(self) -> None:
        with open("settings.json", "r") as file:
            settings = json.load(file)

        self.footstep_sound:py.mixer.Sound = py.mixer.Sound('lyder/footstep.mp3')
        self.volume:float = (settings["volume"]/100)*0.6


    @staticmethod
    def change_pitch(sound, pitch:float=1.0) -> py.mixer.Sound:
        #Leser lyden
        sound_array = py.sndarray.array(sound)

        # Sjekker om lyden er stereo. Må da håndtere begge kanalene
        if sound_array.ndim == 2:
            # Lagrer den nye lyden i en ny array
            resampled_array = np.zeros((int(sound_array.shape[0] / pitch), sound_array.shape[1]), dtype=sound_array.dtype)


            for channel in range(sound_array.shape[1]):
                resampled_array[:, channel] = np.interp(
                    np.linspace(0, sound_array.shape[0], resampled_array.shape[0]),
                    np.arange(sound_array.shape[0]),
                    sound_array[:, channel]
                )
        else:
            resampled_array = np.interp(
                np.linspace(0, len(sound_array), int(len(sound_array) / pitch)),
                np.arange(len(sound_array)),
                sound_array
            ).astype(sound_array.dtype)

        #Lager nytt lydobjekt
        return py.sndarray.make_sound(resampled_array)


    def play_footstep_with_random_pitch(self) -> None:
        #Velger en random pitch mellom 0.8 og 1.2
        random_pitch = random.uniform(0.8, 1.2)

        #Lager nypitchet lyd
        pitched_sound = self.change_pitch(self.footstep_sound, random_pitch)

        #Spiller av lyden
        pitched_sound.set_volume(self.volume)
        pitched_sound.play()


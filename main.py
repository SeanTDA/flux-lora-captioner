import os
import tkinter as tk
from tkinter import filedialog
import base64
import requests

import keys


OPEN_API_KEY = keys.OPEN_API_KEY
print(OPEN_API_KEY)

PROMPT_INTRO = """
A Flux prompt is a 100-200 word descriptive caption that includes the following details:

- Media type e.g. "A CG render of" / "This is a DSLR photography of.." / "This is an illustration of.."
- Angle e.g. "a low angle" / "a wide shot" / "a closeup selfie"
- Trigger word e.g. "A photo of <TRIGGER_WORD>"
- Outfit e.g. "They are wearing a black top hat with a tuxedo"
- Facial Expression e.g. "<TRIGGER_WORD> has a huge grin and is looking happily directly at the camera"
- Body Expression/Action e.g. "They have their arms outstretched and is leaning off to the side while running and holding a red book."
- Environment e.g. "The background is a sunny blurred beach with a park on the side with a sign above that reads Parkland Beaches."
- Lighting e.g. "<TRIGGER_WORD> is basked in dappled lighting, with a harsh shadow across the left side of their face."

Here are some examples of Flux prompts:

An upper body portrait shot of JaimeStevens with short white hair and round, black-framed glasses. He wears a light-colored plaid shirt underneath a beige jacket, giving off a relaxed, casual look. His expression is one of surprise or engagement as he looks slightly to the side, mid-conversation. The background shows an indoor setting, with soft daylight filtering through a window with blinds, creating a calm atmosphere. A colorful piece of art featuring flowers and birds can be seen in the blurred background, adding a touch of warmth to the scene. The composition highlights Harold's upper body, focusing on his attentive expression.

RooRoo is standing with a wide smile on her face, pointing enthusiastically with her left arm extended forward. Her ears are perked up, and her expression is one of excitement and joy, as if she has spotted something fun or interesting. Her tail is balanced behind her, indicating a dynamic and engaged pose. The background shows an indoor environment, complete with home decor elements, enhancing the sense of a playful moment within a cozy setting. This scene captures RooRoo's lively and joyful personality.

The image is a selfie of DanSmith wearing a leather shirt. He is standing on a street in front of a brick building with a sign that reads Cards Galore. He is wearing a black leather jacket and has a serious expression on his face. The street is lined with other buildings and there are cars parked on the side of the road. The sky is overcast and the overall mood of the image is casual and relaxed.

MaxTheFly, dressed in a dirty white tuxedo and a stained top hat, exuding a sinister aura. His body leans forward slightly, as if preparing to strike or scheme, with his wings visible in the background, tattered and torn. Max's large green eyes are narrowed into an evil stare, casting a chilling and menacing expression. His crooked smile adds to the dark, mischievous vibe, while his thick eyebrows are arched menacingly. The lighting casts dramatic shadows across his face and body, emphasizing his sinister nature. The dirty top hat, tilted at an angle, adds to his disheveled yet devious look. The background is dimly lit, with cool blue tones creating a mysterious and shadowy environment that contrasts with the harsh light reflecting off Max’s outfit, further highlighting his unsettling presence. The full-body composition showcases Louie’s small, wiry stature while focusing on his intense expression and scheming posture, giving the scene a sense of malevolence and cunning

The image captures Bonez, a breakdancer known for her agility and precision, in the midst of a dynamic move. With one hand touching the ground and her body angled to the side, she showcases her balance and control. Clad in the European breakdancing uniform, featuring intricate red and blue patterns, she embodies national pride and the spirit of competition. Her focused expression and fluid motion convey both skill and confidence. The event's backdrop, with blurred figures observing her performance, highlights the significance of the moment, placing Bonez at the center of this electrifying scene.

Please write a Flux prompt for the image attached.
"""




# Ensure the dialgoue replaces <TRIGGER_WORD> with
# TODO: First pass correction : give hints e.g. Anything to ignore



def rename_image_files(folder_path):
    # List of valid image file extensions
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    
    # Counter for renaming
    counter = 1

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Get file extension
        file_extension = os.path.splitext(filename)[1].lower()

        # Check if the file has a valid image extension
        if file_extension in valid_extensions:
            # Construct the new filename with the counter
            new_filename = f"{counter}{file_extension}"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_file_path, new_file_path)
            
            print(f"Renamed {filename} to {new_filename}")
            counter += 1



def process_images(folder):
    if not folder:
        print("No folder selected.")
        return

    print("--- FLUX LORA CAPTIONER ---\n")

    # Step 1. Get information
    print("What is the trigger word?")
    print("e.g. JohnSmith / DaveTheDog")
    trigger_word = input("> ")

    # Step 2. Rename images to sequential numbers
    print("")
    rename_image_files(folder)


    





# Initialize Tkinter and hide the root window
root = tk.Tk()
root.withdraw()

# Open a dialog box to select a folder
folder = filedialog.askdirectory(title="Select Folder")

process_images(folder)

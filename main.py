import os
import tkinter as tk
from tkinter import filedialog
import base64
import requests
import keys
from PIL import Image
import matplotlib.pyplot as plt
import shutil


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')






API_OPEN_AI = keys.OPEN_API_KEY

PROMPT_INTRO = """
A Flux prompt is a 100-200 word descriptive caption that includes the following details:

- Media type e.g. "A CG render of" / "This is a DSLR photography of.." / "This is an illustration of.."
- Angle e.g. "a low angle" / "a wide shot" / "a closeup selfie"
- Composition e.g. "<TRIGGER_WORD> is cropped in the center of the frame, tilted slightly"
- Trigger word e.g. "A photo of <TRIGGER_WORD>"
- Outfit e.g. "They are wearing a black top hat with a tuxedo"
- Facial Expression e.g. "<TRIGGER_WORD> has a huge grin and is looking happily directly at the camera"
- Body Expression/Action e.g. "They have their arms outstretched and is leaning off to the side while running and holding a red book."
- Environment e.g. "The background is a sunny blurred beach with a park on the side with a sign above that reads Parkland Beaches."
- Lighting e.g. "<TRIGGER_WORD> is basked in dappled lighting, with a harsh shadow across the left side of their face."

You should refer to the <CHARACTER_TYPE> character in the image as <TRIGGER_WORD>.

Here are some examples of Flux prompts:

An upper body portrait shot of JaimeStevens with short white hair and round, black-framed glasses. He wears a light-colored plaid shirt underneath a beige jacket, giving off a relaxed, casual look. His expression is one of surprise or engagement as he looks slightly to the side, mid-conversation. The background shows an indoor setting, with soft daylight filtering through a window with blinds, creating a calm atmosphere. A colorful piece of art featuring flowers and birds can be seen in the blurred background, adding a touch of warmth to the scene. The composition highlights Harold's upper body, focusing on his attentive expression.
RooRoo is standing with a wide smile on her face, pointing enthusiastically with her left arm extended forward. Her ears are perked up, and her expression is one of excitement and joy, as if she has spotted something fun or interesting. Her tail is balanced behind her, indicating a dynamic and engaged pose. The background shows an indoor environment, complete with home decor elements, enhancing the sense of a playful moment within a cozy setting. This scene captures RooRoo's lively and joyful personality.
The image is a selfie of DanSmith wearing a leather shirt. He is standing on a street in front of a brick building with a sign that reads Cards Galore. He is wearing a black leather jacket and has a serious expression on his face. The street is lined with other buildings and there are cars parked on the side of the road. The sky is overcast and the overall mood of the image is casual and relaxed.
MaxTheFly, dressed in a dirty white tuxedo and a stained top hat, exuding a sinister aura. His body leans forward slightly, as if preparing to strike or scheme, with his wings visible in the background, tattered and torn. Max's large green eyes are narrowed into an evil stare, casting a chilling and menacing expression. His crooked smile adds to the dark, mischievous vibe, while his thick eyebrows are arched menacingly. The lighting casts dramatic shadows across his face and body, emphasizing his sinister nature. The dirty top hat, tilted at an angle, adds to his disheveled yet devious look. The background is dimly lit, with cool blue tones creating a mysterious and shadowy environment that contrasts with the harsh light reflecting off Max’s outfit, further highlighting his unsettling presence. The full-body composition showcases Louie’s small, wiry stature while focusing on his intense expression and scheming posture, giving the scene a sense of malevolence and cunning
The image captures Bonez, a breakdancer known for her agility and precision, in the midst of a dynamic move. With one hand touching the ground and her body angled to the side, she showcases her balance and control. Clad in the European breakdancing uniform, featuring intricate red and blue patterns, she embodies national pride and the spirit of competition. Her focused expression and fluid motion convey both skill and confidence. The event's backdrop, with blurred figures observing her performance, highlights the significance of the moment, placing Bonez at the center of this electrifying scene.

Please write a Flux prompt for the image attached, referring to the <CHARACTER_TYPE> as <TRIGGER_WORD>.
"""

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

IMAGES_TO_FINETUNE = [1,2,3] # Which images to finetune the captions for

def send_openai_request(text_prompt, image_prompt_path):
    image_prompt_base64 = encode_image(image_prompt_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {API_OPEN_AI}"
    }

    payload = {
        "model": "gpt-4-turbo",#"gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text_prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_prompt_base64}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json = response.json()
    response_content = response_json['choices'][0]['message']['content']

    return response_content



def is_valid_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)



def save_caption(file_counter, folder, caption):
    # Construct the file path with the sequential number and .txt extension
    caption_filename = os.path.join(folder, f"{file_counter}.txt")
    # Write the caption to the file
    sanitised_caption = caption.replace("'", "").replace('"', "")
    with open(caption_filename, 'w', encoding='utf-8') as f:
        f.write(sanitised_caption)
    print(f"Saved caption as {caption_filename}")

def rename_image_files(folder_path, train_folder_path):
    # Counter for renaming
    counter = 1

    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Get file extension
        file_extension = os.path.splitext(filename)[1].lower()

        # Check if the file has a valid image extension
        if  is_valid_image_file(filename):
            # Construct the new filename with the counter
            new_filename = f"{counter}{file_extension}"
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(train_folder_path, new_filename)
            
            # Rename the file
            shutil.copy(old_file_path, new_file_path)
            
            print(f"Renamed {filename} to {new_filename}")
            counter += 1

def convert_images_to_png(folder_path):
    # Iterate through each file in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a valid image
        if is_valid_image_file(filename):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Open the image
            with Image.open(file_path) as img:
                # Convert to RGB mode if necessary (to avoid issues with palette images like GIF)
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")

                # Define the new filename with .png extension
                new_filename = os.path.splitext(filename)[0] + ".png"
                new_file_path = os.path.join(folder_path, new_filename)

                # Save the image as PNG
                img.save(new_file_path, "PNG")

                print(f"Converted {filename} to {new_filename}")

                # Optionally, you can remove the original file after converting
                if new_file_path != file_path:
                    os.remove(file_path)


def process_images(folder):
    if not folder:
        print("No folder selected.")
        return

    print("--- FLUX LORA CAPTIONER ---")

    # Step 1. Get information
    print("\nWhat is the trigger word?")
    print("e.g. JohnSmith / DaveTheDog")
    trigger_word = input("> ")

    print("\nWhat is the character type?")
    print("e.g. Human / Toy / Animal")
    character_type = input("> ")

    # Step 2. Rename images to sequential numbers
    print("")
    train_folder_path = os.path.join(folder, "train")
    if not os.path.exists(train_folder_path):
        os.makedirs(train_folder_path)
    print("test")
        
    rename_image_files(folder, train_folder_path)

    # Step 3. Convert all images to PNG
    convert_images_to_png(train_folder_path)

    # Prepare the intro prompt
    prompt_modified = PROMPT_INTRO
    prompt_modified = prompt_modified.replace("<TRIGGER_WORD>",trigger_word)
    prompt_modified = prompt_modified.replace("<CHARACTER_TYPE>",character_type)

    edit_requests = ""

    # Iterate through files
    file_counter = 1
    while True:
        filename = str(file_counter) + ".png"

        # Skip non image files
        if not is_valid_image_file(filename):
            continue

        file_path = os.path.join(train_folder_path, filename)

        # Open and display the image
        image = Image.open(file_path)
        plt.imshow(image)
        plt.axis('off')  # Turn off axis labels
        plt.draw()
        plt.pause(0.001)  # Small pause to allow the image to be displayed

        # Rerun GPT Captioning until user accepts it
        caption_accepted = False
        gpt_caption = ""
        while not caption_accepted:

            print("\nGenerating Caption.. Please Wait..")
            text_prompt = prompt_modified + ("\n" + edit_requests if edit_requests != "" else "")
            gpt_caption = send_openai_request(text_prompt=text_prompt, image_prompt_path=file_path)

            print("\n-------> " + filename + ":")
            if edit_requests != "":
                print(edit_requests)
            print("\nGPT Caption: " + gpt_caption)

            # Edit Requests for Image 1 and 2
            if file_counter in IMAGES_TO_FINETUNE:

                # Edit Requests
                print("\nAny Edit Requests?")
                print("[Blank] = Accepted")
                input_edit_request = input("> ")

                if input_edit_request == "":
                    caption_accepted = True
                else:
                    caption_accepted = False
                    if edit_requests == "":
                        edit_requests = "Special Requests:"
                    edit_requests += "\n- "+input_edit_request
            else:
                caption_accepted = True

        # Close the image window before moving on to the next one
        plt.close()

        # Save Caption
        print("\nCaption Accepted")
        save_caption(file_counter, train_folder_path, gpt_caption)

        # Increment file counter
        file_counter += 1
    

# Initialize Tkinter and hide the root window
root = tk.Tk()
root.withdraw()

# Open a dialog box to select a folder
folder = filedialog.askdirectory(title="Select Folder")

process_images(folder)

# TODO: Ensure it encodes to utf8

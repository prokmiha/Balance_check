# The code creates a web driver that checks which mnemonic phrases are valid
# and collects them into a separate text file for further use.

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

filename = "Correct_phrases.txt"

try:
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://iancoleman.io/bip39/#english")
except Exception as e:
    print(e)

with open("Seed_phrases.txt", "r") as f:
    # Read the words from the file and store them in a list
    words = f.read().strip().splitlines()

# Find the input field on the webpage
input_field = driver.find_element('id', 'phrase')

if os.path.exists(filename):
    with open(filename, "r") as f:
        # Read the existing successful words from the file and store them in a set
        success_words = set(f.read().strip().splitlines())
else:
    success_words = set()

# Initialize a progress bar with the total number of words
progress_bar = tqdm(total=len(words), unit="word(s)")

# The specified number is used to limit the number of checks at once, but it can be removed.
for word in words[:1000]:
    # Clear the input field
    input_field.clear()
    # Enter the current word into the input field
    input_field.send_keys(word)
    # Simulate pressing the Enter key
    input_field.send_keys(Keys.ENTER)

    time.sleep(0.5)

    # Find the feedback element on the page
    feedback = driver.find_element(By.CSS_SELECTOR, ".feedback")
    if feedback.text != "Invalid mnemonic" or feedback.text == '':
        # If the feedback is not "Invalid mnemonic" or empty, the word is valid
        print(f"Valid: {word}")
        # Add the word to the set of successful words
        success_words.add(word)

    # Update the progress bar by one unit
    progress_bar.update(1)

# Close the progress bar
progress_bar.close()

with open(filename, "a") as f:
    try:
        # Write the successful words to the file
        f.write('\n'.join(success_words) + '\n')
    except Exception as e:
        print(e)
        print("Error writing to the file")

# Quit the WebDriver
driver.quit()

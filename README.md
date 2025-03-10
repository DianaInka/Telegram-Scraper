# Telegram-Scraper
Telegram Movie Links Scraper using Selenium

Note: 
Get you default chrome path [ where you have logged in, in chrome! ] 

Get the "Profile Path by pasting this link on the chrome browser you are logged in : chrome://version/

Default “profile path” of chrome[ Example : /home/diana/.config/google-chrome/Profile 1]

--->Process of running this : 
Start Chrome manually with Profile 1 [terminal 1] :

paste this in terminal 1 :- google-chrome --remote-debugging-port=9222 --user-data-dir="/home/diana/.config/google-chrome" --profile-directory="Profile 1"

Keep this terminal open so Selenium can connect to the session. [Remember this command is running in terminal 1] 
This connects Selenium to an already running Chrome instance with remote debugging enabled on port 9222.

Run your script in a separate terminal: [terminal 2]
python3 Telegram_Channel_Scraper.py




----> Install Chrome & ChromeDriver
---->  Install Required Python Libraries:
pip install selenium pyperclip
selenium → Used for web automation
pyperclip → Used to handle clipboard operations



---
Code1 [Telegram Channel Scraper]- Automating the process of extracting a Telegram message/post links using Selenium


---What the code1 does:
Extracts both "Copy Message Link" and "Copy Text".

Uses the scroll-up function to load older messages.

Ensures at least 10 messages are processed.

Scrapes multiple Channels  

Saves the data [ including the id of the links, and not just the text ] to txt file . Saves Extracted Messages to a File


---

---
Code2 [Telegram movie Channel Scraper]- Automating the process of extracting  Telegram channels after the user provides the movie name using Selenium

---What the code1 does:
Chrome WebDriver connected in debugger mode.

Opened Telegram Web.

Clicked on the Telegram search bar.

Clicked on the 'Channels' tab.

Enter the movie name to search: interstellar

Pasted movie name: interstellar

clicked on "show more"

grabbing channel names from the suggested channel items and pasted on terminal


---

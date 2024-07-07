# Before Use
Before you are able to use the program, you need to decide whether or not to set up a Google API project. This will allow you to automatically upload files to YouTube, without having to manually upload the videos. It is recommended but not required.
## Setting up a project
Follow [this](https://console.cloud.google.com/projectcreate) link to set up a Google API project. Create a project name and click create.
On the left side click on `APIs & Services` and then `Enabled APIs & Services`.
Click the button that says `Enable APIs and Services` and then search for `YouTube Data API v3`. Enable this API.
Navigate back to the main page and click on `OAuth Consent Screen`. Select external and click create. Fill out the information (since the app is going to be in test mode the entire time, this information doesn't really matter). Click continue on the scopes screen. Add a test user with an email account that you create (create a new account since there is a good chance the account will get banned or blocked). Finish setting up the app. Now go to the `Credentials` tab. Click on `Create Credentials` at the top and create a new OAuth client ID. You can leave all of the default information. Back on the credentials page, download the `client_secrets.json` file on the right hand side. Add this to the directory that you downloaded from the releases page.
## Use without a project
If you are using the code without a Google API project, then you need to comment out or delete some code. In `encoder.py` comment out or delete lines 94-133, 147-151, and 154. After the code is finished running, upload the video and delete it afterwards.
# Use
## Uploading Files
Download the latest release of the code from the releases tab. Run `encoder.py` using an IDE or from command prompt.
> If using command prompt, open the location where you downloaded the file in file explorer, then in the top type `cmd`. This will open the command prompt. From there type `python encoder.py`.

Ensure that the file you are wanting to upload is in the same directory as `encoder.py`. Input the path to file, including the file extension, along with an fps value.
> When deciding what fps value to use, it is recommended to use a low value for short files so that YouTube still processes the video.

If you are using a Google API project, then click on the link that is generated and enter the security key into the console. The video will then finish uploading. If you are not using a Google API project, simply download the file `final_video.mp4` and upload it to YouTube manually. All unnecessary files will be deleted afterwards.
**Ensure that you save the ID of the video after you have uploaded it, as you will need it to download the file.**
## Downloading Files
Download the latest release of the code from the releases tab if you haven't already. Run `decoder.py` using an IDE or from command prompt.
> If using command prompt, open the location where you downloaded the file in file explorer, then in the top type `cmd`. This will open the command prompt. From there type `python decoder.py`.

When prompted, enter the ID to the video you are wanting to download, along with an output path for the file. It will then automatically download and decode the file from YouTube. All unnecessary files will be deleted afterwards.
# Disclaimer
This is not how YouTube is intended to be used, and it is not how the video format is intended to be used. Due to YouTube and other video compression, the process to upload and download files is quite slow, making this impractical for file storage. Not only that, but videos can get deleted, meaning you lose the file. This also probably violated the YouTube TOS in some way, so your account will likely be banned. If you choose to upload files to YouTube using this, I cannot guarantee that they will not become corrupted or innacurrate. 
# Miscellaneous 
All videos are default set to unlisted, but this can be changed on line 149 of `encoder.py`. Just change unlisted to private or public. **Note that if you make the video public, anyone can access and download the file, even if they don't have access to the decoder.** 

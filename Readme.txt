== MEMRISE AUDIO UPLOADER V 1.1 ==

At the moment, the uploader only supports the following languages:

  Mandarin Chinese (Simplified)

Support for more languages may be added in the future.

--INSTALLATION--

1. Install any version of Python 3
    https://www.python.org/

-Easy way-

2. Set python.exe as the default program for .py files

3. Double click 'interface.py'

-CMD/Terminal way-

2. Navigate to the Memrise Uploader folder like this:

    cd <folder address>
    Example:
      cd C:\Memrise-Audio-Uploader-master\

3. Run the program like this:

    python interface.py

    If it doesn't work, try:
    python3 interface.py

--USAGE--

1. Copy paste your Memrise Cookie. 
How to get the cookie:
- Sign in to Memrise in your browser
- Open Developer Console (ctrl+shift+i)
- Reload the dashboard page
- Go to 'network' tab in developer console and click the file named 'dashboard'. 
- Click on Headers. Then you will see "Cookie" under "Request Headers"

2. Copy paste the Database URL
    Example: https://www.memrise.com/course/5540383/hsk-level-6-definitive-edition/edit/database/6560460/
  (!) Make sure it is not the Levels URL
  (!) Make sure there are no pages at the end of the URL like "?page=2"

3. Enter the exact name of the column containing the words for which the audio
   is required

4. Enter the exact name of the column containing the audio

5. Click 'Start'. When prompted, enter the page range you wish to process and
   monitor the upload progress in the CMD/Terminal window

Enjoy!

--KNOWN ISSUES--

- Does not work well with databases that have 1000+ items (Memrise refuses to update the Audio fields through this method). Splitting larger databases into several smaller ones could help. Last tested in the beginning of 2022.

- Deleting the 'audio' folder breaks the script.
  (However, you can safely delete the files inside the folder)

==============================================================================

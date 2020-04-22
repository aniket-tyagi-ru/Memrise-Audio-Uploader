import os
import sys
import subprocess
import re
import time

try:
    import requests
except:
    subprocess.call([sys.executable,'-m','pip','install','requests'])
    import requests

try:
    from bs4 import BeautifulSoup
except:
    subprocess.call([sys.executable,'-m','pip','install','beautifulsoup4'])
    from bs4 import BeautifulSoup

from variables import *

#1

def mem_login(login_data, get_headers = mem_login_get_headers, post_headers = mem_login_post_headers):
    """Memrise auto login"""
    #Start session
    session = requests.Session()
    #GET request to the login page
    response = session.get(login_url, headers = get_headers)
    print("GET: " + str(response.status_code))
    csrftoken = session.cookies.get_dict()['csrftoken']
    #POST request to the login page
    login_data = mem_login_post_data
    login_data['csrfmiddlewaretoken'] = csrftoken
    response = session.post(login_url, data = login_data,
                                    headers = post_headers)
    print("POST: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception("Access Denied")
    return session, response

def mem_database_page(session, url, headers = mem_edit_get_headers):
    """Memrise database page"""
    response = session.get(url, headers = headers)
    print("GET: " + str(response.status_code))
    return session, response

def mem_soupify(response):
    """Apply Beautiful Soup to page"""
    bs_database = BeautifulSoup(response.text, 'html.parser')
    return bs_database

def mem_soupify_table(response, lang_header, aud_header):
    """Apply Beautiful Soup to the database table"""
    bs_database = mem_soupify(response)
    #Table headers
    bs_table = bs_database.find("table", class_ = "table pool-things")
    bs_t_head = bs_table.find("thead")
    bs_t_headers = bs_t_head.find_all("th")
    #Verify Table headers
    proceed, l_col, a_col = mem_verify_table_headers(bs_t_headers, lang_header, aud_header)
    #If table headers don't check out, kill the script
    if proceed != 1:
        print("Stopping...")
        sys.exit()
    #Table rows
    bs_t_body = bs_table.find("tbody", class_ = "things")
    bs_tr = bs_t_body.find_all("tr")
    print("lang_col: " + str(l_col) + "\n aud_col: " + str(a_col))
    print(str(len(bs_tr)) + " rows...")
    return bs_tr, l_col, a_col

def mem_verify_table_headers(headers, lang_header, aud_header):
    """Verifies langauge and audio table header inputs"""
    l_count = 0
    a_count = 0
    for a in range(len(headers)):
        if lang_header in str(headers[a]):
            l_count += 1
            l_col = a
        if aud_header in str(headers[a]):
            a_count += 1
            a_col = a
    x = 1
    #Language
    if l_count < 1:
        print("Could not find: " + lang_header +
                ". Please check your inputs.")
        x = 0
    elif l_count > 1:
        print("Found multiple: " + lang_header +
                ". Please check your inputs.")
        x = 0
    #Audio
    if a_count < 1:
        print("Could not find: " + aud_header +
                ". Please check your inputs.")
        x = 0
    elif a_count > 1:
        print("Found multiple: " + aud_header +
                ". Please check your inputs.")
        x = 0

    return x, l_col, a_col

def mem_last_page_number(database):
    """Returns the number of the last page in the database"""
    #Could change the class filter to make it more general using re.compile
    bs_pagination = database.find("ul", class_ = 'pagination pagination-sm')
    pages = []
    #Could just take the last thing in the list
    for li in bs_pagination.find_all("li"):
        try:
            x = int(li.get_text())
        except:
            continue
        else:
            pages.append(x)
    return max(pages)

def input_page_range(last_page):
    def positive_integer(x):
        try:
            x = int(x)
        except:
            print("Invalid input")
            return 0
        else:
            if x > 0:
                return 1, x
            else:
                print("Invalid input")
                return 0
    pages = [1,1]
    print("Select page range.")
    a = 0
    while a < 2:
        if a == 0:
            message = "First"
            check = 1
        else:
            message = "Last"
            check = pages[0]
        x = input(message + " page: ")
        y, x = positive_integer(x)
        if y == 1:
            if x > last_page:
                print("Out of range. Last page in database is: " + str(last_page))
            elif x >= check:
                pages[a] = x
                a += 1
    return pages

#2

def mem_process_table(session, rows, l_col, a_col, url):
    """Uploads missing audio to memrise database"""
    for row in range(len(rows)):
        bs_td_audio = rows[row].find_all("td")[a_col]
        audio_files = bs_td_audio.find("button").get_text()
        #If row has audio, skip the row
        if "no audio" not in audio_files:
            print("Skip row: " + str(row+1) + "(" + audio_files.replace(" ", "").replace("\n","")[0] + " files)")
            continue
        else:
            bs_td_word = rows[row].find_all("td")[l_col]
            word = bs_td_word.find("div", class_ = "text").get_text()
            print("No audio: " + word)
            #Download word from Baidu
            x = 0
            try:
                x = baidu_query(word)
            except:
                print("Baidu Connection Error")
            if x == 0:
                continue
            else:
                #Reload edit course page
                headers = mem_edit_get_headers
                headers['Referer'] = url
                session, response = mem_database_page(session, url = url, headers = headers)
                #Upload word to memrise
                csrftoken = session.cookies.get_dict()['csrftoken']
                data = mem_audio_post_data
                data["csrfmiddlewaretoken"] = csrftoken
                data["thing_id"] = int(rows[row].get("data-thing-id"))
                data["cell_id"] = a_col
                session = mem_upload_audio(session, data, word)

def baidu_query(word):
    """Queries for 'word' in Baidu and downloads audio"""
    def get_term_header(bs_baidu):
        """Find term header on dictionary page"""
        term_header = bs_baidu.find("div", attrs = {"id": "term-header"} )
        if not term_header:
            term_header = bs_baidu.find("div", attrs = {"id": "word-header"} )
        return term_header

    website = "https://dict.baidu.com"
    url = website + "/s?wd=" + word
    #Get url
    response = requests.get(url, headers = baidu_get_headers)
    bs_baidu = BeautifulSoup(response.text, 'html.parser')
    # Q: Is response an Entry page or Search Results?
    # A: Only Entry page has div with id "term-header" or "word-header"
    term_header = get_term_header(bs_baidu)
    if not term_header:
        print("Search results...")
        #In first search result, if exact match to 'word' is found, proceed
        try:
            bs_search_item = bs_baidu.find("div", attrs = {"class": "poem-list-item"})
            text = bs_search_item.find("a").get_text().replace(" ","").replace("\n","")
            chars = len(word)
            print(str(chars) + " - " + word + " (word)")
            print(str(len(text[:chars])) + " - " + text[:chars] + " (text)")
        except:
            print("Problem with search results")
            return 0
        if text[:chars] == word:
            print("Exact match found.")
            try:
                url = website + bs_search_item.find("a").get("href")
                response = requests.get(url, headers = baidu_get_headers)
                bs_baidu = BeautifulSoup(response.text, 'html.parser')
                term_header = get_term_header(bs_baidu)
            except:
                print("Problem with entry page or URL.")
                return 0
            #Try to download the audio
            return baidu_download(term_header, word)
        #If exact match is not found, return an error
        else:
            print("Exact match not found for: " + word)
            return 0
    else:
        print("Entry found...")
        #Try to download the audio
        return baidu_download(term_header, word)

def baidu_download(term_header, word):
    """Download audio from entry page"""
    try:
        audio_url = term_header.find("a", class_ = re.compile("mp3"))
    except:
        print("Problem with entry page.")
        return 0
    if audio_url is None:
        print("Audio URL not found.")
        return 0
    else:
        try:
            audio_url = audio_url.get("url")
            print("Downloading")
            response = requests.get(audio_url, headers = baidu_get_headers)
            filename = word + ".mp3"
            open(os.path.join(os.path.dirname(__file__), "audio", filename), "wb").write(response.content)
            return 1
        except:
            print("Download error")
            return 0

def mem_upload_audio(session, data, word, headers = mem_audio_post_headers):
    """Upload audio to Memrise (Ajax POST request)"""
    url = "https://www.memrise.com/ajax/thing/cell/upload_file/"
    filename = word + ".mp3"
    file = open(os.path.join(os.path.dirname(__file__),"audio",filename), "rb")
    files = {"f": file}
    print("Uploading: " + filename)
    response = session.post(url, headers = headers, data = data, files = files)
    print("POST: " + str(response.status_code))
    return session

#Main

def main(inputs = []):
    #Assign inputs
    if inputs:
        database_url, lang_header, aud_header = assign_inputs(inputs)
    #Login
    session, response = mem_login(login_data = mem_login_post_data)
    session, response = mem_database_page(session, url = database_url)
    #Get number of database pages
    database = mem_soupify(response)
    last_page = mem_last_page_number(database)
    print("Pages: " + str(last_page))
    #Prompt page range to process
    pages = input_page_range(last_page)
    print("Selected range: " + str(pages[0]) + " - " + str(pages[1]))

    #Process pages
    for page in range(pages[0], pages[1] + 1):
        url = database_url + "?page=" + str(page)
        print("Page " + str(page) + ": " + url)
        #Resoupify for each new page
        session, response = mem_database_page(session, url)
        rows, l_col, a_col = mem_soupify_table(response, lang_header, aud_header)
        #Upload missing audio
        mem_process_table(session, rows, l_col, a_col, url = url)
    print("Finished.")

if __name__ == "__main__":
    main()

#===
#A 403 error means the server does not allow you to go in
#Without browser headers:
#   CSRF verification failed.

#===Contents===
#This file contains:
#1. Headers from the browser
    #Python 'requests' does not provide a Referer header.
    #Adding a Referer header to the request allowed the server to log us in.
    #This website does not care about the User-Agent, but we include it just
    #in case.
    #(A Referer header is the url the user was on before making the current
    #request.)
#2. POST variables

def assign_inputs(inputs):
    mem_login_post_data['username'] = inputs[0]
    mem_login_post_data['password'] = inputs[1]
    database_url = inputs[2]
    lang_header = inputs[3]
    aud_header = inputs[4]
    mem_audio_post_headers['referer'] = database_url
    return database_url, lang_header, aud_header

login_url = "https://app.memrise.com/login/"
database_url = ""
home_url = "https://app.memrise.com/home/"
lang_header = ""
aud_header = ""

#Memrise access
mem_login_get_headers = {
    # "Host":             "www.memrise.com",
    "User-Agent":       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0",
    # "Accept":           "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    # "Accept-Language":  "en-GB,en;q=0.5",
    # "Accept-Encoding":  "gzip, deflate, br",
    # "Referer":          "https://www.memrise.com/",
    # "DNT":              "1",
    # "Connection":       "keep-alive",
    # # "Cookie":           "",
    # "Upgrade-Insecure-Requests": "1",
    # "TE":               "Trailers"
    }

mem_login_post_headers = {
    # "Host": "www.memrise.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    # "Accept-Language": "en-GB,en;q=0.5",
    # "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://app.memrise.com/login/",
    # "Content-Type": "application/x-www-form-urlencoded",
    # "Content-Length": "130",
    # "Origin": "https://www.memrise.com",
    # "DNT": "1",
    # # "Cookie": "",
    # "Connection": "keep-alive",
    # "Upgrade-Insecure-Requests": "1"
    }

mem_login_post_data = {
    "csrfmiddlewaretoken":  "",
    "username":             "",
    "password":             "",
    # "next":                 ""
    }

mem_edit_get_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Referer": home_url
    }

#Audio download
baidu_get_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Referer": "https://dict.baidu.com/"
    }

#Audio upload
mem_audio_post_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:73.0) Gecko/20100101 Firefox/73.0",
    "Referer": database_url
    }

mem_audio_post_data = {
    "thing_id": "",
    "cell_id": "",
    "cell_type": "column",
    "csrfmiddlewaretoken": "",
    }

# mem_audio_post_files = {
#     "f": ""
#     # open('audio.mp3', 'rb')
#     }

#===Info===
#Network requests can include additional information in the form of
#REQUEST HEADERS (and FORM DATA).
#If something is wrong with the data in the headers, the server might not let
#you in.
#This issue could be solved by copying the headers a browser uses for a specific
#url.

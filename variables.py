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
    cookie = inputs[0]
    database_url = inputs[1]
    lang_header = inputs[2]
    aud_header = inputs[3]
    mem_edit_get_headers['cookie'] = cookie
    mem_audio_post_headers['cookie'] = cookie
    mem_audio_post_headers['referer'] = database_url
    return database_url, lang_header, aud_header

#login_url = "https://app.memrise.com/v1.17/auth/access_token/"
database_url = ""
home_url = "https://app.memrise.com/home/"
lang_header = ""
aud_header = ""
cookie = ""

host = "app.memrise.com"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"

mem_edit_get_headers = {
    "User-Agent": user_agent,
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "max-age=0",
    "cookie": cookie,   
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1"
    #"Referer": home_url
    }

#Audio download
baidu_get_headers = {
    "User-Agent": user_agent,
    "Referer": "https://dict.baidu.com/"
    }

#Audio upload
mem_audio_post_headers = {
    #"cache-control": "max-age=0",
    #"sec-fetch-dest": "iframe",
    #"sec-fetch-mode": "navigate",
    #"sec-fetch-site": "same-origin",
    #"sec-gpc": "1",
    "User-Agent": user_agent,
    "Cookie": cookie, 
    "Host": host,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://app.memrise.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Referer": database_url,
    "Upgrade-Insecure-Requests": "1",
    "TE": "Trailers",
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

#Memrise access
# mem_login_get_headers = {
    # "Host":             "www.memrise.com",
    # "User-Agent":       user_agent,
    # "Accept":           "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    # "Accept-Language":  "en-GB,en;q=0.5",
    # "Accept-Encoding":  "gzip, deflate, br",
    # "Referer":          "https://www.memrise.com/app",
    # "DNT":              "1",
    # "Connection":       "keep-alive",
    # # "Cookie":           "",
    # "Upgrade-Insecure-Requests": "1",
    # "TE":               "Trailers"
    # }

# mem_login_get_headers = {
    # "User-Agent":       user_agent,
    # "Referer":          home_url,
    # "cookie":           cookie  
    # }

# mem_login_post_data = {
    # "csrfmiddlewaretoken":  "",
    # "username":             "",
    # "password":             "",
    # "client_id": "",
    # "grant_type": "password",
    # "next":                 ""
    # }

#===Info===
#Network requests can include additional information in the form of
#REQUEST HEADERS (and FORM DATA).
#If something is wrong with the data in the headers, the server might not let
#you in.
#This issue could be solved by copying the headers a browser uses for a specific
#url.

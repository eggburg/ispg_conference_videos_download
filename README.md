# Download ISPG conference videos to current folder

### 1. Extract all the video youtube links from the web page to a text file
./gen_info.py "./lobby_day2.html" "xxxx@xxx.edu" "my_password" > day2_yt_links.txt

### 2. Donwload all the videos from the text file using x2converter
python3 scirpt.py ./day2_yt_links.txt

# Download ISPG conference videos to the current folder

### 1. Extract all the videos links from the web page to a text file (using Day 2 as example)
./gen_info.py "./lobby_day2.html" "xxxx@xxx.edu" "my_password" > day2_yt_links.txt

### 2. Donwload all the videos from the text file using x2converter (using Day 2 as example)
python3 scirpt.py ./day2_yt_links.txt

# Overview
The script extracts the youtube links from the conference pages, and bulk downloads all the videos. 

This tool doesn't use youtube-dl due to its uncertain life cycle. Instead, the downloading is acheived using the online download service x2convert.com via web scraping scripts.

# Instruction

### 1. To extract all the videos links from the website to a text file (using Day 2 as example)
```
python3 gen_info.py conference_websites/lobby_day2.html xxx@xxxxx.edu my_password > yt_links/day2_yt_links.txt
```

### 2. To donwload all the videos from the text file using x2converter (using Day 2 as example)
```
python3 x2convert.py yt_links/day2_yt_links.txt
```

### 3. To find the downloaded mp4 vidoes at ./my_mp4
```
ls my_mp4
```

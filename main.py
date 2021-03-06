#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pip install pytube
# pip install nuitka
# Windows
# pip install pyinstaller pywin32 pywin32-ctypes
# Linux
# pip install altgraph pyinstaller pyinstaller-hooks-contrib
#
# Linux: PyQT5 PyQT5-sip PyQT5-QT PyQT5-QT5 PyQT6 PyQT6-sip PyQT6-QT
# Windows: PyQT5 PyQT5-sip PyQT6 PyQT6-sip
#
# nuitka3 hello.py
# python -m nuitka --mingw64 main.py
#
# pyinstaller hello.py
# --onefile — сборка в один файл, т.е. файлы .dll не пишутся.
# --windowed -при запуске приложения, будет появляться консоль.
# --noconsole — при запуске приложения, консоль появляться не будет.
# --icon=app.ico — добавляем иконку в окно.
# --paths — возможность вручную прописать путь к необходимым файлам, если pyinstaller
# не может их найти(например: --paths D:\python35\Lib\site-packages\PyQt5\Qt\bin)
# pyinstaller --onefile --icon=name.ico --noconsole myscript.py
# 

import re
import pathlib
import pytube

Quality = ''
isVideoCount = ''
onVideo = []
fileLogs = str(pathlib.Path(pathlib.Path.cwd()).resolve().joinpath("logs.txt"))

video_url = []

def on_progress2(stream, chunk, bytes_remaining):
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining
	percentage_of_completion = round(bytes_downloaded / total_size * 100)
	print(percentage_of_completion)

def on_progress(stream, chunk, bytes_remaining):
	global isVideoCount
	global onVideo
	global fileLogs
	total_size = stream.filesize
	bytes_downloaded = total_size - bytes_remaining
	percentage_of_completion = round(bytes_downloaded / total_size * 100)
	if percentage_of_completion == 100:
		print(f"{percentage_of_completion}%\t{isVideoCount}\t[OK]")
	elif percentage_of_completion < 100 and percentage_of_completion > 0:
		print(f"{percentage_of_completion}%\t{isVideoCount}")
	else:
		print(f"Download video {onVideo[0]} ERROR!")
		with open(fileLogs, 'a+') as f:
			f.write(f"{onVideo[0]}\n")
			f.write(f"{onVideo[1]}\n")
			f.write(f"{onVideo[2]}\n")

def filterName(innames: str) -> str:
	outname = str(innames).replace('|', '.').replace('%', '.').replace(':', '.').replace('"', '.').replace("'", ".").replace('<', '.').replace('>', '.')\
	.replace('[', '.').replace(']', '.').replace('{', '.').replace('}', '.').replace('#', '.').replace('$', '.').replace('?', '.')\
	.replace('`', '.').replace('~', '.').replace('@', '.').replace('!', '.').replace('&', '.').replace('^', '.').replace('*', '.').replace('/','.')\
	.replace('\\','.')
	pattern = r'(.)\1+'
	repl = r'\1'
	return re.sub(pattern,repl,outname).strip()

def getTitle(urlFile: str) -> str:
	global Quality
	yt = pytube.YouTube(urlFile)
	Quality = yt.streams.get_highest_resolution().resolution
	outname = filterName(yt.title) + '_' + Quality + '.mp4'
	pattern = r'(.)\1+'
	repl = r'\1'
	outname = re.sub(pattern,repl,outname).strip()
	return outname

def getClearTitle(urlFile: str) -> str:
	global Quality
	yt = pytube.YouTube(urlFile)
	Quality = yt.streams.get_highest_resolution().resolution
	outname = filterName(yt.title)
	return outname

def downloadYouTube(urlFile: str, onPath: str = None, FName: str = None):
	yt = pytube.YouTube(urlFile, on_progress_callback=on_progress)
	yt = yt.streams.get_highest_resolution()
	yt.download(output_path=onPath, filename=FName)

def getPlayList(link: str):
	playlist = pytube.Playlist(link)
	counter = len(playlist.video_urls)
	videoList = []
	for url in playlist.video_urls:
		videoList.append(url)
	return counter, videoList[:]

def checkPath(onPath: str):
	downloadpath = str(pathlib.Path(onPath).resolve())
	if not pathlib.Path(downloadpath).exists():
		pathlib.Path(downloadpath).mkdir(parents=True, exist_ok=True)
	return downloadpath

def checkPathText(TextFile: str):
	path_parent = str(pathlib.Path(TextFile).parent.resolve())
	if not pathlib.Path(path_parent).exists():
		checkPath(path_parent)
		return False
	else:
		return True

def downloadPlayList(link: str, inPath: str):
	global isVideoCount
	global onVideo
	global Quality
	global video_url
	download_path = checkPath(inPath)
	if link != '':
		video_url.clear()
		all_count, video_url = getPlayList(link)
	else:
		all_count = len(video_url)
	print(f"Number of videos in playlist: {all_count}")
	index = 1
	for onURL in video_url:
		fname = str(index) + '.' + getTitle(onURL)
		isVideoCount = f"{index}/{all_count}\t{Quality}"
		onVideo.clear()
		onVideo+=[fname]
		onVideo+=[link]
		onVideo.append(isVideoCount)
		print(f"{fname}\n{isVideoCount}")
		downloadYouTube(onURL, download_path, fname)
		index+=1

def downloadVideo(link: str, inPath: str):
	global onVideo
	download_path = checkPath(inPath)
	fname = getTitle(link)
	onVideo.clear()
	onVideo+=[fname]
	onVideo+=[link]
	onVideo.append(f"1/1\t{Quality}")
	print(fname)
	downloadYouTube(link, download_path, fname)

def getVideoInfo(link: str) -> list:
	global isVideoCount
	global Quality
	global video_url
	videoList = []
	video_url.clear()
	all_count, video_url = getPlayList(link)
	index = 1
	for onURL in video_url:
		print(f"Get info: {onURL} ({index}/{all_count})")
		fname = getClearTitle(onURL)
		isVideoCount = f"({index}/{all_count},{Quality})"
		print(f"Info: {fname} ({Quality})")
		videoList.append({'info': isVideoCount, 'title': fname, 'url': onURL})
		index+=1
	print('Get info [OK].')
	return videoList[:]

def getVideoLIST() -> list:
	global isVideoCount
	global Quality
	global video_url
	videoList = []
	all_count = len(video_url)
	index = 1
	for onURL in video_url:
		print(f"Get info: {onURL} ({index}/{all_count})")
		fname = getClearTitle(onURL)
		isVideoCount = f"({index}/{all_count},{Quality})"
		print(f"Info: {fname} ({Quality})")
		videoList.append({'info': isVideoCount, 'title': fname, 'url': onURL})
		index+=1
	print('Get info [OK].')
	return videoList[:]

def getVideoOne(link: str) -> list:
	global isVideoCount
	global Quality
	videoList = []
	print(f"Get info: {link} (1/1)")
	fname = getClearTitle(link)
	isVideoCount = f"(1/1,{Quality})"
	print(f"Info: {fname} ({Quality})")
	videoList.append({'info': isVideoCount, 'title': fname, 'url': link})
	print('Get info [OK].')
	return videoList[:]

def saveOneAllInfo(link: str, textFile: str, isInfo: bool = True):
	info = getVideoOne(link)
	print("The file is write info on one Video. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			index = 1
			for item in info:
				if isInfo:
					outstr = str(index) + '. ' + item['title'] + '\n' + item['info'] + '\n'
				else:
					outstr = str(index) + '. ' + item['title'] + '\n'
				f.write(outstr)
				index+=1
			f.write('\n')
			index = 1
			for item in info:
				outstr = item['url'] + '\n'
				f.write(outstr)
				index+=1
			f.write('---------------------------------\n')
		print('The file info on one Video is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def savePlayList(link: str, textFile: str, isInfo: bool = True):
	if link != '':
		info = getVideoInfo(link)
	else:
		info = getVideoLIST()
	print("The file is write info on PlayList. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			index = 1
			for item in info:
				if isInfo:
					outstr = str(index) + '. ' + item['title'] + '\n' + item['info'] + '\n'
				else:
					outstr = str(index) + '. ' + item['title'] + '\n'
				f.write(outstr)
				index+=1
			f.write('\n')
			index = 1
			for item in info:
				outstr = item['url'] + '\n'
				f.write(outstr)
				index+=1
			f.write('---------------------------------\n')
		print('The file info on PlayList is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def saveURLVideo(link: str, textFile: str, isIndex: bool = False):
	print("The file is write info on one Video. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			if isIndex:
				outstr ='1. ' + link + '\n'
			else:
				outstr = link + '\n'
			f.write(outstr)
			f.write('---------------------------------\n')
		print('The file info on one Video is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def readURLTextFile(onFile: str):
	global video_url
	txtFile = str(pathlib.Path(onFile).resolve())
	if pathlib.Path(txtFile).exists():
		with open(txtFile, 'r') as f:
			output = f.read().splitlines()
		video_url = output[:]
	else:
		print(f"Error! The file {txtFile} of not found!")

def saveURLPlayList(link: str, textFile: str, isIndex: bool = False):
	global video_url
	if link != '':
		video_url.clear()
		_, video_url = getPlayList(link)
	print("The file is write info on PlayList. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			count = 1
			for item in video_url:
				if isIndex:
					outstr = str(count) + '. ' + item + '\n'
				else:
					outstr = item + '\n'
				f.write(outstr)
				count+=1
			f.write('---------------------------------\n')
		print('The file info on PlayList is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def saveOneInfo(link: str, textFile: str, isInfo: bool = True):
	info = getVideoOne(link)
	print("The file is write info on one Video. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			index = 1
			for item in info:
				if isInfo:
					outstr = str(index) + '. ' + item['title'] + '\n' + item['info'] + '\n'
				else:
					outstr = str(index) + '. ' + item['title'] + '\n'
				f.write(outstr)
				index+=1
			f.write('---------------------------------\n')
		print('The file info on one Video is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def saveInfoPlayList(link: str, textFile: str, isInfo: bool = True):
	if link != '':
		info = getVideoInfo(link)
	else:
		info = getVideoLIST()
	print("The file is write info on PlayList. Please, wait.")
	if checkPathText(textFile):
		with open(textFile, 'a+') as f:
			index = 1
			for item in info:
				if isInfo:
					outstr = str(index) + '. ' + item['title'] + '\n' + item['info'] + '\n'
				else:
					outstr = str(index) + '. ' + item['title'] + '\n'
				f.write(outstr)
				index+=1
			f.write('---------------------------------\n')
		print('The file info on PlayList is [OK].')
	else:
		print(f"Error! The file {textFile} of not found!")

def main():
	# test
	#url = 'https://www.youtube.com/watch?v=V3h2iq2mylI&list=PLlWXhlUMyoobAlP3mZ0_uuJagsDSg_5YT&index=2'
	#url = 'https://www.youtube.com/playlist?list=PLlWXhlUMyoobAlP3mZ0_uuJagsDSg_5YT'
	#url = 'https://www.youtube.com/playlist?list=PLA0M1Bcd0w8zPwP7t-FgwONhZOHt9rz9E'
	#folder = '/home/mikl/003/python-oop/'
	#playlist_text = '/home/mikl/003/playlist.txt'
	#readURLTextFile(playlist_text)
	#downloadPlayList('', folder)
	#saveURLPlayList(url, playlist_text, False)
	#playlist_text = '/home/mikl/003/playlist2.txt'
	#saveInfoPlayList(url, playlist_text, False)
	#downloadPlayList(url, folder)
	#plfile = './playlist-test2.txt'
	#playlist_text = 'playlist.txt'
	#readURLTextFile(playlist_text)
	#
	# URL Error. Только для спонсоров. Не скачивает 5,7,10,13,14,17,19,23,25,27,30,32,35,38
	# url = 'https://www.youtube.com/playlist?list=PLQAt0m1f9OHvyjJNjZK_unnLwMOXPTja8'
	# url = 'https://www.youtube.com/watch?v=Gnt7abcf4_M&list=PLQAt0m1f9OHvyjJNjZK_unnLwMOXPTja8&index=6'
	#
	'''
	print('savePlayList variant-1')
	savePlayList('', plfile, False)
	print('savePlayList variant-2')
	savePlayList('', plfile, True)
	print('saveInfoPlayList variant-1')
	saveInfoPlayList('', plfile, False)
	print('saveInfoPlayList variant-2')
	saveInfoPlayList('', plfile, True)
	print('saveURLPlayList variant-1')
	saveURLPlayList('', plfile, False)
	print('saveURLPlayList variant-2')
	saveURLPlayList('', plfile, True)
	'''
	'''
	print('savePlayList variant-1')
	savePlayList(url, plfile, False)
	print('savePlayList variant-2')
	savePlayList(url, plfile, True)
	print('saveInfoPlayList variant-1')
	saveInfoPlayList(url, plfile, False)
	print('saveInfoPlayList variant-2')
	saveInfoPlayList(url, plfile, True)
	print('saveURLPlayList variant-1')
	saveURLPlayList(url, plfile, False)
	print('saveURLPlayList variant-2')
	saveURLPlayList(url, plfile, True)
	'''
	'''
	print('saveOneAllInfo variant-1')
	saveOneAllInfo(url, plfile, False)
	print('saveOneAllInfo variant-2')
	saveOneAllInfo(url, plfile, True)
	print('saveOneInfo variant-1')
	saveOneInfo(url, plfile, False)
	print('saveOneInfo variant-2')
	saveOneInfo(url, plfile, True)
	print('saveURLVideo variant-1')
	saveURLVideo(url, plfile, False)
	print('saveURLVideo variant-2')
	saveURLVideo(url, plfile, True)
	'''
	#downloadPlayList('', folder)
	'''
	if 'playlist' in url:
		#downloadPlayList(url, folder)
	else:
		#downloadVideo(url, folder)
	'''
	'''
		url = 'https://www.youtube.com/playlist?list=PLlWXhlUMyoobAlP3mZ0_uuJagsDSg_5YT'
		folder = '/home/mikl/003/'
		yt = pytube.Playlist(url)
		index = 1
		for item in yt.videos:
			item.register_on_progress_callback(on_progress)
			fname = str(index) + '.' + filterName(item.title)
			dnwld = item.streams.get_highest_resolution()
			dnwld.download(output_path=folder, filename=fname)
			index+=1
	'''

if __name__ == '__main__':
    main()

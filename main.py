import tkinter
import customtkinter
import yt_dlp

# progress hook function to update the progress bar
def progress_hook(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes',0) # total bytes of the video
        downloaded_size = d.get('downloaded_bytes', 0) # get the downloaded size so far

        if total_size > 0:
            percentage = downloaded_size / total_size * 100 # percentage calculation
            pPercentage.configure(text=f"{percentage: .2f}%") 
            progressBar.set(downloaded_size/total_size)  # update progress bar values
        else:
            pPercentage.configure(text="0%")
            progressBar.set(0)
    app.update() #forcing tkinder to update the GUI

# Download video function using yt-dlp
def startDownload():
    try:
        ytLink = link.get() # getting the youtube link from the gui

        ydl_opts = {
        
            'format': 'best', # best format download
            'outtmpl': '%(title)s.%(ext)s', # this saves the downloaded file with title name and extension
            'progress_hooks': [progress_hook] # set the progress hook function
        }

        

        #extracting the video 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict   = ydl.extract_info(ytLink, download=False) # getting the info about the video
            video_title = info_dict.get('title', 'unknown title') # Get the title from the video info

        # Update the label to show the video title
        
        videoTitle.configure(text=f"{video_title}")

        #download the video 
        ydl.download([ytLink])

        finishLabel.configure(text="VIDEO DOWNLOADED !", text_color="green")
        progressBar.set(1) # progress bar set to 100% after full download

    except Exception as e:
        finishLabel.configure(text=" Download ERROR :( ", text_color="red")
        

#function to download the audio file using yt_dlp
def startAudioDownload():
    try:
        ytLink = link.get() #get the link from the GUI

        # Set yt-dlp options to download only the audio and convert to MP3
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio format available
            'outtmpl': '%(title)s.%(ext)s',  # Save with audio title and extension
            'progress_hooks': [progress_hook]  # Set the progress hook
        }

        #Extracting the audio info 
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict   = ydl.extract_info(ytLink, download=False) # get the video info
            audio_title = info_dict.get('title','Unknown Title')

        videoTitle.configure(text=f"Audio Title : {audio_title}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ytLink])

        finishLabel.configure(text="AUDIO DOWNLOADED !", text_color="green")
        progressBar.set(1)
    except Exception as e:
        finishLabel.configure(text=" Download ERROR :( ", text_color="red")
        



# Systems settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# app layout
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")

# title of the current video 
videoTitle = customtkinter.CTkLabel(app, text="")
videoTitle.pack(padx=40,pady=40)

# APP name and title
title = customtkinter.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10)

# link input area
url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=45, textvariable=url)
link.pack(padx=10, pady=10)

# Download finish text
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progess percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app,width=400)
progressBar.set(0) 
progressBar.pack(padx=10,pady=10)

# download video button
download = customtkinter.CTkButton(app, text="Download Video", command=startDownload)
download.pack(padx=10, pady=10)

#download audio button
download_audio = customtkinter.CTkButton(app, text="Download Audio", command=startAudioDownload)
download_audio.pack(padx=10, pady=10)
        

# Run app
app.mainloop()
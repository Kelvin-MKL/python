import PySimpleGUI as ps
from pytube import YouTube


def progress_check(stream, chunk, bytes_remaining):
    progress_amount = 100 - round( bytes_remaining / stream.filesize* 100)
    window['-PROGRESSBAR-'].update(progress_amount)

def on_complete(stream, file_path):
    window['-PROGRESSBAR-'].update(0)
    ps.Popup('The file is successfully downloaded!', title= ':)!')


ps.theme('DarkAmber')


input_tab = [
    [ps.Input(key='-INPUT-'), ps.Button('Submit')],
    [ps.Button('Clear', key='-Clear-')]
]

info_tab = [
    [ps.Text('Title:'), ps.Text('', key='-TITLE-')],
    [ps.Text('Length:'), ps.Text('', key='-LENGTH-')],
    [ps.Text('Views:'), ps.Text('', key='-VIEWS-')],
    [ps.Text('Author:'), ps.Text('', key='-AUTHOR-')],
    [ps.Text('Description:'), ps.Multiline('', key='-DESCRIPTION-', size=(40, 20), disabled=True)]
]

download_tab = [
    [ps.Frame('Best Quality',
        [[ps.Button('Download', key='-BEST-'),
            ps.Text('', key='-HIGHRESOLUTION-'),
            ps.Text('', key='-LARGESIZE-')]])],
    [ps.Frame('Worst Quality',
        [[ps.Button('Download', key = '-WORST-'),
            ps.Text('', key = '-LOWRESOLUTION-'),
            ps.Text('', key = '-SMALLSIZE-')]])],
    [ps.Frame('Audio',
        [[ps.Button('Download', key = '-AUDIO-'),
            ps.Text('', key = '-AUDIOSIZE-')]])],
    [ps.Frame('Location',
        [[ps.FolderBrowse(key= '-FOLDER-'), ps.Input(key='-FILE-')]])],
    [ps.VPush()],
    [ps.ProgressBar(100, size = (20, 20), expand_x = True, key = '-PROGRESSBAR-')]

]

layout = [[ps.TabGroup([[
    ps.Tab('input', input_tab),ps.Tab('info', info_tab), ps.Tab('Download', download_tab)
]])]]


window = ps.Window('Youtube Video Downloader', layout)
#window = ps.Window('Youtube Video Downloader', start_layout)  # The title of the window
download_path = str
while True:
    event, values = window.read()

    if event == ps.WINDOW_CLOSED:
        break
    if event == 'Submit':
        video_object = YouTube(values['-INPUT-'], on_progress_callback= progress_check, on_complete_callback= on_complete)    # fetching data from the link
        #window.close()
        #window = ps.Window('Youtube Downloader', layout, finalize = True)

        # update video
        window['-TITLE-'].update(video_object.title)
        window['-LENGTH-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)
        window['-DESCRIPTION-'].update(video_object.description)

        # download
        window['-LARGESIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576)} MB')
        window['-HIGHRESOLUTION-'].update(video_object.streams.get_highest_resolution().resolution)
        window['-SMALLSIZE-'].update(f'{round(video_object.streams.get_lowest_resolution().filesize / 1048576)} MB')
        window['-LOWRESOLUTION-'].update(video_object.streams.get_lowest_resolution().resolution)
        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576)} MB')

    if event == '-BEST-':
        download_path = values['-FILE-']
        video_object.streams.get_highest_resolution().download(output_path=download_path)

    if event == '-WORST-':
        download_path = values['-FILE-']
        video_object.streams.get_lowest_resolution().download(output_path=download_path)
    if event == '-AUDIO-':

        download_path = values['-FILE-']
        video_object.streams.get_audio_only().download(output_path=download_path)
    if event == '-Clear-':
        window['-INPUT-'].update('')


window.close()



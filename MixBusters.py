from pytube import YouTube as yt
import subprocess
from re import findall,search
from os import mkdir,remove

nopeChars = {'\\':'~','/':'~',':':';','*':'#','?':'¿','"':"``",'<':'(','>':')'}

def progreso(stream, chunk, file_handle, bytes_remaining):
    print(str(round(bytes_remaining/1024/1024,2))+'Mb restantes\r',end = '')
    return

def stampSegundos(tStamp):
    splitedTStamp = tStamp.split(':')
    if len(splitedTStamp) == 2:
        minutos,segundos = map(int,splitedTStamp)
        horas = 0
    else:
        horas,minutos,segundos = map(int,splitedTStamp)
    
    segs = horas*60*60 + minutos*60 + segundos
    return segs

def salir(*args):
    for arg in args:
        print(arg)
    exit()

def sanitizarNombre(nombre):
    for x in nopeChars:
        nombre = nombre.replace(x,nopeChars[x])
    return nombre

def getSilenceByMinDb(file,stamp):
    stampCeil = stamp+5
    stampFloor = stamp-5
    cmd = 'ffprobe -v 0 -f lavfi -i amovie="\'{}\'",aselect="between(t\,{}\,{})",astats=metadata=1:reset=1 -show_entries frame=pkt_pts_time:frame_tags=lavfi.astats.Overall.RMS_level -of csv=p=0'.format(file,stampFloor,stampCeil)
    dbs = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()[0]
    dbs = str(dbs).split('\\r\\n')
    dbs = [[float(y) for y in x.split(',')] for x in filter(lambda x: False if "'" in x else True,dbs)]
    newStamp,_ = min(dbs,key = lambda x: x[1])
    return newStamp

def split(inputFileName,paresTiempoCancion,duracion):
    outputFileName = inputFileName.replace('Downloads/','')
    try: mkdir('Output/'+outputFileName)
    except FileExistsError: pass
    print('Setting up slice timestamps...')
    for par in paresTiempoCancion:
        stamp = stampSegundos(par[0])
        par[0] = getSilenceByMinDb(inputFileName,stamp)
    cmd = 'ffmpeg -i "{}" -y -acodec mp3 -v 0 -ss {} -to {} "Output/{}/{}.mp3"'
    end = duracion
    print('Slicing...')
    for tStamp, cancion in paresTiempoCancion:
        cancion = sanitizarNombre(cancion)
        init = tStamp
        print('Creating file {}... '.format(cancion))
        command = cmd.format(inputFileName,init,end,outputFileName,cancion)
        subprocess.run(command,shell=True)
        end = init
        print('OK')

def getPares(descripcion):
    paresTiempoCancion = [list(filter(lambda a: a,x)) for x in findall('(?s)(?:(?P<artistSongPre>.*?)(?P<timeStampPost>(?:\d{1,2}:)?\d{1,2}:\d{1,2})(?=\n))|(?:(?P<timeStampPre>(?:\d{1,2}:)?\d{1,2}:\d{1,2})(?P<artistSongPost>.*?(?=\n)))',descripcion)]
    if not paresTiempoCancion: salir('Mmmm... no hay tracklist en la descripcion')
    paresTiempoCancion.reverse()
    return [[x.strip() for x in [i,j]] for i,j in paresTiempoCancion]

def main():
    url = input('> ')
    video = yt(url)
    video.register_on_progress_callback(progreso)

    stream = video.streams.filter(only_audio=True).first()
    descripcion = video.description
    duracion = video.length

    paresTiempoCancion = getPares(descripcion)

    if search('\d{1,2}:\d{1,2}',paresTiempoCancion[0][1]):
        [x.reverse() for x in paresTiempoCancion]
    elif search('\d{1,2}:\d{1,2}',paresTiempoCancion[0][0]):
        pass
    else: salir('Mmmm... problemas con el formato',paresTiempoCancion)

    print('Descargando:\n')
    fileName = stream.download('Downloads/')

    split(fileName,paresTiempoCancion,duracion)

# main()
from pytube import YouTube as yt
import subprocess
from re import findall,search
from os import mkdir

nopeChars = {'\\':'~','/':'~',':':';','*':'#','?':'¿','"':"``",'<':'(','>':')'}

def progreso(stream, chunk, file_handle, bytes_remaining):
    print(str(round(bytes_remaining/1024/1024,2))+'Mb restantes\r',end = '')
    return

def stampSegundos(tStamp):
    minutos,segundos = map(int,tStamp.split(':'))
    stampSegundos = minutos*60 + segundos
    return stampSegundos

def salir(*args):
    for arg in args:
        print(arg)
    exit()

def sanitizarNombre(nombre):
    for x in nopeChars:
        nombre = nombre.replace(x,nopeChars[x])
    return nombre

def split(iFile,paresTiempoCancion,duracion):
    fName = iFile.split('/')[1]
    try: mkdir('Output/'+fName)
    except FileExistsError: pass
    cmd = 'ffmpeg -i "{}" -acodec mp3 -n -v 0 -ss {} -to {} "Output/{}/{}.mp3"'

    end = duracion
    for tStamp, cancion in paresTiempoCancion:
        cancion = sanitizarNombre(cancion)
        init = stampSegundos(tStamp)
        print('Generando archivo {}... '.format(cancion),end='')
        _ = subprocess.call(cmd.format(iFile,init,end,fName,cancion),shell=True)
        end = init
        print('OK')

def getPares(descripcion):
    paresTiempoCancion = [list(filter(lambda a: a,x)) for x in findall('(?s)(?:(?P<artistSongPre>.*?)(?P<timeStampPost>\d{1,2}:\d{1,2})(?=\n))|(?:(?P<timeStampPre>\d{1,2}:\d{1,2})(?P<artistSongPost>.*?(?=\n)))',descripcion)]
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
    titulo = stream.download('Downloads/')

    split(titulo,paresTiempoCancion,duracion)

main()
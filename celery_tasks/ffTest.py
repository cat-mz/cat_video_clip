from ffmpy import FFmpeg

path = "/home/cat/videos_test/cat_ihome.mp4"


def clip(input_path, startTime, endTime, output_name):
    ff = FFmpeg(inputs={
        input_path: "-ss {} -t {} -i {} -vcodec copy -acodec copy ../video_clip/{}".format(startTime, endTime,
                                                                                           input_path,
                                                                                           output_name)
    })
    print(ff.cmd)
    ff.run()


'''
ffmpeg -i video/vvvv.mp4 -f image2 -vf fps=fps=1 out%d.png
ffmpeg -i video/vvvv.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//
ffmpeg -i video/vvvv.mp4 -f image2 -vf fps=fps=1 out%d.png
ffmpeg -i video/vvvv.mp4  -c copy -map 0 -y -f segment -segment_list video/playlist.m3u8 -segment_time 1  -bsf:v h264_mp4toannexb   video/cat_output%03d.ts


ffmpeg -i cat_ihome.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//
ffmpeg -i cat_ihome.mp4 -f image2 -vf fps=fps=1 out.png

ffmpeg -ss 0:1:30 -t 0:0:20 -i input.avi -vcodec copy -acodec copy output.avi    //剪切
            开始时间                结束时间
ffmpeg -ss 0:0:30 -t 0:1:30 -i cat_ihome.mp4 -vcodec copy -acodec copy output1234.mp4    //剪切

'''

if __name__ == '__main__':
    clip(input_path=path, startTime='0:0:20', endTime='0:1:10', output_name='out123456.mp4')

'''
from ffmpy import FFmpeg
 
ff = FFmpeg(inputs={'/home/cat/videos_test/cat_ihome.mp4': ['t','0','30']},
            outputs={'/home/cat/videos_test/2.mp4': None})
print(ff.cmd)
ff.run()

ff = FFmpeg(inputs={'/home/cat/videos_test/cat_ihome.mp4': "ffmpeg -i cat_ihome.mp4 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"})


'''

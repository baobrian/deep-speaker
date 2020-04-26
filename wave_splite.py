# coding=utf-8
from pydub import AudioSegment
import os
import json


# 操作函数
def get_wav_make(dataDir,id_index):
    os.chdir('/Users/baozilin/PycharmProjects/3.6project/deep-speaker/new_sample/'+id_index)
    sound = AudioSegment.from_wav(dataDir)
    id_list=[]
    duration = sound.duration_seconds * 1000  # 音频时长（ms）
    if duration<6000:
        return False
    else:
        step = 1
        for i in range(int(duration / 3000)):
            begin = (i * 3) * 1000
            end = (i + 1) * 3 * 1000
            cut_wav = sound[begin:end]  # 以毫秒为单位截取[begin, end]区间的音频
            cut_wav.export(id_index+'_00' + str(step) + '.wav', format='wav')  # 存储新的wav文件
            step = step + 1
        return True


def main():
    # 路径需绝对路径
    # audio_path = '/Users/baozilin/PycharmProjects/3.6project/deep-speaker/subject/'
    # audio_warhouse = '/Users/baozilin/PycharmProjects/3.6project/deep-speaker/deep-speaker-databak/VCTK-Corpus/wav48/'
    audio_path = '/Users/baozilin/PycharmProjects/3.6project/deep-speaker/new_subject/'
    audio_warhouse = '/Users/baozilin/PycharmProjects/3.6project/deep-speaker/new_sample/'
    files = os.listdir(audio_path)
    id_list = []
    for file in files:
        os.chdir(audio_warhouse)
        id_index = file.replace('.wav', '')[0:18]
        path = audio_warhouse + id_index
        # wav_path = audio_path + '44058219881201293X_MhAAqV4O_62AYHhiAAFwLDa60ok310.wav'
        wav_path = audio_path + file
        if not os.path.exists(path):
            os.makedirs(path)

            if get_wav_make(wav_path, id_index):
                id_list.append(id_index)
        else:
            continue
    # os.chdir(audio_warhouse)
    # id_list = id_list[0:-10]
    # test_index = id_list[-9:-1]
    # dict = {"AUDIO": {"SAMPLE_RATE": 8000, "SPEAKERS_TRAINING_SET": id_list, "SPEAKERS_TESTING_SET": test_index}}
    # os.chdir('/Users/baozilin/PycharmProjects/3.6project/deep-speaker/')
    # with open("conf.json", "w") as f:
    #     f.write(json.dumps(dict, separators=(',', ':')))

    return


if __name__ == '__main__':

    main()
    print('数据预处理加工完成')
import logging
import os
import shutil
import time
from argparse import ArgumentParser
import random
import numpy as np
from audio_reader import AudioReader
from constants import c
from utils import InputsGenerator


def arg_parse():
    arg_p = ArgumentParser()
    arg_p.add_argument('--audio_dir', required=True)
    arg_p.add_argument('--cache_output_dir', required=True)
    arg_p.add_argument('--regenerate_full_cache', action='store_true')
    arg_p.add_argument('--update_cache', action='store_true')
    arg_p.add_argument('--generate_training_inputs', action='store_true')
    arg_p.add_argument('--multi_threading', action='store_true')
    arg_p.add_argument('--unseen_speakers')  # p225,p226 example.
    arg_p.add_argument('--get_embeddings')  # p225 example.
    return arg_p


def regenerate_full_cache(audio_reader, args):
    cache_output_dir = os.path.expanduser(args.cache_output_dir)
    print('The directory containing the cache is {}.'.format(cache_output_dir))
    print('Going to wipe out and regenerate the cache in 5 seconds. Ctrl+C to kill this script.')
    time.sleep(5)
    try:
        shutil.rmtree(cache_output_dir)
    except:
        pass
    os.makedirs(cache_output_dir)
    audio_reader.build_cache()


def generate_cache_from_training_inputs(audio_reader, args):
    cache_dir = os.path.expanduser(args.cache_output_dir)
    inputs_generator = InputsGenerator(cache_dir=cache_dir,
                                       audio_reader=audio_reader,
                                       max_count_per_class=1000,
                                       speakers_sub_list=None,
                                       multi_threading=args.multi_threading)
    inputs_generator.start_generation()


def main():
    args = arg_parse().parse_args()

    audio_reader = AudioReader(input_audio_dir=args.audio_dir,
                               output_cache_dir=args.cache_output_dir,
                               sample_rate=c.AUDIO.SAMPLE_RATE,
                               multi_threading=args.multi_threading)

    # if args.regenerate_full_cache:
    #     regenerate_full_cache(audio_reader, args)
    #     exit(1)
    #
    # if args.update_cache:
    #     audio_reader.build_cache()
    #     exit(1)
    #
    # if args.generate_training_inputs:
    #     generate_cache_from_training_inputs(audio_reader, args)
    #     exit(1)


    if args.unseen_speakers is not None:
        unseen_speakers = [x.strip() for x in args.unseen_speakers.split(',')]
        from unseen_speakers import inference_unseen_speakers
        list=c.AUDIO.SPEAKERS_TRAINING_SET
        scores_vector=np.zeros((len(list)+1,1))
        target_label_vector=np.zeros((len(list)+1,1))
        for index,compont in enumerate(list):
            # compare_speaker=random.choice(speakers)
            score=inference_unseen_speakers(audio_reader, unseen_speakers[0],compont)
            scores_vector[index]=score
            if unseen_speakers[0]==compont:
                target_label_vector[index]=1
            else:
                target_label_vector[index]=0
        score = inference_unseen_speakers(audio_reader, unseen_speakers[0], unseen_speakers[1])
        scores_vector[index+1]=score
        target_label_vector[index+1]=1
        np.save('./roc_data/scores_vector.npy',scores_vector)
        np.save('./roc_data/target_label_vector.npy',target_label_vector)
        print('roc data finished')
        exit(1)

    # if args.get_embeddings is not None:
    #     speaker_id = args.get_embeddings.strip()
    #     from unseen_speakers import inference_embeddings
    #     inference_embeddings(audio_reader, speaker_id)
    #     exit(1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
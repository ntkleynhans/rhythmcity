#!/usr/bin/env python3

import argparse
import json
import os
import random

def what_lang(tags):
  if 'sot' in tags or '_tsn' in tags:
    return 'Setswana', 'sot'
  if 'zul' in tags or '_xho' in tags:
    return 'isiZulu', 'zul'
  return 'English', 'eng'

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("json", help="Input JSON file")
  parser.add_argument("oggdir", help="Ogg folder")
  args = parser.parse_args()

  with open(args.json, 'r') as f:
    data = json.load(f)

  tasks = []
  text = []
  for anno_id in data['order']:
    utt = data['annotations'][anno_id]
    lang, tag = what_lang(utt['lang_tags'])
    editor = 'editor_{}_{}'.format(tag, random.randrange(1,6))

    tasks.append({
      'start': data['time_slots'][utt['start_time']],
      'end': data['time_slots'][utt['end_time']],
      'editor': editor,
      'speaker': '{},{}'.format(anno_id, utt['lang_tags']),
      'language': lang
    })

    text.append(utt['text'])

  with open(args.json.replace('.json', '_uploader.json'), 'w') as f:
      json.dump({'project_name': os.path.basename(args.json.replace('.json','')),
          'oggfile': os.path.join(args.oggdir, data['audio_file'].replace('.wav', '.ogg')), 'tasks': tasks, 'text': text}, f, indent=4)

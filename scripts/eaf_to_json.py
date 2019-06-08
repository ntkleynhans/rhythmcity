#!/usr/bin/env python3

from xml.dom import minidom
import argparse
import json

TAGS = set(['_afr', '_eng', '_fly', '_nso', '_sot', '_tsn', '_xho', '_zul'])

def extract_tags(text):
  tags = set()
  for lang in TAGS:
    if lang in text:
      tags.add(lang)

  tags = list(tags)
  if len(tags) == 0:
    tags.append('_eng')

  tags.sort()
  return ':'.join(tags)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("eaf", help="Input EAF file")
  args = parser.parse_args()

  xmldoc = minidom.parse(args.eaf)

  time_slots = {}
  for time_slot in xmldoc.getElementsByTagName('TIME_SLOT'):
    time_slots[time_slot.attributes['TIME_SLOT_ID'].value] = float(time_slot.attributes['TIME_VALUE'].value)/1000.0

  annotations = {}
  order = []
  for anno in xmldoc.getElementsByTagName('ANNOTATION'):
    for align in anno.getElementsByTagName('ALIGNABLE_ANNOTATION'):
      if 'CVE_REF' not in align.attributes:
        annotation_id = align.attributes['ANNOTATION_ID'].value
        order.append(annotation_id)
        start_time = align.attributes['TIME_SLOT_REF1'].value
        end_time = align.attributes['TIME_SLOT_REF2'].value

        for value in align.getElementsByTagName('ANNOTATION_VALUE'):
          for text in value.childNodes:
            lang_tags = extract_tags(text.nodeValue)
            annotations[annotation_id] = {'start_time': start_time, 'end_time': end_time, 'text': text.nodeValue, 'lang_tags': lang_tags}

  json_file = args.eaf.replace('.eaf','.json')
  data = {'time_slots': time_slots, 'annotations': annotations, 'order': order}
  with open(json_file, 'w') as f:
    json.dump(data, f, indent=4)

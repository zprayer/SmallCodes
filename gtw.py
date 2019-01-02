from xml.etree.ElementTree import parse, Element
from openpyxl import load_workbook
import os


def addREFNode(parent, parametername, frame, word):
    e = Element('REF',
                {
                    'FrameIncrement': '0',
                    'WordIncrement': '0',
                    'Frame': str(frame),
                    'Word': str(word),
                    'CVTMode': 'Enabled',
                    'ExtReads': '0',
                    'SuperMode': 'Data',
                    'IsParameterStream': 'No',
                    'ParameterName': parametername,
                    'OutRate': '32',
                    'InRate': '32',
                })
    parent.append(e)


# get input file path
icdfp = input('429 ICD file path: \n')
xmlfp = input('TTC xml file path: \n')
icdfp = icdfp[1:-1] if icdfp.startswith('"') else icdfp  # get rid of " if file name contains space
xmlfp = xmlfp[1:-1] if xmlfp.startswith('"') else xmlfp  # same as above


# set output file path
dirpath, filename = os.path.split(xmlfp)
outputfilename = filename.split('.')[0]+'-ADDGTW'+'.xml'
outputxmlfp = os.path.join(dirpath, outputfilename)


# declare region
pcm_format_path = 'PROJECT/HARDWARE/BOX/CARD/SETTINGS/PCM_FORMAT'
words_per_frame_path = 'PROJECT/HARDWARE/BOX/CARD/SETTINGS/GENERAL_SETUP/WORDS_PER_FRAME'
frames_per_major_frame_path = 'PROJECT/HARDWARE/BOX/CARD/SETTINGS/GENERAL_SETUP/FRAMES_PER_MAJOR_FRAME'


# load ttc xml and fetch number of words and frames
doc = parse(xmlfp)
frames = int(doc.find(frames_per_major_frame_path).text)
words = int(doc.find(words_per_frame_path).text)


# load icd xlsx, get telemetry parameters and messages
wb = load_workbook(icdfp,
                   data_only=True)  # get value instead formula
ws = wb.worksheets[0]  # first sheet default
rows = ws.rows
next(rows)  # skip the header row
parameters = list(r[8].value for r in rows if r[13].value is not None
                  )  # filter telemetry parameters, r[8] is '参数符号', r[13] is '是否遥测监控'
messages = []
for p in parameters:
    messages.append(p + '_O')
    messages.append(p + '_R')


# seating messages
seating = {}
idxframe, idxword = 1, 1
for m in messages:
    seating[m] = (idxframe, idxword)
    idxframe += 1
    if idxframe > frames:
        idxword += 1
        idxframe = 1


# generate ttc xml

# add REF_TYPE node under PCM_FORMAT
pcm_format_node = doc.find(pcm_format_path)  # parent node
ref_type_element = Element('REF_TYPE', {'Name': 'PCM'})  # child node
pcm_format_node.append(ref_type_element)

# redirect to PCM REF_TYPE node
for n in pcm_format_node.findall('REF_TYPE'):
    if n.attrib['Name'] == 'PCM':
        ref_type_pcm_node = n

# add REF nodes under PCM REF_TYPE
for (k, v) in seating.items():
    addREFNode(ref_type_pcm_node, k, *v)


# write xml file
doc.write(outputxmlfp)

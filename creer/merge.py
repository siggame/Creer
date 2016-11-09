from creer.utilities import extract_str

MERGE_KEYWORD_START_PRE = "<<-- Creer-Merge: "
MERGE_KEYWORD_START_POST = " -->>"
MERGE_KEYWORD_END_PRE = "<<-- /Creer-Merge: "
MERGE_KEYWORD_END_POST = " -->>"

def with_data(data, pre_comment, key, alt, add_tags):
    merged = []
    if add_tags:
        merged.extend([pre_comment, MERGE_KEYWORD_START_PRE, key, MERGE_KEYWORD_START_POST," - Code you add between this comment and the end comment will be preserved between Creer re-runs.\n"])
    if key in data:
        print("    + merging", key)
        merged.append(data[key])
    else:
        if alt[len(alt) - 1] != "\n" and add_tags:
            alt = alt + "\n"
        merged.append(alt)
    if add_tags:
        merged.extend([pre_comment, MERGE_KEYWORD_END_PRE, key, MERGE_KEYWORD_END_POST])
    return "".join(merged)

def generate_data(file_contents):
    data = {}
    recording = None
    for line in file_contents:
        if MERGE_KEYWORD_END_PRE in line:
            recording = None
        elif MERGE_KEYWORD_START_PRE in line:
            split = line.split()
            recording = extract_str(line, MERGE_KEYWORD_START_PRE, MERGE_KEYWORD_START_POST)
            data[recording] = []
        elif recording:
            data[recording].append(line)

    merge_data = {}
    for key, lines in data.items():
        merge_data[key] = "".join(lines)
    return merge_data
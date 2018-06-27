import math
from mido import MidiFile
import music21
import operator
import pylab as plt
from matplotlib_venn import venn3

input_files = {
    "in/Star Trek TNG kurz.mid": "F minor", "in/sleepsat.mid": "E- major", "in/silentnight.mid": "C major",
    "in/shephard.mid": "F major", "in/sesame.mid": "C minor",
    "in/scooby.mid": "C major", "in/Sara.mid": "C major", "in/santacom.mid": "C major", "in/rudolph.mid": "C major",
    "in/Rikasmies.mid": "C minor",
    "in/reichwaehr.mid": "C minor", "in/prima.mid": "C major", "in/policeacademy.mid": "C major",
    "in/pipi-langstrumpf.mid": "C major", "in/Petteri.mid": "C major",
    "in/superman.mid": "G major", "in/StheB.mid": "G major", "in/Sternenhimmel.mid": "G major",
    "in/starwars-imperial.mid": "D minor", "in/starwars.mid": "C minor",
    "in/99 Luftballons.mid": "D minor", "in/90210.mid": "F major", "in/Zorbas.mid": "D major",
    "in/ZieGindsKomtDeStoomboot.mid": "F major",
    "in/you R not alone.mid": "D minor",
    "in/X Files.mid": "E minor", "in/winnerabba.mid": "B major", "in/WalkOfLife.mid": "A major",
    "in/Uralinpihlaja.mid": "D minor", "in/tlc.mid": "C major",
    "in/Titanic.mid": "C major", "in/tannebaum.mid": "F major",

    "in/oxygen.mid": "C minor", "in/ohcome.mid": "D minor", "in/Oh_come.mid": "G major",
    "in/offspring_getajob.mid": "A minor", "in/o_little.mid": "F major",
    "in/o_la_paloma.mid": "G major", "in/nur getrumt.mid": "C major",
    "in/Niemals in New York 2.mid": "C major", "in/nie wieder.mid": "C major", "in/murka.mid": "D minor",
    "in/Mit 66 Jahren.mid": "F major", "in/Mission_impossible.mid": "E- major",
    "in/mief.mid": "C major", "in/marmor-stein.mid": "C major",
    "in/major tom.mid": "F major", "in/Macarena.mid": "F major",
    "in/LivingRoom.mid": "D minor", "in/liquido.mid": "A minor",

    "in/Lindenstrae2.mid": "C major", "in/kiss.mid": "A minor", "in/Insel m. 2 Bergen.mid": "C major",
    "in/indiana.mid": "C major", "in/howmuchisthefish.mid": "A minor", "in/HoheBerge.mid": "D major",
    "in/GWein.mid": "A minor",

    "in/GuteZeiten.mid": "A minor", "in/Griechischer Wein2.mid": "A minor",
    "in/goodbad.mid": "A minor", "in/good.mid": "F major", "in/godfather.mid": "C minor",
    "in/god_rest.mid": "D minor", "in/gl_ck.mid": "C major", "in/FofS.mid": "G major",

    "in/flintstones.mid": "A minor", "in/flieger.mid": "C major",
    "in/Eldanka.mid": "D minor", "in/Elamaa_juoksuhaudoissa.mid": "G minor",
    "in/einfallfuer2.mid": "A minor", "in/Ein_Fall_Fuer_Zwei.mid": "A minor",
    "in/east_end.mid": "B- major", "in/DschingesKhan.mid": "A minor",
    "in/deutschlandlied.mid": "G major", "in/denneboom.mid": "F major",
    # "in/davy.mid": "C major",
    "in/Cucaracha.mid": "C major",
    "in/cccp.mid": "A major", "in/boom.mid": "F major", "in/Bittersweetharmonie.mid": "A- major",
    "in/big big girl.mid": "C major", "in/Biene Maja.mid": "C major",
    "in/away.mid": "F major", "in/advkal8.mid": "C major", "in/advkal10.mid": "C major",
    "in/advkal12.mid": "A minor", "in/advkal15.mid": "C major",
    "in/advkal17.mid": "C major"

}
major_profile = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
minor_profile = [5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17, 6.33, 2.68, 3.52]
ignored_messages = ["note_off", "polytouch", "control_change", "program_change", "aftertouch",
                    "pitchwheel", "sysex", "quarter_frame", "songpos", "song_select", "tune_request",
                    "clock", "start", "continue", "stop", "active_sensing", "reset"]
correlate_krumh = {"10": "A", "11": "B-", "12": "B", "1": "C", "2": "D-", "3": "D", "4": "E-",
                   "5": "E", "6": "F", "7": "G-", "8": "G", "9": "A-"}
correlate_algo = {9: "A", 10: "A ♯ or B ♭", 11: "B", 0: "C", 1: "C ♯ or D ♭", 2: "D", 3: "D ♯ or E ♭",
                  4: "E", 5: "F", 6: "F ♯ or  G ♭", 7: "G", 8: "G ♯ or A ♭"}
notes_letters = [['C', 'A'],
                 ['F', 'D', 'G', 'E'],
                 ['B-', 'G', 'D', 'B'],
                 ['E-', 'C', 'A', 'F+'],
                 ['A-', 'F', 'E', 'C+'],
                 ['D-', 'B-', 'B', 'G+'],
                 ['G-', 'E-', 'F+', 'D+'],
                 ['C-', 'A-', 'C+', 'A+']]
signs_by_key = {
    'C major': 0, 'A minor': 0,
    'F major': 1, 'D minor': 1, 'G major': 1, 'E minor': 1,
    'B- major': 2, 'G minor': 2, 'D major': 2, 'B minor': 2,
    'E- major': 3, 'C minor': 3, 'A major': 3, 'F+ minor': 3,
    'A- major': 4, 'F minor': 4, 'E major': 4, 'C+ minor': 4,
    'D- major': 5, 'B- minor': 5, 'B major': 5, 'G+ minor': 5,
    'G- major': 6, 'E- minor': 6, 'F+ major': 6, 'D+ minor': 6,
}
notes_num = [[0, 9],
             [7, 5, 4, 2],
             [2, 10, 11, 7],
             [9, 3, 6, 0],
             [4, 8, 1, 5],
             [11, 1, 8, 10],
             [6, 6, 3, 3],
             [1, 11, 10, 8]]
signs = [6, 1, 8, 3, 10]
sharps = [6, 1, 8, 3, 10, 5, 0]
flats = [10, 3, 8, 1, 6, 11, 4]
major_intervals = [2, 2, 1, 2, 2, 2, 1]
minor_intervals = [2, 1, 2, 2, 1, 2, 2]
relative_key = {"C major": "A minor", "D- major": "B- minor", "D major": "B minor", "E- major": "C minor",
                "E major": "C+ minor", "F major": "D minor", "F+ major": "D+ minor", "G- major": "E- minor",
                "G major": "E minor", "A- major": "F minor", "A major": "F+ minor", "B- major": "G minor",
                "B major": "G+ minor",
                }


def get_closely_related_keys(key1):
    # take the key itself without lad to get the 4th and the 5th stages
    letter = [chr(ord((key1[:len(key1) - 6])[0]) + 3), chr(ord((key1[:len(key1) - 6])[0]) + 4)]
    lad = key1[len(key1) - 5:]
    for i in range(len(letter)):
        letter[i] += " " + lad
    return letter


def helper(x, y):
    meanX = mean(x)
    meanY = mean(y)
    numerator = 0
    denominator_one = 0
    denominator_two = 0
    for j in range(12):
        numerator += (x[j] - meanX) * (y[j] - meanY)
        denominator_one += (x[j] - meanX) * (x[j] - meanX)
        denominator_two += (y[j] - meanY) * (y[j] - meanY)
    denominator = math.sqrt(denominator_one * denominator_two)
    return numerator, denominator


def mean(arr):
    size = len(arr)
    summ = 0
    for i in range(size):
        summ += arr[i]
    return summ / size


def is_a_sign(x):
    return signs.__contains__(x)


def is_a_sharp(x):
    return sharps.__contains__(x)


def is_a_flat(x):
    return flats.__contains__(x)


def get_key(midi_file):
    r_major = [0] * 12
    r_minor = [0] * 12
    frequency = [0] * 12
    y = [0] * 12
    for i in midi_file.tracks:
        for j in i[2:]:
            # print("This is j: ", j)
            if not j.is_meta and not ignored_messages.__contains__(j.type):  # and j.velocity != 0 :
                # print("This is j: ", j)
                my_note = j.note
                frequency[my_note % 12] += 1
    x = major_profile
    for i in range(12):
        for j in range(12):
            y[j] = frequency[(j + i) % 12]
        help = helper(x, y)
        r_major[i] = help[0] / help[1]
    x = minor_profile
    for i in range(12):
        for j in range(12):
            y[j] = frequency[(j + i + 3) % 12]
        help = helper(x, y)
        r_minor[i] = help[0] / help[1]
    max_r = -100000
    fit_key = 0
    for i in range(12):
        if max_r < r_major[i]:
            max_r = r_major[i]
            fit_key = i + 1
            lad = "major"
    for i in range(12):
        if max_r < r_minor[i]:
            max_r = r_minor[i]
            fit_key = -i - 1
            lad = "minor"
    return (str)(correlate_krumh[(str)(abs(fit_key))] + " " + (str)(lad))


def algo(file):
    frequency = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
    note_count = 0
    last_note = 0
    for i in file.tracks:
        for j in i[2:len(i)]:
            if not j.is_meta and not ignored_messages.__contains__(j.type) and j.velocity != 0:
                last_note = j.note
                note_count += 1
                frequency[last_note % 12] += 1
    last_note = last_note % 12

    the_signs = []
    the_sharps = []
    the_flats = []
    sign_count = 0
    meanX = mean(frequency)
    we_have_flats = False
    sorted_frequency = sorted(frequency.items(), key=operator.itemgetter(1))
    sorted_frequency.reverse()
    sorted_frequency = sorted_frequency[:8]

    for i in range(12):
        if frequency[i] > 1:
            if is_a_sign(i):
                the_signs.append(i)
                sign_count += 1
    if the_signs.__contains__(signs[len(signs) - 1]):
        we_have_flats = True
        for x in the_signs: the_flats.append(x)

    potential_note_num = []
    for i in range(7):
        for j in range(0, 1):
            if sorted_frequency[i][1] != 0:
                potential_note_num.append(sorted_frequency[i][j])
    potential_notes_letters = []
    for i in range(len(potential_note_num)):
        potential_notes_letters.append(correlate_algo[(potential_note_num[i])])

    k = 0
    for n in potential_notes_letters:
        if len(n) > 2:
            if we_have_flats:
                potential_notes_letters[k] = n[7:]
            else:
                potential_notes_letters[k] = n[:3]
        k += 1
    if sign_count == 0 or we_have_flats:
        major_begin = notes_num[sign_count][0]
        minor_begin = notes_num[sign_count][1]
    else:
        major_begin = notes_num[sign_count][2]
        minor_begin = notes_num[sign_count][3]
    potential_note_num.sort()
    major = []
    minor = []
    for i in major_intervals:
        major_begin += i
        major.append(major_begin % 12)
    for i in minor_intervals:
        minor_begin += i
        minor.append(minor_begin % 12)
    major_count = 0
    minor_count = 0
    for i in range(7):
        if potential_note_num.__contains__(i) and major.__contains__(i):
            major_count += 1
        if potential_note_num.__contains__(i) and minor.__contains__(i):
            minor_count += 1
    if major_count >= minor_count:
        if sign_count == 0 or we_have_flats:
            if (correlate_algo[(last_note)]) == str(notes_letters[sign_count][0]):
                flag = True
            return str(notes_letters[sign_count][0]) + " major"
        else:
            if (correlate_algo[(last_note)]) == str(notes_letters[sign_count][2]):
                flag = True
            return str(notes_letters[sign_count][2]) + " major"

    elif minor_count >= major_count:
        if sign_count == 0 or we_have_flats:
            if (correlate_algo[(last_note)]) == str(notes_letters[sign_count][1]):
                flag = True
            return str(notes_letters[sign_count][1]) + " minor"
        else:
            if str(correlate_algo[(last_note)]) == str(notes_letters[sign_count][3]):
                flag = True
            return str(notes_letters[sign_count][3]) + " minor"


def are_relative(one, two):
    return relative_key.get(str(one)) == str(two) or relative_key.get(str(two)) == str(one)


def are_closely_related(key1, key2):
    return get_closely_related_keys(key1).__contains__(key2) or are_relative(get_closely_related_keys(key1)[0],
                                                                             key2) or are_relative(
        get_closely_related_keys(key1)[1], key2)


def is_true(key):
    return input_files[x] == key


num_of_files = len(input_files)
# number of right outputs of a single algorithm not considering the others
mus_num = 0
krumhansl_num = 0
algo_num = 0

two_agree_two_right_num = 0
all_agree_all_right_num = 0
two_agree_one_right_num = 0

all_agree_num = 0
strictly_two_agree_num = 0
none_agree_num = 0
none_agree_none_right_num = 0
all_agree_none_right_num = 0
two_agree_none_right_num = 0

all_agree_none_right_relative_num = 0
mus_relative = 0
krum_relative = 0
algo_relative = 0

mus_relative_when_none_right = 0
krum_relative_when_none_right = 0
algo_relative_when_none_right = 0

mus_relative_when_none_agree_one_right = 0
krum_relative_when_none_agree_one_right = 0
algo_relative_when_none_agree_one_right = 0

none_agree_mus_right = 0
none_agree_krum_right = 0
none_agree_algo_right = 0

none_agree_one_right = 0
mus_closely_related = 0
krum_closely_related = 0
algo_closely_related = 0

all_agree_none_right_closely_related_num = 0

mus_closely_related_when_none_agree_one_right = 0
krum_closely_related_when_none_agree_one_right = 0
algo_closely_related_when_none_agree_one_right = 0

mus_key_wrong_when_none_agree_one_right = 0
all_agree_none_right_something_diff = 0

krum_key_wrong_when_none_agree_one_right = 0
algo_key_wrong_when_none_agree_one_right = 0

krum_relative_when_two_agree_two_right = 0
krum_closely_related_when_two_agree_two_right = 0
algo_relative_when_two_agree_two_right = 0
algo_closely_related_when_two_agree_two_right = 0
mus_relative_when_two_agree_two_right = 0
mus_closely_related_when_two_agree_two_right = 0

two_agree_two_right_mus_right = 0

two_agree_none_right_num += 1
krum_relative_when_two_agree_none_right = 0
krum_closely_related_when_two_agree_none_right = 0
algo_relative_when_two_agree_none_right = 0
algo_closely_related_when_two_agree_none_right = 0
mus_relative_when_two_agree_none_right = 0
mus_closely_related_when_two_agree_none_right = 0

two_agree_one_right_num = 0
krum_relative_when_two_agree_one_right = 0
krum_closely_related_when_two_agree_one_right = 0
algo_relative_when_two_agree_one_right = 0
algo_closely_related_when_two_agree_one_right = 0
algo_closely_related_when_two_agree_one_right = 0
mus_relative_when_two_agree_one_right = 0
mus_closely_related_when_two_agree_one_right = 0

two_agree_two_right_krum_right = 0
two_agree_two_right_algo_right = 0
two_agree_one_right_mus_right = 0
two_agree_one_right_krum_right = 0
two_agree_one_right_algo_right = 0

krum_something_diff_when_two_agree_two_right = 0
algo_something_diff_when_two_agree_two_right = 0
mus_something_diff_when_two_agree_two_right = 0

mus_something_diff_when_none_agree_one_right = 0
krum_something_diff_when_none_agree_one_right = 0
algo_something_diff_when_none_agree_one_right = 0

for x in input_files:
    mid = MidiFile(x)
    true_key = input_files[x]
    mus_key = music21.converter.parse(x).analyze('key')
    krum_key = get_key(mid)
    algo_key = algo(mid)
    mus_key = mus_key.tonic.name + " " + mus_key.mode

    # find out if each single algorithm determined a right key or a relative key or something else
    #     for Music21
    if is_true(mus_key):
        mus_num += 1
    elif are_relative(mus_key, true_key):
        mus_relative += 1
    elif are_closely_related(true_key, mus_key):
        mus_closely_related += 1
    #     for Krumhansl
    if is_true(krum_key):
        krumhansl_num += 1
    elif are_relative(krum_key, true_key):
        krum_relative += 1
    elif are_closely_related(true_key, krum_key):
        krum_closely_related += 1
    #     for algorithm SA
    if is_true((algo_key)):
        algo_num += 1
    elif are_relative(algo_key, true_key):
        algo_relative += 1
    elif are_closely_related(true_key, algo_key):
        algo_closely_related += 1

    #  number of coincidences
    #  all 3 give the same output
    all_agree = mus_key == krum_key and mus_key == algo_key
    if all_agree:
        all_agree_num += 1
    #  strictly 2 give the same output
    strictly_two_agree = (mus_key == krum_key and mus_key != algo_key) or (
            mus_key == algo_key and mus_key != krum_key) or (krum_key == algo_key and krum_key != mus_key)
    if strictly_two_agree:
        strictly_two_agree_num += 1
    #  no algoritm gives the same output
    none_agree = mus_key != krum_key and mus_key != algo_key and krum_key != algo_key
    if none_agree:
        none_agree_num += 1

    #  number of right answers taking into account the number of coincidences
    one_or_three_right = is_true(mus_key) ^ is_true(krum_key) ^ is_true(algo_key)
    at_least_one_right = is_true(mus_key) or is_true(krum_key) or is_true(algo_key)

    #  3 right answers when 3 coincide
    all_right = (is_true(mus_key) and is_true(krum_key) and is_true(algo_key))
    if all_right and all_agree:
        all_agree_all_right_num += 1
    #  0 right answers when 3 coincide
    if not at_least_one_right and all_agree:
        all_agree_none_right_num += 1
        if are_relative(mus_key, true_key):
            all_agree_none_right_relative_num += 1
        elif are_closely_related(true_key, mus_key):
            all_agree_none_right_closely_related_num += 1
        else:
            all_agree_none_right_something_diff += 1

    #  2 right answers when 2 coincide
    strictly_two_right = (not one_or_three_right and at_least_one_right)
    if strictly_two_right and strictly_two_agree:
        two_agree_two_right_num += 1

        if is_true(mus_key):
            two_agree_two_right_mus_right += 1
            if is_true(krum_key):
                two_agree_two_right_krum_right += 1
                if are_relative(algo_key, true_key):
                    algo_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, algo_key):
                    algo_closely_related_when_two_agree_two_right += 1
                elif not is_true(algo_key):
                    print("mus true, algo")
                    algo_something_diff_when_two_agree_two_right += 1
            elif is_true(algo_key):
                two_agree_two_right_algo_right += 1
                if are_relative(krum_key, true_key):
                    krum_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, krum_key):
                    krum_closely_related_when_two_agree_two_right += 1
                elif not is_true(krum_key):
                    print("mus true, krum")
                    krum_something_diff_when_two_agree_two_right += 1
        elif is_true(krum_key):
            two_agree_two_right_krum_right += 1
            if is_true(mus_key):
                two_agree_two_right_mus_right += 1
                if are_relative(algo_key, true_key):
                    algo_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, algo_key):
                    algo_closely_related_when_two_agree_two_right += 1
                elif not is_true(algo_key):
                    print("krum true, algo")
                    algo_something_diff_when_two_agree_two_right += 1
            elif is_true(algo_key):
                two_agree_two_right_algo_right += 1
                if are_relative(mus_key, true_key):
                    mus_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, mus_key):
                    mus_closely_related_when_two_agree_two_right += 1
                elif not is_true(mus_key):
                    print("krum true, mus")
                    mus_something_diff_when_two_agree_two_right += 1
        elif is_true(algo_key):
            two_agree_two_right_algo_right += 1
            if is_true(mus_key):
                two_agree_two_right_mus_right += 1
                if are_relative(krum_key, true_key):
                    krum_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, krum_key):
                    krum_closely_related_when_two_agree_two_right += 1
                elif not is_true(krum_key):
                    print("algo true, krum")
                    krum_something_diff_when_two_agree_two_right += 1
            if is_true(krum_key):
                two_agree_two_right_krum_right += 1
                if are_relative(mus_key, true_key):
                    mus_relative_when_two_agree_two_right += 1
                elif are_closely_related(true_key, mus_key):
                    mus_closely_related_when_two_agree_two_right += 1
                elif not is_true(mus_key):
                    print("algo true, mus")
                    mus_something_diff_when_two_agree_two_right += 1

    # 1 right answer when 0 coincide
    if none_agree and at_least_one_right:
        none_agree_one_right += 1

        # none agree but one output can be right
        #     what determined music21: right, relative or related?
        if is_true(mus_key):
            none_agree_mus_right += 1
        elif are_relative(mus_key, true_key):
            mus_relative_when_none_agree_one_right += 1
        elif are_closely_related(true_key, mus_key):
            mus_closely_related_when_none_agree_one_right += 1
        else:
            mus_something_diff_when_none_agree_one_right += 1
        #     what determined Krumhansl: right, relative or related?
        if is_true(krum_key):
            none_agree_krum_right += 1
        elif are_relative(krum_key, true_key):
            krum_relative_when_none_agree_one_right += 1
        elif are_closely_related(true_key, krum_key):
            krum_closely_related_when_none_agree_one_right += 1
        else:
            krum_something_diff_when_none_agree_one_right += 1
        #      what determined  Algorithm SA: right, relative or related?
        if is_true(algo_key):
            none_agree_algo_right += 1
        elif are_relative(algo_key, true_key):
            algo_relative_when_none_agree_one_right += 1
        elif are_closely_related(true_key, algo_key):
            algo_closely_related_when_none_agree_one_right += 1
        else:
            algo_something_diff_when_none_agree_one_right += 1
    # 0 right answers when 0 coincide
    if none_agree and not at_least_one_right:
        none_agree_none_right_num += 1
        if are_relative(mus_key, true_key):
            mus_relative_when_none_right += 1
        if are_relative(krum_key, true_key):
            krum_relative_when_none_right += 1
        if are_relative(algo_key, true_key):
            algo_relative_when_none_right += 1

    #     0 right answers when 2 coincide
    if strictly_two_agree and not at_least_one_right:
        two_agree_none_right_num += 1
        if are_relative(krum_key, true_key):
            krum_relative_when_two_agree_none_right += 1
        elif are_closely_related(true_key, krum_key):
            krum_closely_related_when_two_agree_none_right += 1
        if are_relative(algo_key, true_key):
            algo_relative_when_two_agree_none_right += 1
        elif are_closely_related(true_key, algo_key):
            algo_closely_related_when_two_agree_none_right += 1
        if are_relative(mus_key, true_key):
            mus_relative_when_two_agree_none_right += 1
        elif are_closely_related(true_key, mus_key):
            mus_closely_related_when_two_agree_none_right += 1
    strictly_one_right = one_or_three_right and not all_right
    # 1 right answer when 2 coincide
    if strictly_one_right and strictly_two_agree:
        two_agree_one_right_num += 1
        if is_true(mus_key):
            two_agree_one_right_mus_right += 1
            if is_true(krum_key):
                two_agree_one_right_krum_right += 1
            elif are_relative(krum_key, true_key):
                krum_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, krum_key):
                krum_closely_related_when_two_agree_one_right += 1
            if is_true(algo_key):
                two_agree_one_right_algo_right += 1
            elif are_relative(algo_key, true_key):
                algo_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, algo_key):
                algo_closely_related_when_two_agree_one_right += 1
        elif is_true(krum_key):
            two_agree_one_right_krum_right += 1
            if is_true(mus_key):
                two_agree_one_right_mus_right += 1
            elif are_relative(mus_key, true_key):
                mus_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, mus_key):
                mus_closely_related_when_two_agree_one_right += 1
            if is_true(algo_key):
                two_agree_one_right_algo_right += 1
            elif are_relative(algo_key, true_key):
                algo_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, algo_key):
                algo_closely_related_when_two_agree_one_right += 1
        elif is_true(algo_key):
            two_agree_one_right_algo_right += 1
            if is_true(mus_key):
                two_agree_one_right_mus_right += 1
            elif are_relative(mus_key, true_key):
                mus_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, mus_key):
                mus_closely_related_when_two_agree_one_right += 1
            if is_true(krum_key):
                two_agree_one_right_krum_right += 1
            elif are_relative(krum_key, true_key):
                krum_relative_when_two_agree_one_right += 1
            elif are_closely_related(true_key, krum_key):
                krum_closely_related_when_two_agree_one_right += 1

f = open("output.txt", 'w')


def print_words():
    # 3 agree, 3 right
    f.write(' '.join(
        ("If all outputs agree, then they are right in",
         format(all_agree_all_right_num / all_agree_num * 100,
                ".2f") + "% of cases"
         )))
    # 3 agree, 0 right
    f.write(''.join("\nIf all outputs agree, then none is right in " +
                    format(all_agree_none_right_num / all_agree_num * 100,
                           ".2f") + "% of cases\n\tThey determined a relative key in " + format(
        all_agree_none_right_relative_num / all_agree_num * 100,
        ".2f") + "% of cases\n\tClosely related key in " + format(
        all_agree_none_right_closely_related_num / all_agree_none_right_num * 100,
        ".2f") + "% of cases\n\tSomething different in " + format(
        all_agree_none_right_something_diff / all_agree_num * 100, ".2f") + "% of cases"))
    # 2 agree, 2 right
    f.write(''.join("\nIf two outputs agree, these two outputs are right in " +
                    format(two_agree_two_right_num / strictly_two_agree_num * 100,
                           ".2f") + "% of cases. "))
    #  what about the third one?
    #  if 2 agree, music21 right?
    f.write(''.join(
        "The third one is mistaken. \n\tOverall, if two outputs agree and these two outputs are right, then music21 is right in " + format(
            two_agree_two_right_mus_right / two_agree_two_right_num * 100, ".2f")) + "% of cases")
    # if 2 agree, music21 relative?
    f.write(''.join(
        "\n\tMusic21 determined a relative key in " + format(mus_relative_when_two_agree_two_right) + "% of cases"))
    # if 2 agree, music21 closely related?
    f.write(''.join("\n\tMusic21 determined a closely related key in " + format(
        mus_closely_related_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))
    # if 2 agree, music21 something different?
    f.write(''.join("\n\tMusic21 something different in " + format(
        mus_something_diff_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))

    #  if 2 agree, Krumhansl algorithm right?
    f.write(''.join(
        "\n\t\tOverall, if two outputs agree and these two outputs are right, then Krumhansl algorithm is right in " + format(
            two_agree_two_right_krum_right / two_agree_two_right_num * 100, ".2f")) + "% of cases")
    # if 2 agree, Krumhansl algorithm relative?
    f.write(''.join(
        "\n\t\tKrumhansl algorithm determined a relative key in " + format(
            krum_relative_when_two_agree_two_right) + "% of cases"))
    # if 2 agree, Krumhansl algorithm closely related?
    f.write(''.join("\n\t\tKrumhansl algorithm determined a closely related key in " + format(
        krum_closely_related_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))
    # if 2 agree, Krumhansl something different?
    f.write(''.join("\n\t\tKrumhansl algorithm determined something different in " + format(
        krum_something_diff_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))
    #  if 2 agree, algorithm SA  right?
    f.write(''.join(
        "\n\t\t\tOverall, if two outputs agree and these two outputs are right, then algorithm SA  is right in " + format(
            two_agree_two_right_algo_right / two_agree_two_right_num * 100, ".2f")) + "% of cases")
    # if 2 agree, algorithm SA  relative?
    f.write(''.join(
        "\n\t\t\talgorithm SA  determined a relative key in " + format(
            algo_relative_when_two_agree_two_right) + "% of cases"))
    # if 2 agree, algorithm SA  closely related?
    f.write(''.join("\n\t\t\talgorithm SA  determined a closely related key in " + format(
        algo_closely_related_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))
    # if 2 agree, algorithm SA something different?
    f.write(''.join("\n\t\t\talgorithm SA  determined something different in " + format(
        algo_something_diff_when_two_agree_two_right / two_agree_two_right_num * 100, ".2f") + "% of cases"))
    # 2 agree but the third one is right
    f.write(
        ''.join("\nIf two outputs agree, the third one is right in " + format(
            two_agree_one_right_num / strictly_two_agree_num * 100,
            ".2f") + "% of cases"))
    # what's the problem with these two?

    f.write(''.join("\nIf two outputs agree, none is right in " +
                    format(two_agree_none_right_num / strictly_two_agree_num * 100,
                           ".2f") + "% of cases"))
    f.write(''.join("\nIf all outputs are different,they are all wrong in " + format(
        none_agree_none_right_num / none_agree_num * 100,
        ".2f") + "% of cases"))
    f.write(''.join("\nIf no output is the same, then there is one right output in " + format(
        none_agree_one_right / none_agree_num * 100, ".2f") + "% of cases: "))
    # mus right
    f.write(
        ''.join("\nIf no output is the same, then Music21 gives the right answer in " + format(
            none_agree_mus_right / none_agree_one_right * 100,
            ".2f") + "% of cases, if it is mistaken, then it determines a relative "
                     "key in " + format(
            mus_relative_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + "% of cases, closely related in " + format(
            mus_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + " something different in " + format(
            mus_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases"))
    f.write(''.join(
        "\nIf no output is the same, then Krumhansl gives the right answer in " + format(
            none_agree_krum_right / none_agree_one_right * 100,
            ".2f") + "% of cases, if it is mistaken, then it determines a relative key in " + format(
            krum_relative_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + "% of cases, closely related in " + format(
            krum_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + " something different in " + format(
            krum_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases"))
    f.write(''.join("\nIf no output is the same, then Algorithm SA gives the right answer in " + format(
        none_agree_algo_right / none_agree_one_right * 100,
        ".2f") + "% of cases, if it is mistaken, then it determines a relative key in " + format(
        algo_relative_when_none_agree_one_right / none_agree_one_right * 100,
        ".2f") + "% of cases, closely related in " + format(
        algo_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
        ".2f") + " something different in " + format(
        algo_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases\n\n"))


def print_table():
    f.write(''.join("\n Number of outputs " + "     Number of correct " +
                    "\nthat agree on the " + "        outputs given" +
                    "\n     answer            the number of coincidences\n"))
    f.write(''.join("    3 - " + format(all_agree_num / num_of_files * 100, ".2f") + "%               3 - " + format(
        all_agree_all_right_num / all_agree_num * 100,
        ".2f") + "%\n"))
    f.write(''.join("            " + "                 0 - " + format(all_agree_none_right_num / all_agree_num * 100,
                                                                      ".2f") + "%\n"))
    f.write(''.join(
        "    2 - " + format(strictly_two_agree_num / num_of_files * 100, ".2f") + "%               2 - " + format(
            two_agree_two_right_num / strictly_two_agree_num * 100,
            ".2f") + "%\n"))
    f.write(''.join(
        "            " + "                 1 - " + format(two_agree_one_right_num / strictly_two_agree_num * 100,
                                                          ".2f") + "%\n"))
    f.write(''.join(
        "            " + "                 0 - " + format(two_agree_none_right_num / strictly_two_agree_num * 100,
                                                          ".2f") + "%\n"))

    f.write(''.join(
        "    0 - " + format(none_agree_num / num_of_files * 100, ".2f") + "%          " + "  1 right - " + format(
            none_agree_one_right / none_agree_num * 100, ".2f") +
        "%\n                        1 (music21) - " + format(
            none_agree_mus_right / none_agree_one_right * 100,
            ".2f") + "%   relative key - " + format(mus_relative_when_none_agree_one_right / none_agree_one_right * 100,
                                                    ".2f") + "%, closely related key - " + format(
            mus_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + " something different in " + format(
            mus_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases\n"))
    f.write(
        ''.join("                       1 (Krumhansl) - " + format(none_agree_krum_right / none_agree_one_right * 100,
                                                                   ".2f") + "%   relative key - " + format(
            krum_relative_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + "% of cases, closely related in " + format(
            krum_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + "%, something different in " + format(
            krum_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases\n"))
    f.write(''.join(
        "                       1 (Algorithm SA) - " + format(none_agree_algo_right / none_agree_one_right * 100,
                                                              ".2f") + "%   relative key - " + format(
            algo_relative_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + "% of cases, closely related in " + format(
            algo_closely_related_when_none_agree_one_right / none_agree_one_right * 100,
            ".2f") + " something different in " + format(
            algo_something_diff_when_none_agree_one_right / none_agree_one_right * 100, ".2f") + "% of cases\n\n"))


print_words()
print_table()

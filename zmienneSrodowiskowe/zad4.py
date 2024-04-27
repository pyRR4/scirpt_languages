import os
import subprocess
import sys

import printFunctions


def analyze_single_file(path):
    try:
        subprocess_output = subprocess.run(['java', '-cp', 'external_file/src', 'Main', path], input=path,
                                           encoding='ascii', capture_output=True)
        return subprocess_output
    except subprocess.CalledProcessError:
        return None


def analyze_files(directory):
    files = 0
    all_chars = 0
    all_words = 0
    all_lines = 0
    all_most_used_word = ''
    all_num_of_uses_word = 0
    all_most_used_char = ''
    all_num_of_uses_char = 0

    try:
        iterator = os.scandir(directory)

        for entry in iterator:
            if entry.name.endswith(".txt"):
                file_path = os.path.join(directory, entry)
                completed_process = analyze_single_file(file_path)
                if completed_process is not None:
                    subprocess_output = completed_process.stdout.strip().split('\t')
                    files += 1

                    lines = int(subprocess_output[1])
                    all_lines += lines

                    words = int(subprocess_output[2])
                    all_words += words

                    chars = int(subprocess_output[3])
                    all_chars += chars

                    most_used_word = subprocess_output[4]
                    num_of_uses_word = int(subprocess_output[5])
                    if num_of_uses_word > all_num_of_uses_word:
                        all_most_used_word = most_used_word
                        all_num_of_uses_word = num_of_uses_word

                    most_used_char = subprocess_output[6]
                    num_of_uses_char = int(subprocess_output[7])
                    if num_of_uses_char > all_num_of_uses_char:
                        all_most_used_char = most_used_char
                        all_num_of_uses_char = num_of_uses_char
        output = {
            "Processed files: ": files,
            "Number of chars: ": all_chars,
            "Number of words: ": all_words,
            "Number of lines: ": all_lines,
            "Most used word: ": ("\"" + all_most_used_word + "\""),
            "Most used char: ": ("\"" + all_most_used_char + "\"")
        }
        printFunctions.print_dict(output, False)

    except FileNotFoundError:
        printFunctions.print_error("Nie znaleziono folderu/niepoprawna ścieżka do folderu.")
    except OSError:
        printFunctions.print_error("Niepoprawna nazwa pliku")
    except ValueError:
        printFunctions.print_error("Blad podczas analizowania pliku")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        analyze_files(sys.argv[1])
    else:
        printFunctions.print_error("Niepoprawna ilosc argumentow!")

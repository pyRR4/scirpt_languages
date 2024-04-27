import argparse
import sys

import printFunctions
import ssh_log_reader
import features


def validate_value(value):
    try:
        int_n = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("%s nie jest liczbą całkowitą" % value)
    if int_n <= 0:
        raise argparse.ArgumentTypeError("%s nie liczbą dodatnią" % value)
    return int_n


def setup_parser():
    parser = argparse.ArgumentParser(prog="Logi SSH",
                                     description="Program obsługujący logi SSH")
    parser.add_argument("path", help="Scieżka do pliku z logami - wymagana")
    parser.add_argument("-l", "--level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='DEBUG', help='Minimalny poziom logowania - opcjonalny')

    subcommand_parser = parser.add_subparsers(title='Dodatkowe funkcje', dest='subparser')
    ip_parser = subcommand_parser.add_parser(name='get_ip', help='pobierz adresy IPv4 z logów')
    user_parser = subcommand_parser.add_parser(name='get_users', help='pobierz nazwy użytkowników z logów')
    message_parser = subcommand_parser.add_parser(name="get_message_type", help='pobierz typ wiadomości wiersza')

    random_user_entries_parser = subcommand_parser.add_parser(name="get_random_entries",
                                                              help='pobierz n logów losowego użytkownika, '
                                                                   'użycie: get_random_entries n')
    random_user_entries_parser.add_argument('n', type=int, help='liczba wyświetlanych logów, liczba całkowita > 0')

    calc_time_parser = subcommand_parser.add_parser(name='calc_avg_time',
                                                    help='pobierz średni czas trwania i odchylenie'
                                                         'standardowe czasu trwania połączeń SSH '
                                                         'dla wszystkich użytkowników w sekundach')

    calc_time_parser_global = subcommand_parser.add_parser(name='calc_avg_time_global',
                                                           help='pobierz średni czas trwania i odchylenie'
                                                                'standardowe czasu trwania połączeń SSH globalnie'
                                                                'w sekundach ')

    logging_freq_parser = subcommand_parser.add_parser(name='logging_freq',
                                                       help='wyświetl użytkowników, którzy logowali '
                                                            'się najrzadziej i najczęściej')

    return parser


if __name__ == "__main__":

    # read_logs("SSH.log")
    # printFunctions.print_list_of_dict(features.random_entries(read_logs("SSH.log", False)))
    # printFunctions.print_times(features.calc_time(ssh_log_reader.read_logs("SSH.log", False)))
    # printFunctions.print_list(features.count_logins(features.get_user_logs(ssh_log_reader.read_logs("SSH.log", False))))
    parser = setup_parser()
    args = parser.parse_args()

    log_level = args.level
    if log_level is not None:
        logs = ssh_log_reader.read_logs(args.path, logger_level=log_level)
    else:
        logs = ssh_log_reader.read_logs(args.path)

    if args.subparser == "get_ip":
        printFunctions.print_list(list(ssh_log_reader.get_ip_set(logs)))

    elif args.subparser == "get_users":
        printFunctions.print_list(list(ssh_log_reader.get_user_set(logs)))

    elif args.subparser == "get_message_type":
        printFunctions.print_list(ssh_log_reader.get_messages(logs))

    elif args.subparser == "get_random_entries":
        try:
            n = validate_value(args.n)
        except argparse.ArgumentTypeError:
            printFunctions.print_error("Niepoprawny argument!")
            sys.exit(1)
        printFunctions.print_list(features.random_entries(logs, n))

    elif args.subparser == "calc_avg_time":
        printFunctions.print_times(features.calc_time(logs))
    elif args.subparser == "calc_avg_time_global":
        printFunctions.print_times(features.calc_time(logs, True))
    elif args.subparser == "logging_freq":
        printFunctions.print_dict(features.count_logins(logs), False)

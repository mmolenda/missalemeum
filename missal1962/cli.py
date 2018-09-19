
import datetime
from factory import MissalFactory
import argparse


def print_all(missal):
    for date_, lit_day_container in missal.items():
        # if not {1, 2}.intersection(set([i.rank for i in lit_day_container.all])):
        #     continue

        if date_.weekday() == 6:
            print("---")
        if date_.day == 1:
            print(f"\n\n=== {date_.month} ===\n")

        collect = []
        padding = 40
        for i in ('tempora', 'celebration', 'commemoration'):
            items = getattr(lit_day_container, i, None)
            if not items:
                collect.append('-')
            else:
                repr_ = f"[{items[0].name}:{items[0].rank}] {items[0].title}"
                if len(repr_) > padding:
                    repr_ = repr_[:padding - 3] + '…'
                collect.append(repr_)
        te, ce, co = collect
        print(f"{date_.strftime('%A %Y-%m-%d').ljust(padding)} "
              f"{te.ljust(padding)} {ce.ljust(padding)} {co.ljust(padding)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', '-y', help='A year for which the missal will be generated',
                        type=int, default=datetime.datetime.utcnow().year)
    parser.add_argument('--locale', '-l', default='pl_la')


    args = parser.parse_args()
    missal = MissalFactory.create(args.year, args.locale)
    print_all(missal)


if __name__ == "__main__":
    main()






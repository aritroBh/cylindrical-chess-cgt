from solver import headline_checks


def main():
    verdicts = headline_checks()
    failed = [row for row in verdicts if not row[2]]
    for claim, detail, passed in verdicts:
        print(f"{'PASS' if passed else 'FAIL'} {claim}: {detail}")
    assert not failed, f"{len(failed)} headline checks failed"


if __name__ == '__main__':
    main()

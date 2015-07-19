#!/usr/bin/env python

SEP = '// -- COMMON -- //'

def get_between_sep(fname, sep):
    with open(fname, 'rb') as f:
        contents = f.read()
    parts = contents.split(sep)
    assert len(parts) == 3
    return parts


def main(tplname, fname):
    parts = get_between_sep(fname, SEP)
    common = get_between_sep(tplname, SEP)[1]
    parts[1] = common
    contents = SEP.join(parts)
    with open(fname, 'wb') as f:
        f.write(contents)
    return 0


##


class ProgramError(Exception):
    pass

def run():
    from sys import argv, stderr
    try:
        exit(main(*argv[1:]) or 0)
    except ProgramError, exc:
        print >> stderr, exc
    except TypeError, exc:
        if exc.message.startswith("main() takes"):
            print >> stderr, exc
        else:
            raise

if __name__ == '__main__':
    run()

import os


def avatars_size(path: str, gigs_allowed_size: int):
    if os.path.getsize(path) > gigs_allowed_size * (1024 ** 3):
        print(f'Avatars takes too much space: more than {gigs_allowed_size} GB')
        exit()

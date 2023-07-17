import pandas as pd
from pathlib import Path


def prepare_data(in_file: Path, out_file: str) -> None:
    col = ['Time', 'Metres', 'Error Rate', 'Station 1', 'Station 2', 'cip-x']
    df = pd.DataFrame(columns=col)

    with open(in_file) as file:
        for line in file:
            row = line.split()
            if len(row) < 15:
                continue

            # Название 1 из станций с пробелом
            if len(row) == 16:
                if row[4].isdigit():
                    merge_part_list(row, 3, 5)
                else:
                    merge_part_list(row, 4, 6)

            # Название обеих станций с пробелом
            elif len(row) == 17:
                merge_part_list(row, 3, 5)
                merge_part_list(row, 5, 7)
            df.loc[len(df.index)] = row[:6]

    for i in range(3):
        df[col[i]] = df[col[i]].astype(float)

    df.to_csv(out_file, index=False)


def merge_part_list(lst: list[str], start: int, stop: int) -> None:
    mixed_str = ' '.join(lst[start:stop])
    del lst[start:stop]
    lst.insert(start, mixed_str)


dir_raw = 'raw_data'
dir_prepared = 'prepared_data'
file_num = 0

for path in Path(dir_raw).iterdir():
    file_num += 1
    out_file = '{}/{}_{}.csv'.format(dir_prepared, file_num, path.stem)
    prepare_data(path, out_file)

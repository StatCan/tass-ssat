import json
from pathlib import Path
from .conf import excel as excel


def convert(source, target):
    out = Path("scenarios").resolve() # TODO: Configurable?
    s = Path(source).resolve()

    ext = s.suffix

    if ext == '.xlsx' or ext == '.xlsm':
        jobs = excel.convert(s)
    else:
        return # TODO: raise Exception?

    created = []
    if isinstance(jobs, list) and len(jobs) > 1:
        for x in jobs:
            t = out.joinpath(target, f'{x["Job"]["title"]}--{x["Job"]["uuid"]}').with_suffix(".json").resolve()
            t.parent.mkdir(parents=True, exist_ok=True)
            with open(t, 'w+', encoding='utf-8') as f:
                json.dump(x, f, indent=4)
            created.append(str(t))
    elif isinstance(jobs, list) and len(jobs) == 1:
        t = out.joinpath(target).with_suffix(".json").resolve()
        t.mkdir(parents=True, exist_ok=True)
        with open(t, 'w+', encoding='utf-8') as f:
            json.dump(jobs[0], f, indent=4)
    elif isinstance(jobs, str):
        t = out.joinpath(target).with_suffix(".json").resolve()
        t.mkdir(parents=True, exist_ok=True)
        with open(t, 'w+', encoding='utf-8') as f:
            json.dump(jobs, f, indent=4)

        created.append(str(t))


    return created
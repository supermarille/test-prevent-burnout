import os.path
import shutil
from datetime import datetime
from unidecode import unidecode
from git import Repo
from collections import defaultdict


# Clone repository to process it
def init(repo_url:str , local_repo_path: str) -> Repo:
    if not os.path.exists(local_repo_path):
        os.makedirs(local_repo_path)
        return Repo.clone_from(repo_url, local_repo_path)
    else:
        return Repo.init(local_repo_path)


def is_weekend(date: datetime) -> bool:
    return date.weekday() > 4


def is_off_hours(date: datetime) -> bool:
    return 8 >= date.hour >= 20


# Delete cloned repository
def clean(local_repo_path: str):
    if os.path.exists(local_repo_path):
        shutil.rmtree(local_repo_path)


def get_stats(repo: Repo):
    commits = repo.iter_commits()
    name_stats = defaultdict(lambda: defaultdict(int))
    for commit in commits:
        normalized_name = unidecode(commit.author.name.upper())
        name_stats[normalized_name]['total'] += 1
        if is_weekend(commit.committed_datetime) or is_off_hours(commit.committed_datetime):
            name_stats[normalized_name]['off_work'] += 1
            name_stats[normalized_name]['rate'] = round(name_stats[normalized_name]['off_work'] / name_stats[normalized_name]['total'] * 100)

    for name, stats in name_stats.items():
        print(f"{name}: {stats['rate']}% ({stats['off_work']}/{stats['total']})")


if __name__ == '__main__':
    repo_url = "https://git.entrouvert.org/entrouvert/passerelle.git"
    local_repo_path = 'cloned_repo'

    repo = init(repo_url, local_repo_path)
    get_stats(repo)
    # clean(local_repo_path)


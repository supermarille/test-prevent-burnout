import os.path
import shutil
import argparse
from datetime import datetime, timedelta
from unidecode import unidecode
from git import Repo
from collections import defaultdict


"""
    Clone repository to process it
"""
def init(repo_url: str, local_repo_path: str) -> Repo:
    if not os.path.exists(local_repo_path):
        os.makedirs(local_repo_path)
        return Repo.clone_from(repo_url, local_repo_path)
    else:
        return Repo.init(local_repo_path)


"""
    Delete cloned repository
"""
def clean(local_repo_path: str):
    if os.path.exists(local_repo_path):
        shutil.rmtree(local_repo_path)


"""
    Process date user options
"""
def custom_date(last_week: bool, date: datetime) -> datetime | None:
    if last_week:
        return datetime.today() - timedelta(days=7)
    if date is not None:
        return date
    return None


def is_weekend(date: datetime) -> bool:
    return date.weekday() > 4


def is_off_hours(date: datetime) -> bool:
    return 8 >= date.hour >= 20


"""
    Sort by name alphabetical order.
"""
def print_sorted_by_name(name_stats: dict[str, defaultdict[str, int]]):
    sorted_names = sorted(name_stats.keys())
    for name in sorted_names:
        print(
            f"{name} : {name_stats[name]['rate']}% ({name_stats[name]['off_work']}/{name_stats[name]['total']})"
        )


"""
    Sort by decreasing rate order when applicable and the rest by reversed name order.
"""
def print_sorted_by_rate(name_stats: dict[str, defaultdict[str, int]]):
    s = sorted(name_stats.items(), key=lambda x: (x[1]["rate"], x[0]), reverse=True)
    for item in s:
        print(
            f"{item[0]} : {item[1]['rate']}% ({item[1]['off_work']}/{item[1]['total']})"
        )


"""
    Iterate on commits to count the off works submissions by author.
"""
def get_stats(
    repo: Repo, start_date: datetime | None
) -> dict[str, defaultdict[str, int]]:
    if since is None:
        commits = repo.iter_commits()
    else:
        commits = repo.iter_commits(since=start_date)
    name_stats: dict[str, defaultdict[str, int]] = {}
    for commit in commits:
        normalized_name = unidecode(commit.author.name.upper())
        if normalized_name not in name_stats.keys():
            name_stats[normalized_name] = defaultdict(int)
        name_stats[normalized_name]["total"] += 1
        if is_weekend(commit.committed_datetime) or is_off_hours(
            commit.committed_datetime
        ):
            name_stats[normalized_name]["off_work"] += 1

    for name, stats in name_stats.items():
        name_stats[name]["rate"] = round(stats["off_work"] / stats["total"] * 100)

    return name_stats


if __name__ == "__main__":
    repo_url = "https://git.entrouvert.org/entrouvert/passerelle.git"
    local_repo_path = "cloned_repo"

    # Custom date options
    parser = argparse.ArgumentParser()
    group_date = parser.add_mutually_exclusive_group()
    group_date.add_argument(
        "--last-week", action="store_true", help="Report for the last 7 days."
    )
    group_date.add_argument(
        "--since-date",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d"),
        help="Report since given date. Date format is yyyy-mm-dd.",
    )
    parser.add_argument("--by-name", action="store_true", help="Report sorted by names.")

    args = parser.parse_args()
    since = custom_date(args.last_week, args.since_date)

    repo = init(repo_url, local_repo_path)
    stats = get_stats(repo, since)
    if args.by_name:
        print_sorted_by_name(stats)
    else:
        print_sorted_by_rate(stats)
    clean(local_repo_path)

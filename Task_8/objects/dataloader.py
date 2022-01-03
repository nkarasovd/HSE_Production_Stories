from collections import namedtuple
from typing import List

import numpy as np
import pandas as pd

Issue = namedtuple("Issue", ["id", "timestamp", "summary", "description", "version"])


class Dataloader:
    def __init__(self, versions: List[int]):
        self.versions = versions
        self.issues = []

    def load_from_df(self, df: pd.DataFrame) -> 'Dataloader':
        for index, row in df.iterrows():
            if row["Affected versions"] is np.nan:
                continue
            for v in row["Affected versions"]:
                if v in self.versions:
                    issue = Issue(row["idReadable"],
                                  row["created"],
                                  row["summary"],
                                  row["description"],
                                  v)
                    self.issues.append(issue)

        return self

    def get_issues_by_version(self, version) -> List[Issue]:
        return [issue for issue in self.issues if issue.version == version]

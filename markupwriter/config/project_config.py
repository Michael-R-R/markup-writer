#!/usr/bin/python

import os

from .base_config import BaseConfig


class ProjectConfig(BaseConfig):
    dir: str = None
    projectName: str = None
    
    def init(wd: str):
        ProjectConfig.dir = None
        ProjectConfig.projectName = None
    
    def reset(wd: str):
        ProjectConfig.init(wd)
        
    def hasActiveProject() -> bool:
        return ProjectConfig.dir is not None
    
    def filePath() -> str | None:
        if ProjectConfig.dir is None:
            return None
        return os.path.join(ProjectConfig.dir, ProjectConfig.projectName)
    
    def contentPath() -> str | None:
        if ProjectConfig.dir is None:
            return None
        return os.path.join(ProjectConfig.dir, "data/content/")
# Description
In-development plain-text with rich-text previewing support novel writing application. Aims to deliver 
a distraction free presentation with easy to use in-text markup language, fast document switching, and a set of tools
to support large novel organization needs.

Inspired by <a href="https://github.com/KDE/ghostwriter">ghostwriter</a>, <a href="https://github.com/vkbo/novelWriter">novelWriter</a>, and <a href="https://github.com/NvChad/NvChad">NvChad</a>

# Showcase
<video src="https://github.com/Michael-R-R/markup-writer/assets/54217603/a6d5950c-af11-4f22-b1bc-2011abc55a86" width="320" height="200" controls preload></video>
<p align=center><img align=center src="https://github.com/Michael-R-R/markup-writer/assets/54217603/c0eccbbd-4697-44ec-bd22-a5801ee004b7"></p>
<p align=center><img align=center src="https://github.com/Michael-R-R/markup-writer/assets/54217603/fc7a7e4f-5310-4907-b62a-956d4af5922c"></p>

## Features
+ Open source
+ Free forever
+ Fast document opening/saving
+ Fast navigation
+ Vim-like editor
+ Custom markup language
+ Document reference tags
+ Multi-tab preview with support to view either plain/html text
+ Flexible document tree
+ Text search and replace functionality
+ Telescope functionality (search project files)
+ Spell correct
+ epub3 exporter
+ Plus more to come...

## Dependices
+ PyQt6 6.6.1
+ pyenchant 3.2.2
+ Python >=3.6.1

# Navigation

## Document Tree
| Mappings       | Action                                                    |
| -------------- | --------------------------------------------------------- |
| `F1`           | Focus in                                                  |
| `w`            | Previous item                                             |
| `s`            | Next item                                                 |
| `o`            | Open item                                                 |
| `p`            | Preview item                                              |


## Document Editor
| Mappings       | Action                                                    |
| -------------- | --------------------------------------------------------- |
| `F2`           | Focus in                                                  |
| `Coming soon`  | To be added                                               |

## Preview Tab
| Mappings       | Action                                                    |
| -------------- | --------------------------------------------------------- |
| `F3`           | Focus in                                                  |
| `a`            | Previous item                                             |
| `d`            | Next item                                                 |
| `h`            | Scroll content left                                       |
| `j`            | Scroll content down                                       |
| `k`            | Scroll content up                                         |
| `l`            | Scroll content right                                      |


## Telescope
| Mappings       | Action                                                    |
| -------------- | --------------------------------------------------------- |
| `Ctrl + p`     | Open telescope                                            |
| `esc`          | Close telescope                                           |
| `enter`        | Toggle search/select mode                                 |
| `w`            | Previous item (select mode)                               |
| `s`            | Next item (select mode)                                   |
| `j`            | Scroll preview down (select mode)                         |
| `k`            | Scroll preview up (select mode)                           |
| `o`            | Open file (select mode)                                   |
| `p`            | Preview file (select mode)                                |

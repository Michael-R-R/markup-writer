# Description
In-development, vim-like text editor with rich-text previewing support. Built for large novel construction. Powered by custom mark up language. Aims to deliver 
a distraction free presentation with easy to use in-text markup language, fast document switching, and a set of tools
to support large novel organization needs.

Inspired by <a href="https://github.com/KDE/ghostwriter">ghostwriter</a>, <a href="https://github.com/vkbo/novelWriter">novelWriter</a>, and <a href="https://github.com/NvChad/NvChad">NvChad</a>

No AI slop

No installation required

# Showcase (old build)
<video src="https://github.com/Michael-R-R/markup-writer/assets/54217603/eac84838-eb4f-425c-9871-9e4044077db7" width="320" height="200" controls preload></video>

## Main Window
<img width="1817" height="870" alt="main window" src="https://github.com/user-attachments/assets/59f71e34-ee7b-4c0c-ae0c-bcb19063dee4" />

## In Text Reference Highlighting
<img width="1477" height="775" alt="intext-highlight" src="https://github.com/user-attachments/assets/5da4e8ed-bade-4f8c-964d-250b1eeff3bb" />

## Main + Preview Windows
<img width="1852" height="987" alt="main + previews" src="https://github.com/user-attachments/assets/613ea974-5a2a-4ee1-8ff4-d927e1266aae" />

## Editor Tags Preview
<img width="1817" height="871" alt="editor tag preview" src="https://github.com/user-attachments/assets/9261bb51-5a21-4f68-9a11-f85b021ac1f1" />

## Telescope Preview
<img width="1819" height="870" alt="telescope" src="https://github.com/user-attachments/assets/901a57a0-7711-41bc-986f-a9ecf62b4a74" />

## EPUB Exporter
<p align=center><img align=center src="https://github.com/Michael-R-R/markup-writer/assets/54217603/fc7a7e4f-5310-4907-b62a-956d4af5922c"></p>

## Features
+ Open source
+ Free forever
+ Autosave
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

## Markup Tags
| Tag            | Description                                               |
| -------------- | --------------------------------------------------------- |
|  `@tag`        | Creates a tag that can be referenced in other documents   |
|  `@char`       | Reference a character tag (works like @ref)               |
|  `@loc`        | Reference a location tag (works like @ref)                |
|  `@ref`        | Reference a tag                                           |
|  `@title`      | Creates a Header 1                                        |
|  `@chapter`    | Creates a Header 2                                        |
|  `@scene`      | Creates a line break adding '***' to the document         |
|  `@section`    | Creates empty line break                                  |
|  `@i`          | Italicize                                                 |
|  `@b`          | Bold                                                      |
|  `@alignl`     | Align left                                                |
|  `@alignc`     | Align center                                              |
|  `@alignr`     | Align right                                               |
|  `@img`        | Import an image                                           |

## Contributions
Not accepting contributions at this time

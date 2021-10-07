FontList
==========

Quickly cycle between your favorite fonts in Sublime Text with the press of a key. Some research says that this makes you productive.

Installation
------------


Usage
-----

You can cycle through the fonts by pressing the `F10` key, and cycle backwards with `Shift+F10`.

You need to set the `font_list` key in the `FontList.sublime-settings`(<u>Preferences>Package Settings>FontList>Settings</u>) file to a list of fonts you want to cycle within. The fonts need to be **pre-installed** on the system.

You can specify just a font name or an object with the properties `font_face`, `font_size`, `line_padding_bottom`, `line_padding_top`, `word_wrap` and `wrap_width`. `font_face` is a required property on the object.

```JSON
{
  "font_list":
    [
      "Andale Mono",
      "Consolas",
      "Courier",
      "Courier New",
      "Envy Code R",
      "Inconsolata",
      "Lucida Console",
      "Menlo",
      "Meslo LG S",
      "Meslo LG M",
      "Meslo LG L",
      "Monaco",
      "ProFontX",
      "Source Code Pro",
      "Ubuntu Mono"
    ]
}
```

```JSON
{
  "font_list":
  [
    {
      "font_face": "JetBrains Mono",
      "font_size": 12,
      "line_padding_bottom": 1,
      "line_padding_top": 1,
      "word_wrap": "auto",
      "wrap_width": 80
    },
    {
      "font_face": "Georgia",
      "font_size": 15,
      "line_padding_bottom": 3,
      "line_padding_top": 3,
      "word_wrap": true,
      "wrap_width": 50
    },
    {
      "font_face": "Verdana",
      "font_size": 12,
      "line_padding_bottom": 3,
      "line_padding_top": 3,
      "word_wrap": true,
      "wrap_width": 50
    },
    {
      "font_face": "Roboto",
      "font_size": 13,
      "line_padding_bottom": 2,
      "line_padding_top": 2,
      "word_wrap": true,
      "wrap_width": 50
    }
  ]
}
```

Or even a mixed approach:

```JSON
{
  "font_list": [
    {
      "font_face": "Lucida Console",
      "line_padding_bottom": 1,
      "line_padding_top": 1
    },
    {
      "font_face": "Code New Roman",
      "line_padding_bottom": -1,
      "line_padding_top": -1
    },
    "Fira Code Retina",
    "Incolsolata"
  ]
}

```

Configuration
-------------

To change the keyboard shortcut for next and previous font, bind the
```json
{
  "command": "next_font"
}
```
and
```json
{
  "command": "next_font",
  "args": {
      "delta": -1
  }
}
```
commands respectively to the desired keys.

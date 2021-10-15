import os
import sublime
import sublime_plugin


font_attributes = (
    'font_face',
    'font_size',
    'line_padding_bottom',
    'line_padding_top',
    'word_wrap',
    'wrap_width'
)

PREFS_FILE = 'Preferences.sublime-settings'
SETTINGS_FILE = 'FontList.sublime-settings'

CURRENT_KIND = (sublime.KIND_ID_COLOR_GREENISH, "✓", "Current")


def get_font(settings):
    return { k: settings.get(k) for k in font_attributes}


def contains(font1, font2):
    return all(k in font1 and font1[k] == font2[k] for k in font2)


def get_font_list(settings, default_font):
    font_list, selected = [], -1
    for font in settings.get('font_list', []):
        if isinstance(font, str):
            font = {'font_face': font}
        elif isinstance(font, dict):
            pass
        else:
            continue
        if contains(default_font, font) and selected == -1:
            selected = len(font_list)
        font_list.append(font)

    if selected == -1:
        font_list.insert(0, default_font)
        selected = 0

    return font_list, selected


class ShowCurrentFontCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view_settings = self.view.settings()
        sublime.message_dialog(
            '\n'.join("%s: %s" % (opt, view_settings.get(opt))
                for opt in font_attributes)
            )


class NextFontCommand(sublime_plugin.WindowCommand):
    def run(self, reverse=False):
        prefs = sublime.load_settings(PREFS_FILE)
        settings = sublime.load_settings(SETTINGS_FILE)
        font_list, selected = get_font_list(settings, get_font(prefs))

        if reverse:
            font_list = font_list[selected-1:] + font_list[:selected-1]
        else:
            font_list = font_list[selected+1:] + font_list[:selected+1]

        prefs.update(font_list[0])
        settings.set('font_list', font_list)
        sublime.save_settings(PREFS_FILE)
        sublime.save_settings(SETTINGS_FILE)


class SwitchFontCommand(sublime_plugin.WindowCommand):
    def run(self, font):
        pass

    def input(self, args):
        return FontInputHandler()


class FontInputHandler(sublime_plugin.ListInputHandler):
    views = None

    def name(self):
        return 'font'

    def cancel(self):
        self.reset_views()
        self.prefs.update(self.current_font)

    def confirm(self, selected):
        font = self.font_list.pop(selected)
        font_list = [font, *self.font_list]
        self.prefs.update(font)
        self.settings.set('font_list', font_list)
        sublime.save_settings(PREFS_FILE)
        sublime.save_settings(SETTINGS_FILE)

    def preview(self, index):
        self.last_previewed = index

        def preview(index):
            # The font to preview has been updated since
            # the timeout was created
            if index != self.last_previewed:
                return
            font = self.font_list[index]
            if contains(get_font(self.prefs), font):
                return
            self.prefs.update(font)
            for v in self.overridden_views():
                v['settings'].update(font)

        sublime.set_timeout(lambda: preview(index), 250)

        return ""

    def list_items(self):
        self.window = sublime.active_window()
        self.prefs = sublime.load_settings(PREFS_FILE)
        self.settings = sublime.load_settings(SETTINGS_FILE)
        self.current_font = get_font(self.prefs)
        self.font_list, selected = get_font_list(
            self.settings, self.current_font)
        items = [
            sublime.ListInputItem(
                font.get('font_face', ''),
                i,
                details=', '.join(f'{k}: {v}' for k, v in font.items()),
                kind=CURRENT_KIND if i == selected else sublime.KIND_AMBIGUOUS)
            for i, font in enumerate(self.font_list)
        ]
        return (items, selected)

    def overridden_views(self, find=True):
        """
        :param find:
            A bool that controls if the list of views with overridden
            font face should be determined, if not already present

        :return:
            A list of dict objects containing the keys:
             - "settings": a sublime.Settings object for the view
             - "original": a string of the original "font_face" setting for the view
        """

        if self.views is None:
            if find is False:
                return []
            # If the font face hasn't been changed, we won't
            # be able to detect overrides
            if get_font(self.prefs) == self.current_font:
                return []
            vs = []
            for i in range(self.window.num_groups()):
                v = self.window.active_view_in_group(i)
                if v:
                    if self.is_view_specific(v):
                        settings = v.settings()
                        vs.append({
                            'settings': settings,
                            'original': get_font(settings)
                        })
            self.views = vs
        return self.views

    def is_view_specific(self, view):
        """
        :param view:
            A sublime.View object

        :return:
            A bool if the font_face is specific to the view
        """

        vfont = get_font(view.settings())
        return not contains(self.current_font, vfont)

    def reset_views(self):
        """
        Reset view-specific font
        """

        for v in self.overridden_views(find=False):
            v['settings'].update(v['original'])

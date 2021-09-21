import os
import sublime
import sublime_plugin

pkg_font_options = (
    'font_face',
    'font_size',
    'line_padding_bottom',
    'line_padding_top',
    'word_wrap',
    'wrap_width'
)

def update_font(delta, user_settings_file, user_settings, pkg_settings):
    font_list = pkg_settings.get('font_list', [])
    if not font_list:
        sublime.status_message("FontCycle: There is no font to choose from")
        return

    font_index = 0
    font_found = False
    font_list_length = len(font_list)
    user_font_face = user_settings.get('font_face')
    for index, font in enumerate(font_list):
        if not isinstance(font, dict):
            if type(font) != type(''):
                sublime.error_message(
                    "******************* FontCycler *******************\n"
                    "The elements of font_list must be a string or dict.")
            font_list[index] = { 'font_face': font }
        font_face = font_list[index].get('font_face')
        if not font_found and font_face == user_font_face:
            font_index = index
            font_found = True

    font_index += delta
    font_index %= font_list_length

    font = font_list[font_index]
    for key in pkg_font_options:
        if key in font and user_settings.has(key):
            user_settings.set(key, font[key])
    sublime.save_settings(user_settings_file)
    s = sublime.active_window().active_view().settings()
    sublime.status_message('Font Face: %s:%d' % (
            s.get('font_face'), s.get('font_size')))

def next_font_from_settings(delta, user_settings_file, user_settings):
    def update_current_font():
        update_font(0, user_settings_file, user_settings, pkg_settings)

    pkg_settings = sublime.load_settings('FontCycler.sublime-settings')
    update_font(delta, user_settings_file, user_settings, pkg_settings)
    pkg_settings.clear_on_change('font_list')
    pkg_settings.add_on_change('font_list', update_current_font)

def get_syntax_special_file(view_settings):
    syntax, _ = os.path.splitext(os.path.basename(view_settings.get('syntax')))
    return syntax + '.sublime-settings'


class NextFontCommand(sublime_plugin.WindowCommand):
    def run(self, delta=1):
        view_settings = self.window.active_view().settings()
        syntax_special_file = get_syntax_special_file(view_settings)
        syntax_special = sublime.load_settings(syntax_special_file)
        if syntax_special.has('font_face'):
            next_font_from_settings(delta, syntax_special_file, syntax_special)
        else:
            preferences_file = 'Preferences.sublime-settings'
            preferences = sublime.load_settings(preferences_file)
            next_font_from_settings(delta, preferences_file, preferences)


class ShowCurrentFontCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view_settings = self.view.settings()
        sublime.message_dialog(
            '\n'.join("%s: %s" % (opt, view_settings.get(opt))
                for opt in pkg_font_options)
            )

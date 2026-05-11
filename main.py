from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import threading, requests

BACKEND = "https://haniee-production.up.railway.app"
Window.clearcolor = (0.04, 0.04, 0.1, 1)

PROMPT = "Eres FREED, agente móvil del señor Estiven. Personalidad: Jefe Maestro de Halo. Directo, militar, leal. Llama siempre jefe al usuario."

class FreedApp(App):
    def build(self):
        self.title = "FREED"
        root = BoxLayout(orientation='vertical', padding=10, spacing=8)

        # Header
        header = Label(text="⚔ FREED — AGENTE MÓVIL", color=(0,1,0.53,1),
                      size_hint_y=None, height=40, font_size=18, bold=True)
        root.add_widget(header)

        # Chat area
        self.chat = Label(text="FREED: Agente en línea, jefe. ¿Cuál es la misión?\n",
                         color=(0,1,0.53,1), size_hint_y=None, font_size=13,
                         text_size=(Window.width-30, None), halign='left', valign='top')
        self.chat.bind(texture_size=self.chat.setter('size'))

        scroll = ScrollView(size_hint=(1,1))
        scroll.add_widget(self.chat)
        self.scroll = scroll
        root.add_widget(scroll)

        # Input
        inp_row = BoxLayout(size_hint_y=None, height=48, spacing=8)
        self.inp = TextInput(hint_text='Directiva para Freed...',
                            background_color=(0.1,0.1,0.2,1),
                            foreground_color=(0,1,0.53,1),
                            cursor_color=(0,1,0.53,1),
                            multiline=False, font_size=14)
        self.inp.bind(on_text_validate=self.send)

        btn = Button(text='▶', size_hint_x=None, width=48,
                    background_color=(0,0.4,0.2,1), color=(0,1,0.53,1))
        btn.bind(on_press=self.send)

        btn_v = Button(text='🤖', size_hint_x=None, width=48,
                      background_color=(0.3,0.1,0.6,1), color=(0.8,0.7,1,1))
        btn_v.bind(on_press=self.ask_viernes)

        inp_row.add_widget(self.inp)
        inp_row.add_widget(btn)
        inp_row.add_widget(btn_v)
        root.add_widget(inp_row)

        return root

    def add_msg(self, who, text, color=""):
        self.chat.text += f"\n{who}: {text}\n"
        self.scroll.scroll_y = 0

    def send(self, *a):
        msg = self.inp.text.strip()
        if not msg: return
        self.inp.text = ""
        self.add_msg("Jefe", msg)
        threading.Thread(target=self._call_freed, args=(msg,), daemon=True).start()

    def _call_freed(self, msg):
        try:
            r = requests.post(f"{BACKEND}/freed/chat",
                json={"message": msg, "context": "Android APK"},
                timeout=30)
            resp = r.json().get("response", "Sin respuesta")
        except Exception as e:
            resp = f"Error: {e}"
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.add_msg("FREED", resp), 0)

    def ask_viernes(self, *a):
        msg = self.inp.text.strip() or "Estado general"
        self.inp.text = ""
        self.add_msg("→VIERNES", msg)
        threading.Thread(target=self._call_viernes, args=(msg,), daemon=True).start()

    def _call_viernes(self, msg):
        try:
            r = requests.post(f"{BACKEND}/freed/viernes",
                json={"message": msg}, timeout=30)
            resp = r.json().get("response", "Sin respuesta")
        except Exception as e:
            resp = f"Viernes no disponible: {e}"
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.add_msg("VIERNES", resp), 0)

if __name__ == '__main__':
    FreedApp().run()

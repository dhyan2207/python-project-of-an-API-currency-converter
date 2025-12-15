
import wx
import wx.grid
from forex_python.converter import CurrencyRates
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.dates as mdates


# --- Configuration ---
# Updated Map with Emoji Flags for "Image-like" feel without external assets
CURRENCY_MAP = {
    "USD": "🇺🇸 USD - United States",
    "EUR": "🇪🇺 EUR - Eurozone",
    "GBP": "🇬🇧 GBP - United Kingdom",
    "JPY": "🇯🇵 JPY - Japan",
    "INR": "🇮🇳 INR - India",
    "CAD": "🇨🇦 CAD - Canada",
    "AUD": "🇦🇺 AUD - Australia",
    "CHF": "🇨🇭 CHF - Switzerland",
    "NZD": "🇳🇿 NZD - New Zealand",
    "ZAR": "🇿🇦 ZAR - South Africa",
    "CNY": "🇨🇳 CNY - China",
    "KRW": "🇰🇷 KRW - South Korea",
    "SGD": "🇸🇬 SGD - Singapore",
    "MXN": "🇲🇽 MXN - Mexico",
    "BRL": "🇧🇷 BRL - Brazil",
    "RUB": "🇷🇺 RUB - Russia",
    "HKD": "🇭🇰 HKD - Hong Kong",
    "SEK": "🇸🇪 SEK - Sweden",
    "NOK": "🇳🇴 NOK - Norway",
    "DKK": "🇩🇰 DKK - Denmark",
    "TRY": "🇹🇷 TRY - Turkey",
    "MYR": "🇲🇾 MYR - Malaysia",
    "THB": "🇹🇭 THB - Thailand",
    "IDR": "🇮🇩 IDR - Indonesia",
    "PLN": "🇵🇱 PLN - Poland",
    "PHP": "🇵🇭 PHP - Philippines",
    "CZK": "🇨🇿 CZK - Czech Republic",
    "HUF": "🇭🇺 HUF - Hungary",
    "ILS": "🇮🇱 ILS - Israel",
    "SAR": "🇸🇦 SAR - Saudi Arabia",
    "AED": "🇦🇪 AED - UAE",
    "CLP": "🇨🇱 CLP - Chile",
    "COP": "🇨🇴 COP - Colombia",
    "VND": "🇻🇳 VND - Vietnam"
}


class GraphDialog(wx.Dialog):
    # A popup window to display two matplotlib graphs (From vs USD and To vs USD) 
    def __init__(self, parent, from_curr, to_curr, history_from, history_to, time_frame_label):
        super().__init__(parent, title=f"Currency Trends vs USD", size=(700, 750))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))
        
        self.from_curr = from_curr
        self.to_curr = to_curr
        self.history_from = history_from
        self.history_to = history_to
        self.time_frame_label = time_frame_label
        
        self.init_ui()
        self.Center()


    def init_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)


        # Header
        lbl_title = wx.StaticText(panel, label=f"Comparison: Value of 1 USD ({self.time_frame_label})")
        lbl_title.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_title.SetForegroundColour("#202124") 
        sizer.Add(lbl_title, 0, wx.ALL | wx.CENTER, 20)


        # Figures
        self.figure, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 8), dpi=100)
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvas(panel, -1, self.figure)


        # Plot Logic
        self.plot_on_axis(self.ax1, self.from_curr, self.history_from, '#1a73e8') # Blue
        self.plot_on_axis(self.ax2, self.to_curr, self.history_to, '#d93025') # Red
        
        self.figure.tight_layout()
        self.figure.subplots_adjust(hspace=0.4)


        sizer.Add(self.canvas, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        
        btn_close = wx.Button(panel, label="Close Graph")
        btn_close.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
        sizer.Add(btn_close, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)


        panel.SetSizer(sizer)


    def plot_on_axis(self, ax, currency_code, history_data, color):
        ax.set_facecolor('white')
        dates = list(history_data.keys())
        rates = list(history_data.values())
        
        # Sort
        sorted_pairs = sorted(zip(dates, rates))
        dates = [d for d, r in sorted_pairs]
        rates = [r for d, r in sorted_pairs]


        ax.plot(dates, rates, linestyle='-', color=color, linewidth=2)
        ax.fill_between(dates, rates, color=color, alpha=0.1)
        
        ax.set_title(f"1 USD in {currency_code}", loc='left', fontsize=10, fontweight='bold', color='#5f6368')
        ax.set_ylabel("Amount per 1 USD", fontsize=9)
        ax.set_xlabel("Time", fontsize=9)


        # Styling
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', linestyle=':', color='#dadce0')
        
        if "Year" in self.time_frame_label:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        else:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            
        ax.tick_params(axis='both', colors='#5f6368', labelsize=8)



class CurrencyFrame(wx.Frame):
    def __init__(self):
        # Increased size to accommodate the card layout comfortable
        super().__init__(parent=None, title='Currency Converter', size=(450, 750))
        
        # Soft blue-grey background similar to the reference image header
        self.SetBackgroundColour(wx.Colour(240, 244, 248)) 
        
        self.c = CurrencyRates()
        self.panel = wx.Panel(self)
        
        self.init_ui()
        self.Center()
        self.Show()


    def init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --- 1. App Header ---
        header_sizer = wx.BoxSizer(wx.VERTICAL)
        
        lbl_app_name = wx.StaticText(self.panel, label="Currency Converter")
        lbl_app_name.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_app_name.SetForegroundColour("#1e3a8a") # Dark Blue
        
        lbl_sub = wx.StaticText(self.panel, label="Check live rates & analyze trends")
        lbl_sub.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT))
        lbl_sub.SetForegroundColour("#64748b") # Grey blue
        
        header_sizer.Add(lbl_app_name, 0, wx.ALIGN_CENTER | wx.TOP, 30)
        header_sizer.Add(lbl_sub, 0, wx.ALIGN_CENTER | wx.BOTTOM, 20)
        
        main_sizer.Add(header_sizer, 0, wx.EXPAND)


        # --- 2. The "Card" Container ---
        # We simulate a card by using a panel with a white background
        card_panel = wx.Panel(self.panel)
        card_panel.SetBackgroundColour(wx.Colour(255, 255, 255))
        card_sizer = wx.BoxSizer(wx.VERTICAL)


        # Common styles for input boxes
        input_bg_color = wx.Colour(243, 244, 246) # Light grey for inputs
        font_input = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        font_label = wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        # Font specifically for Emoji support on Windows
        font_emoji = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Segoe UI Emoji")


        # --- Row A: Source Currency ---
        lbl_amount = wx.StaticText(card_panel, label="Amount")
        lbl_amount.SetFont(font_label)
        lbl_amount.SetForegroundColour("#6b7280")
        card_sizer.Add(lbl_amount, 0, wx.LEFT | wx.TOP, 20)
        
        row_a_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Dropdown A
        self.combo_items = sorted(list(CURRENCY_MAP.values()))
        self.combo_from = wx.ComboBox(card_panel, choices=self.combo_items, style=wx.CB_READONLY, size=(160, 45))
        self.combo_from.SetFont(font_emoji) # Apply emoji font
        # Default USD
        idx_usd = next(i for i, s in enumerate(self.combo_items) if "USD" in s)
        self.combo_from.SetSelection(idx_usd)
        
        # Amount Input
        self.txt_amount = wx.TextCtrl(card_panel, value="1000", size=(120, 45), style=wx.TE_RIGHT | wx.BORDER_NONE)
        self.txt_amount.SetBackgroundColour(input_bg_color)
        self.txt_amount.SetFont(font_input)
        
        row_a_sizer.Add(self.combo_from, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        row_a_sizer.Add(self.txt_amount, 1, wx.EXPAND | wx.LEFT, 10)
        
        card_sizer.Add(row_a_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)


        # --- Row B: Swap Button (Centered) ---
        swap_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_swap = wx.Button(card_panel, label="⇅", size=(40, 40))
        self.btn_swap.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btn_swap.SetBackgroundColour("#1e3a8a")
        self.btn_swap.SetForegroundColour("white")
        self.btn_swap.Bind(wx.EVT_BUTTON, self.on_swap)
        
        swap_sizer.Add(self.btn_swap, 0, wx.ALIGN_CENTER)
        card_sizer.Add(swap_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 15)


        # --- Row C: Target Currency ---
        lbl_converted = wx.StaticText(card_panel, label="Converted Amount")
        lbl_converted.SetFont(font_label)
        lbl_converted.SetForegroundColour("#6b7280")
        card_sizer.Add(lbl_converted, 0, wx.LEFT, 20)


        row_c_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Dropdown B
        self.combo_to = wx.ComboBox(card_panel, choices=self.combo_items, style=wx.CB_READONLY, size=(160, 45))
        self.combo_to.SetFont(font_emoji) # Apply emoji font
        # Default EUR
        idx_eur = next(i for i, s in enumerate(self.combo_items) if "EUR" in s)
        self.combo_to.SetSelection(idx_eur)
        
        # Result Display (Simulated as Read-only TextCtrl for look)
        self.txt_result = wx.TextCtrl(card_panel, value="---", size=(120, 45), style=wx.TE_RIGHT | wx.TE_READONLY | wx.BORDER_NONE)
        self.txt_result.SetBackgroundColour(input_bg_color)
        self.txt_result.SetFont(font_input)
        self.txt_result.SetForegroundColour("#1e3a8a") # Make result blue
        
        row_c_sizer.Add(self.combo_to, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        row_c_sizer.Add(self.txt_result, 1, wx.EXPAND | wx.LEFT, 10)
        
        card_sizer.Add(row_c_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)


        # --- Row D: Indicative Rate ---
        self.lbl_rate = wx.StaticText(card_panel, label="Indicative Exchange Rate\n---")
        self.lbl_rate.SetForegroundColour("#6b7280")
        self.lbl_rate.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        card_sizer.Add(self.lbl_rate, 0, wx.ALL | wx.LEFT, 20)
        
        # --- Bottom of Card: Convert Button ---
        self.btn_convert = wx.Button(card_panel, label="Convert Now", size=(-1, 50))
        self.btn_convert.SetBackgroundColour("#1e3a8a")
        self.btn_convert.SetForegroundColour("white")
        self.btn_convert.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self.btn_convert.Bind(wx.EVT_BUTTON, self.on_convert)
        
        card_sizer.Add(self.btn_convert, 0, wx.EXPAND | wx.ALL, 20)


        card_panel.SetSizer(card_sizer)
        
        # Add Card to Main Sizer with some padding (margin)
        main_sizer.Add(card_panel, 0, wx.EXPAND | wx.ALL, 20)


        # --- 3. Footer / Trends Section ---
        footer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.time_options = ["1 Week", "1 Month", "1 Year", "5 Years", "10 Years"]
        self.combo_time = wx.ComboBox(self.panel, choices=self.time_options, style=wx.CB_READONLY, size=(120, 35))
        self.combo_time.SetSelection(1) # Default 1 Month
        
        self.btn_graph = wx.Button(self.panel, label="View Trend Graph", size=(150, 35))
        self.btn_graph.Bind(wx.EVT_BUTTON, self.on_show_graph)
        
        footer_sizer.Add(self.combo_time, 0, wx.RIGHT, 10)
        footer_sizer.Add(self.btn_graph, 0, wx.LEFT, 10)
        
        main_sizer.Add(footer_sizer, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)


        self.panel.SetSizer(main_sizer)


    def get_code_from_selection(self, selection):
        # Extracts "USD" from "🇺🇸 USD - United States"
        if selection:
            parts = selection.split(" ")
            if len(parts) > 1:
                return parts[1] # The code is usually the second element
        return None


    def on_swap(self, event):
        # Swap indices
        idx_from = self.combo_from.GetSelection()
        idx_to = self.combo_to.GetSelection()
        self.combo_from.SetSelection(idx_to)
        self.combo_to.SetSelection(idx_from)
        # Trigger convert update if there is a value
        if self.txt_amount.GetValue():
            self.on_convert(None)


    def on_convert(self, event):
        try:
            amount_str = self.txt_amount.GetValue()
            if not amount_str:
                return


            from_sel = self.combo_from.GetValue()
            to_sel = self.combo_to.GetValue()
            
            from_code = self.get_code_from_selection(from_sel)
            to_code = self.get_code_from_selection(to_sel)


            amount = float(amount_str)
            
            self.SetCursor(wx.Cursor(wx.CURSOR_WAIT))
            
            rate = self.c.get_rate(from_code, to_code)
            result = amount * rate
            
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))


            self.txt_result.SetValue(f"{result:.2f}")
            self.lbl_rate.SetLabel(f"Indicative Exchange Rate\n1 {from_code} = {rate:.4f} {to_code}")
            
            self.panel.Layout()


        except ValueError:
            wx.MessageBox("Please enter a valid numeric amount.", "Input Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            wx.MessageBox(f"Error: {str(e)}", "Connection Error", wx.OK | wx.ICON_ERROR)


    def on_show_graph(self, event):
        from_sel = self.combo_from.GetValue()
        to_sel = self.combo_to.GetValue()
        from_code = self.get_code_from_selection(from_sel)
        to_code = self.get_code_from_selection(to_sel)
        time_frame = self.combo_time.GetValue()
        
        # Logic to determine days and step
        days_to_fetch = 30
        step = 2
        if time_frame == "1 Week": days_to_fetch, step = 7, 1
        elif time_frame == "1 Month": days_to_fetch, step = 30, 2
        elif time_frame == "1 Year": days_to_fetch, step = 365, 7
        elif time_frame == "5 Years": days_to_fetch, step = 365*5, 30
        elif time_frame == "10 Years": days_to_fetch, step = 365*10, 60


        busy = wx.BusyInfo(f"Fetching data for {from_code} & {to_code}...")
        
        try:
            today = datetime.date.today()
            history_from = {}
            history_to = {}
            
            for i in range(days_to_fetch, -1, -step):
                d = today - datetime.timedelta(days=i)
                # Rate vs USD (Fixed: Now gets "Amount of X per 1 USD")
                if from_code == "USD": r1 = 1.0
                else: r1 = self.c.get_rate("USD", from_code, d)
                
                if to_code == "USD": r2 = 1.0
                else: r2 = self.c.get_rate("USD", to_code, d)
                
                history_from[d] = r1
                history_to[d] = r2
            
            del busy 
            dlg = GraphDialog(self, from_code, to_code, history_from, history_to, time_frame)
            dlg.ShowModal()
            dlg.Destroy()


        except Exception as e:
            del busy
            wx.MessageBox(f"Graph Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


# --- Execution ---
if __name__ == '__main__':
    app = wx.App()
    frame = CurrencyFrame()
    app.MainLoop()

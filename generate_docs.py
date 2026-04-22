from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem

# ── Output path ──────────────────────────────────────────────────────────────
OUTPUT = "/sessions/trusting-ecstatic-hypatia/mnt/react-crypto-tracker-master/CryptoHunter_Project_Documentation.pdf"

# ── Colour palette ───────────────────────────────────────────────────────────
GOLD        = colors.HexColor("#EEBC1D")
DARK_BG     = colors.HexColor("#14161a")
DARK2       = colors.HexColor("#1e2128")
LIGHT_GOLD  = colors.HexColor("#FFF3CD")
CODE_BG     = colors.HexColor("#1e2128")
WHITE       = colors.white
GREY        = colors.HexColor("#888888")
GREEN       = colors.HexColor("#0ECB81")
RED         = colors.HexColor("#F44336")

W, H = A4

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    """Clone an existing style with overrides."""
    parent = base.get(name, base["Normal"])
    s = ParagraphStyle(name + str(id(kw)), parent=parent, **kw)
    return s

cover_title   = S("Title", fontSize=38, textColor=GOLD, alignment=TA_CENTER,
                   fontName="Helvetica-Bold", leading=46, spaceAfter=8)
cover_sub     = S("Normal", fontSize=16, textColor=WHITE, alignment=TA_CENTER,
                   fontName="Helvetica", leading=22, spaceAfter=4)
cover_meta    = S("Normal", fontSize=11, textColor=GREY, alignment=TA_CENTER,
                   fontName="Helvetica", leading=16)

h1 = S("Heading1", fontSize=22, textColor=GOLD, fontName="Helvetica-Bold",
        spaceBefore=18, spaceAfter=8, leading=28)
h2 = S("Heading2", fontSize=16, textColor=GOLD, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6, leading=22)
h3 = S("Heading3", fontSize=13, textColor=LIGHT_GOLD, fontName="Helvetica-Bold",
        spaceBefore=10, spaceAfter=4, leading=18)
h4 = S("Heading4", fontSize=11, textColor=LIGHT_GOLD, fontName="Helvetica-BoldOblique",
        spaceBefore=8, spaceAfter=3, leading=16)

body = S("Normal", fontSize=10, textColor=WHITE, fontName="Helvetica",
          leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
body_left = S("Normal", fontSize=10, textColor=WHITE, fontName="Helvetica",
               leading=16, spaceAfter=6)
bullet_s = S("Normal", fontSize=10, textColor=WHITE, fontName="Helvetica",
              leading=15, spaceAfter=3, leftIndent=12)
code_s = S("Code", fontSize=9, textColor=colors.HexColor("#F8F8F2"),
            fontName="Courier", leading=13, spaceAfter=4,
            backColor=CODE_BG, leftIndent=10, rightIndent=10,
            borderPadding=(4, 6, 4, 6))
note_s = S("Normal", fontSize=9, textColor=GOLD, fontName="Helvetica-Oblique",
            leading=13, spaceAfter=4, leftIndent=8)
label_s = S("Normal", fontSize=9, textColor=GREY, fontName="Helvetica",
             leading=13)
tag_s = S("Normal", fontSize=9, textColor=GREEN, fontName="Courier-Bold",
           leading=13)

# ── Helpers ───────────────────────────────────────────────────────────────────
def HR():
    return HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8, spaceBefore=4)

def SP(h=6):
    return Spacer(1, h)

def P(text, style=body):
    return Paragraph(text, style)

def Bul(items, style=bullet_s):
    """Render a list of strings as bullet paragraphs."""
    out = []
    for it in items:
        out.append(Paragraph(f"&#8226;  {it}", style))
    return out

def Code(text):
    lines = text.strip("\n")
    # Escape < and > so ReportLab doesn't try to parse JSX/HTML as XML tags
    lines = lines.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return Paragraph(lines.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_s)

def FileHeader(filename, role):
    """Coloured banner for each file section."""
    data = [[filename, role]]
    t = Table(data, colWidths=[6*cm, 10.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK2),
        ("TEXTCOLOR",  (0,0), (0,0),   GOLD),
        ("TEXTCOLOR",  (1,0), (1,0),   WHITE),
        ("FONTNAME",   (0,0), (0,0),   "Helvetica-Bold"),
        ("FONTNAME",   (1,0), (1,0),   "Helvetica"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("ROWPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("BOX",        (0,0), (-1,-1), 1, GOLD),
    ]))
    return t

def ConceptBox(title, explanation):
    data = [[title], [explanation]]
    t = Table(data, colWidths=[16.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), GOLD),
        ("BACKGROUND", (0,1), (0,1), DARK2),
        ("TEXTCOLOR",  (0,0), (0,0), DARK_BG),
        ("TEXTCOLOR",  (0,1), (0,1), WHITE),
        ("FONTNAME",   (0,0), (0,0), "Helvetica-Bold"),
        ("FONTNAME",   (0,1), (0,1), "Helvetica"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("ROWPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("BOX",        (0,0), (-1,-1), 0.5, GOLD),
    ]))
    return t

def flow_table(rows):
    """Two-column table: step | description."""
    t = Table(rows, colWidths=[4.5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,-1), GOLD),
        ("BACKGROUND",   (1,0), (1,-1), DARK2),
        ("TEXTCOLOR",    (0,0), (0,-1), DARK_BG),
        ("TEXTCOLOR",    (1,0), (1,-1), WHITE),
        ("FONTNAME",     (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",     (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWPADDING",   (0,0), (-1,-1), 6),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("GRID",         (0,0), (-1,-1), 0.3, GREY),
        ("BOX",          (0,0), (-1,-1), 0.8, GOLD),
    ]))
    return t

# ── Document setup ───────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm,  bottomMargin=2*cm,
    title="Crypto Hunter – Project Documentation",
    author="Claude / Cowork",
)

story = []

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    SP(60),
    P("Crypto Hunter", cover_title),
    SP(6),
    P("React Project – Complete Beginner's Documentation", cover_sub),
    SP(16),
    HR(),
    SP(10),
    P("Everything you need to understand this project after 30 days away", cover_meta),
    SP(4),
    P("File-by-file breakdown  •  React concepts  •  Sequential workflow  •  Code walkthroughs", cover_meta),
    SP(60),
    P("Prepared for: ajet  |  Stack: React, React Router, Material-UI, CoinGecko API, Chart.js", cover_meta),
    PageBreak(),
]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — WHAT IS THIS PROJECT?
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("1. What Is This Project?", h1), HR(),
    P("""Crypto Hunter is a <b>cryptocurrency tracking web application</b> built with React. It lets users see
live prices for the top 100 cryptocurrencies, browse trending coins, switch between USD and INR,
and click any coin to explore a detailed page with a historical price chart.""", body),
    SP(),
    P("What you can do in the app:", h3),
    *Bul([
        "See the top 100 coins ranked by market capitalisation with live prices.",
        "Search/filter coins by name or symbol.",
        "Switch currency between USD ($ ) and INR (&#8377;) from the header.",
        "Watch a scrolling carousel of the top trending coins at the top of the homepage.",
        "Click any coin row to open its detail page showing a price chart.",
        "On the detail page, switch the chart between 24 hours, 30 days, 3 months, and 1 year.",
    ]),
    SP(10),
    P("Technology Stack", h3),
]

tech_rows = [
    ["Technology", "What it does in this project"],
    ["React 17",        "Core UI library – builds the interface from reusable components"],
    ["React Router DOM","Handles page navigation without reloading the browser"],
    ["Material-UI (MUI)","Pre-built styled components (AppBar, Table, Typography, etc.)"],
    ["Axios",           "Makes HTTP requests to the CoinGecko API"],
    ["Chart.js / react-chartjs-2", "Draws the interactive historical price line chart"],
    ["react-alice-carousel", "Scrolling carousel widget for trending coins"],
    ["react-html-parser", "Safely renders HTML from the API's coin description text"],
    ["CoinGecko API",   "Free public API that provides all cryptocurrency data"],
]
t = Table(tech_rows, colWidths=[5.5*cm, 11*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), GOLD),
    ("BACKGROUND",  (0,1), (-1,-1), DARK2),
    ("TEXTCOLOR",   (0,0), (-1,0), DARK_BG),
    ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWPADDING",  (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("GRID",        (0,0), (-1,-1), 0.3, GREY),
    ("BOX",         (0,0), (-1,-1), 0.8, GOLD),
]))
story += [t, PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — REACT CONCEPTS FOR BEGINNERS
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("2. React Concepts Used — Beginner Primer", h1), HR(),
    P("""Before diving into files, here is a plain-English explanation of every React feature
this project uses. Refer back here whenever you see unfamiliar syntax.""", body),
    SP(8),
]

concepts = [
    ("Component",
     "A JavaScript function that returns HTML-like code (JSX). Think of it as a reusable "
     "lego brick. Every file in src/components/ and src/Pages/ is a component. "
     "Example: Banner() is a component that returns the hero image section."),
    ("JSX",
     "Looks like HTML written inside JavaScript. React converts it to real browser DOM. "
     "Angle brackets like <Typography> or <div> inside a .js file are JSX."),
    ("useState",
     "A React hook that stores data inside a component and re-renders the UI whenever "
     "that data changes. Syntax: const [value, setValue] = useState(initialValue). "
     "Used everywhere — CoinsTable stores the coin list, CoinInfo stores selected days, etc."),
    ("useEffect",
     "A React hook that runs code AFTER the component appears on screen. "
     "Used to fetch data from APIs. The [] at the end means 'run only once on mount'. "
     "If you put [currency] it means 're-run whenever currency changes'."),
    ("Props",
     "Short for 'properties'. Data passed from a parent component down to a child. "
     "Like function arguments. Example: <CoinInfo coin={coin} /> passes the coin object "
     "to CoinInfo as a prop."),
    ("Context API",
     "A way to share data across ALL components without passing props through every level. "
     "CryptoContext stores currency and symbol globally. Any component can read it with "
     "the CryptoState() function."),
    ("React Router (useHistory / useParams / Link / Route)",
     "Lets the app show different 'pages' by changing the URL without a real page reload. "
     "useHistory().push('/coins/bitcoin') navigates to a coin page. "
     "useParams() reads the :id from the URL. "
     "<Route path='/coins/:id' component={CoinPage} /> maps a URL pattern to a component."),
    ("makeStyles / ThemeProvider",
     "Material-UI's way of writing CSS inside JavaScript. makeStyles returns a hook "
     "that gives you class names. ThemeProvider sets a dark/light theme for all MUI components inside it."),
    ("Axios",
     "A library to call HTTP APIs. axios.get(url) sends a GET request and returns the response. "
     "The { data } destructuring pulls out the .data field from the response object."),
    ("async / await",
     "Modern JavaScript syntax for handling asynchronous operations (like API calls) "
     "without getting into messy .then() chains. await pauses until the API responds."),
]

for title, explanation in concepts:
    story += [ConceptBox(title, explanation), SP(6)]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — FILE STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("3. Project File Structure", h1), HR(),
    P("Every file and what layer it belongs to:", body),
    SP(6),
    Code(
        "react-crypto-tracker-master/\n"
        "├── public/\n"
        "│   ├── index.html          ← The ONE real HTML page (SPA shell)\n"
        "│   └── banner2.jpg         ← Hero background image\n"
        "└── src/\n"
        "    ├── index.js            ← App entry point – mounts React into index.html\n"
        "    ├── CryptoContext.js    ← Global state (currency, symbol)\n"
        "    ├── App.js              ← Router setup + page routes\n"
        "    ├── config/\n"
        "    │   ├── api.js          ← All API URL functions\n"
        "    │   └── data.js         ← Static data (chart day buttons)\n"
        "    ├── Pages/\n"
        "    │   ├── HomePage.js     ← Route '/' → Banner + CoinsTable\n"
        "    │   └── CoinPage.js     ← Route '/coins/:id' → Coin detail\n"
        "    └── components/\n"
        "        ├── Header.js       ← Top navigation bar (always visible)\n"
        "        ├── CoinsTable.js   ← Table of 100 coins with search & pagination\n"
        "        ├── CoinInfo.js     ← Historical price chart + day selector\n"
        "        ├── SelectButton.js ← Reusable gold button (24h/30d/3m/1y)\n"
        "        └── Banner/\n"
        "            ├── Banner.js   ← Hero section wrapper\n"
        "            └── Carousel.js ← Auto-scrolling trending coins strip"
    ),
    PageBreak(),
]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — SEQUENTIAL WORKFLOW
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("4. Application Workflow — Sequential Order", h1), HR(),
    P("4.1  When the app first loads (URL = '/')", h2),
    SP(4),
    flow_table([
        ["Step 1\nindex.js",    "React boots up. ReactDOM.render() injects the entire app into the <div id='root'> "
                                "inside public/index.html. CryptoContext wraps App so global state is available everywhere."],
        ["Step 2\nCryptoContext", "Initialises currency='INR' and symbol='₹'. These values are now accessible "
                                  "by any component in the tree via CryptoState()."],
        ["Step 3\nApp.js",      "BrowserRouter activates. Header always renders. React Router reads the current URL. "
                                "URL is '/' → HomePage component is mounted."],
        ["Step 4\nHomePage.js", "Renders two children: Banner and CoinsTable, stacked vertically."],
        ["Step 5\nBanner.js",   "Renders the hero section with the background image and the tagline text. "
                                "Also renders the Carousel component inside it."],
        ["Step 6\nCarousel.js", "useEffect fires → axios.get(TrendingCoins) hits the CoinGecko API → "
                                "stores top 10 trending coins in state → renders them as clickable "
                                "AliceCarousel items that auto-scroll."],
        ["Step 7\nCoinsTable.js","useEffect fires → axios.get(CoinList) hits the CoinGecko API → stores "
                                 "100 coins in state → renders the searchable, paginated table."],
        ["Step 8\nHeader.js",   "Renders the AppBar with the 'Crypto Hunter' logo and the USD/INR dropdown."],
    ]),
    SP(14),
    P("4.2  When the user clicks a coin row", h2),
    SP(4),
    flow_table([
        ["Click event\nCoinsTable.js", "onClick on the TableRow calls history.push('/coins/bitcoin'). "
                                       "No page reload — React Router intercepts it."],
        ["Route match\nApp.js",        "React Router sees the new URL '/coins/bitcoin'. It matches "
                                       "the <Route path='/coins/:id'> rule and mounts CoinPage."],
        ["useParams\nCoinPage.js",     "useParams() extracts the string 'bitcoin' from the URL as { id }."],
        ["API call\nCoinPage.js",      "useEffect fires → axios.get(SingleCoin('bitcoin')) → stores full "
                                       "coin object in state → renders sidebar with image, name, "
                                       "description, rank, price, and market cap."],
        ["CoinInfo\nCoinInfo.js",      "CoinPage passes the coin object as a prop. CoinInfo calls "
                                       "HistoricalChart API for 1 day by default → renders the "
                                       "gold line chart via react-chartjs-2."],
        ["SelectButton\nCoinInfo.js",  "Four SelectButton components render below the chart. Clicking one "
                                       "updates the 'days' state → useEffect re-fires → fetches new "
                                       "historical data → chart redraws."],
    ]),
    SP(14),
    P("4.3  When the user changes currency", h2),
    SP(4),
    flow_table([
        ["Select change\nHeader.js",   "User picks USD from the dropdown. onChange calls setCurrency('USD') "
                                       "from CryptoContext."],
        ["Context update\nCryptoContext", "currency state changes to 'USD', symbol changes to '$'. "
                                          "Every component that reads CryptoState() automatically re-renders."],
        ["Re-fetch\nCarousel.js",      "useEffect has [currency] as dependency → re-fetches trending coins "
                                       "in USD and re-renders the carousel with new prices."],
        ["Re-fetch\nCoinsTable.js",    "useEffect has [currency] as dependency → re-fetches all 100 coins "
                                       "in USD and re-renders the table."],
    ]),
    PageBreak(),
]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — FILE BY FILE BREAKDOWN
# ═══════════════════════════════════════════════════════════════════════════════
story += [P("5. File-by-File Breakdown", h1), HR()]

# ─── 5.1 index.js ─────────────────────────────────────────────────────────────
story += [
    FileHeader("src/index.js", "Application Entry Point"),
    SP(6),
    P("What is this file?", h3),
    P("""This is the very first JavaScript file that runs when the browser loads the app.
It has one job: take your entire React application and inject it into the real HTML page
(public/index.html). Without this file, React has nowhere to attach itself.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    P("Nothing visible directly — it is the launcher. It connects React to the browser.", body),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "ReactDOM.render(\n"
        "  <React.StrictMode>\n"
        "    <CryptoContext>\n"
        "      <App />\n"
        "    </CryptoContext>\n"
        "  </React.StrictMode>,\n"
        "  document.getElementById('root')\n"
        ");"
    ),
    *Bul([
        "<b>ReactDOM.render()</b> — Mounts React onto the page. Everything inside the first argument becomes visible in the browser.",
        "<b>React.StrictMode</b> — A development helper that warns you about potential problems. Has no visual effect.",
        "<b>CryptoContext</b> — Wraps the entire app so currency and symbol are available everywhere.",
        "<b>App /</b> — Your root component. All pages, headers, and routes live inside here.",
        "<b>document.getElementById('root')</b> — Finds the &lt;div id='root'&gt; in public/index.html and puts React inside it.",
    ]),
    P("React features used: ReactDOM.render, Context wrapping.", note_s),
    HR(), SP(6),
]

# ─── 5.2 CryptoContext.js ────────────────────────────────────────────────────
story += [
    FileHeader("src/CryptoContext.js", "Global State – Currency & Symbol"),
    SP(6),
    P("What is this file?", h3),
    P("""This file creates a global 'data store' using React's Context API.
Instead of passing currency and symbol as props through every single component,
any component can simply call CryptoState() to get the current currency and the matching symbol.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    P("Nothing visible. It is purely a data provider that wraps the whole app.", body),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "const Crypto = createContext();\n\n"
        "const CryptoContext = ({ children }) => {\n"
        "  const [currency, setCurrency] = useState('INR');\n"
        "  const [symbol, setSymbol]     = useState('₹');\n\n"
        "  useEffect(() => {\n"
        "    if (currency === 'INR') setSymbol('₹');\n"
        "    else if (currency === 'USD') setSymbol('$');\n"
        "  }, [currency]);\n\n"
        "  return (\n"
        "    <Crypto.Provider value={{ currency, setCurrency, symbol }}>\n"
        "      {children}\n"
        "    </Crypto.Provider>\n"
        "  );\n"
        "};"
    ),
    *Bul([
        "<b>createContext()</b> — Creates the global container. Think of it as an empty box that will hold shared data.",
        "<b>useState('INR')</b> — Default currency is INR. useState('&#8377;') sets default symbol.",
        "<b>useEffect([currency])</b> — Watches currency. When it changes, automatically updates the symbol to match.",
        "<b>Crypto.Provider value={...}</b> — Broadcasts currency, setCurrency, and symbol to all children.",
        "<b>export const CryptoState = () => useContext(Crypto)</b> — A shortcut function. "
        "Any component calls CryptoState() to read the shared values.",
    ]),
    P("React features used: createContext, useContext, useState, useEffect.", note_s),
    HR(), SP(6),
]

# ─── 5.3 App.js ──────────────────────────────────────────────────────────────
story += [
    FileHeader("src/App.js", "Router + Layout Shell"),
    SP(6),
    P("What is this file?", h3),
    P("""App.js is the layout controller of the entire application. It sets up React Router
(the system that shows different pages based on the URL) and always renders the Header.
Think of it as the building's main corridor — the Header is always on every floor,
and the rooms you enter depend on which URL you navigate to.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "Always: the Header (navigation bar at the top).",
        "At URL '/': the Homepage component (Banner + CoinsTable).",
        "At URL '/coins/:id': the CoinPage component (coin detail + chart).",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "<BrowserRouter>\n"
        "  <div className={classes.App}>   ← Black background wrapper\n"
        "    <Header />                    ← Always rendered on every page\n"
        "    <Route path='/' component={Homepage} exact />\n"
        "    <Route path='/coins/:id' component={CoinPage} exact />\n"
        "  </div>\n"
        "</BrowserRouter>"
    ),
    *Bul([
        "<b>BrowserRouter</b> — Activates React Router for the whole app.",
        "<b>className={classes.App}</b> — Applies the dark background (#14161a) and minimum full-screen height.",
        "<b>Header /</b> — Renders on every page, every time. It is outside the Route tags intentionally.",
        "<b>Route path='/' exact</b> — Only shows Homepage when the URL is exactly '/'. The 'exact' prevents it matching '/coins/bitcoin' too.",
        "<b>Route path='/coins/:id'</b> — :id is a dynamic segment. '/coins/bitcoin', '/coins/ethereum' all match this same route.",
    ]),
    P("React features used: React Router (BrowserRouter, Route), makeStyles.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ─── 5.4 Header.js ───────────────────────────────────────────────────────────
story += [
    FileHeader("src/components/Header.js", "Navigation Bar"),
    SP(6),
    P("What is this file?", h3),
    P("""The Header is the top navigation bar visible on every page of the app.
It shows the app name 'Crypto Hunter' on the left (which also acts as a home button)
and a currency selector dropdown on the right.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "A dark AppBar (navigation bar) spanning the full width.",
        "'Crypto Hunter' text in gold on the left — clicking it navigates back to the homepage.",
        "A dropdown on the right to switch between USD and INR.",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "const { currency, setCurrency } = CryptoState();\n"
        "const history = useHistory();\n\n"
        "// Logo click → go home\n"
        "<Typography onClick={() => history.push('/')} ...>\n"
        "  Crypto Hunter\n"
        "</Typography>\n\n"
        "// Currency dropdown\n"
        "<Select value={currency} onChange={(e) => setCurrency(e.target.value)}>\n"
        "  <MenuItem value={'USD'}>USD</MenuItem>\n"
        "  <MenuItem value={'INR'}>INR</MenuItem>\n"
        "</Select>"
    ),
    *Bul([
        "<b>CryptoState()</b> — Reads the current currency and the setCurrency updater from the global context.",
        "<b>useHistory()</b> — Gives access to the router so history.push('/') navigates to the homepage.",
        "<b>Typography onClick</b> — The title text is a clickable home button. No separate &lt;a&gt; tag needed.",
        "<b>Select / MenuItem</b> — Material-UI dropdown. When user selects USD, onChange fires setCurrency('USD'), "
        "updating the global context and triggering re-fetches in Carousel and CoinsTable.",
        "<b>ThemeProvider darkTheme</b> — Wraps the AppBar in a dark Material-UI theme so it renders with dark styling.",
    ]),
    P("React features used: useHistory (React Router), Context (CryptoState), makeStyles, Material-UI components.", note_s),
    HR(), SP(6),
]

# ─── 5.5 config/api.js ───────────────────────────────────────────────────────
story += [
    FileHeader("src/config/api.js", "API URL Factory Functions"),
    SP(6),
    P("What is this file?", h3),
    P("""A simple utility file that exports four functions — each returns a CoinGecko API URL
string. Centralising URLs here means if the API ever changes, you only update one place.""", body),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "// Top 100 coins by market cap\n"
        "export const CoinList = (currency) =>\n"
        "  `https://api.coingecko.com/api/v3/coins/markets\n"
        "   ?vs_currency=${currency}&order=market_cap_desc&per_page=100`;\n\n"
        "// Single coin full details\n"
        "export const SingleCoin = (id) =>\n"
        "  `https://api.coingecko.com/api/v3/coins/${id}`;\n\n"
        "// Historical price data for the chart\n"
        "export const HistoricalChart = (id, days, currency) =>\n"
        "  `https://api.coingecko.com/api/v3/coins/${id}/market_chart\n"
        "   ?vs_currency=${currency}&days=${days}`;\n\n"
        "// Trending coins carousel\n"
        "export const TrendingCoins = (currency) =>\n"
        "  `https://api.coingecko.com/api/v3/coins/markets\n"
        "   ?vs_currency=${currency}&order=gecko_desc&per_page=10`;"
    ),
    *Bul([
        "<b>CoinList(currency)</b> — Called by CoinsTable. Returns 100 coins sorted by market cap in the given currency.",
        "<b>SingleCoin(id)</b> — Called by CoinPage. Returns all details for one specific coin.",
        "<b>HistoricalChart(id, days, currency)</b> — Called by CoinInfo. Returns price history as an array of [timestamp, price] pairs.",
        "<b>TrendingCoins(currency)</b> — Called by Carousel. Returns 10 trending coins sorted by CoinGecko's own trend score.",
    ]),
    P("No React features — pure JavaScript template literals.", note_s),
    HR(), SP(6),
]

# ─── 5.6 config/data.js ──────────────────────────────────────────────────────
story += [
    FileHeader("src/config/data.js", "Static Data – Chart Day Options"),
    SP(6),
    P("What is this file?", h3),
    P("""Exports a single array called chartDays. This is the data behind the four time-range
buttons (24 Hours, 30 Days, 3 Months, 1 Year) on the coin detail chart.""", body),
    SP(4),
    Code(
        "export const chartDays = [\n"
        "  { label: '24 Hours', value: 1   },\n"
        "  { label: '30 Days',  value: 30  },\n"
        "  { label: '3 Months', value: 90  },\n"
        "  { label: '1 Year',   value: 365 },\n"
        "];"
    ),
    *Bul([
        "Each object has a <b>label</b> (displayed on the button) and a <b>value</b> (number of days passed to the API).",
        "CoinInfo loops over this array with .map() to render four SelectButton components.",
        "Keeping this here (not hardcoded in CoinInfo) makes it easy to add or remove time ranges.",
    ]),
    P("No React features — pure static JavaScript data.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ─── 5.7 Pages/HomePage.js ───────────────────────────────────────────────────
story += [
    FileHeader("src/Pages/HomePage.js", "Home Page (Route '/')"),
    SP(6),
    P("What is this file?", h3),
    P("""HomePage is the page you see when you first open the app.
It is a simple wrapper component — it has no logic of its own. Its only job is to
stack two components on screen: the Banner hero section on top, and the CoinsTable below.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "The full-width banner with background image, title, subtitle, and the trending carousel.",
        "The coins table with search bar and paginated list of 100 cryptocurrencies.",
    ]),
    SP(4),
    Code(
        "const Homepage = () => {\n"
        "  return (\n"
        "    <>\n"
        "      <Banner />      ← Hero section\n"
        "      <CoinsTable />  ← Coins list\n"
        "    </>\n"
        "  );\n"
        "};"
    ),
    *Bul([
        "<b>&lt;&gt; ... &lt;/&gt;</b> — React Fragment. Groups two elements without adding a real &lt;div&gt; to the DOM.",
        "No state, no API calls, no logic here — it delegates everything to Banner and CoinsTable.",
    ]),
    P("React features used: Functional component, React Fragment.", note_s),
    HR(), SP(6),
]

# ─── 5.8 Banner/Banner.js ────────────────────────────────────────────────────
story += [
    FileHeader("src/components/Banner/Banner.js", "Hero Section"),
    SP(6),
    P("What is this file?", h3),
    P("""Banner renders the large hero section at the top of the homepage — the area with
the background image, the 'Crypto Hunter' heading, the subtitle, and the scrolling
trending coins strip (Carousel).""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "A full-width 400px-tall section with the banner2.jpg background image.",
        "Large bold 'Crypto Hunter' heading in white.",
        "A grey subtitle: 'Get all the Info regarding your favorite Crypto Currency'.",
        "The auto-scrolling Carousel of trending coins in the lower half.",
    ]),
    SP(4),
    Code(
        "// Background image applied via CSS class\n"
        "banner: { backgroundImage: 'url(./banner2.jpg)' }\n\n"
        "// Layout: 400px tall, split into tagline (top 40%) and carousel (bottom 50%)\n"
        "bannerContent: { height: 400, flexDirection: 'column', justifyContent: 'space-around' }\n\n"
        "return (\n"
        "  <div className={classes.banner}>\n"
        "    <Container>\n"
        "      <div className={classes.tagline}>\n"
        "        <Typography variant='h2'>Crypto Hunter</Typography>\n"
        "        <Typography variant='subtitle2'>Get all the Info...</Typography>\n"
        "      </div>\n"
        "      <Carousel />   ← Renders the scrolling coins strip\n"
        "    </Container>\n"
        "  </div>\n"
        ");"
    ),
    *Bul([
        "<b>makeStyles</b> — Creates CSS-in-JS styles. The 'banner' class sets the background image.",
        "<b>Container</b> — Material-UI wrapper that centres content and adds horizontal padding.",
        "<b>Typography variant='h2'</b> — Renders a styled &lt;h2&gt; heading.",
        "<b>Carousel /</b> — Delegates the scrolling coins strip to its own component.",
    ]),
    P("React features used: makeStyles, Material-UI components, component composition.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ─── 5.9 Banner/Carousel.js ──────────────────────────────────────────────────
story += [
    FileHeader("src/components/Banner/Carousel.js", "Trending Coins Auto-Scroll Strip"),
    SP(6),
    P("What is this file?", h3),
    P("""Carousel fetches the top 10 trending cryptocurrencies from the CoinGecko API
and displays them in an auto-scrolling horizontal strip inside the banner.
Each coin is clickable — it navigates you to that coin's detail page.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "An infinite auto-scrolling strip showing coin logo, symbol, 24h % change (green or red), and price.",
        "On small screens: 2 items visible. On screens wider than 512px: 4 items visible.",
        "Clicking any coin item navigates to /coins/{id}.",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "// State + context\n"
        "const [trending, setTrending] = useState([]);\n"
        "const { currency, symbol } = CryptoState();\n\n"
        "// API call on mount and whenever currency changes\n"
        "const fetchTrendingCoins = async () => {\n"
        "  const { data } = await axios.get(TrendingCoins(currency));\n"
        "  setTrending(data);\n"
        "};\n"
        "useEffect(() => { fetchTrendingCoins(); }, [currency]);\n\n"
        "// Build carousel items\n"
        "const items = trending.map((coin) => {\n"
        "  let profit = coin.price_change_percentage_24h >= 0;\n"
        "  return (\n"
        "    <Link to={`/coins/${coin.id}`}>   ← Clickable → coin detail page\n"
        "      <img src={coin.image} height='80' />\n"
        "      <span>{coin.symbol} <span style={{color: profit ? 'green' : 'red'}}>\n"
        "        {coin.price_change_percentage_24h.toFixed(2)}%\n"
        "      </span></span>\n"
        "      <span>{symbol} {coin.current_price}</span>\n"
        "    </Link>\n"
        "  );\n"
        "});\n\n"
        "// Responsive config\n"
        "const responsive = { 0: {items:2}, 512: {items:4} };\n\n"
        "return <AliceCarousel mouseTracking infinite autoPlay\n"
        "         autoPlayInterval={1000} animationDuration={1500}\n"
        "         responsive={responsive} items={items} />;"
    ),
    *Bul([
        "<b>useState([])</b> — trending starts as an empty array; filled after the API responds.",
        "<b>useEffect([currency])</b> — Runs fetchTrendingCoins immediately AND every time the currency changes.",
        "<b>trending.map()</b> — Converts raw API data into JSX carousel items.",
        "<b>profit variable</b> — Boolean: true if 24h change is positive. Used to colour the percentage green or red.",
        "<b>Link to={`/coins/${coin.id}`}</b> — React Router link. Navigates without page reload.",
        "<b>AliceCarousel</b> — Third-party component. autoPlay + infinite = endless scrolling loop.",
        "<b>responsive</b> — Breakpoint config: show 2 items on mobile, 4 on wider screens.",
    ]),
    P("React features used: useState, useEffect, Context (CryptoState), React Router (Link), .map().", note_s),
    HR(), SP(6),
]

# ─── 5.10 CoinsTable.js ──────────────────────────────────────────────────────
story += [
    FileHeader("src/components/CoinsTable.js", "Main Coins Table (Homepage)"),
    SP(6),
    P("What is this file?", h3),
    P("""The heart of the homepage. CoinsTable fetches the top 100 cryptocurrencies,
renders them in a searchable table with four columns, and adds pagination so only
10 rows show at a time. Clicking any row navigates to that coin's detail page.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "Section heading: 'Cryptocurrency Prices by Market Cap'.",
        "A search text field to filter by coin name or symbol.",
        "A table with columns: Coin (logo + symbol + name), Price, 24h Change (green/red), Market Cap.",
        "Pagination bar at the bottom to browse all 100 coins in pages of 10.",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "// State\n"
        "const [coins, setCoins]   = useState([]);   // All 100 coins from API\n"
        "const [loading, setLoading] = useState(false);\n"
        "const [search, setSearch] = useState('');   // Search field value\n"
        "const [page, setPage]     = useState(1);    // Current pagination page\n\n"
        "// Fetch all coins when component mounts or currency changes\n"
        "const fetchCoins = async () => {\n"
        "  setLoading(true);\n"
        "  const { data } = await axios.get(CoinList(currency));\n"
        "  setCoins(data);\n"
        "  setLoading(false);\n"
        "};\n"
        "useEffect(() => { fetchCoins(); }, [currency]);"
    ),
    Code(
        "// Search filter function\n"
        "const handleSearch = () => {\n"
        "  return coins.filter(\n"
        "    (coin) =>\n"
        "      coin.name.toLowerCase().includes(search) ||\n"
        "      coin.symbol.toLowerCase().includes(search)\n"
        "  );\n"
        "};"
    ),
    Code(
        "// Pagination slice: show 10 rows for current page\n"
        "handleSearch().slice((page-1)*10, (page-1)*10+10).map((row) => {\n"
        "  const profit = row.price_change_percentage_24h > 0;\n"
        "  return (\n"
        "    <TableRow onClick={() => history.push(`/coins/${row.id}`)}>  ← Navigation\n"
        "      <TableCell>logo + symbol + name</TableCell>\n"
        "      <TableCell>{symbol} {row.current_price}</TableCell>\n"
        "      <TableCell style={{color: profit?'green':'red'}}>\n"
        "        {row.price_change_percentage_24h}%\n"
        "      </TableCell>\n"
        "      <TableCell>Market Cap (shortened)</TableCell>\n"
        "    </TableRow>\n"
        "  );\n"
        "})"
    ),
    *Bul([
        "<b>useState for coins</b> — Holds the raw array of 100 coin objects from the API.",
        "<b>useState for loading</b> — Shows a gold LinearProgress bar while the API is loading.",
        "<b>useState for search</b> — Updates every keystroke via the TextField onChange.",
        "<b>useState for page</b> — Tracks which pagination page the user is on.",
        "<b>useEffect([currency])</b> — Refetches whenever currency switches between USD/INR.",
        "<b>handleSearch()</b> — Filters coins array on every render based on the search string. No extra state needed.",
        "<b>.slice()</b> — Pure JavaScript. Cuts the filtered array to show only the current page's 10 items.",
        "<b>profit variable</b> — Determines text colour: green for positive change, red for negative.",
        "<b>numberWithCommas()</b> — Formats large numbers with commas (e.g. 30,000 instead of 30000).",
        "<b>history.push()</b> — On row click, navigates to /coins/bitcoin etc.",
        "<b>Pagination</b> — Material-UI component. onChange updates the page state → .slice() shows new rows.",
    ]),
    P("React features used: useState, useEffect, useHistory (Router), Context, .map(), .filter(), .slice(), makeStyles.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ─── 5.11 Pages/CoinPage.js ──────────────────────────────────────────────────
story += [
    FileHeader("src/Pages/CoinPage.js", "Coin Detail Page (Route '/coins/:id')"),
    SP(6),
    P("What is this file?", h3),
    P("""CoinPage renders when a user clicks a coin. It reads the coin ID from the URL,
fetches full details for that specific coin from the CoinGecko API, and displays a
sidebar with the coin's image, description, rank, price, and market cap.
The right side is occupied by CoinInfo which shows the price chart.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "LEFT SIDEBAR (30% width): coin logo (200px), name, first sentence of description, rank, current price, market cap.",
        "RIGHT SECTION (70% width): the CoinInfo chart component.",
        "A gold LinearProgress loading bar while the API is being called.",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "// Read coin id from the URL ('/coins/bitcoin' → id = 'bitcoin')\n"
        "const { id } = useParams();\n"
        "const [coin, setCoin] = useState();\n\n"
        "// Fetch coin details once on mount\n"
        "const fetchCoin = async () => {\n"
        "  const { data } = await axios.get(SingleCoin(id));\n"
        "  setCoin(data);\n"
        "};\n"
        "useEffect(() => { fetchCoin(); }, []);\n\n"
        "// Guard: show loader until data arrives\n"
        "if (!coin) return <LinearProgress style={{ backgroundColor: 'gold' }} />;"
    ),
    Code(
        "// LEFT SIDEBAR renders:\n"
        "<img src={coin?.image.large} height='200' />   ← Large coin logo\n"
        "<Typography>{coin?.name}</Typography>           ← Coin name\n"
        "<Typography>                                   ← First sentence of description\n"
        "  {ReactHtmlParser(coin?.description.en.split('. ')[0])}.\n"
        "</Typography>\n\n"
        "// Market data\n"
        "Rank:          {coin?.market_cap_rank}\n"
        "Current Price: {coin?.market_data.current_price[currency.toLowerCase()]}\n"
        "Market Cap:    {coin?.market_data.market_cap[currency.toLowerCase()]}\n\n"
        "// RIGHT SECTION\n"
        "<CoinInfo coin={coin} />   ← Passes coin data to chart component"
    ),
    *Bul([
        "<b>useParams()</b> — Extracts the dynamic :id segment from the URL.",
        "<b>useState() with no default</b> — coin starts as undefined. The 'if (!coin)' guard prevents rendering before data arrives.",
        "<b>useEffect([])</b> — Empty array means fetch ONCE when the page mounts. No re-fetching on currency change here.",
        "<b>coin?.image.large</b> — The ?. is optional chaining. Safe way to access nested properties without crashing if undefined.",
        "<b>coin?.description.en.split('. ')[0]</b> — Splits description into sentences and takes only the first one.",
        "<b>ReactHtmlParser()</b> — The description from the API contains HTML tags (&lt;a&gt;, &lt;b&gt; etc.). This renders them safely.",
        "<b>currency.toLowerCase()</b> — The API returns prices as {usd: 30000, inr: 2500000}. Lowercasing 'USD' gives the key 'usd'.",
        "<b>makeStyles with theme.breakpoints</b> — Makes the layout responsive: side-by-side on desktop, stacked on mobile.",
        "<b>CoinInfo coin={coin}</b> — Passes the full coin object down as a prop to the chart component.",
    ]),
    P("React features used: useParams (Router), useState, useEffect, optional chaining, props, makeStyles with breakpoints.", note_s),
    HR(), SP(6),
]

# ─── 5.12 CoinInfo.js ────────────────────────────────────────────────────────
story += [
    FileHeader("src/components/CoinInfo.js", "Historical Price Chart"),
    SP(6),
    P("What is this file?", h3),
    P("""CoinInfo receives the coin object as a prop and renders the right-hand side of the
coin detail page. It fetches historical price data and draws an interactive line chart.
Below the chart are four time-range buttons (24h, 30d, 3m, 1y).
Clicking a button re-fetches the data for that time range and redraws the chart.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "A gold circular loading spinner (250px, thin) while historical data is loading.",
        "A gold line chart showing price over time (x-axis: dates/times, y-axis: price).",
        "Four SelectButton components below the chart for time range selection.",
    ]),
    SP(4),
    P("Code Sections Explained:", h3),
    Code(
        "// State\n"
        "const [historicData, setHistoricData] = useState();   // Array of [timestamp, price]\n"
        "const [days, setDays]   = useState(1);                 // Default: 1 day\n"
        "const [flag, setFlag]   = useState(false);             // Loading flag\n"
        "const { currency } = CryptoState();\n\n"
        "// Fetch historical data whenever 'days' changes\n"
        "const fetchHistoricData = async () => {\n"
        "  const { data } = await axios.get(HistoricalChart(coin.id, days, currency));\n"
        "  setFlag(true);\n"
        "  setHistoricData(data.prices);   // data.prices = [[timestamp, price], ...]\n"
        "};\n"
        "useEffect(() => { fetchHistoricData(); }, [days]);"
    ),
    Code(
        "// Chart data construction\n"
        "<Line\n"
        "  data={{\n"
        "    labels: historicData.map((coin) => {\n"
        "      let date = new Date(coin[0]);     // coin[0] is Unix timestamp in ms\n"
        "      // If 1 day view: show time (e.g. '3:30 PM')\n"
        "      // Otherwise: show date (e.g. '4/15/2024')\n"
        "      return days === 1 ? time : date.toLocaleDateString();\n"
        "    }),\n"
        "    datasets: [{\n"
        "      data: historicData.map((coin) => coin[1]),  // coin[1] is the price\n"
        "      label: `Price (Past ${days} Days) in ${currency}`,\n"
        "      borderColor: '#EEBC1D',   // Gold line\n"
        "    }],\n"
        "  }}\n"
        "  options={{ elements: { point: { radius: 1 } } }}  ← Tiny dots on the line\n"
        "/>"
    ),
    Code(
        "// Time range buttons\n"
        "{chartDays.map((day) => (\n"
        "  <SelectButton\n"
        "    key={day.value}\n"
        "    onClick={() => { setDays(day.value); setFlag(false); }}\n"
        "    selected={day.value === days}\n"
        "  >\n"
        "    {day.label}\n"
        "  </SelectButton>\n"
        "))}"
    ),
    *Bul([
        "<b>useState(1) for days</b> — Default chart range is 1 day. Changing this triggers a re-fetch via useEffect.",
        "<b>useEffect([days])</b> — Runs fetchHistoricData whenever 'days' changes — NOT on currency change (intentional simplification).",
        "<b>flag state</b> — Used to prevent the chart from rendering with stale data while new data is being loaded.",
        "<b>data.prices</b> — The API returns {prices: [[ts,price], ...]}. Only the prices array is stored.",
        "<b>coin[0]</b> — Unix timestamp in milliseconds. new Date(ts) converts it to a JavaScript Date object.",
        "<b>days===1 ? time : date</b> — When viewing 24h, show time labels. For longer ranges, show date labels.",
        "<b>historicData.map(coin => coin[1])</b> — Extracts just the price value from each [timestamp, price] pair.",
        "<b>chartDays.map()</b> — Loops over the 4 options from config/data.js and creates a SelectButton for each.",
        "<b>selected={day.value === days}</b> — Passes a boolean to SelectButton so the active button gets the gold style.",
        "<b>CircularProgress</b> — Material-UI spinner shown while historicData is undefined or flag is false.",
    ]),
    P("React features used: useState, useEffect, props, Context (CryptoState), .map(), react-chartjs-2 (Line), Material-UI.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ─── 5.13 SelectButton.js ────────────────────────────────────────────────────
story += [
    FileHeader("src/components/SelectButton.js", "Reusable Chart Time-Range Button"),
    SP(6),
    P("What is this file?", h3),
    P("""SelectButton is a tiny reusable component used as the time-range toggle buttons
below the price chart (24 Hours, 30 Days, 3 Months, 1 Year).
It renders as a gold-bordered span that highlights gold when it is the active selection.""", body),
    SP(4),
    P("What it renders on the website:", h3),
    *Bul([
        "A gold-bordered rectangular button with label text.",
        "When selected=true: fills gold background with black text.",
        "When hovered: also fills gold.",
    ]),
    SP(4),
    Code(
        "const SelectButton = ({ children, selected, onClick }) => {\n"
        "  // Styles change dynamically based on 'selected' prop\n"
        "  const useStyles = makeStyles({\n"
        "    selectbutton: {\n"
        "      border: '1px solid gold',\n"
        "      backgroundColor: selected ? 'gold' : '',    ← Gold if active\n"
        "      color:           selected ? 'black' : '',   ← Black text if active\n"
        "      fontWeight:      selected ? 700 : 500,\n"
        "      '&:hover': { backgroundColor: 'gold', color: 'black' },\n"
        "    },\n"
        "  });\n\n"
        "  return (\n"
        "    <span onClick={onClick} className={classes.selectbutton}>\n"
        "      {children}   ← The button label text ('24 Hours', etc.)\n"
        "    </span>\n"
        "  );\n"
        "};"
    ),
    *Bul([
        "<b>{ children, selected, onClick }</b> — Three props received from the parent (CoinInfo).",
        "<b>children</b> — Whatever is placed between &lt;SelectButton&gt;...&lt;/SelectButton&gt; tags. Here it is the label text.",
        "<b>selected</b> — Boolean prop. When true, applies gold background styles.",
        "<b>onClick</b> — Function prop. Called when user clicks the button. The parent defines what happens (setDays).",
        "<b>makeStyles inside the component</b> — This is valid but unusual; the style depends on the 'selected' prop value.",
        "This pattern is called a <b>controlled component</b> — the parent owns the state, the child just displays and triggers.",
    ]),
    P("React features used: functional component, props (children, selected, onClick), makeStyles with dynamic styles.", note_s),
    HR(), SP(6),
]

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — DATA FLOW MAP
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("6. Data Flow Map — How Data Moves Through the App", h1), HR(),
    P("""This section shows which component fetches what data, what API it calls,
what it stores, and what it renders from that data.""", body),
    SP(8),
]

data_flow = [
    ["Component", "API Called", "Data Stored in State", "Rendered from Data"],
    ["Carousel.js",    "TrendingCoins(currency)",        "trending[] – 10 coin objects",
     "Coin logo, symbol, 24h %, price in carousel"],
    ["CoinsTable.js",  "CoinList(currency)",             "coins[] – 100 coin objects",
     "Table rows: logo, name, price, 24h change, market cap"],
    ["CoinPage.js",    "SingleCoin(id)",                 "coin – 1 full coin object",
     "Sidebar: large logo, name, description, rank, price, market cap"],
    ["CoinInfo.js",    "HistoricalChart(id, days, currency)", "historicData[] – [[ts, price], ...]",
     "Line chart with time labels and gold price line"],
]
t = Table(data_flow, colWidths=[3.5*cm, 4*cm, 4*cm, 5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), GOLD),
    ("BACKGROUND",  (0,1), (-1,-1), DARK2),
    ("TEXTCOLOR",   (0,0), (-1,0), DARK_BG),
    ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 8),
    ("ROWPADDING",  (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("GRID",        (0,0), (-1,-1), 0.3, GREY),
    ("BOX",         (0,0), (-1,-1), 0.8, GOLD),
    ("WORDWRAP",    (0,0), (-1,-1), True),
]))
story += [t, SP(16)]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — REACT FEATURES CHEAT SHEET
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("7. React Features Used — Where and Why", h1), HR(),
    SP(4),
]

react_usage = [
    ["React Feature", "Files Used In", "What It Does in This Project"],
    ["useState",          "All components",                   "Stores API data, loading flags, search text, selected days, pagination page"],
    ["useEffect",         "Carousel, CoinsTable, CoinPage, CoinInfo", "Triggers API fetches on mount and on state/prop changes"],
    ["useContext / createContext", "CryptoContext, Header, Carousel, CoinsTable, CoinInfo", "Shares currency and symbol globally without prop drilling"],
    ["useHistory",        "Header, CoinsTable",               "Programmatically navigates to a new URL route"],
    ["useParams",         "CoinPage",                         "Reads the :id dynamic segment from the URL"],
    ["React Router Route","App.js",                           "Maps URL patterns to page components"],
    ["Link",              "Carousel",                         "Client-side navigation anchor (no page reload)"],
    ["Props",             "CoinPage→CoinInfo, CoinInfo→SelectButton", "Passes data and callbacks from parent to child"],
    ["children prop",     "SelectButton",                     "Renders content placed between opening and closing tags"],
    ["makeStyles",        "All components",                   "CSS-in-JS — creates scoped, dynamic styles"],
    ["ThemeProvider",     "CoinsTable, CoinInfo, Header",     "Sets Material-UI dark theme for all components inside it"],
    [".map()",            "Carousel, CoinsTable, CoinInfo",   "Transforms data arrays into arrays of JSX elements"],
    [".filter()",         "CoinsTable",                       "Filters coins array based on search text"],
    [".slice()",          "CoinsTable",                       "Cuts array to show only current page's 10 rows"],
    ["Optional chaining (?.)", "CoinPage",                   "Safely accesses nested object properties without crashing"],
    ["async / await",     "All fetching functions",           "Handles asynchronous API calls cleanly"],
]
t = Table(react_usage, colWidths=[4*cm, 5*cm, 7.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), GOLD),
    ("BACKGROUND",  (0,1), (-1,-1), DARK2),
    ("TEXTCOLOR",   (0,0), (-1,0), DARK_BG),
    ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 8),
    ("ROWPADDING",  (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 6),
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("GRID",        (0,0), (-1,-1), 0.3, GREY),
    ("BOX",         (0,0), (-1,-1), 0.8, GOLD),
]))
story += [t, PageBreak()]

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — QUICK REFERENCE GLOSSARY
# ═══════════════════════════════════════════════════════════════════════════════
story += [
    P("8. Quick Reference — Key Terms Glossary", h1), HR(),
    SP(6),
]

glossary = [
    ["Term", "Plain-English Meaning"],
    ["Component",       "A JavaScript function that returns JSX (UI). The building block of React apps."],
    ["Hook",            "A special React function starting with 'use'. useState, useEffect, useContext are all hooks."],
    ["State",           "Data stored inside a component. When state changes, the component re-renders."],
    ["Props",           "Data passed from a parent component to a child, like function arguments."],
    ["Re-render",       "React automatically updates the UI whenever state or props change."],
    ["JSX",             "HTML-like syntax written in JavaScript files. React converts it to browser DOM."],
    ["Context",         "A global data store. Avoids passing props through every level of the tree."],
    ["SPA",             "Single Page Application. Only one HTML file; React swaps content without full reloads."],
    ["API",             "Application Programming Interface. A URL you call to get data (here: CoinGecko)."],
    ["Axios",           "A library that makes HTTP GET/POST requests to APIs."],
    ["Mount",           "When a component appears on screen for the first time. useEffect([], []) runs on mount."],
    ["Unmount",         "When a component is removed from screen (e.g. navigating away from CoinPage)."],
    ["Dynamic route",   "A URL pattern with a variable segment: /coins/:id matches /coins/bitcoin, /coins/eth, etc."],
    ["Optional chaining","The ?. operator. coin?.image means: if coin is undefined, return undefined instead of crashing."],
    ["Destructuring",   "const { data } = response — extracts the 'data' key from the response object directly."],
]
t = Table(glossary, colWidths=[4*cm, 12.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND",  (0,0), (-1,0), GOLD),
    ("BACKGROUND",  (0,1), (-1,-1), DARK2),
    ("TEXTCOLOR",   (0,0), (-1,0), DARK_BG),
    ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
    ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME",    (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE",    (0,0), (-1,-1), 9),
    ("ROWPADDING",  (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN",      (0,0), (-1,-1), "TOP"),
    ("GRID",        (0,0), (-1,-1), 0.3, GREY),
    ("BOX",         (0,0), (-1,-1), 0.8, GOLD),
]))
story += [t, SP(20)]

# Footer note
story += [
    HR(),
    P("End of Documentation  |  Crypto Hunter React Project  |  Prepared for: ajet", label_s),
]

# ── Build ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generated: {OUTPUT}")

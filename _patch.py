"""DAMI plánovač -> LAYLA. Spúšťa sa raz nad skopírovaným index.html."""
import pathlib, re
p = pathlib.Path(__file__).parent / "index.html"
s = p.read_text(encoding="utf-8")

def rep(a, b, count=1):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, count)

rep("<title>DAMI – Instagram grid</title>", "<title>LAYLA – Instagram grid</title>")
rep("--red: #e3151d;", "--red: #8a715f;")
rep('<option value="tone">Tón (tmavý / svetlý / červený)</option>', '<option value="tone">Tón (tmavý / svetlý)</option>')
rep('<label><input type="checkbox" data-opt="red"><span>Červené akcenty rozptýliť<small>posty s veľkým červeným D nesusedia</small></span></label>', "")
# jediný vzhľad = pôvodné posty (bez Papier/Dielňa/Hĺbka)
s = re.sub(r'<div class="seg" data-seg="look".*?</div>', "", s, count=1, flags=re.S)
s = re.sub(r'<button class="btn" data-toggle="depth".*?</button>', "", s, count=1, flags=re.S)
rep('depth: url.has("d") ? url.get("d") === "1" : !!saved.depth, look: ["off", "g", "c"].includes(url.get("g")) ? url.get("g") : url.get("g") === "1" ? "g" : url.get("g") === "0" ? "off" : (typeof saved.look === "string" ? saved.look : saved.look === false ? "off" : "g"),',
    'depth: false, look: "off",')
rep('const KEY = "dami-grid-planner2-v7";', 'const KEY = "layla-grid-planner-v1";')
rep('setData("text/plain", "dami")', 'setData("text/plain", "layla")')
s = s.replace("dami-grid-", "layla-grid-")

# profil
rep('<img src="avatar.png" alt="DAMI">', '<img src="avatar.png" alt="LAYLA">')
s = re.sub(r"<h1>pracovne_odevy_dami ", "<h1>masazelayla ", s, count=1)
rep('<div class="nm">DAMI pracovné odevy</div>', '<div class="nm">Masáže Layla · Piešťany</div>')
rep("Sledovatelia: <b>2 431</b></span><span>Sledované: <b>218</b>", "Sledovatelia: <b>486</b></span><span>Sledované: <b>212</b>")
rep('<div class="bio">Pracovné odevy a obuv pre gastro, zdravotníctvo, remeslo aj priemysel.<br>Oblečenie, čo maká. · Gaštanová 6396, Piešťany</div>',
    '<div class="bio">Masáže, bankovanie a maderoterapia v súkromnom štúdiu.<br>Hodžova 4304/20, Piešťany · denne 8:00 – 20:00 · rezervácia online</div>')
s = s.replace("dami-pracovne-odevy.sk", "masazelayla.sk")

# highlighty
start = s.index("  const ICO = {"); end = s.index("  };", start) + 4
s = s[:start] + '''  const ICO = {
    Masáže: '<path d="M4 15c2.5-1 5-1 8 0s5.5 1 8 0"/><path d="M4 19c2.5-1 5-1 8 0s5.5 1 8 0"/><circle cx="12" cy="7" r="3"/>',
    Bankovanie: '<path d="M7 9a5 5 0 0 1 10 0v2H7z"/><path d="M5 11h14v2a7 7 0 0 1-14 0z"/>',
    Maderoterapia: '<rect x="9" y="3" width="6" height="18" rx="3"/><path d="M9 7h6M9 11h6M9 15h6"/>',
    Poukazy: '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M3 11h18M12 7v13"/><path d="M12 7c-2-4-6-3-5 0M12 7c2-4 6-3 5 0"/>',
    Recenzie: '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>',
    Štúdio: '<path d="M12 3c-1 3-4 4.5-4 8a4 4 0 0 0 8 0c0-3.5-3-5-4-8z"/><path d="M6 21h12"/>',
    Piešťany: '<path d="M12 21s-6.5-6-6.5-11.2A6.5 6.5 0 0 1 12 3.3a6.5 6.5 0 0 1 6.5 6.5C18.5 15 12 21 12 21z"/><circle cx="12" cy="9.8" r="2.4"/>',
  };''' + s[end:]

# kategórie
s = re.sub(r"  const CAT = \{.*?\};\n", '''  const CAT = { znacka: ["Značka / logo", "#c2ad98"], masaz: ["Masáž", "#60a5fa"], madero: ["Maderoterapia", "#a3b86c"], priestor: ["Štúdio / atmosféra", "#fbbf24"], sluzby: ["Služby", "#f472b6"], rezervacia: ["Rezervácia", "#38bdf8"], citat: ["Citát / myšlienka", "#a78bfa"], poukaz: ["Darčekový poukaz", "#f97316"], recenzie: ["Recenzie", "#3ecf6e"], vizual: ["Ucelený vizuál", "#8a715f"], web: ["Web", "#38bdf8"] };\n''', s, count=1, flags=re.S)
rep('const TONE = { dark: ["Tmavý", "#111", "#666"], light: ["Svetlý", "#f2f2f2"], red: ["Červený akcent", "#e3151d"] };',
    'const TONE = { dark: ["Tmavý", "#111", "#666"], light: ["Svetlý", "#f2f2f2"] };')
rep('V: ["Ucelený vizuál", "#e3151d"]', 'V: ["Fotka + text", "#c2ad98"]')

# príbeh za gridom
start = s.index('<section class="story">'); end = s.index("</section>", start) + len("</section>")
s = s[:start] + '''<section class="story">
  <div class="story__eb">Príbeh za gridom</div>
  <h2>Hodina, ktorá patrí <em>len vám.</em></h2>
  <p class="story__lead">Piešťany sú mesto oddychu, no väčšina ľudí ho prežíva v zhone. Masáže Layla sú <b>malé súkromné štúdio na Hodžovej</b>: sviečky, teplé svetlo, drevo a ticho. Žiadna veľká wellness prevádzka, ale <b>jedna masérka, Laura</b>, ktorá sa venuje len vám. Feed preto nepôsobí ako katalóg služieb. Ukazuje <b>pocit, s ktorým od nej ľudia odchádzajú</b>: uvoľnené telo, pokojnú hlavu a čas pre seba.</p>
  <blockquote class="quote">„Telo v pohode. Myseľ v pokoji.“ Nie je to sľub zázraku, ale pozvanie na hodinu, počas ktorej sa nemusíte nikam ponáhľať.<small>Hlavná myšlienka komunikácie LAYLA</small></blockquote>
  <div class="pillars">
    <div class="pillar"><span>01 · ATMOSFÉRA</span><h3>Teplé svetlo a ticho</h3><p>Sviečky, drevo, rastliny a mäkké textúry. Tmavé fotky štúdia striedajú svetlé krémové posty, takže feed dýcha a pôsobí pokojne.</p></div>
    <div class="pillar"><span>02 · DOTYK</span><h3>Ruky, nie tváre</h3><p>Detaily rúk, chrbta a chodidiel ukazujú remeslo bez prehnaných sľubov. Klient sa v nich vidí sám seba, nie modelku.</p></div>
    <div class="pillar"><span>03 · PROCEDÚRY</span><h3>Masáž, bankovanie, madero</h3><p>Každá procedúra má vlastnú sériu: drevené nástroje maderoterapie, sklenené banky, oleje. Vecne vysvetľuje, čo procedúra je a pre koho.</p></div>
    <div class="pillar"><span>04 · ZNAČKA</span><h3>LAYLA ako podpis</h3><p>Logo, jemná olivová linka a krémový papier sa opakujú. Profil je rozpoznateľný už v náhľade, aj keď v ňom nie je žiadna tvár.</p></div>
    <div class="pillar"><span>05 · AKCIA</span><h3>Rezervácia a poukaz</h3><p>Pravidelne sa vracia jasná výzva: rezervácia online za minútu a darčekový poukaz. Pred Vianocami ťahá najviac práve poukaz.</p></div>
  </div>
</section>''' + s[end:]

# prínosy v pláne
rep('`<b>Jednotný vizuálny štýl</b> – farby, D symbol a typografia sa opakujú, DAMI je rozpoznateľné už v náhľade feedu.`',
    '`<b>Jednotný vizuálny štýl</b> – krémový papier, olivová linka a logo LAYLA sa opakujú, profil je rozpoznateľný už v náhľade feedu.`')
s = re.sub(r'      `<b>\$\{shop\} postov ťahá ľudí do predajne.*?\n.*?\n.*?\n.*?\n', '''      `<b>${cnt("rezervacia")} postov vedie k rezervácii</b> – online rezervácia za minútu, priamo z odkazu v profile.`,
      `<b>${cnt("poukaz")} posty s darčekovým poukazom</b> – najsilnejšie v novembri a decembri.`,
      `<b>${cnt("masaz") + cnt("madero")} postov o procedúrach</b> – masáž, bankovanie a maderoterapia; dajú sa pustiť aj ako platená reklama v okolí Piešťan.`,
''', s, count=1, flags=re.S)
rep("const shop = cnt(\"predajna\") + cnt(\"mesto\");\n", "")
s = s.replace("<b>označenie hotelov, reštaurácií a firiem</b>, ktoré DAMI oblieka, QR kód v predajni", "<b>spoluprácu s kúpeľmi, hotelmi a salónmi v okolí</b>, QR kód v štúdiu")
s = s.replace("ktoré DAMI oblieka", "")
p.write_text(s, encoding="utf-8")
left = [m.start() for m in re.finditer(r"(?i)dami|červen|predajn|pracovn", s)]
print("ok, zvyšky:", len(left))
for i in left[:12]:
    print("  ", s[max(0, i - 60):i + 60].replace("\n", " "))

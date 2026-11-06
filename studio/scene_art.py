"""Original vector illustrations for the Quiet Hours scene vocabulary."""

KEYS = """
<g stroke="#171628" stroke-width="11" stroke-linejoin="round">
  <circle cx="253" cy="240" r="85" fill="none"/>
  <g transform="rotate(-22 271 260)">
    <path d="M265 222h151a53 53 0 1 1 0 105H302v45h-31v-24h-34v-91z" fill="#f2c643"/>
    <circle cx="407" cy="274" r="20" fill="#fff6e2"/>
    <path d="M301 260h67" fill="none" stroke-linecap="round"/>
  </g>
  <g transform="rotate(24 275 233)">
    <path d="M275 182h162a58 58 0 1 1 0 116h-25v55h-29v-26h-34v26h-27v-53h-47z" fill="#d9d7f2"/>
    <circle cx="432" cy="239" r="23" fill="#fff6e2"/>
    <path d="M312 222h71m-71 32h49" fill="none" stroke-linecap="round"/>
  </g>
</g>
"""

MAT = """
<g transform="rotate(-10 380 265)">
  <rect x="106" y="135" width="545" height="310" rx="39" fill="#171628" opacity=".22" transform="translate(15 20)"/>
  <rect x="106" y="135" width="545" height="310" rx="39" fill="#263eb5" stroke="#171628" stroke-width="8"/>
  <rect x="125" y="153" width="507" height="274" rx="25" fill="url(#weave)" stroke="#9baffc" stroke-width="3" stroke-dasharray="5 6"/>
  <path d="M497 427v-60h102v60" fill="#fff6e2"/>
  <g fill="#263eb5"><path d="M519 385h7v24h-7zm14 0h7v24h-7zm-12 9h17v6h-17z"/><path d="M550 385h7v16h10v-16h7v24h-24z"/></g>
</g>
"""

ART = {
    "citation": """
<g transform="rotate(-8 372 257)">
  <rect x="135" y="86" width="490" height="361" rx="12" fill="#171628" opacity=".24" transform="translate(15 19)"/>
  <rect x="135" y="86" width="490" height="361" rx="12" fill="#fff6e2" stroke="#171628" stroke-width="8"/>
  <path d="M135 132h490m-490 270h490" stroke="#171628" stroke-width="6"/>
  <path d="M155 103h131m278 0h42m-437 319h410" stroke="#171628" stroke-width="3" stroke-dasharray="6 4"/>
</g>
<g stroke="#171628" stroke-width="10" fill="none" stroke-linecap="round">
  <path d="M96 152l-42-15m44-30-25-28m577 274 49 12m-48 21 37 32"/>
</g>
"""
    + KEYS,
    "clipboard": """
<g transform="rotate(8 380 275)">
  <rect x="214" y="41" width="330" height="471" rx="18" fill="#f48072" stroke="#171628" stroke-width="9"/>
  <rect x="238" y="78" width="282" height="402" rx="7" fill="#fff6e2" stroke="#171628" stroke-width="5"/>
  <path d="M319 52h121v45H319z" fill="#b8c5fb" stroke="#171628" stroke-width="8"/>
  <g stroke="#171628" stroke-width="4">
    <path d="M265 145h226m-226 80h226m-226 72h226m-226 72h226m-226 72h133"/>
    <path d="M272 171h26v26h-26zm0 75h26v26h-26zm0 72h26v26h-26zm0 72h26v26h-26z" fill="none"/>
    <path d="M274 182l11 13 30-31" stroke="#d23b34" stroke-width="8" fill="none" stroke-linecap="round"/>
  </g>
</g>
""",
    "packshot": MAT,
    "stamp": KEYS
    + """
<g transform="rotate(-13 386 396)">
  <rect x="221" y="344" width="330" height="111" rx="8" fill="#f2c643" stroke="#171628" stroke-width="10"/>
  <path d="M245 364h282v71H245z" fill="none" stroke="#171628" stroke-width="4" stroke-dasharray="9 5"/>
  <path d="M334 402l28 27 68-67" fill="none" stroke="#263eb5" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/>
</g>
""",
    "end": MAT,
}


def illustration(style):
    return f"""<svg class="illustration" viewBox="0 0 760 560" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs><pattern id="weave" width="13" height="13" patternUnits="userSpaceOnUse">
  <path d="M-2 2l4-4m-4 17L15-2M11 15l4-4" stroke="#a5b8ff" stroke-width="2" opacity=".48"/>
</pattern></defs>
{ART.get(style, ART["citation"])}
</svg>"""
